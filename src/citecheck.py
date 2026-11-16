"""Check the citations in an agent transcript (shared by agent.py and run_queries.py).

A citation is `literature/md/<key>.md:L<start>-L<end>`. It is
  valid      the key is in the catalog, the file exists and the line range lies inside it;
  searched   additionally, the range lies inside a hit that src/search.py printed in the
             same transcript (AGENT.md: cite only passages the search returned).
Search hits are recognised in the text output (`[3] 7.97  literature/md/...:L10-L20 § ...`)
in --json output (`"citation": "literature/md/...:L10-L20 § ..."`) and in the evidence
lines of `ontology.py show` (`evidence: [literature/md/...:L10-L20]`); those lines are
not counted as citations of the answer.

  python3 src/citecheck.py transcript.txt       # prints the report
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CITE = re.compile(r"(literature/md/([\w.-]+)\.md):L(\d+)-L(\d+)")
HIT_LINE = re.compile(r'^\s*(?:\[\d+\]\s+[\d.]+\s+|"citation":\s*"|evidence:\s*\[)literature/md/')
LOOSE_REF = re.compile(r"literature/md/([\w.-]+)\.md(?!:L\d)")


def catalog_keys():
    cat = yaml.safe_load((ROOT / "literature" / "catalog.yaml").read_text(encoding="utf-8"))
    return {p["key"] for p in cat["papers"]}


def _n_lines(path, cache={}):
    if path not in cache:
        f = ROOT / path
        cache[path] = len(f.read_text(encoding="utf-8").splitlines()) if f.exists() else 0
    return cache[path]


def check(text, keys=None):
    keys = catalog_keys() if keys is None else keys
    hits, cited = [], []
    for line in text.splitlines():
        target = hits if HIT_LINE.match(line) else cited
        target.extend((p, k, int(a), int(b)) for p, k, a, b in CITE.findall(line))
    valid, invalid, unsearched = set(), set(), set()
    for p, k, a, b in cited:
        ref = f"{p}:L{a}-L{b}"
        if k not in keys or not (1 <= a <= b <= _n_lines(p)):
            invalid.add(ref)
            continue
        valid.add(ref)
        if not any(p == hp and ha <= a and b <= hb for hp, _, ha, hb in hits):
            unsearched.add(ref)
    return {"valid": sorted(valid), "invalid": sorted(invalid), "unsearched": sorted(unsearched),
            "search_hits": len(hits), "refs_without_lines": sorted(set(LOOSE_REF.findall(text)))}


def summary(r):
    s = f"{len(r['valid'])} valid, {len(r['invalid'])} invalid, {len(r['unsearched'])} not returned by search.py"
    return s + (" - OK" if r["valid"] and not r["invalid"] and not r["unsearched"] else " - CHECK")


def report(r):
    out = [f"[citations] {summary(r)}"]
    out += [f"  invalid:    {c}" for c in r["invalid"]]
    out += [f"  not found in a search hit: {c}" for c in r["unsearched"]]
    if not r["valid"] and not r["invalid"]:
        out.append("  the answer has no line-range citations")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(report(check(Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore"))))
