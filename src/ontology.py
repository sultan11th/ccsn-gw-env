"""Validate, render and query the project ontology (ontology/concepts.yaml).

Usage
  python3 src/ontology.py validate        # dangling relations, unknown sources, evidence, data columns
  python3 src/ontology.py graph           # writes ontology/graph.md (Mermaid, rendered by GitHub)
  python3 src/ontology.py show f_peak     # concept card: definition, relations + evidence, data, sources
  python3 src/ontology.py show beta       # lookup also works by label or synonym
  python3 src/ontology.py list            # all concepts grouped
  python3 src/ontology.py audit           # coverage of the library, retrieval of each concept,
                                          # evidence for claims, generic synonyms (needs the index)

A relation target is a concept id or {to: <id>, evidence: "literature/md/<key>.md:L<a>-L<b>"}.
"""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "concepts.yaml"
CATALOG = ROOT / "literature" / "catalog.yaml"
GRAPH = ROOT / "ontology" / "graph.md"
DATA_DICT = ROOT / "data" / "data" / "data_dictionary.csv"
INDEX = ROOT / "index" / "index.json"
CITE = re.compile(r"^literature/md/([\w.-]+)\.md:L(\d+)-L(\d+)$")
CLAIMS = ("depends_on", "estimates")          # relation types that should carry evidence
GENERIC_DF = 0.05                              # a lowercase one-word synonym in > 5 % of chunks is too generic
EDGE_STYLE = {"is_a": "-->", "part_of": "-->", "depends_on": "==>", "estimates": "-.->",
              "uses": "-.->", "related_to": "---"}


def load():
    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    papers = {p["key"]: p for p in yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["papers"]}
    return onto, papers


def relations(onto, evidence=False):
    """Yield (source, relation, target) or, with evidence=True, (source, relation, target, citation)."""
    rels = list(onto["relation_types"])
    for cid, c in onto["concepts"].items():
        for r in rels:
            for t in c.get(r, []) or []:
                target, ev = (t.get("to"), t.get("evidence")) if isinstance(t, dict) else (t, None)
                yield (cid, r, target, ev) if evidence else (cid, r, target)


def data_columns():
    """Column names of the local dataset (None if data/ is absent)."""
    if not DATA_DICT.exists():
        return None
    with open(DATA_DICT, newline="", encoding="utf-8") as f:
        return {r["column"] for r in csv.DictReader(f) if r["file"] == "parameters.csv"} | {"strain"}


def check_citation(cite, papers):
    m = CITE.match(str(cite or ""))
    if not m:
        return "evidence must look like literature/md/<key>.md:L<a>-L<b>"
    key, a, b = m.group(1), int(m.group(2)), int(m.group(3))
    if key not in papers:
        return f"evidence paper '{key}' not in literature/catalog.yaml"
    f = ROOT / "literature" / "md" / f"{key}.md"
    if not f.exists():
        return None                                 # library not built here; checked where it is
    n = len(f.read_text(encoding="utf-8").splitlines())
    return None if 1 <= a <= b <= n else f"evidence lines L{a}-L{b} outside {f.name} ({n} lines)"


def validate(onto, papers):
    errors, warnings = [], []
    concepts, rels = onto["concepts"], onto["relation_types"]
    allowed = set(rels) | {"label", "group", "synonyms", "definition", "sources", "data_columns"}
    cols = data_columns()
    seen = {}
    for cid, c in concepts.items():
        for field in c:
            if field not in allowed:
                errors.append(f"{cid}: unknown field '{field}'")
        for field in ("label", "group", "definition", "sources"):
            if not c.get(field):
                errors.append(f"{cid}: missing '{field}'")
        if c.get("group") and c["group"] not in onto["groups"]:
            errors.append(f"{cid}: unknown group '{c['group']}'")
        for s in c.get("sources", []) or []:
            if s not in papers:
                errors.append(f"{cid}: source '{s}' not in literature/catalog.yaml")
            elif not papers[s].get("active", True):
                warnings.append(f"{cid}: source '{s}' is inactive (not in the library)")
        for term in [c.get("label", "")] + list(c.get("synonyms", []) or []):
            t = str(term).lower()
            if t in seen and seen[t] != cid:
                warnings.append(f"synonym '{term}' used by both {seen[t]} and {cid}")
            seen[t] = cid
        if cols is not None:
            for col in c.get("data_columns", []) or []:
                if col not in cols:
                    errors.append(f"{cid}: data column '{col}' not in data/data/data_dictionary.csv")
    for src, r, dst, ev in relations(onto, evidence=True):
        if dst not in concepts:
            errors.append(f"{src} --{r}--> '{dst}': target concept not defined")
        if dst == src:
            errors.append(f"{src} --{r}--> itself")
        if ev:
            problem = check_citation(ev, papers)
            if problem:
                errors.append(f"{src} --{r}--> {dst}: {problem}")
    return errors, warnings


def find(onto, term):
    concepts = onto["concepts"]
    t = term.lower().strip()
    if t in concepts:
        return t
    for cid, c in concepts.items():
        names = [str(c.get("label", ""))] + [str(s) for s in c.get("synonyms", []) or []]
        if t in (n.lower() for n in names):
            return cid
    matches = [cid for cid, c in concepts.items() if t in str(c.get("label", "")).lower()]
    return matches[0] if len(matches) == 1 else None


def show(onto, papers, term):
    cid = find(onto, term)
    if not cid:
        sys.exit(f"No concept matches '{term}'. Try: python3 src/ontology.py list")
    c = onto["concepts"][cid]
    print(f"{c['label']}  [{cid}, group: {c['group']}]")
    print(f"  Definition: {c['definition']}")
    if c.get("synonyms"):
        print(f"  Synonyms:   {', '.join(map(str, c['synonyms']))}")
    def ev_text(ev):
        if not ev:
            return ""
        m = CITE.match(ev)
        return f"\n       evidence: [{ev}]  ->  sed -n '{m.group(2)},{m.group(3)}p' literature/md/{m.group(1)}.md"
    out = [(r, t, ev) for s, r, t, ev in relations(onto, evidence=True) if s == cid]
    inc = [(s, r, ev) for s, r, t, ev in relations(onto, evidence=True) if t == cid]
    for r, t, ev in out:
        print(f"  -> {r:10s} {onto['concepts'][t]['label']} [{t}]{ev_text(ev)}")
    for s, r, ev in inc:
        print(f"  <- {r:10s} {onto['concepts'][s]['label']} [{s}]{ev_text(ev)}")
    if c.get("data_columns"):
        cols = [x for x in c["data_columns"] if x != "strain"]
        print(f"  Data:       {', '.join(c['data_columns'])} (data/data/)")
        if cols:
            print(f"              python3 src/data.py stats {cols[0]} --by eos")
        if "strain" in c["data_columns"]:
            print("              python3 src/data.py strain <run_id>")
    print("  Sources:")
    for s in c.get("sources", []):
        p = papers.get(s, {})
        print(f"    {s}: {p.get('authors', '?')} ({p.get('year', '?')}), {p.get('venue', '?')}"
              f"  -> literature/md/{s}.md")


def mermaid_label(text):
    return str(text).replace('"', "#quot;")


def graph(onto):
    concepts = onto["concepts"]
    lines = ["graph LR"]
    for g, title in onto["groups"].items():
        lines.append(f'  subgraph {g}["{mermaid_label(title)}"]')
        for cid, c in concepts.items():
            if c["group"] == g:
                lines.append(f'    {cid}["{mermaid_label(c["label"])}"]')
        lines.append("  end")
    for s, r, t, ev in relations(onto, evidence=True):
        lines.append(f"  {s} {EDGE_STYLE.get(r, '-->')}|{r}{' *' if ev else ''}| {t}")
    n_rel = sum(1 for _ in relations(onto))
    body = "\n".join(lines)
    GRAPH.write_text(
        "# Concept graph\n\n"
        f"Generated from `ontology/concepts.yaml` by `python3 src/ontology.py graph` "
        f"({len(concepts)} concepts, {n_rel} relations). Do not edit by hand.\n\n"
        "Arrows: `-->` is_a / part_of, `==>` depends_on, `-.->` estimates / uses, `---` related_to. "
        "`*` marks a relation with a cited passage (`python3 src/ontology.py show <concept>`).\n\n"
        f"```mermaid\n{body}\n```\n", encoding="utf-8")
    print(f"Wrote {GRAPH.relative_to(ROOT)} ({len(concepts)} concepts, {n_rel} relations)")


def audit(onto, papers, as_json=False):
    """Coverage, self-retrieval, evidence and synonym checks; returns the result dict."""
    concepts = onto["concepts"]
    active = sorted(k for k, p in papers.items() if p.get("active", True))
    used = {s for c in concepts.values() for s in c.get("sources", [])}
    res = {"uncovered_papers": [k for k in active if k not in used]}
    claims = [(s, r, t, ev) for s, r, t, ev in relations(onto, evidence=True) if r in CLAIMS]
    res["claims"] = len(claims)
    res["claims_without_evidence"] = [f"{s} {r} {t}" for s, r, t, ev in claims if not ev]
    if INDEX.exists():
        miss = []
        for cid, c in concepts.items():
            r = subprocess.run([sys.executable, str(ROOT / "src" / "search.py"), str(c["label"]), "-k", "5", "--json"],
                               capture_output=True, text=True)
            keys = {h["key"] for h in json.loads(r.stdout or "[]")}
            if not keys & set(c.get("sources", [])):
                miss.append(cid)
        res["retrieval_misses"] = miss
        idx = json.loads(INDEX.read_text(encoding="utf-8"))
        sys.path.insert(0, str(ROOT / "src"))
        from textnorm import tokenize
        n = len(idx["chunks"])
        df = {}
        for ch in idx["chunks"]:
            for t in set(ch["tokens"].split()):
                df[t] = df.get(t, 0) + 1
        generic = []
        for cid, c in concepts.items():
            for syn in c.get("synonyms", []) or []:
                toks = tokenize(str(syn))
                acronym = any(ch.isupper() for ch in str(syn))   # CCSN, EOS, LIGO: names, not common words
                if len(toks) == 1 and not acronym and df.get(toks[0], 0) / n > GENERIC_DF:
                    generic.append(f"{cid}: '{syn}' in {df[toks[0]] / n:.0%} of chunks")
        res["generic_synonyms"] = generic
    if as_json:
        return res
    print(f"Library coverage: {len(active) - len(res['uncovered_papers'])}/{len(active)} papers are a source of some concept")
    for k in res["uncovered_papers"]:
        print(f"  not used: {k}")
    print(f"Evidence: {res['claims'] - len(res['claims_without_evidence'])}/{res['claims']} depends_on/estimates relations cite a passage")
    for x in res["claims_without_evidence"]:
        print(f"  no evidence: {x}")
    if "retrieval_misses" in res:
        print(f"Retrieval: {len(concepts) - len(res['retrieval_misses'])}/{len(concepts)} concepts find one of their "
              f"sources in the top 5 when their label is searched")
        for x in res["retrieval_misses"]:
            print(f"  miss: {x} ({concepts[x]['label']})")
        print(f"Generic one-word synonyms (> {GENERIC_DF:.0%} of chunks): {len(res['generic_synonyms'])}")
        for x in res["generic_synonyms"]:
            print(f"  {x}")
    else:
        print("Retrieval and synonym checks skipped: no index (run: python3 src/build_index.py)")
    return res


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"validate", "graph", "show", "list", "audit"}:
        sys.exit(__doc__)
    onto, papers = load()
    cmd = sys.argv[1]
    errors, warnings = validate(onto, papers)
    if cmd == "validate" or errors:
        for w in warnings:
            print(f"warning: {w}")
        for e in errors:
            print(f"ERROR: {e}")
        if errors:
            sys.exit(1)
        if cmd == "validate":
            n_rel = sum(1 for _ in relations(onto))
            print(f"Ontology OK: {len(onto['concepts'])} concepts, {n_rel} relations, "
                  f"{len(onto['relation_types'])} relation types")
            return
    if cmd == "graph":
        graph(onto)
    elif cmd == "show":
        if len(sys.argv) < 3:
            sys.exit("Usage: python3 src/ontology.py show <concept|synonym>")
        show(onto, papers, " ".join(sys.argv[2:]))
    elif cmd == "audit":
        audit(onto, papers)
    elif cmd == "list":
        for g, title in onto["groups"].items():
            print(f"{title}:")
            for cid, c in onto["concepts"].items():
                if c["group"] == g:
                    print(f"  {cid:24s} {c['label']}")


if __name__ == "__main__":
    main()
