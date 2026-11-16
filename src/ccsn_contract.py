"""Data contract for the CCSN bounce dataset (METHOD.md §4, rules C1-C14).

    python3 src/ccsn_contract.py [data_dir]      # prints one line per rule, exit 1 on a violation

data_dir holds parameters.csv, data_dictionary.csv and timeseries/strain.csv.gz.
Default: $CCSN_DATA, else data/data (full, local only), else checks/fixtures/data.
Standard library only.
"""
import csv
import gzip
import hashlib
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FULL = ROOT / "data" / "data"
FRAGMENT = ROOT / "checks" / "fixtures" / "data"
REVISIONS = ROOT / "checks" / "data_revision.json"

COLUMNS = ["run_id", "progenitor_mass", "eos", "A", "omega_0", "rotation_scale", "A_eff", "omega_0_eff",
           "t_bounce_signal_end", "dh_bounce_max", "dh_bounce_min", "delta_dh", "dh_prebounce_max", "f_peak",
           "omega_max", "beta_ic_b", "beta_b", "mgrav_ic_b", "mrest_ic_b", "mgrav_ic_pb", "mgrav_b", "j_ic_b",
           "j_b", "rho_c_b", "rho_c_pb", "T_c_b", "s_c_b", "ye_c_b", "alpha_c_b", "r_pns_eq_b", "r_pns_pole_b"]
STRINGS = {"run_id", "eos"}
UNITS = {"run_id": "", "progenitor_mass": "Msun", "eos": "", "A": "km", "omega_0": "rad/s", "rotation_scale": "",
         "A_eff": "km", "omega_0_eff": "rad/s", "t_bounce_signal_end": "s", "dh_bounce_max": "cm",
         "dh_bounce_min": "cm", "delta_dh": "cm", "dh_prebounce_max": "cm", "f_peak": "Hz", "omega_max": "rad/s",
         "beta_ic_b": "", "beta_b": "", "mgrav_ic_b": "Msun", "mrest_ic_b": "Msun", "mgrav_ic_pb": "Msun",
         "mgrav_b": "Msun", "j_ic_b": "g cm^2/s", "j_b": "g cm^2/s", "rho_c_b": "g/cm^3", "rho_c_pb": "g/cm^3",
         "T_c_b": "MeV", "s_c_b": "kB/baryon", "ye_c_b": "", "alpha_c_b": "", "r_pns_eq_b": "km",
         "r_pns_pole_b": "km"}
EOS = {"BHBl", "BHBlp", "GShenFSU1.7", "GShenFSU2.1", "GShenNL3", "HSDD2", "HSFSG", "HSIUF", "HSNL3", "HSTM1",
       "HSTMA", "HShen", "HShenH", "LS180", "LS220", "LS375", "SFHo", "SFHx"}
SCALE = {15: 1.11049, 27: 1.3416, 40: 1.7674}
GRID = {300: 15.0, 329: 12.5, 365: 11.5, 410: 10.5, 467: 9.5, 538: 8.5, 634: 7.5, 761: 7.0, 951: 6.0,
        1268: 5.0, 10000: 3.5}                       # A [km] -> largest omega_0 [rad/s]; smallest is 3.0
DH_MAX = 2000.0                                      # |D h| bound [cm]
RANGES = {"t_bounce_signal_end": (0, 0.01, False), "f_peak": (500, 1500, True), "omega_max": (0, 1e4, False),
          "rho_c_b": (5e13, 3e15, True), "rho_c_pb": (5e13, 3e15, True), "T_c_b": (0, 50, False),
          "s_c_b": (0, 5, False), "mgrav_ic_b": (0, 5, False), "mrest_ic_b": (0, 5, False),
          "mgrav_ic_pb": (0, 5, False), "mgrav_b": (0, 5, False), "r_pns_eq_b": (0, 200, False),
          "r_pns_pole_b": (0, 200, False), "j_ic_b": (0, math.inf, False), "j_b": (0, math.inf, False)}
REL = 1e-3
DT = 1 / 16384
OVERSHOOT = 1.01                                     # C14 tolerance (METHOD.md §3)


def data_dir(arg=None):
    if arg:
        return Path(arg)
    if os.environ.get("CCSN_DATA"):
        return Path(os.environ["CCSN_DATA"])
    return FULL if (FULL / "parameters.csv").exists() else FRAGMENT


def md5(path):
    return hashlib.md5(Path(path).read_bytes()).hexdigest()


def revision(d):
    """Name of the known revision ('full' or 'fragment') whose MD5 sums match, else None."""
    known = json.loads(REVISIONS.read_text(encoding="utf-8"))
    sums = {f: md5(Path(d) / f) for f in ("parameters.csv", "timeseries/strain.csv.gz", "data_dictionary.csv")
            if (Path(d) / f).exists()}
    for name, rev in known.items():
        if rev["md5"] == sums:
            return name
    return None


def read_raw(d):
    with open(Path(d) / "parameters.csv", newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        return next(rd), list(rd)


def load(d):
    """Typed rows of parameters.csv (floats for numeric columns)."""
    header, raw = read_raw(d)
    return [{k: (v if k in STRINGS else float(v)) for k, v in zip(header, r)} for r in raw]


def read_strain(d):
    with gzip.open(Path(d) / "timeseries" / "strain.csv.gz", "rt", newline="") as f:
        rd = csv.reader(f)
        return next(rd), list(rd)


def close(a, b, rel=REL):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-30)


def _first(bad, n=3):
    return "; ".join(map(str, bad[:n])) + (f" (+{len(bad) - n} more)" if len(bad) > n else "")


def check(d):
    """Run C1-C14; returns {rule: list of violation descriptions} (empty list = rule holds)."""
    d = Path(d)
    out = {}
    header, raw = read_raw(d)
    out["C1 columns"] = [] if header == COLUMNS else [f"header {header}"]
    if out["C1 columns"]:
        return out                                   # nothing else is meaningful
    bad = []
    for i, r in enumerate(raw):
        if len(r) != len(COLUMNS):
            bad.append(f"row {i + 2}: {len(r)} cells")
            continue
        for k, v in zip(COLUMNS, r):
            if v == "":
                bad.append(f"row {i + 2} {k}: empty")
            elif k not in STRINGS:
                try:
                    if not math.isfinite(float(v)):
                        bad.append(f"row {i + 2} {k}: {v}")
                except ValueError:
                    bad.append(f"row {i + 2} {k}: '{v}' is not a number")
    out["C2 types"] = bad
    if bad:
        return out
    rows = load(d)

    with open(d / "data_dictionary.csv", newline="", encoding="utf-8") as f:
        units = {r["column"]: r["unit"] for r in csv.DictReader(f) if r["file"] == "parameters.csv"}
    out["C3 units"] = [f"{k}: dictionary '{units.get(k)}' != contract '{u}'" for k, u in UNITS.items()
                       if units.get(k, None) != u]

    ids = [r["run_id"] for r in rows]
    bad = [f"duplicate {x}" for x in sorted({x for x in ids if ids.count(x) > 1})] if len(set(ids)) < len(ids) else []
    for r in rows:
        want = f"s{int(r['progenitor_mass'])}_A{int(r['A'])}_w{r['omega_0']:.2f}_{r['eos']}"
        if r["run_id"] != want:
            bad.append(f"{r['run_id']} != {want}")
    out["C4 key"] = bad

    out["C5 categories"] = [f"{r['run_id']}: progenitor {r['progenitor_mass']} / eos {r['eos']}" for r in rows
                            if r["progenitor_mass"] not in SCALE or r["eos"] not in EOS]

    bad, cells = [], {}
    for r in rows:
        a, w = r["A"], r["omega_0"]
        if a not in GRID or not (3.0 <= w <= GRID[a]) or not close(w * 2, round(w * 2), 1e-9):
            bad.append(f"{r['run_id']}: A={a}, omega_0={w} not on the grid")
        cells[(r["progenitor_mass"], r["eos"])] = cells.get((r["progenitor_mass"], r["eos"]), 0) + 1
    bad += [f"{c}: {n} runs > 138" for c, n in cells.items() if n > 138]
    out["C6 grid"] = bad

    out["C7 rotation_scale"] = [f"{r['run_id']}: s={r['rotation_scale']}" for r in rows
                                if r["progenitor_mass"] in SCALE and not close(r["rotation_scale"], SCALE[r["progenitor_mass"]], 1e-6)]

    bad = []
    for r in rows:
        s = r["rotation_scale"]
        if not close(r["A_eff"], s * r["A"]):
            bad.append(f"{r['run_id']}: A_eff {r['A_eff']} != s*A {s * r['A']:.6g}")
        if not close(r["omega_0_eff"], r["omega_0"] / s ** 2):
            bad.append(f"{r['run_id']}: omega_0_eff {r['omega_0_eff']} != omega_0/s^2 {r['omega_0'] / s ** 2:.6g}")
        if not close(r["delta_dh"], r["dh_bounce_max"] - r["dh_bounce_min"]):
            bad.append(f"{r['run_id']}: delta_dh {r['delta_dh']} != max-min {r['dh_bounce_max'] - r['dh_bounce_min']:.6g}")
    out["C8 identities"] = bad

    bad = []
    for r in rows:
        if not (r["dh_bounce_max"] > 0 > r["dh_bounce_min"]):
            bad.append(f"{r['run_id']}: dh_bounce_max {r['dh_bounce_max']}, dh_bounce_min {r['dh_bounce_min']}")
        for k in ("dh_bounce_max", "dh_bounce_min", "delta_dh", "dh_prebounce_max"):
            if abs(r[k]) > DH_MAX:
                bad.append(f"{r['run_id']}: |{k}| = {abs(r[k])} > {DH_MAX}")
        for k, (lo, hi, closed) in RANGES.items():
            v = r[k]
            ok = (lo <= v <= hi) if closed else (lo < v <= hi)
            if not ok:
                bad.append(f"{r['run_id']}: {k} = {v} outside {'[' if closed else '('}{lo}, {hi}]")
    out["C9 ranges"] = bad

    known = json.loads(REVISIONS.read_text(encoding="utf-8"))
    rev = revision(d)
    if rev is None:
        out["C10 revision"] = [f"MD5 sums match no known revision in {REVISIONS.relative_to(ROOT)}"]
    else:
        out["C10 revision"] = [] if len(rows) == known[rev]["rows"] else [f"{len(rows)} rows, manifest {known[rev]['rows']}"]

    sh, srows = read_strain(d)
    sids = [r[0] for r in srows]
    out["C11 strain alignment"] = [] if sids == ids else [
        f"{len(sids)} strain rows vs {len(ids)}; first mismatch at row "
        f"{next((i for i, (a, b) in enumerate(zip(sids, ids)) if a != b), min(len(sids), len(ids))) + 2}"]

    bad = []
    try:
        t = [float(x) for x in sh[1:]]
    except ValueError:
        t = []
        bad.append("time headers are not numbers")
    if t:
        if len(t) != 131:
            bad.append(f"{len(t)} time columns, contract 131")
        steps = [b - a for a, b in zip(t, t[1:])]
        off = [i for i, s_ in enumerate(steps) if not close(s_, DT)]
        if off:
            bad.append(f"non-uniform step at columns {off[:5]}")
        if not close(t[0], -0.00195312, 1e-5):
            bad.append(f"first sample {t[0]} s != -0.00195312 s")
        if not any(abs(x) < 1e-12 for x in t):
            bad.append("t = 0 is not a sample")
    sh_ok = sh[0] == "run_id"
    if not sh_ok:
        bad.append(f"first strain column is '{sh[0]}'")
    out["C12 time grid"] = bad

    bad, under = [], []
    by_id = {r["run_id"]: r for r in rows}
    for row in srows:
        try:
            v = [float(x) for x in row[1:]]
        except ValueError:
            bad.append(f"{row[0]}: empty or non-numeric cell")
            continue
        if len(v) != len(sh) - 1:
            bad.append(f"{row[0]}: {len(v)} samples")
        if any(not math.isfinite(x) or abs(x) > DH_MAX for x in v):
            bad.append(f"{row[0]}: value outside +-{DH_MAX} cm")
        r = by_id.get(row[0])
        if r and v and min(v) < OVERSHOOT * r["dh_bounce_min"]:
            under.append(f"{row[0]}: min strain {min(v)} < {OVERSHOOT} * dh_bounce_min {r['dh_bounce_min']}")
    out["C13 strain cells"] = bad
    out["C14 strain vs dh_bounce_min"] = under
    return out


def main():
    d = data_dir(sys.argv[1] if len(sys.argv) > 1 else None)
    res = check(d)
    print(f"data: {d} (revision: {revision(d) or 'unknown'})")
    for rule, bad in res.items():
        print(f"{'PASS' if not bad else 'FAIL'}  {rule}" + (f": {_first(bad)}" if bad else ""))
    n_bad = sum(bool(b) for b in res.values())
    print("contract OK" if not n_bad else f"contract VIOLATED ({n_bad} rules)")
    sys.exit(1 if n_bad else 0)


if __name__ == "__main__":
    main()
