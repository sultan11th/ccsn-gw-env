"""Tiny local proxy between the agent (Goose) and an OpenAI-compatible model server.

Why it exists
  * Adds fields to every request that Goose cannot set itself, e.g. for DeepSeek
    {"thinking": {"type": "disabled"}} (with thinking on, DeepSeek requires
    reasoning_content to be sent back on tool-using turns, otherwise HTTP 400).
  * Adds the real API key, so the key never appears in Goose's configuration.
  * Counts tokens (prompt / completion) per request and appends them to a JSONL log,
    which replaces the token budget that the course wrapper keeps for Yandex AI Studio.
  * Caps tool output: every tool result in the conversation longer than max_tool_chars
    is cut (head + tail) before it reaches the model, so one `cat` or `grep -r` cannot
    fill the context of a small local model or cost a fortune on an API.
  * Enforces a budget per run: after token_budget tokens or max_requests model calls it
    refuses further requests (HTTP 400 with a clear message), which ends the agent's run.

It forwards every path unchanged: a request to http://127.0.0.1:<port>/v1/chat/completions
goes to <upstream>/v1/chat/completions. Streaming (SSE) responses are passed through as
they arrive. Standard library only.

Used by src/agent.py; can also run on its own:
  python3 src/llm_proxy.py --upstream http://localhost:11434 --log results/agent_runs/usage.jsonl
"""
import argparse
import datetime as dt
import json
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class ProxyServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, upstream, api_key=None, inject=None, log_path=None, label="",
                 max_tool_chars=None, token_budget=None, max_requests=None):
        super().__init__(("127.0.0.1", 0), _Handler)
        self.max_tool_chars = max_tool_chars
        self.token_budget = token_budget
        self.max_requests = max_requests
        self.upstream = upstream.rstrip("/")
        self.api_key = api_key
        self.inject = inject or {}
        self.log_path = log_path
        self.label = label
        self.lock = threading.Lock()
        self.totals = {"requests": 0, "prompt_tokens": 0, "completion_tokens": 0, "errors": 0,
                       "truncated": 0, "refused": None}

    @property
    def url(self):
        return f"http://127.0.0.1:{self.server_address[1]}"

    def record(self, model, usage, status):
        with self.lock:
            self.totals["requests"] += 1
            if status >= 400:
                self.totals["errors"] += 1
            if usage:
                self.totals["prompt_tokens"] += int(usage.get("prompt_tokens") or 0)
                self.totals["completion_tokens"] += int(usage.get("completion_tokens") or 0)
            if self.log_path:
                row = {"time": dt.datetime.now().isoformat(timespec="seconds"), "label": self.label,
                       "model": model, "status": status, **{k: (usage or {}).get(k) for k in
                       ("prompt_tokens", "completion_tokens", "total_tokens")}}
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(row) + "\n")

    def over_budget(self):
        t = self.totals
        if self.max_requests and t["requests"] >= self.max_requests:
            return f"request limit reached ({self.max_requests} model calls in this run)"
        used = t["prompt_tokens"] + t["completion_tokens"]
        if self.token_budget and used >= self.token_budget:
            return f"token budget reached ({used:,} of {self.token_budget:,} tokens in this run)"
        return None

    def cap_tools(self, messages):
        """Cut long tool results (head + tail); returns the number of results cut."""
        n, cap = 0, self.max_tool_chars
        if not cap:
            return 0
        for m in messages if isinstance(messages, list) else []:
            if not isinstance(m, dict) or m.get("role") != "tool":
                continue
            c = m.get("content")
            parts = c if isinstance(c, list) else [c]
            for i, part in enumerate(parts):
                text = part.get("text") if isinstance(part, dict) else part
                if isinstance(text, str) and len(text) > cap:
                    head, tail = text[: cap * 3 // 4], text[-cap // 4:]
                    cut = (f"{head}\n[... {len(text) - len(head) - len(tail):,} characters cut by the proxy. "
                           f"Do not print whole files: use src/search.py, sed -n 'a,bp' on a short range, "
                           f"or src/data.py ...]\n{tail}")
                    if isinstance(part, dict):
                        part["text"] = cut
                    else:
                        parts[i] = cut
                    n += 1
            if not isinstance(c, list):
                m["content"] = parts[0]
        return n

    def start(self):
        threading.Thread(target=self.serve_forever, daemon=True).start()
        return self


class _Handler(BaseHTTPRequestHandler):
    server: ProxyServer

    def log_message(self, *args):  # keep the agent's terminal clean
        pass

    def _forward(self, method):
        srv = self.server
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0)) if method == "POST" else None
        model, stream = None, False
        if body:
            try:
                data = json.loads(body)
            except ValueError:
                data = None
            if isinstance(data, dict):
                for k, v in srv.inject.items():
                    data.setdefault(k, v)
                n_cut = srv.cap_tools(data.get("messages"))
                if n_cut:
                    with srv.lock:
                        srv.totals["truncated"] = max(srv.totals["truncated"], n_cut)
                stream = bool(data.get("stream"))
                if stream:
                    data.setdefault("stream_options", {"include_usage": True})
                model = data.get("model")
                body = json.dumps(data).encode()
        reason = srv.over_budget() if method == "POST" else None
        if reason:
            srv.totals["refused"] = reason
            msg = json.dumps({"error": {"message": f"proxy: {reason}; stop and give your final answer",
                                        "type": "budget_exceeded"}}).encode()
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            return
        headers = {"Content-Type": self.headers.get("Content-Type", "application/json"),
                   "Accept": self.headers.get("Accept", "*/*")}
        auth = f"Bearer {srv.api_key}" if srv.api_key else self.headers.get("Authorization")
        if auth:
            headers["Authorization"] = auth
        req = urllib.request.Request(srv.upstream + self.path, data=body, headers=headers, method=method)
        try:
            resp = urllib.request.urlopen(req, timeout=600)
            status = resp.status
        except urllib.error.HTTPError as e:
            resp, status = e, e.code
        except urllib.error.URLError as e:
            msg = json.dumps({"error": {"message": f"proxy: cannot reach {srv.upstream}: {e.reason}"}}).encode()
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            srv.record(model, None, 502)
            return

        self.send_response(status)
        ctype = resp.headers.get("Content-Type", "application/json")
        self.send_header("Content-Type", ctype)
        usage = None
        if "text/event-stream" in ctype:              # SSE: pass through as it arrives
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            buf = b""
            while True:
                chunk = resp.read1(8192) if hasattr(resp, "read1") else resp.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
                buf += chunk
                *lines, buf = buf.split(b"\n")
                for line in lines:
                    if line.startswith(b"data:") and b'"usage"' in line:
                        try:
                            u = json.loads(line[5:].strip()).get("usage")
                            usage = u or usage
                        except ValueError:
                            pass
        else:
            payload = resp.read()
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            try:
                usage = json.loads(payload).get("usage")
            except (ValueError, AttributeError):
                pass
        srv.record(model, usage, status)

    def do_POST(self):
        self._forward("POST")

    def do_GET(self):
        self._forward("GET")


def main():
    ap = argparse.ArgumentParser(description="Local OpenAI-compatible proxy with field injection and token log.")
    ap.add_argument("--upstream", required=True, help="e.g. http://localhost:11434 or https://api.deepseek.com")
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--inject", default="{}", help='JSON merged into each request, e.g. \'{"thinking":{"type":"disabled"}}\'')
    ap.add_argument("--log", default=None, help="append token usage as JSONL")
    ap.add_argument("--max-tool-chars", type=int, default=None, help="cut tool results longer than this")
    ap.add_argument("--token-budget", type=int, default=None, help="refuse requests after this many tokens")
    ap.add_argument("--max-requests", type=int, default=None, help="refuse requests after this many model calls")
    a = ap.parse_args()
    srv = ProxyServer(a.upstream, a.api_key, json.loads(a.inject), a.log, max_tool_chars=a.max_tool_chars,
                      token_budget=a.token_budget, max_requests=a.max_requests)
    print(srv.server_address[1], flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
