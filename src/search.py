"""Search the local library (BM25 over paragraph chunks of literature/md).

Usage
  python3 src/search.py "f_peak dependence on the EOS" -k 8
  python3 src/search.py "bounce amplitude T/|W|" --file richers2017
  python3 src/search.py "SHAP" --own                 # only my papers
  python3 src/search.py --exact "772" --file richers2017
  python3 src/search.py "leave-one-EOS-out" --json   # machine-readable
  python3 src/search.py --papers                     # list indexed papers

Each hit prints a citation that can be checked directly:
  literature/md/<key>.md:L<start>-L<end> § <section path>
  ->  sed -n '<start>,<end>p' literature/md/<key>.md

Query terms are expanded with synonyms from ontology/concepts.yaml
(e.g. "beta" also matches T/|W|). Standard library only.

JSON output: list of {rank, score, key, own, citation, file, section,
line_start, line_end, text}.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textnorm import tokenize  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index" / "index.json"
K1, B = 1.2, 0.75
SYN_WEIGHT = 0.4


def load_index():
    if not INDEX.exists():
        sys.exit("Index not found. Run: python3 src/build_index.py")
    return json.loads(INDEX.read_text(encoding="utf-8"))


def contains(seq, sub):
    n = len(sub)
    return n > 0 and any(seq[i:i + n] == sub for i in range(len(seq) - n + 1))


def expand(query, groups):
    """Return {token: weight}; ontology synonyms of matched concepts get SYN_WEIGHT."""
    q = tokenize(query)
    weights = {t: 1.0 for t in q}
    for g in groups:
        phrases = [tokenize(p) for p in g["phrases"]]
        if any(contains(q, p) for p in phrases):
            for p in phrases:
                for t in p:
                    weights.setdefault(t, SYN_WEIGHT)
    return weights


def snippet(text, terms, width=320):
    flat = re.sub(r"\s+", " ", text)
    sentences = re.split(r"(?<=[.!?])\s+", flat)
    best = max(sentences, key=lambda s: sum(t in tokenize(s) for t in terms)) if terms else flat
    return best if len(best) <= width else best[:width].rsplit(" ", 1)[0] + " ..."


def main():
    ap = argparse.ArgumentParser(description="Search the local CCSN-GW library.")
    ap.add_argument("query", nargs="?", default="", help="free-text query")
    ap.add_argument("-k", type=int, default=8, help="number of hits (default 8)")
    ap.add_argument("--file", action="append", default=[], help="restrict to paper key(s); repeatable")
    ap.add_argument("--own", action="store_true", help="only papers co-authored by me")
    ap.add_argument("--exact", help="keep only chunks containing this string (case-insensitive)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--papers", action="store_true", help="list indexed papers and exit")
    a = ap.parse_args()

    idx = load_index()
    papers, chunks = idx["papers"], idx["chunks"]

    if a.papers:
        rows = sorted(papers.items(), key=lambda kv: (not kv[1]["own"], kv[0]))
        if a.json:
            print(json.dumps([{"key": k, **v} for k, v in rows], ensure_ascii=False, indent=1))
            return
        for k, p in rows:
            print(f"{'own' if p['own'] else 'ext'}  {k:28s} {p['year']}  {p['chunks']:4d} chunks  {p['venue']}")
        own = sum(p["own"] for p in papers.values())
        print(f"\n{len(papers)} papers ({own} own, {len(papers) - own} external), {len(chunks)} chunks; built {idx['built']}")
        return

    if not a.query and not a.exact:
        ap.error("give a query, --exact, or --papers")
    unknown = [f for f in a.file if f not in papers]
    if unknown:
        sys.exit(f"Unknown paper key(s): {', '.join(unknown)}. See: python3 src/search.py --papers")

    # corpus statistics over the whole library (filters do not change IDF)
    toks = [c["tokens"].split() for c in chunks]
    n = len(chunks)
    avgdl = sum(map(len, toks)) / n
    df = Counter(t for ts in toks for t in set(ts))

    weights = expand(a.query, idx.get("synonym_groups", [])) if a.query else {}
    needle = a.exact.lower() if a.exact else None
    hits = []
    for i, c in enumerate(chunks):
        if a.file and c["key"] not in a.file:
            continue
        if a.own and not papers[c["key"]]["own"]:
            continue
        if needle and needle not in c["text"].lower():
            continue
        if weights:
            tf = Counter(toks[i])
            dl = len(toks[i])
            score = 0.0
            for t, w in weights.items():
                f = tf.get(t, 0)
                if f:
                    idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                    score += w * idf * f * (K1 + 1) / (f + K1 * (1 - B + B * dl / avgdl))
            if score <= 0:
                continue
        else:
            score = c["text"].lower().count(needle)
        hits.append((score, i))

    if weights:
        hits.sort(key=lambda h: -h[0])
    hits = hits[: max(a.k, 0)]
    out = []
    for rank, (score, i) in enumerate(hits, 1):
        c = chunks[i]
        out.append({
            "rank": rank, "score": round(score, 3), "key": c["key"], "own": papers[c["key"]]["own"],
            "citation": f"{c['file']}:L{c['line_start']}-L{c['line_end']} § {c['section']}",
            "file": c["file"], "section": c["section"],
            "line_start": c["line_start"], "line_end": c["line_end"], "text": c["text"],
        })

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    if not out:
        scope = []
        if a.own:
            scope.append("own papers")
        if a.file:
            scope.append("papers " + ", ".join(a.file))
        print(f"No results{' in ' + ' and '.join(scope) if scope else ''}.")
        return
    terms = list(weights) or tokenize(a.exact or "")
    for h in out:
        print(f"[{h['rank']}] {h['score']:.2f}  {h['citation']}")
        print(f"    {snippet(h['text'], terms)}\n")


if __name__ == "__main__":
    main()
