"""Query the simulation dataset in data/ without printing large files.

The agent must use this tool instead of cat/zcat/head/pandas on data/: one row of the
strain file alone is 131 numbers, the parameter table has 7,438 rows. Every command
prints a short result (at most --limit rows, default 20, hard cap 50).

Usage
  python3 src/data.py info                                   # files, sizes, time grid
  python3 src/data.py columns                                # every column with unit and meaning
  python3 src/data.py params --where "eos==SFHo" --where "progenitor_mass==27" --cols A,omega_0,beta_ic_b,f_peak
  python3 src/data.py params --where "eos in SFHo,LS220" --where "beta_ic_b>=0.05" --sort f_peak --limit 10
  python3 src/data.py stats f_peak --by eos                  # count, mean, std, min, median, max
  python3 src/data.py corr beta_ic_b delta_dh --where "progenitor_mass==15"
  python3 src/data.py strain s27_A634_w6.00_SFHo             # summary of one waveform
  python3 src/data.py strain s27_A634_w6.00_SFHo --every 10  # also print every 10th sample
  python3 src/data.py params --where "eos==SFHo" --out results/sfho.csv   # full selection to a file

Filters: col==v, col!=v, col>=v, col<=v, col>v, col<v, "col in a,b,c". Repeat --where to combine (AND).
Times in the strain file are in seconds, t = 0 at core bounce, -1.95 ms to +5.98 ms.
Standard library only (matplotlib is used by `plot` if it is installed).
"""
import argparse
import csv
import gzip
import math
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "data"
PARAMS = DATA / "parameters.csv"
STRAIN = DATA / "timeseries" / "strain.csv.gz"
DICT = DATA / "data_dictionary.csv"
HARD_CAP = 50
OPS = ("==", "!=", ">=", "<=", ">", "<")


def die(msg):
    sys.exit(f"data.py: {msg}")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


def fmt(v):
    if isinstance(v, float):
        if v == 0 or math.isnan(v):
            return str(v)
        a = abs(v)
        return f"{v:.4g}" if 1e-3 <= a < 1e5 else f"{v:.4e}"
    return str(v)


def load_params():
    if not PARAMS.exists():
        die(f"{PARAMS.relative_to(ROOT)} not found (the dataset is local only, see data/README.md)")
    with open(PARAMS, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        rows = [{k: num(v) for k, v in r.items()} for r in rd]
        return rd.fieldnames, rows


def dictionary():
    if not DICT.exists():
        return {}
    with open(DICT, newline="", encoding="utf-8") as f:
        return {(r["file"], r["column"]): (r["unit"], r["description"]) for r in csv.DictReader(f)}


def parse_where(expr, cols):
    m = re.fullmatch(r"\s*(\w+)\s+in\s+(.+)", expr)
    if m:
        col, vals = m.group(1), {num(v.strip()) for v in m.group(2).split(",")}
        op = "in"
    else:
        m = re.fullmatch(r"\s*(\w+)\s*(==|!=|>=|<=|>|<)\s*(.+?)\s*", expr)
        if not m:
            die(f"cannot parse filter '{expr}' (use e.g. \"eos==SFHo\", \"beta_ic_b>=0.05\", \"eos in SFHo,LS220\")")
        col, op, vals = m.group(1), m.group(2), num(m.group(3).strip("'\""))
    if col not in cols:
        die(f"unknown column '{col}'. See: python3 src/data.py columns")

    def ok(row):
        v = row[col]
        if op == "in":
            return v in vals
        if op in ("==", "!="):
            return (v == vals) == (op == "==")
        if isinstance(v, str) or isinstance(vals, str):
            die(f"'{op}' needs numbers: {expr}")
        return {">=": v >= vals, "<=": v <= vals, ">": v > vals, "<": v < vals}[op]
    return ok


def select(rows, cols, wheres):
    tests = [parse_where(w, cols) for w in wheres]
    return [r for r in rows if all(t(r) for t in tests)]


def check_cols(names, cols):
    bad = [c for c in names if c not in cols]
    if bad:
        die(f"unknown column(s): {', '.join(bad)}. See: python3 src/data.py columns")


def print_table(header, rows, limit, total):
    cells = [[fmt(r[c]) for c in header] for r in rows[:limit]]
    width = [max(len(h), *(len(c[i]) for c in cells)) if cells else len(h) for i, h in enumerate(header)]
    print("  ".join(h.ljust(w) for h, w in zip(header, width)))
    for c in cells:
        print("  ".join(v.ljust(w) for v, w in zip(c, width)))
    print(f"({total} rows matched; showing {min(limit, total)})")


def limit_of(a):
    return max(1, min(a.limit, HARD_CAP))


def cmd_info(a):
    cols, rows = load_params()
    with gzip.open(STRAIN, "rt", newline="") as f:
        times = next(csv.reader(f))[1:]
    eos = sorted({r["eos"] for r in rows})
    prog = sorted({r["progenitor_mass"] for r in rows})
    print(f"data/data/parameters.csv            {len(rows)} rows x {len(cols)} columns (key: run_id)")
    print(f"data/data/timeseries/strain.csv.gz  D*h+ [cm], {len(times)} samples at 16384 Hz, "
          f"t = {float(times[0]) * 1e3:.2f} .. {float(times[-1]) * 1e3:.2f} ms (t = 0 at bounce)")
    print("data/data/data_dictionary.csv       unit and description of every column")
    print("Row i is the same simulation in every file; run_id = s<progenitor>_A<A km>_w<omega_0>_<EOS>.")
    print(f"progenitor_mass: {', '.join(fmt(p) for p in prog)} Msun;  {len(eos)} EOS: {', '.join(eos)}")
    print("Note: derived parameters were computed from the full -50..+12.7 ms data, not from this trimmed strain.")
    print("Columns: " + ", ".join(cols))


def cmd_columns(a):
    cols, _ = load_params()
    d = dictionary()
    for c in cols:
        unit, desc = d.get(("parameters.csv", c), ("", ""))
        desc = desc if len(desc) <= 110 else desc[:107] + "..."
        print(f"{c:22s} {unit or '-':12s} {desc}")
    unit, desc = d.get(("timeseries/strain.csv.gz", "(all time columns)"), ("cm", "D*h+"))
    print(f"{'strain (timeseries)':22s} {unit:12s} {desc[:110]}")


def cmd_params(a):
    cols, rows = load_params()
    sel = select(rows, cols, a.where)
    show = ["run_id"] + [c for c in (a.cols.split(",") if a.cols else []) if c != "run_id"] if a.cols else cols[:8]
    check_cols(show, cols)
    if a.sort:
        check_cols([a.sort], cols)
        sel.sort(key=lambda r: (isinstance(r[a.sort], str), r[a.sort]), reverse=a.desc)
    if a.out:
        out = ROOT / a.out
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(show)
            w.writerows([[r[c] for c in show] for r in sel])
        print(f"wrote {len(sel)} rows x {len(show)} columns -> {a.out}")
        return
    print_table(show, sel, limit_of(a), len(sel))
    if not a.cols:
        print("(first 8 columns; choose others with --cols a,b,c)")


def describe(vals):
    vals = [v for v in vals if isinstance(v, float) and not math.isnan(v)]
    if not vals:
        return None
    return {"count": len(vals), "mean": statistics.fmean(vals), "std": statistics.pstdev(vals),
            "min": min(vals), "median": statistics.median(vals), "max": max(vals)}


def cmd_stats(a):
    cols, rows = load_params()
    check_cols([a.column] + ([a.by] if a.by else []), cols)
    sel = select(rows, cols, a.where)
    groups = {}
    for r in sel:
        groups.setdefault(r[a.by] if a.by else "all", []).append(r[a.column])
    out = []
    for g in sorted(groups, key=lambda x: (isinstance(x, str), x)):
        d = describe(groups[g])
        if d:
            out.append({"group": g, **d})
    if not out:
        die(f"no numeric values of {a.column} in the selection")
    print(f"{a.column}" + (f" by {a.by}" if a.by else "") + (f"  where {' and '.join(a.where)}" if a.where else ""))
    print_table(["group", "count", "mean", "std", "min", "median", "max"], out, limit_of(a), len(out))


def cmd_corr(a):
    cols, rows = load_params()
    check_cols([a.x, a.y], cols)
    pairs = [(r[a.x], r[a.y]) for r in select(rows, cols, a.where)
             if isinstance(r[a.x], float) and isinstance(r[a.y], float)]
    if len(pairs) < 3:
        die("fewer than 3 numeric pairs in the selection")
    xs, ys = zip(*pairs)
    r = statistics.correlation(xs, ys)
    slope, icept = statistics.linear_regression(xs, ys)
    print(f"n = {len(pairs)}  Pearson r({a.x}, {a.y}) = {r:.4f}  linear fit: {a.y} = {slope:.4g} * {a.x} + {icept:.4g}"
          + (f"  where {' and '.join(a.where)}" if a.where else ""))


def strain_row(run_id):
    with gzip.open(STRAIN, "rt", newline="") as f:
        rd = csv.reader(f)
        times = [float(t) for t in next(rd)[1:]]
        for row in rd:
            if row[0] == run_id:
                return times, [float(v) for v in row[1:]]
    die(f"run_id '{run_id}' not found. Find ids with: python3 src/data.py params --where ...")


def cmd_strain(a):
    times, h = strain_row(a.run_id)
    i_min, i_max = min(range(len(h)), key=h.__getitem__), max(range(len(h)), key=h.__getitem__)
    print(f"{a.run_id}: D*h+ [cm], {len(h)} samples, t = {times[0] * 1e3:.2f} .. {times[-1] * 1e3:.2f} ms")
    print(f"min {fmt(h[i_min])} cm at t = {times[i_min] * 1e3:.3f} ms;  max {fmt(h[i_max])} cm at t = {times[i_max] * 1e3:.3f} ms;"
          f"  max - min = {fmt(h[i_max] - h[i_min])} cm")
    if a.out:
        out = ROOT / a.out
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["t_s", "dh_plus_cm"])
            w.writerows(zip(times, h))
        print(f"wrote {len(h)} samples -> {a.out}")
    if a.every:
        step = max(a.every, math.ceil(len(h) / HARD_CAP))
        print("t_ms      dh_plus_cm")
        for i in range(0, len(h), step):
            print(f"{times[i] * 1e3:8.3f}  {fmt(h[i])}")
        if step != a.every:
            print(f"(step raised to {step} to stay within {HARD_CAP} lines)")


def cmd_plot(a):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        die("matplotlib is not installed; save the data with --out and plot elsewhere")
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    for rid in a.run_ids:
        t, h = strain_row(rid)
        ax.plot([x * 1e3 for x in t], h, label=rid, lw=1)
    ax.set_xlabel("t - t_bounce [ms]")
    ax.set_ylabel("D h+ [cm]")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"saved {out.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser(description="Query data/ (short outputs only).",
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    sub.add_parser("columns")

    def common(p):
        p.add_argument("--where", action="append", default=[], help='filter, e.g. "eos==SFHo"; repeatable')
        p.add_argument("--limit", type=int, default=20, help=f"rows to print (max {HARD_CAP})")

    p = sub.add_parser("params")
    common(p)
    p.add_argument("--cols", help="comma-separated columns (run_id is always shown)")
    p.add_argument("--sort", help="sort by this column")
    p.add_argument("--desc", action="store_true", help="sort descending")
    p.add_argument("--out", help="write the full selection to this CSV (path relative to the repo, e.g. results/x.csv)")
    p = sub.add_parser("stats")
    common(p)
    p.add_argument("column")
    p.add_argument("--by", help="group by this column, e.g. eos or progenitor_mass")
    p = sub.add_parser("corr")
    common(p)
    p.add_argument("x")
    p.add_argument("y")
    p = sub.add_parser("strain")
    p.add_argument("run_id")
    p.add_argument("--every", type=int, default=0, help="also print every n-th sample")
    p.add_argument("--out", help="save this waveform as CSV (e.g. results/strain_x.csv)")
    p = sub.add_parser("plot")
    p.add_argument("run_ids", nargs="+")
    p.add_argument("--out", required=True, help="PNG path, e.g. results/figs/strain.png")
    a = ap.parse_args()
    if getattr(a, "out", None) and not (ROOT / a.out).resolve().is_relative_to((ROOT / "results").resolve()):
        die("--out must be inside results/")
    globals()[f"cmd_{a.cmd}"](a)


if __name__ == "__main__":
    main()
