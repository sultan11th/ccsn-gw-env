"""Build the committed data fragment from the full local dataset (METHOD.md §3).

    python3 scripts/make_fragment.py          # data/data -> checks/fixtures/data + checks/data_revision.json

Keeps all runs with A in {634, 1268} km, every column and the full time grid; the gzip
header has mtime 0, so the output is byte-identical on every run.
"""
import csv
import gzip
import hashlib
import io
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "data"
DST = ROOT / "checks" / "fixtures" / "data"
REV = ROOT / "checks" / "data_revision.json"
KEEP_A = {"634", "1268"}
FILES = ("parameters.csv", "timeseries/strain.csv.gz", "data_dictionary.csv")


def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def main():
    if not (SRC / "parameters.csv").exists():
        sys.exit(f"{SRC} not found: the full dataset is local only")
    (DST / "timeseries").mkdir(parents=True, exist_ok=True)
    with open(SRC / "parameters.csv", newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        header = next(rd)
        rows = [r for r in rd if r[header.index("A")] in KEEP_A]
    keep = {r[0] for r in rows}
    with open(DST / "parameters.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    with gzip.open(SRC / "timeseries" / "strain.csv.gz", "rt", newline="") as f:
        rd = csv.reader(f)
        sh = next(rd)
        srows = [r for r in rd if r[0] in keep]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(sh)
    w.writerows(srows)
    with open(DST / "timeseries" / "strain.csv.gz", "wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as gz:
            gz.write(buf.getvalue().encode("utf-8"))
    shutil.copyfile(SRC / "data_dictionary.csv", DST / "data_dictionary.csv")

    n_full = sum(1 for _ in open(SRC / "parameters.csv", encoding="utf-8")) - 1
    rev = {"full": {"rows": n_full, "md5": {f: md5(SRC / f) for f in FILES}},
           "fragment": {"rows": len(rows), "md5": {f: md5(DST / f) for f in FILES},
                        "made_by": "scripts/make_fragment.py (A in {634, 1268} km)"}}
    REV.write_text(json.dumps(rev, indent=1) + "\n", encoding="utf-8")
    print(f"fragment: {len(rows)} runs -> {DST.relative_to(ROOT)}; revisions -> {REV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
