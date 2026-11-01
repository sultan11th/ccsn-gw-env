"""Run the course agent (Goose, as packaged by AI4Science) with a local model or DeepSeek.

The course wrapper `ai4science` only talks to Yandex AI Studio (3M tokens/day). This
launcher starts the same Goose binary with the same course instructions, but points it
at another OpenAI-compatible server, so that only the model changes:

  local     a model server on this machine, e.g. vLLM (http://localhost:8000) or
            Ollama (http://localhost:11434); no token limit
  deepseek  DeepSeek API                  https://api.deepseek.com   (pay per token)

Usage
  python3 src/agent.py --backend local                        # interactive session
  python3 src/agent.py --backend local run "What is f_peak?"  # one task, then exit
  python3 src/agent.py --backend deepseek run "..."
  python3 src/agent.py --backend local --model qwen3-coder:30b run "..."   # e.g. Ollama tag
  python3 src/agent.py --backend local --dry-run run "..."    # show what would run

Settings (environment or a .env file in the repository root, never committed)
  AI4SCIENCE_HOME    folder of the AI4Science clone (default ~/AI4Science); used for the
                     Goose binary (.tools/goose) and the course instructions (recipes/ai4science.yaml)
  LOCAL_URL          default http://localhost:8000 (vLLM); Ollama: http://localhost:11434
  LOCAL_MODEL        default qwen3-coder-30b (the name the server reports, e.g. vLLM --served-model-name)
  DEEPSEEK_MODEL     default deepseek-flash   DEEPSEEK_API_KEY  required for --backend deepseek
  LOCAL_CONTEXT      context window told to Goose for the local model (default 32768; keep it
                     equal to the server's limit: vLLM --max-model-len, Ollama OLLAMA_CONTEXT_LENGTH)

What the agent gets: the course instructions + this project's AGENT.md as system prompt,
and Goose's built-in `developer` tools (shell, file editor), which is all it needs to run
src/search.py and src/ontology.py. Token usage is logged to results/agent_runs/usage.jsonl.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_proxy import ProxyServer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
USAGE_LOG = ROOT / "results" / "agent_runs" / "usage.jsonl"

BACKENDS = {
    "local": {"url_env": "LOCAL_URL", "url": "http://localhost:8000", "model_env": "LOCAL_MODEL",
              "model": "qwen3-coder-30b", "key_env": "LOCAL_API_KEY", "inject": {},
              "context_env": "LOCAL_CONTEXT", "context": 32768},
    "deepseek": {"url_env": "DEEPSEEK_URL", "url": "https://api.deepseek.com", "model_env": "DEEPSEEK_MODEL",
                 "model": "deepseek-flash", "key_env": "DEEPSEEK_API_KEY",
                 # thinking off: with thinking on, tool-using turns must resend reasoning_content
                 "inject": {"thinking": {"type": "disabled"}},
                 "context_env": "DEEPSEEK_CONTEXT", "context": 128000},
}

MINIMAL_PROMPT = """You are a research assistant working in the user's project folder through a shell.
Run commands to find facts; never answer factual questions from memory. Run code before reporting results.
Keep answers short. The project contract below (AGENT.md) has priority over these lines."""


def load_dotenv(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def course_home():
    return Path(os.environ.get("AI4SCIENCE_HOME", "~/AI4Science")).expanduser()


def find_goose():
    home = course_home()
    for p in (home / ".tools" / "goose", home / ".tools" / "goose.exe"):
        if p.exists():
            return str(p)
    return shutil.which("goose")


def course_instructions():
    recipe = course_home() / "recipes" / "ai4science.yaml"
    if not recipe.exists():
        return None
    import yaml  # PyYAML is in requirements.txt
    return (yaml.safe_load(recipe.read_text(encoding="utf-8")) or {}).get("instructions")


def system_prompt(kind):
    base = course_instructions() if kind == "course" else None
    if kind == "course" and not base:
        print("[agent] course recipe not found; using the minimal prompt (set AI4SCIENCE_HOME)", file=sys.stderr)
    contract = (ROOT / "AGENT.md").read_text(encoding="utf-8")
    used = "course" if base else "minimal"
    return used, (base or MINIMAL_PROMPT) + "\n\n# Project contract (AGENT.md, read from the project folder)\n\n" + contract


def main():
    ap = argparse.ArgumentParser(description="Course agent (Goose) with a local model or DeepSeek.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--backend", choices=BACKENDS, required=True)
    ap.add_argument("--model", help="override the model name")
    ap.add_argument("--prompt", choices=["course", "minimal"], default="course",
                    help="course = AI4Science instructions + AGENT.md (default); minimal = short prompt + AGENT.md")
    ap.add_argument("--mode", choices=["auto", "smart_approve", "approve", "chat"],
                    help="Goose permission mode (default: auto for run, smart_approve for sessions)")
    ap.add_argument("--dry-run", action="store_true", help="print the command and settings, do not start")
    ap.add_argument("task", nargs=argparse.REMAINDER, help='"run" followed by the task text, or nothing for a session')
    a = ap.parse_args()

    load_dotenv(ROOT / ".env")
    b = BACKENDS[a.backend]
    model = a.model or os.environ.get(b["model_env"], b["model"])
    upstream = os.environ.get(b["url_env"]) or (os.environ.get("OLLAMA_URL") if a.backend == "local" else None) or b["url"]
    key = os.environ.get(b["key_env"]) if b["key_env"] else None
    if a.backend == "deepseek" and not key and not a.dry_run:
        sys.exit(f"{b['key_env']} is not set (environment or .env in the repository root)")
    run_mode = bool(a.task) and a.task[0] == "run"
    task = " ".join(a.task[1:]) if run_mode else ""
    if a.task and not run_mode:
        ap.error('use: run "<task>", or no arguments for an interactive session')
    if run_mode and not task:
        ap.error("run: task text is missing")

    goose = find_goose()
    if not goose and not a.dry_run:
        sys.exit("Goose not found. Install AI4Science (it downloads Goose to .tools/) and set AI4SCIENCE_HOME, "
                 "or put `goose` on PATH.")

    fd, prompt_path = tempfile.mkstemp(suffix=".md", prefix="ccsn-agent-prompt-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        prompt_used, prompt_text = system_prompt(a.prompt)
        f.write(prompt_text)

    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    proxy = ProxyServer(upstream, key, b["inject"], str(USAGE_LOG), label=f"{a.backend}:{model}")
    env = os.environ.copy()
    env.update({
        "GOOSE_PROVIDER": "openai",                      # Ollama and DeepSeek both speak the OpenAI API
        "OPENAI_HOST": proxy.url,
        "OPENAI_BASE_PATH": "/v1/chat/completions",
        "OPENAI_API_KEY": "via-proxy",                   # the proxy adds the real key
        "GOOSE_MODEL": model,
        "GOOSE_CONTEXT_LIMIT": os.environ.get(b["context_env"], str(b["context"])),
        "GOOSE_MODE": a.mode or ("auto" if run_mode else "smart_approve"),
        "GOOSE_SYSTEM_PROMPT_FILE_PATH": prompt_path,
        "GOOSE_TEMPERATURE": os.environ.get("GOOSE_TEMPERATURE", "0.2"),
        "GOOSE_PATH_ROOT": str(ROOT / ".goose"),
        "GOOSE_TELEMETRY_ENABLED": "false",
    })
    cmd = [goose or "goose"]
    cmd += (["run", "--no-profile", "--no-session", "--with-builtin", "developer", "-t", task] if run_mode
            else ["session", "--no-profile", "--with-builtin", "developer"])

    if a.dry_run:
        shown = {k: env[k] for k in ("GOOSE_PROVIDER", "GOOSE_MODEL", "GOOSE_CONTEXT_LIMIT", "GOOSE_MODE")}
        print(f"backend:  {a.backend} -> {upstream} (thinking injected: {bool(b['inject'])})")
        print(f"model:    {model}")
        print(f"home:     {course_home()} (AI4SCIENCE_HOME)")
        print(f"prompt:   {prompt_used} ({len(open(prompt_path, encoding='utf-8').read()):,} chars incl. AGENT.md)")
        print(f"goose:    {goose or 'NOT FOUND'}")
        print(f"env:      {shown}")
        print(f"command:  {' '.join(cmd[:-1] + [repr(cmd[-1])]) if run_mode else ' '.join(cmd)}")
        os.unlink(prompt_path)
        proxy.server_close()
        return 0

    proxy.start()
    try:
        rc = subprocess.run(cmd, env=env, cwd=ROOT).returncode
    finally:
        proxy.shutdown()
        os.unlink(prompt_path)
        t = proxy.totals
        print(f"\n[agent] {a.backend}:{model} - {t['requests']} requests, {t['prompt_tokens']:,} prompt + "
              f"{t['completion_tokens']:,} completion tokens, {t['errors']} errors (log: "
              f"{USAGE_LOG.relative_to(ROOT)})", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
