"""Self-test of the environment. Run from the repository root:  python3 tests/selftest.py

Part 1 (offline, always): copies the scripts into a temporary directory, converts
two synthetic e-prints from tests/fixtures (a multi-file .tar.gz and a single-file
.gz), builds an index and checks search, filters, citations and line ranges.
Part 2 (this repository): catalog consistency, ontology validity, Mermaid graph up to
date, REPORT.md appendix identical to AGENT.md, and, if an index exists, that every
citation resolves to real lines.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures"
PY = sys.executable
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


def run(args, cwd):
    return subprocess.run([PY] + args, cwd=cwd, capture_output=True, text=True)


def offline_pipeline():
    tmp = Path(tempfile.mkdtemp(prefix="ccsn_selftest_"))
    try:
        shutil.copytree(ROOT / "src", tmp / "src", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "ontology", tmp / "ontology")
        (tmp / "literature").mkdir()
        cat = yaml.safe_load((ROOT / "literature" / "catalog.yaml").read_text(encoding="utf-8"))
        cat["papers"] += [
            {"key": "fx_rotation", "arxiv": "0000.00001", "authors": "Fixture", "year": 2026,
             "venue": "fixture", "doi": None, "own": True, "active": True, "verified": False, "topic": "fixture A"},
            {"key": "fx_ml", "arxiv": "0000.00002", "authors": "Fixture", "year": 2026,
             "venue": "fixture", "doi": None, "own": False, "active": True, "verified": False, "topic": "fixture B"},
        ]
        (tmp / "literature" / "catalog.yaml").write_text(yaml.safe_dump(cat, sort_keys=False), encoding="utf-8")

        r1 = run(["src/fetch_arxiv.py", "fx_rotation", "--local", str(FIX / "eprint_a.tar.gz")], tmp)
        check("fetch: multi-file tar.gz e-print -> Markdown via LaTeX", r1.returncode == 0 and "via latex" in r1.stdout, r1.stderr[-300:])
        r2 = run(["src/fetch_arxiv.py", "fx_ml", "--local", str(FIX / "eprint_b.gz")], tmp)
        check("fetch: single-file gzip e-print -> Markdown via LaTeX", r2.returncode == 0 and "via latex" in r2.stdout, r2.stderr[-300:])
        md = (tmp / "literature" / "md" / "fx_rotation.md").read_text(encoding="utf-8") if r1.returncode == 0 else ""
        check("fetch: \\input{} file was resolved", "## Methods" in md or "# Methods" in md)
        check("fetch: equations kept as LaTeX math", "$T/|W|" in md)
        check("fetch: front matter written", md.startswith("---\nkey: fx_rotation"))

        r = run(["src/build_index.py"], tmp)
        check("index: builds", r.returncode == 0 and "Indexed" in r.stdout, r.stderr[-300:])

        def search(*args):
            out = run(["src/search.py", *args, "--json"], tmp)
            return json.loads(out.stdout) if out.returncode == 0 and out.stdout.strip() else []

        hits = search("bounce amplitude rotation", "-k", "3")
        check("search: relevant chunk ranked first", bool(hits) and hits[0]["key"] == "fx_rotation"
              and "Bounce amplitude" in hits[0]["section"], str(hits[:1]))
        check("search: citation has file, line range and section",
              bool(hits) and hits[0]["citation"].startswith("literature/md/fx_rotation.md:L") and " § " in hits[0]["citation"])
        if hits:
            lines = (tmp / hits[0]["file"]).read_text(encoding="utf-8").splitlines()
            span = "\n".join(lines[hits[0]["line_start"] - 1: hits[0]["line_end"]])
            check("search: cited line range contains the chunk text", hits[0]["text"].splitlines()[0] in span)
        beta = search("beta", "-k", "3")
        check("search: synonym expansion (beta -> T/|W|)", any("T/|W|" in h["text"] for h in beta), str(beta[:1]))
        check("search: --exact finds a number", any("999" in h["text"] for h in search("--exact", "999")))
        check("search: --own excludes external papers",
              all(h["own"] for h in search("cross-validation", "--own"))
              and bool(search("random cross-validation overestimates"))
              and not search("random cross-validation overestimates", "--own", "--exact", "overestimates"))
        check("search: --file restricts to one paper", {h["key"] for h in search("equation of state", "--file", "fx_ml")} == {"fx_ml"})
        empty = run(["src/search.py", "zzzzqqq", "--own"], tmp)
        check("search: says 'No results' instead of guessing", "No results" in empty.stdout)
        papers = run(["src/search.py", "--papers"], tmp)
        check("search: --papers lists the library", "fx_rotation" in papers.stdout and "1 own" in papers.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def proxy_and_launcher():
    """Local model proxy against a mock OpenAI-compatible server; agent.py dry run."""
    import threading
    import urllib.request
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    sys.path.insert(0, str(ROOT / "src"))
    from llm_proxy import ProxyServer
    seen = {}

    class Mock(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            seen["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen["auth"] = self.headers.get("Authorization")
            if seen["body"].get("stream"):
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                self.wfile.write(b'data: {"choices":[{"delta":{"content":"ok"}}]}\n\n'
                                 b'data: {"choices":[],"usage":{"prompt_tokens":5,"completion_tokens":1}}\n\ndata: [DONE]\n\n')
                return
            b = b'{"choices":[{"message":{"content":"ok"}}],"usage":{"prompt_tokens":10,"completion_tokens":2}}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

    up = ThreadingHTTPServer(("127.0.0.1", 0), Mock)
    threading.Thread(target=up.serve_forever, daemon=True).start()
    px = ProxyServer(f"http://127.0.0.1:{up.server_address[1]}", "KEY", {"thinking": {"type": "disabled"}}).start()

    def post(d):
        req = urllib.request.Request(px.url + "/v1/chat/completions", data=json.dumps(d).encode(),
                                     headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req, timeout=10).read().decode()

    out = post({"model": "m", "messages": []})
    check("proxy: forwards, injects fields and the API key",
          '"ok"' in out and seen["body"].get("thinking") == {"type": "disabled"} and seen["auth"] == "Bearer KEY")
    out = post({"model": "m", "messages": [], "stream": True})
    check("proxy: streams SSE and counts tokens", "[DONE]" in out and px.totals["prompt_tokens"] == 15, str(px.totals))
    px.shutdown()
    up.shutdown()
    r = run(["src/agent.py", "--backend", "deepseek", "--dry-run", "run", "test"], ROOT)
    check("agent.py: dry run builds the Goose command", r.returncode == 0 and "--with-builtin developer" in r.stdout
          and "thinking injected: True" in r.stdout, r.stderr[-300:])


def repository():
    cat = yaml.safe_load((ROOT / "literature" / "catalog.yaml").read_text(encoding="utf-8"))["papers"]
    keys = [p["key"] for p in cat]
    check("catalog: keys unique", len(keys) == len(set(keys)))
    need = {"key", "arxiv", "authors", "year", "venue", "own", "active", "verified", "topic"}
    missing = [p.get("key", "?") for p in cat if not need <= set(p)]
    check("catalog: required fields present", not missing, ", ".join(missing))
    check("catalog: arXiv IDs are strings", all(isinstance(p["arxiv"], str) for p in cat))
    act = [p for p in cat if p.get("active", True)]
    own = sum(bool(p["own"]) for p in act)
    print(f"      catalog: {len(act)} active papers ({own} own, {len(act) - own} external), {len(cat) - len(act)} optional")

    r = run(["src/ontology.py", "validate"], ROOT)
    check("ontology: valid", r.returncode == 0, r.stdout[-400:])
    graph = (ROOT / "ontology" / "graph.md").read_text(encoding="utf-8") if (ROOT / "ontology" / "graph.md").exists() else ""
    before = graph
    run(["src/ontology.py", "graph"], ROOT)
    after = (ROOT / "ontology" / "graph.md").read_text(encoding="utf-8")
    check("ontology: graph.md is up to date", before == after, "regenerated now; commit it")

    report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
    agent = (ROOT / "AGENT.md").read_text(encoding="utf-8").strip()
    check("report: Appendix A is identical to AGENT.md", agent in report,
          "run: python3 tests/selftest.py --sync-report")

    idx = ROOT / "index" / "index.json"
    if idx.exists():
        data = json.loads(idx.read_text(encoding="utf-8"))
        bad = 0
        for c in data["chunks"][:: max(1, len(data["chunks"]) // 300)]:
            f = ROOT / c["file"]
            lines = f.read_text(encoding="utf-8").splitlines() if f.exists() else []
            span = "\n".join(lines[c["line_start"] - 1: c["line_end"]])
            bad += c["text"].split()[0] not in span
        check("library: sampled citations resolve to the right lines", bad == 0, f"{bad} mismatches; rebuild the index")
        missing_md = [p["key"] for p in act if not (ROOT / "literature" / "md" / f"{p['key']}.md").exists()]
        check("library: every active paper is converted", not missing_md, ", ".join(missing_md))
    else:
        print("      library: no index yet (run: make fetch index) - skipped")


def sync_report():
    """Replace Appendix A of REPORT.md with the current AGENT.md."""
    report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
    start, end = "<!-- AGENT.md:BEGIN -->", "<!-- AGENT.md:END -->"
    head, rest = report.split(start)
    _, tail = rest.split(end)
    agent = (ROOT / "AGENT.md").read_text(encoding="utf-8").strip()
    (ROOT / "REPORT.md").write_text(f"{head}{start}\n\n{agent}\n\n{end}{tail}", encoding="utf-8")
    print("REPORT.md Appendix A synced with AGENT.md")


if __name__ == "__main__":
    if "--sync-report" in sys.argv:
        sync_report()
        sys.exit(0)
    print("Part 1: offline pipeline on synthetic fixtures")
    offline_pipeline()
    proxy_and_launcher()
    print("\nPart 2: this repository")
    repository()
    n_fail = results.count(False)
    print(f"\n{'selftest OK' if not n_fail else f'selftest FAILED ({n_fail} of {len(results)} checks)'}")
    sys.exit(1 if n_fail else 0)
