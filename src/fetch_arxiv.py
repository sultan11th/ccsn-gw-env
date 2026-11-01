"""Download papers from arXiv and convert them to Markdown in literature/md/.

Usage
  python3 src/fetch_arxiv.py richers2017               # one or more catalog keys
  python3 src/fetch_arxiv.py --all                     # every active catalog entry not yet converted
  python3 src/fetch_arxiv.py --all --force             # re-convert everything
  python3 src/fetch_arxiv.py richers2017 --local ~/Downloads/1701.02752.tar.gz
                                                       # convert a file you downloaded yourself
  python3 src/fetch_arxiv.py --meta 2401.11635         # print arXiv metadata (to fill a catalog row)
  python3 src/fetch_arxiv.py --check                   # compare catalog.yaml with arXiv metadata

Conversion order (first that succeeds wins):
  1. LaTeX source  (arxiv.org/e-print/<id>) -> pandoc -> GitHub Markdown, equations kept as $...$
  2. arXiv HTML    (arxiv.org/html/<id>)    -> pandoc
  3. PDF           (arxiv.org/pdf/<id>)     -> marker_single or mineru if installed, else pypdf
                                               (pypdf gives one "## Page N" section per page)
The paper is only registered through literature/catalog.yaml: add a row first.
Downloads go to literature/raw/<key>/ (read-only afterwards). arXiv is asked at
most once every 3 s, as its API terms of use require. Needs: pandoc >= 2.19
(on PATH, or via `pip install pypandoc_binary`) and PyYAML.
"""
import argparse
import datetime as dt
import gzip
import io
import re
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "literature" / "catalog.yaml"
RAW = ROOT / "literature" / "raw"
MD = ROOT / "literature" / "md"
UA = "ccsn-gw-agent-env/1.0 (personal research library; contact: repository owner)"
DELAY = 3.0
MIN_CHARS = 1500
# pandoc drops title/abstract from GFM body output; this template keeps them
TEMPLATE = "$if(title)$# $title$\n\n$endif$$if(abstract)$## Abstract\n\n$abstract$\n\n$endif$$body$\n"
_last = [0.0]


# ----------------------------------------------------------------------------- network
def get(url, retries=3):
    for attempt in range(retries):
        wait = DELAY - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                _last[0] = time.time()
                return r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            _last[0] = time.time()
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(DELAY * 5 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            _last[0] = time.time()
            if attempt < retries - 1:
                time.sleep(DELAY * 3)
                continue
            raise
    raise RuntimeError(f"giving up on {url}")


def metadata(arxiv_id):
    """Title, authors, first-version year, DOI, journal ref and version from the arXiv API."""
    xml, _ = get(f"https://export.arxiv.org/api/query?id_list={arxiv_id}&max_results=1")
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    entry = ET.fromstring(xml).find("a:entry", ns)
    if entry is None or entry.find("a:title", ns) is None:
        raise ValueError(f"arXiv API returned no entry for {arxiv_id}")

    def text(path):
        return re.sub(r"\s+", " ", entry.findtext(path, default="", namespaces=ns) or "").strip()

    return {
        "title": text("a:title"),
        "authors": [a.findtext("a:name", default="", namespaces=ns).strip() for a in entry.findall("a:author", ns)],
        "year_v1": int(text("a:published")[:4] or 0),
        "doi": text("x:doi") or None,
        "journal_ref": text("x:journal_ref") or None,
        "version": text("a:id").rsplit("/", 1)[-1],
    }


# ----------------------------------------------------------------------------- unpacking
def safe_extract(tf, dest):
    if sys.version_info >= (3, 12):
        tf.extractall(dest, filter="data")
        return
    root = dest.resolve()
    for m in tf.getmembers():
        target = (dest / m.name).resolve()
        if (m.isfile() or m.isdir()) and (target == root or root in target.parents):
            tf.extract(m, dest)


def unpack(blob, dest):
    """Store an arXiv e-print. Returns 'tar', 'tex' or 'pdf'.

    /e-print/<id> serves a gzipped tar for multi-file submissions, a gzipped
    single .tex file for one-file submissions, or a PDF when no source exists.
    """
    dest.mkdir(parents=True, exist_ok=True)
    if blob[:4] == b"%PDF":
        (dest / "paper.pdf").write_bytes(blob)
        return "pdf"
    data = gzip.decompress(blob) if blob[:2] == b"\x1f\x8b" else blob
    if data[:4] == b"%PDF":
        (dest / "paper.pdf").write_bytes(data)
        return "pdf"
    try:
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            safe_extract(tf, dest)
        return "tar"
    except tarfile.ReadError:
        (dest / "main.tex").write_bytes(data)
        return "tex"


def main_tex(src):
    """The file with \\documentclass and \\begin{document}; prefer common names, then the largest."""
    cands = []
    for t in src.rglob("*.tex"):
        s = t.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"^[^%\n]*\\documentclass", s, re.M) and "\\begin{document}" in s:
            cands.append(t)
    if not cands:
        return None
    named = [t for t in cands if t.stem.lower() in {"main", "ms", "paper", "manuscript", "article"}]
    return (named or sorted(cands, key=lambda t: t.stat().st_size, reverse=True))[0]


# ----------------------------------------------------------------------------- converters
def good(md_text):
    return len(md_text) >= MIN_CHARS and len(re.findall(r"^#{1,6} ", md_text, re.M)) >= 2


PANDOC_MIN = (2, 19)
PANDOC_HELP = """pandoc >= 2.19 is required to convert LaTeX/HTML to Markdown. Install it with one of:
  pip install pypandoc_binary        # no sudo; bundles a recent pandoc, found automatically
  conda install -c conda-forge pandoc
  https://github.com/jgm/pandoc/releases  (.deb / .msi / .pkg)
Note: `sudo apt install pandoc` on Ubuntu 22.04 gives pandoc 2.9, which is too old."""


def find_pandoc():
    """Path of a usable pandoc: PATH first, then the binary bundled by pypandoc_binary."""
    cands = [shutil.which("pandoc")]
    try:
        import pypandoc
        cands.append(pypandoc.get_pandoc_path())
    except Exception:  # pypandoc not installed, or it has no bundled binary
        pass
    for exe in filter(None, cands):
        try:
            out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=30).stdout
        except OSError:
            continue
        m = re.search(r"pandoc\S*\s+(\d+)\.(\d+)", out)
        if m and (int(m.group(1)), int(m.group(2))) >= PANDOC_MIN:
            return exe
        if m:
            print(f"Found pandoc {m.group(1)}.{m.group(2)} at {exe}, but >= 2.19 is needed.", file=sys.stderr)
    return None


PANDOC = None
GFM = "gfm"   # set in main(): newer pandoc writes math as $`...`$ unless tex_math_gfm is switched off


def gfm_format(exe):
    exts = subprocess.run([exe, "--list-extensions=gfm"], capture_output=True, text=True, timeout=30).stdout
    return "gfm-tex_math_gfm+tex_math_dollars" if "tex_math_gfm" in exts else "gfm"


def pandoc(src, fmt, cwd):
    tpl = Path(cwd) / ".gfm_template.md"
    tpl.write_text(TEMPLATE, encoding="utf-8")
    r = subprocess.run([PANDOC, "-f", fmt, "-t", GFM, "--wrap=none", "-s", f"--template={tpl.name}", src.name],
                       cwd=cwd, capture_output=True, text=True, timeout=300)
    tpl.unlink(missing_ok=True)
    return r.stdout if r.returncode == 0 else ""


def from_latex(src_dir):
    tex = main_tex(src_dir)
    if not tex:
        return ""
    md = pandoc(tex, "latex", tex.parent)        # run inside the source tree so \input resolves
    return md if good(md) else ""


def from_html(html_bytes, src_dir):
    html = html_bytes.decode("utf-8", errors="ignore")
    m = re.search(r"<article\b.*?</article>", html, re.S)  # arXiv/LaTeXML body, without page chrome
    page = src_dir / "paper.html"
    page.write_text(m.group(0) if m else html, encoding="utf-8")
    md = pandoc(page, "html", src_dir)
    return md if good(md) else ""


def from_pdf(pdf, src_dir):
    if shutil.which("marker_single"):
        out = src_dir / "marker"
        subprocess.run(["marker_single", str(pdf), "--output_dir", str(out)], capture_output=True, timeout=3600)
        for f in sorted(out.rglob("*.md")):                 # marker writes <out>/<stem>/<stem>.md
            md = f.read_text(encoding="utf-8", errors="ignore")
            if good(md):
                return md, "pdf-marker"
    if shutil.which("mineru"):
        out = src_dir / "mineru"
        subprocess.run(["mineru", "-p", str(pdf), "-o", str(out)], capture_output=True, timeout=3600)
        for f in sorted(out.rglob("*.md")):
            md = f.read_text(encoding="utf-8", errors="ignore")
            if good(md):
                return md, "pdf-mineru"
    try:
        from pypdf import PdfReader
    except ImportError:
        return "", None
    pages = [p.extract_text() or "" for p in PdfReader(str(pdf)).pages]
    md = "\n\n".join(f"## Page {i}\n\n{t.strip()}" for i, t in enumerate(pages, 1))
    return (md, "pdf-pypdf") if len(md) >= MIN_CHARS else ("", None)


def convert(key, arxiv_id, local=None):
    """Return (markdown, method). Raises RuntimeError if every route fails."""
    src = RAW / key
    if src.exists():
        shutil.rmtree(src)
    src.mkdir(parents=True)
    if local:
        blob = Path(local).expanduser().read_bytes()
        if blob.lstrip()[:1] == b"<":                         # an HTML page saved by hand
            md = from_html(blob, src)
            if md:
                return md, "html"
            raise RuntimeError("local HTML file could not be converted")
        kind = unpack(blob, src)
    else:
        try:
            blob, _ = get(f"https://arxiv.org/e-print/{arxiv_id}")
            kind = unpack(blob, src)
        except urllib.error.HTTPError as e:
            print(f"  e-print unavailable ({e.code})", file=sys.stderr)
            kind = None
    if kind in ("tar", "tex"):
        md = from_latex(src)
        if md:
            return md, "latex"
        print("  pandoc on LaTeX failed or produced too little text; trying HTML", file=sys.stderr)
    if not local:
        try:
            html, _ = get(f"https://arxiv.org/html/{arxiv_id}")
            md = from_html(html, src)
            if md:
                return md, "html"
        except urllib.error.HTTPError as e:
            print(f"  no arXiv HTML ({e.code}); trying PDF", file=sys.stderr)
    pdf = src / "paper.pdf"
    if not pdf.exists() and not local:
        blob, _ = get(f"https://arxiv.org/pdf/{arxiv_id}")
        pdf.write_bytes(blob)
    if pdf.exists():
        md, method = from_pdf(pdf, src)
        if md:
            return md, method
    raise RuntimeError("all conversion routes failed (LaTeX, HTML, PDF)")


def write_markdown(entry, md, method, meta):
    header = {
        "key": entry["key"], "arxiv": str(entry["arxiv"]),
        "title": (meta or {}).get("title") or entry.get("topic"),
        "authors": (meta or {}).get("authors") or entry.get("authors"),
        "arxiv_version": (meta or {}).get("version"),
        "method": method, "fetched": dt.date.today().isoformat(),
    }
    MD.mkdir(parents=True, exist_ok=True)
    out = MD / f"{entry['key']}.md"
    out.write_text("---\n" + yaml.safe_dump(header, allow_unicode=True, sort_keys=False) + "---\n\n" + md,
                   encoding="utf-8")
    return out


# ----------------------------------------------------------------------------- commands
def load_catalog():
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["papers"]


def fetch(entry, local=None):
    print(f"{entry['key']} (arXiv:{entry['arxiv']})")
    meta = None
    if not local:
        try:
            meta = metadata(entry["arxiv"])
        except Exception as e:  # metadata is nice to have, not required
            print(f"  metadata unavailable: {e}", file=sys.stderr)
    md, method = convert(entry["key"], entry["arxiv"], local)
    out = write_markdown(entry, md, method, meta)
    print(f"  OK via {method} -> {out.relative_to(ROOT)} ({len(md):,} chars)")


def surname(name):
    return re.sub(r"[^a-z]", "", name.split()[-1].lower()) if name else ""


def check(entries):
    problems = 0
    for e in entries:
        try:
            m = metadata(e["arxiv"])
        except Exception as ex:
            print(f"{e['key']}: cannot fetch metadata ({ex})")
            problems += 1
            continue
        notes = []
        first = surname(m["authors"][0]) if m["authors"] else ""
        if first and first not in re.sub(r"[^a-z]", "", e.get("authors", "").split(",")[0].lower()):
            notes.append(f"first author on arXiv is {m['authors'][0]!r}")
        if e.get("doi") and m["doi"] and e["doi"].lower() != m["doi"].lower():
            notes.append(f"DOI differs: catalog {e['doi']} vs arXiv {m['doi']}")
        if not e.get("doi") and m["doi"]:
            notes.append(f"arXiv lists DOI {m['doi']}")
        if m["journal_ref"]:
            notes.append(f"arXiv journal_ref: {m['journal_ref']}")
        status = "OK " if not any(n.startswith(("first", "DOI")) for n in notes) else "CHECK"
        problems += status == "CHECK"
        print(f"{status} {e['key']}: {m['title'][:70]}")
        for n in notes:
            print(f"      {n}")
    print(f"\n{len(entries)} entries checked, {problems} need attention")
    return problems


def main():
    ap = argparse.ArgumentParser(description="Fetch arXiv papers into literature/md/.")
    ap.add_argument("keys", nargs="*", help="catalog keys to fetch")
    ap.add_argument("--all", action="store_true", help="all active entries")
    ap.add_argument("--force", action="store_true", help="re-convert even if the Markdown exists")
    ap.add_argument("--local", help="convert this downloaded file (e-print .tar.gz/.gz/.tex, .pdf or .html) for one key")
    ap.add_argument("--meta", metavar="ARXIV_ID", help="print arXiv metadata and exit")
    ap.add_argument("--check", action="store_true", help="compare the catalog with arXiv metadata")
    a = ap.parse_args()

    if a.meta:
        print(yaml.safe_dump(metadata(a.meta), allow_unicode=True, sort_keys=False))
        return
    if not a.check:
        global PANDOC, GFM
        PANDOC = find_pandoc()
        if not PANDOC:
            sys.exit(PANDOC_HELP)
        GFM = gfm_format(PANDOC)
    catalog = load_catalog()
    by_key = {e["key"]: e for e in catalog}
    if a.check:
        sys.exit(1 if check([e for e in catalog if e.get("active", True)]) else 0)
    if a.local and len(a.keys) != 1:
        ap.error("--local needs exactly one key")
    unknown = [k for k in a.keys if k not in by_key]
    if unknown:
        sys.exit(f"Not in literature/catalog.yaml: {', '.join(unknown)} (add a row first)")
    todo = [by_key[k] for k in a.keys] if a.keys else [e for e in catalog if e.get("active", True)] if a.all else []
    if not todo:
        ap.error("give catalog keys or --all")
    if a.all and not a.force:
        todo = [e for e in todo if not (MD / f"{e['key']}.md").exists()]
    failed = []
    for e in todo:
        try:
            fetch(e, a.local)
        except Exception as ex:
            print(f"  FAILED: {ex}", file=sys.stderr)
            failed.append(e["key"])
    print(f"\nDone: {len(todo) - len(failed)} converted, {len(failed)} failed" + (f": {', '.join(failed)}" if failed else ""))
    if failed:
        print("For failures, download the source or PDF in a browser and run:\n"
              "  python3 src/fetch_arxiv.py <key> --local <file>", file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
