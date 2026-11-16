"""HW2 experiment: does T/|W| predict the bounce amplitude on unseen EOS better than omega_0?

    python3 scripts/amp_experiment.py dry | smoke | sweep | full  [--data DIR] [--group eos|family]

--group eos (default) is the original analysis of METHOD.md §7 (6 folds of 3 EOS);
--group family is revision R1 of METHOD.md §9 (5 folds of 2 EOS families).

Steps, models, split, statistics and the decision follow METHOD.md §7-8 exactly. Each step
prints PASSED or exits with code 1, and appends a line to results/hw2/RUNLOG.md; `full`
writes results/hw2/experiment_<revision>.json and .md. Standard library only.
"""
import argparse
import datetime as dt
import json
import math
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import ccsn_contract as cc  # noqa: E402
from hw2lib import EOS_FAMILY, decide, group_kfold, holm, ols, paired_t, rmse  # noqa: E402

OUT = ROOT / "results" / "hw2"
PROGENITORS = (15, 27, 40)
SEEDS = (0, 1, 2, 3, 4)
K = {"eos": 6, "family": 5}
N_GROUPS = {"eos": 18, "family": 10}
GROUP = "eos"                                    # set from --group in main()
REGIME = (0.02, 0.06)
PREDICTORS = ("beta_ic_b", "omega_0")            # test, baseline
ALPHA, DELTA_REL = 0.05, 0.05


def log(step, data, revision, ok, note):
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "RUNLOG.md"
    if not f.exists():
        f.write_text("# HW2 run log\n\n| Time | Step | Data | Revision | Result | Note |\n|---|---|---|---|---|---|\n",
                     encoding="utf-8")
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(f"| {dt.datetime.now():%Y-%m-%d %H:%M:%S} | {step} | {data} | {revision} | "
                 f"{'PASSED' if ok else 'FAILED'} | {note.replace('|', chr(92) + '|')} |\n")


def finish(step, d, rev, ok, note):
    rel = d.relative_to(ROOT) if d.is_relative_to(ROOT) else d
    log(step, rel, rev, ok, note)
    print(f"{step}: {'PASSED' if ok else 'FAILED'} - {note}")
    sys.exit(0 if ok else 1)                         # a step ends here, passed or not


def select(rows, prog):
    return [r for r in rows if r["progenitor_mass"] == prog and REGIME[0] <= r["beta_ic_b"] <= REGIME[1]]


def group_of(r):
    return r["eos"] if GROUP == "eos" else EOS_FAMILY[r["eos"]]


def cv_rmse(rows, x_col, seed):
    """Pooled held-out RMSE of delta_dh over the grouped folds; also the fitted slopes."""
    groups = [group_of(r) for r in rows]
    y_all, yhat_all, slopes = [], [], []
    for train, test in group_kfold(groups, K[GROUP], seed):
        a, b = ols([rows[i][x_col] for i in train], [rows[i]["delta_dh"] for i in train])
        slopes.append(b)
        y_all += [rows[i]["delta_dh"] for i in test]
        yhat_all += [a + b * rows[i][x_col] for i in test]
    return rmse(y_all, yhat_all), slopes


def is_partition(rows, seed):
    groups = [group_of(r) for r in rows]
    folds = group_kfold(groups, K[GROUP], seed)
    tests = sorted(i for _, te in folds for i in te)
    disjoint = all(not ({groups[i] for i in tr} & {groups[i] for i in te}) for tr, te in folds)
    return tests == list(range(len(rows))) and disjoint


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["dry", "smoke", "sweep", "full"])
    ap.add_argument("--data", help="data directory (default: full data if present, else the fragment)")
    ap.add_argument("--group", choices=["eos", "family"], default="eos",
                    help="fold groups: single EOS (METHOD.md §7) or EOS families (revision R1)")
    a = ap.parse_args()
    global GROUP
    GROUP = a.group
    d = cc.data_dir(a.data)
    rev = cc.revision(d) or "unknown"

    # dry -------------------------------------------------------------------------------
    res = cc.check(d)
    broken = [k for k, v in res.items() if v]
    if broken:
        finish(a.step, d, rev, False, f"contract violated: {', '.join(broken)} (run python3 src/ccsn_contract.py)")
    rows = cc.load(d)
    sel = {p: select(rows, p) for p in PROGENITORS}
    counts = {p: (len(v), len({group_of(r) for r in v})) for p, v in sel.items()}
    ok = all(n >= 50 and n_g == N_GROUPS[GROUP] for n, n_g in counts.values())
    note = (f"[groups: {GROUP}] slow runs (n, {GROUP} groups) per progenitor: "
            + ", ".join(f"s{p}: {n}, {e}" for p, (n, e) in counts.items()))
    if a.step == "dry":
        finish("dry", d, rev, ok, "contract OK; " + note)
    if not ok:
        finish(a.step, d, rev, False, "dry condition not met; " + note)

    # smoke -----------------------------------------------------------------------------
    if a.step == "smoke":
        r_beta, slopes = cv_rmse(sel[15], "beta_ic_b", 0)
        r_omega, _ = cv_rmse(sel[15], "omega_0", 0)
        ok = all(math.isfinite(v) and v > 0 for v in (r_beta, r_omega)) and all(s > 0 for s in slopes)
        finish("smoke", d, rev, ok, f"[groups: {GROUP}] s15 seed 0: RMSE beta {r_beta:.3f} cm, omega_0 {r_omega:.3f} cm; "
               f"beta slopes {min(slopes):.4g}..{max(slopes):.4g} cm")

    # sweep -----------------------------------------------------------------------------
    table = {}
    for p in PROGENITORS:
        for s in SEEDS:
            for x in PREDICTORS:
                table[(p, x, s)] = cv_rmse(sel[p], x, s)[0]
    parts = all(is_partition(sel[p], s) for p in PROGENITORS for s in SEEDS)
    ok = all(math.isfinite(v) for v in table.values()) and parts
    if a.step == "sweep":
        finish("sweep", d, rev, ok, f"[groups: {GROUP}] {len(table)} RMSEs finite: {all(math.isfinite(v) for v in table.values())}; "
               f"folds are partitions with disjoint {GROUP} groups: {parts}")
    if not ok:
        finish("full", d, rev, False, "sweep condition not met")

    # full ------------------------------------------------------------------------------
    stats = {}
    for p in PROGENITORS:
        dvals = [table[(p, "beta_ic_b", s)] - table[(p, "omega_0", s)] for s in SEEDS]
        base = [table[(p, "omega_0", s)] for s in SEEDS]
        test = [table[(p, "beta_ic_b", s)] for s in SEEDS]
        t = paired_t(dvals)
        stats[p] = {"n_runs": len(sel[p]), "rmse_beta": test, "rmse_omega": base, "d": dvals, **t,
                    "delta": DELTA_REL * sum(base) / len(base)}
    adj = holm([stats[p]["p"] for p in PROGENITORS])
    for p, pa in zip(PROGENITORS, adj):
        stats[p]["p_holm"] = pa
        stats[p]["decision"] = decide(stats[p]["ci"], stats[p]["mean"], pa, stats[p]["delta"], ALPHA)
    accepted = all(stats[p]["decision"] == "T/|W| better" for p in PROGENITORS)
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"data": str(d.relative_to(ROOT)) if d.is_relative_to(ROOT) else str(d), "revision": rev,
            "group": GROUP, "python": platform.python_version(), "seeds": SEEDS, "k": K[GROUP], "regime": REGIME,
            "alpha": ALPHA,
            "delta_rel": DELTA_REL, "time": dt.datetime.now().isoformat(timespec="seconds")}
    tag = rev if GROUP == "eos" else f"{rev}_family"
    (OUT / f"experiment_{tag}.json").write_text(json.dumps(
        {"meta": meta, "claim_H_accepted": accepted, "per_progenitor": {str(p): v for p, v in stats.items()}},
        indent=1, default=list) + "\n", encoding="utf-8")
    how = ("6 folds of 3 EOS (METHOD.md §7)" if GROUP == "eos"
           else "5 folds of 2 EOS families (METHOD.md §9, revision R1)")
    md = [f"# Claim H on the `{rev}` data, folds grouped by {GROUP}", "",
          f"Data `{meta['data']}` (revision `{rev}`), Python {meta['python']}, seeds {list(SEEDS)}, "
          f"{how}, regime {REGIME[0]} <= T/|W| <= {REGIME[1]}. Generated by "
          f"`python3 scripts/amp_experiment.py full --group {GROUP}`.", "",
          "Held-out RMSE of D·Δh [cm] per seed (T/|W| model / Ω₀ baseline):", "",
          "| Progenitor | Runs | " + " | ".join(f"seed {s}" for s in SEEDS) + " |",
          "|---|---|" + "---|" * len(SEEDS)]
    for p in PROGENITORS:
        st = stats[p]
        md.append(f"| s{p} | {st['n_runs']} | " + " | ".join(
            f"{b:.2f} / {o:.2f}" for b, o in zip(st["rmse_beta"], st["rmse_omega"])) + " |")
    md += ["", "| Variant | Progenitor | Mean RMSE [cm] | SD over seeds [cm] | 95 % interval [cm] |",
           "|---|---|---|---|---|"]
    for p in PROGENITORS:
        st = stats[p]
        for name, vals in (("Ω₀ baseline", st["rmse_omega"]), ("T/|W|", st["rmse_beta"])):
            t = paired_t(vals)
            md.append(f"| {name} | s{p} | {t['mean']:.2f} | {t['sd']:.3f} | [{t['ci'][0]:.2f}; {t['ci'][1]:.2f}] |")
    md += ["", "Paired difference d = RMSE(T/|W|) − RMSE(Ω₀), Holm over the three progenitors:", "",
           "| Progenitor | Mean d [cm] | SD [cm] | 95 % interval [cm] | p | p (Holm) | δ = 5 % of baseline [cm] | Decision |",
           "|---|---|---|---|---|---|---|---|"]
    for p in PROGENITORS:
        st = stats[p]
        md.append(f"| s{p} | {st['mean']:.2f} | {st['sd']:.3f} | [{st['ci'][0]:.2f}; {st['ci'][1]:.2f}] | "
                  f"{st['p']:.2e} | {st['p_holm']:.2e} | {st['delta']:.2f} | {st['decision']} |")
    md += ["", f"**Claim H {'accepted' if accepted else 'not accepted'}** by the rule of "
           f"{'METHOD.md §7' if GROUP == 'eos' else 'METHOD.md §9, revision R1'}."]
    md = [ln.replace("T/|W|", "T/\\|W\\|") if ln.startswith("|") else ln for ln in md]   # pipes in table cells
    (OUT / f"experiment_{tag}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    finish("full", d, rev, True, f"[groups: {GROUP}] claim H {'accepted' if accepted else 'not accepted'}; "
           + "; ".join(f"s{p}: {stats[p]['decision']}" for p in PROGENITORS))


if __name__ == "__main__":
    main()
