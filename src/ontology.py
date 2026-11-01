"""Validate, render and query the project ontology (ontology/concepts.yaml).

Usage
  python3 src/ontology.py validate        # dangling relations, unknown sources, duplicate synonyms
  python3 src/ontology.py graph           # writes ontology/graph.md (Mermaid, rendered by GitHub)
  python3 src/ontology.py show f_peak     # concept card: definition, relations both ways, sources
  python3 src/ontology.py show beta       # lookup also works by label or synonym
  python3 src/ontology.py list            # all concepts grouped
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "concepts.yaml"
CATALOG = ROOT / "literature" / "catalog.yaml"
GRAPH = ROOT / "ontology" / "graph.md"
EDGE_STYLE = {"is_a": "-->", "part_of": "-->", "depends_on": "==>", "estimates": "-.->",
              "uses": "-.->", "related_to": "---"}


def load():
    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    papers = {p["key"]: p for p in yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["papers"]}
    return onto, papers


def relations(onto):
    rels = list(onto["relation_types"])
    for cid, c in onto["concepts"].items():
        for r in rels:
            for t in c.get(r, []) or []:
                yield cid, r, t


def validate(onto, papers):
    errors, warnings = [], []
    concepts, rels = onto["concepts"], onto["relation_types"]
    allowed = set(rels) | {"label", "group", "synonyms", "definition", "sources"}
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
    for src, r, dst in relations(onto):
        if dst not in concepts:
            errors.append(f"{src} --{r}--> '{dst}': target concept not defined")
        if dst == src:
            errors.append(f"{src} --{r}--> itself")
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
    out = [(r, t) for s, r, t in relations(onto) if s == cid]
    inc = [(s, r) for s, r, t in relations(onto) if t == cid]
    for r, t in out:
        print(f"  -> {r:10s} {onto['concepts'][t]['label']} [{t}]")
    for s, r in inc:
        print(f"  <- {r:10s} {onto['concepts'][s]['label']} [{s}]")
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
    for s, r, t in relations(onto):
        lines.append(f"  {s} {EDGE_STYLE.get(r, '-->')}|{r}| {t}")
    n_rel = sum(1 for _ in relations(onto))
    body = "\n".join(lines)
    GRAPH.write_text(
        "# Concept graph\n\n"
        f"Generated from `ontology/concepts.yaml` by `python3 src/ontology.py graph` "
        f"({len(concepts)} concepts, {n_rel} relations). Do not edit by hand.\n\n"
        "Arrows: `-->` is_a / part_of, `==>` depends_on, `-.->` estimates / uses, `---` related_to.\n\n"
        f"```mermaid\n{body}\n```\n", encoding="utf-8")
    print(f"Wrote {GRAPH.relative_to(ROOT)} ({len(concepts)} concepts, {n_rel} relations)")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"validate", "graph", "show", "list"}:
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
    elif cmd == "list":
        for g, title in onto["groups"].items():
            print(f"{title}:")
            for cid, c in onto["concepts"].items():
                if c["group"] == g:
                    print(f"  {cid:24s} {c['label']}")


if __name__ == "__main__":
    main()
