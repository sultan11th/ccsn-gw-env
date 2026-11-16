"""Build the search index over literature/md/*.md.

Usage:  python3 src/build_index.py

Papers are split into chunks of whole paragraphs (about 180 words) inside one
section. Each chunk keeps its heading path ("IV. Results > A. Bounce signal")
and its line range in the Markdown file, so a citation can be checked with
`sed -n 'START,ENDp' literature/md/<key>.md`.

Reference lists and acknowledgments are not indexed: sections named References,
Bibliography or Acknowledg(e)ments are skipped, and so are chunks that look like a
bibliography without such a heading (3 or more entries such as "**442**, 38 (2007)",
"DOI 10.…" or "2013, Astrophys. J., 770"). They matched topic words while saying nothing about them.

Output: index/index.json (chunks, tokens, paper list, ontology synonym groups).
Requires PyYAML; tokenisation is shared with search.py (src/textnorm.py).
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textnorm import tokenize  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MD_DIR = ROOT / "literature" / "md"
CATALOG = ROOT / "literature" / "catalog.yaml"
ONTOLOGY = ROOT / "ontology" / "concepts.yaml"
OUT = ROOT / "index" / "index.json"

TARGET_WORDS = 180      # close a chunk once it reaches this size
MAX_WORDS = 350         # split a single paragraph longer than this
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
SKIP_LINE = re.compile(r"^\s*(!\[|<img|<figure|</figure|<embed)")
SKIP_SECTION = re.compile(r"^(?:[\dIVXA-Z]{1,4}[.)]?\s+|chapter\s+\d+\s+)?"
                          r"(references|bibliography|cross-references|acknowledge?ments?)\.?$", re.I)
BIB_ENTRY = re.compile(r"\*\*\d+\*\*(?:\(\d+\))?,\s*[A-Za-z]?\d+\w*\s*\((?:19|20)\d\d\)|\bdoi:?\s*\[?`?10\.\d|\bDOI 10\.\d|"
                       r"\b(?:19|20)\d\d,\s+(?:Astrophys|Astron|Mon\.|Phys\.|Class\.|Nature|ApJ|MNRAS)", re.I)


def is_back_matter(section, text):
    """True for reference lists and acknowledgments (by heading or by content)."""
    if any(SKIP_SECTION.match(part.strip()) for part in section.split(" > ")):
        return True
    return len(BIB_ENTRY.findall(text)) >= 3


def front_matter(lines):
    """Return (metadata dict, index of first body line)."""
    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 200)):
            if lines[i].strip() == "---":
                try:
                    return yaml.safe_load("\n".join(lines[1:i])) or {}, i + 1
                except yaml.YAMLError:
                    return {}, i + 1
    return {}, 0


def clean_heading(text):
    text = re.sub(r"\{#[^}]*\}", "", text)          # pandoc anchors
    text = re.sub(r"<[^>]+>", "", text)             # html tags
    return re.sub(r"\s+", " ", text).strip() or "Untitled"


def chunk_file(path, key):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    meta, start = front_matter(lines)
    stack, chunks = [], []
    cur, cur_start, cur_end = [], None, None       # current chunk: paragraphs
    para, para_start = [], None                    # current paragraph

    def section():
        return " > ".join(t for _, t in stack) if stack else "Front matter"

    def emit(text_lines, a, b):
        text = "\n".join(text_lines).strip()
        if len(text.split()) < 12 or is_back_matter(section(), text):
            return
        chunks.append({"key": key, "section": section(), "line_start": a, "line_end": b, "text": text})

    def close_chunk():
        nonlocal cur, cur_start, cur_end
        if cur:
            emit(cur, cur_start, cur_end)
        cur, cur_start, cur_end = [], None, None

    def close_para(end_line):
        nonlocal para, para_start, cur, cur_start, cur_end
        if not para:
            return
        words = " ".join(para).split()
        if len(words) > MAX_WORDS:                 # very long paragraph: own chunks
            close_chunk()
            for i in range(0, len(words), TARGET_WORDS):
                emit([" ".join(words[i:i + TARGET_WORDS + 20])], para_start, end_line)
        else:
            if cur_start is None:
                cur_start = para_start
            cur.extend(para + [""])
            cur_end = end_line
            if sum(len(x.split()) for x in cur) >= TARGET_WORDS:
                close_chunk()
        para, para_start = [], None

    for i in range(start, len(lines)):
        line, lineno = lines[i], i + 1
        m = HEADING.match(line)
        if m:
            close_para(lineno - 1)
            close_chunk()
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, clean_heading(m.group(2))))
            continue
        if not line.strip():
            close_para(lineno - 1)
            continue
        if SKIP_LINE.match(line):
            continue
        if para_start is None:
            para_start = lineno
        para.append(line)
    close_para(len(lines))
    close_chunk()
    return meta, chunks


def key_words(key):
    """'richers2017' -> 'richers 2017'; 'abylkairov2025_distance' -> 'abylkairov 2025 distance'."""
    return re.sub(r"(\d+)", r" \1 ", key.replace("_", " "))


def synonym_groups():
    if not ONTOLOGY.exists():
        return []
    concepts = (yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8")) or {}).get("concepts", {})
    groups = []
    for cid, c in concepts.items():
        phrases = [str(c.get("label", cid))] + [str(s) for s in c.get("synonyms", [])]
        groups.append({"concept": cid, "phrases": phrases})
    return groups


def main():
    catalog = {p["key"]: p for p in yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["papers"]}
    files = sorted(MD_DIR.glob("*.md"))
    if not files:
        sys.exit("No Markdown files in literature/md/. Run: python3 src/fetch_arxiv.py --all")
    papers, chunks, unknown = {}, [], []
    for f in files:
        key = f.stem
        if key not in catalog:
            unknown.append(key)
            continue
        meta, cs = chunk_file(f, key)
        entry = catalog[key]
        prefix = key_words(key)
        for c in cs:
            c["id"] = f"{key}#{len(chunks) + 1}"
            c["file"] = f"literature/md/{f.name}"
            c["tokens"] = " ".join(tokenize(prefix + " " + c["section"] + " " + c["text"]))
            chunks.append(c)
        papers[key] = {
            "title": meta.get("title") or entry.get("topic", ""),
            "authors": entry.get("authors"), "year": entry.get("year"),
            "venue": entry.get("venue"), "own": bool(entry.get("own")),
            "method": meta.get("method"), "chunks": len(cs),
        }
    if unknown:
        print(f"WARNING: not in catalog, skipped: {', '.join(unknown)}", file=sys.stderr)
    if not chunks:
        sys.exit("No chunks produced.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "built": dt.datetime.now().isoformat(timespec="seconds"),
        "papers": papers, "synonym_groups": synonym_groups(), "chunks": chunks,
    }, ensure_ascii=False), encoding="utf-8")
    own = sum(p["own"] for p in papers.values())
    print(f"Indexed {len(chunks)} chunks from {len(papers)} papers ({own} own, {len(papers) - own} external) -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
