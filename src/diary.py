"""Append one entry to diary.md in the format of AGENTS.md §7 (date and model filled in).

agent.py calls append_entry() after every `run`, so in run mode the agent never writes
the diary itself. In an interactive session the agent ends with one command:

  python3 src/diary.py --request "How does f_peak depend on the EOS?" \
      --actions "search.py 'f_peak EOS'; sed -n '210,224p' literature/md/richers2017.md" \
      --result "f_peak depends on ... [literature/md/richers2017.md:L210-L224 § ...]" \
      --verification "sed -n '210,224p' literature/md/richers2017.md" --open "none"

The model name comes from CCSN_MODEL, which agent.py sets (never from the agent).
"""
import argparse
import datetime as dt
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIARY = ROOT / "diary.md"


def one_line(s, limit=600):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= limit else s[: limit - 3].rsplit(" ", 1)[0] + "..."


def append_entry(request, actions, result, verification, open_issues="none", model=None, checks=None,
                 title=None, path=DIARY):
    model = model or os.environ.get("CCSN_MODEL") or "unknown (not started via src/agent.py)"
    title = one_line(title or request, 80)
    lines = [f"## {dt.datetime.now():%Y-%m-%d %H:%M} — {title}",
             f"- Request: {one_line(request)}",
             f"- Model: {model}",
             f"- Actions: {one_line(actions, 900) or 'none recorded'}",
             f"- Result: {one_line(result) or 'no summary in the answer'}",
             f"- Verification: {one_line(verification) or 'missing'}"]
    if checks:
        lines.append(f"- Citation check: {one_line(checks)}")
    lines.append(f"- Open issues: {one_line(open_issues) or 'none'}")
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    sep = "" if not text or text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    with open(path, "a", encoding="utf-8") as f:
        f.write(sep + "\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Append an entry to diary.md.")
    ap.add_argument("--request", required=True)
    ap.add_argument("--actions", required=True)
    ap.add_argument("--result", required=True)
    ap.add_argument("--verification", required=True)
    ap.add_argument("--open", default="none", help="open issues")
    a = ap.parse_args()
    append_entry(a.request, a.actions, a.result, a.verification, a.open)
    print("diary.md: entry appended")


if __name__ == "__main__":
    main()
