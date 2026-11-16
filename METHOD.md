# METHOD — Verifier for the CCSN bounce dataset and the amplitude claim (HW2)

Written on 2026-11-17, **before the first run** of the verifier or the experiment.
Revisions after the first run are appended in §9 with date and reason; nothing above §9
is edited after the first run.

## 1. Idea

The project answers questions about gravitational waves (GWs) from rotating core collapse
from a library of papers **and** from my dataset of 7,438 simulations (`data/`, see
`data/README.md`). Every number the agent or I take from the dataset passes through
`src/data.py` and through derived analyses. If the data are corrupted (misaligned rows
between files, a broken identity, units mixed up, a truncated grid) or if an analysis leaks
information between training and test sets, every conclusion built on it is wrong while
looking plausible. The verifier checks this piece:

1. the dataset satisfies a written **contract** (schema, types, units, ranges, key,
   identities, grid, alignment of files, data revision);
2. the data satisfy **physical properties** that any correct simulation output must have;
3. the **EOS-grouped split** used for out-of-distribution evaluation is a partition with no
   EOS shared by training and test data (the "template leakage" that inflates EOS-inference
   results, `literature/md/mitra2026_generalization.md:L17-L17`);
4. one claim from the library, checked on the data with repeats and an acceptance rule:

> **Claim H.** In the slow-rotation regime (0.02 ≤ T/|W| ≤ 0.06), the bounce-signal
> amplitude D·Δh is predicted on *unseen EOS* better by a linear function of the inner-core
> T/|W| at bounce than by a linear function of the grid label Ω₀ (baseline).

Richers et al. report that in the linear regime the bounce amplitude depends approximately
linearly on T/|W| (`literature/md/richers2017.md:L237-L247`); Ω₀ is the natural naive
baseline because it is the input of the simulation and ignores differential rotation (A),
the progenitor structure and the EOS.

## 2. Setup

| | |
|---|---|
| Varied | predictor x ∈ {`beta_ic_b` (test), `omega_0` (baseline)}; progenitor ∈ {15, 27, 40} M☉; seed ∈ {0, 1, 2, 3, 4} |
| Fixed | regime 0.02 ≤ `beta_ic_b` ≤ 0.06; model Δh = a + b·x by ordinary least squares on the training folds only; 6 folds of 3 EOS each |
| Measured | pooled held-out RMSE of `delta_dh` [cm] per (progenitor, predictor, seed); paired difference d = RMSE(beta) − RMSE(omega_0) |

## 3. Data and revision

- **Full data** (local, not in git; CC BY 4.0, my own simulations): `data/data/parameters.csv`
  (7,438 rows × 31 columns), `data/data/timeseries/strain.csv.gz` (D·h₊ in cm, 131 samples,
  −1.95 … +5.98 ms), `data/data/data_dictionary.csv`. Revision (MD5, `data/MD5SUMS`):
  - `parameters.csv` `ce3c743c5db3269cb8147c651d605671`
  - `timeseries/strain.csv.gz` `295790fc5f65dceeecb809df6dd2e4b1`
  - `data_dictionary.csv` `89db9011f677aa5b7e37c3f46687d104`
- **Committed fragment** (for a reviewer's clean clone): `checks/fixtures/data/`, produced
  deterministically by `scripts/make_fragment.py` from the full data: all runs with
  A ∈ {634, 1268} km (3 progenitors × 18 EOS × 15 rotation profiles = 810 runs), same
  columns and time grid. Its MD5 sums and row count are stored in
  `checks/fixtures/MANIFEST.json` and checked by the contract.
- The verifier uses the full data when `data/data/` exists, otherwise the fragment;
  `CCSN_DATA=<dir>` selects a directory explicitly. Results state which data were used.
- Before this method was written I explored the full data once (2026-11-17) to see whether
  the identities hold and how many runs fall into the slow regime: all identities held; in 8
  rapid rotators (T/|W| ≈ 0.16–0.18) the resampled strain dips 0.1–0.6 % below
  `dh_bounce_min` (measured at the native rate) at bounce. This motivates the 1 % tolerance
  of rule C14. No model was fitted.

## 4. Contract (checked by `checks/test_contract.py`)

| # | Rule |
|---|---|
| C1 | `parameters.csv` has exactly these 31 columns in this order: run_id, progenitor_mass, eos, A, omega_0, rotation_scale, A_eff, omega_0_eff, t_bounce_signal_end, dh_bounce_max, dh_bounce_min, delta_dh, dh_prebounce_max, f_peak, omega_max, beta_ic_b, beta_b, mgrav_ic_b, mrest_ic_b, mgrav_ic_pb, mgrav_b, j_ic_b, j_b, rho_c_b, rho_c_pb, T_c_b, s_c_b, ye_c_b, alpha_c_b, r_pns_eq_b, r_pns_pole_b |
| C2 | Types: `run_id`, `eos` strings; every other cell a finite float; no empty cells |
| C3 | Units in `data_dictionary.csv` equal the contract units (Msun, km, rad/s, s, cm, Hz, g cm^2/s, g/cm^3, MeV, kB/baryon, dimensionless) for every column |
| C4 | Key: `run_id` unique and equal to `s<progenitor>_A<A>_w<omega_0 with 2 decimals>_<eos>` |
| C5 | Categories: progenitor ∈ {15, 27, 40}; eos ∈ the 18 EOS of `data/README.md` |
| C6 | Grid: A ∈ {300, 329, 365, 410, 467, 538, 634, 761, 951, 1268, 10000} km; Ω₀ a multiple of 0.5 rad/s within the per-A range of the grid table; at most 138 runs per (progenitor, EOS) |
| C7 | `rotation_scale` = 1.11049 (s15), 1.3416 (s27), 1.7674 (s40) |
| C8 | Identities (relative tolerance 1e-3): `A_eff` = s·A; `omega_0_eff` = Ω₀/s²; `delta_dh` = `dh_bounce_max` − `dh_bounce_min` |
| C9 | Ranges: 0 < t_bounce_signal_end ≤ 0.01 s; dh_bounce_max > 0 > dh_bounce_min; all D·h values within ±2000 cm; 500 ≤ f_peak ≤ 1500 Hz; 0 < omega_max ≤ 1e4 rad/s; 5e13 ≤ rho_c_b, rho_c_pb ≤ 3e15 g/cm³; 0 < T_c_b ≤ 50 MeV; 0 < s_c_b ≤ 5 kB/baryon; 0 < masses ≤ 5 Msun; 0 < r_pns ≤ 200 km; j > 0 |
| C10 | Row count equals the manifest (7,438 for the full data, 810 for the fragment) and the MD5 sums equal the revision in §3 (full) or the manifest (fragment) |
| C11 | `strain.csv.gz`: first column `run_id` in exactly the order of `parameters.csv` |
| C12 | Time grid: 131 columns, uniform step 1/16384 s (relative tolerance 1e-3), first sample −1.95312 ms, t = 0 included |
| C13 | Strain cells: no empty cell, all finite, all within ±2000 cm |
| C14 | min(strain) ≥ 1.01 · `dh_bounce_min` (the resampled signal may overshoot the native-rate minimum by < 1 %, §3) |

## 5. Physical properties (checked by `checks/test_properties.py`)

| # | Property | Reason |
|---|---|---|
| P1 | `mgrav_ic_b` < `mrest_ic_b` | gravitational binding energy is negative, so gravitational mass < rest mass |
| P2 | `r_pns_pole_b` ≤ `r_pns_eq_b` | centrifugal support flattens a rotating core (oblate), never prolate |
| P3 | 0 < `ye_c_b` < 0.5 | charge neutrality and neutronisation: the collapsed centre is neutron-rich |
| P4 | 0 < `alpha_c_b` < 1 | the lapse is below 1 inside a gravitational well and positive without a horizon |
| P5 | `mgrav_ic_b` ≤ `mgrav_b` and `j_ic_b` ≤ `j_b` | the inner core is part of the grid |
| P6 | 0 < `beta_ic_b` < 0.27 and 0 < `beta_b` < 0.27 | rotating cores at bounce stay below the dynamical bar-mode threshold T/|W| ≈ 0.27 |
| P7 | at fixed (progenitor, EOS, A), `beta_ic_b` and `j_ic_b` strictly increase with Ω₀ while T/|W| < 0.08 | more initial rotation gives more rotation at bounce in the slow regime (Richers: the trend reverses only for rapid rotation, `literature/md/richers2017.md:L573-L575`) |

## 6. Split and statistics code (checked by `checks/test_splits.py`, `checks/test_stats.py`)

- `group_kfold(groups, k, seed)`: every row in exactly one test fold (partition: no row lost
  or repeated); no group (EOS) in both the training and test part of any fold; folds
  non-empty; same seed ⇒ same folds; checked on 200 generated inputs with random n, k and
  group sizes, and on the real EOS labels.
- Statistics: OLS recovers an exact line; RMSE is 0 on a perfect fit; Student-t CDF matches
  tabulated quantiles (t₀.₉₇₅ with 4 d.o.f. = 2.776); Holm-adjusted p-values are ≥ raw,
  monotone in the raw order and ≤ 1.
- `src/data.py`: a filter `--where X --where Y` returns the intersection of the two single
  filters; `--out` written twice gives identical bytes.

## 7. Acceptance rule for Claim H (fixed before the first run)

1. The contract (§4) and the properties (§5) pass on the data used; otherwise stop.
2. Runs: per progenitor, all runs with 0.02 ≤ `beta_ic_b` ≤ 0.06.
3. Models: Δh = a + b·x by OLS on the training folds only, x = `beta_ic_b` or `omega_0`.
4. Split: 6 folds, the 18 EOS assigned 3 per fold at random by `group_kfold` with seeds
   0, 1, 2, 3, 4; both models use the **same folds** for a seed (paired design).
5. Metric: pooled held-out RMSE of `delta_dh` over the 6 test folds; d_s = RMSE_beta − RMSE_omega.
6. Test: per progenitor, two-sided paired t-test of d over the 5 seeds; Holm correction over
   the 3 progenitors at α = 0.05; 95 % t-interval for the mean of d. All 5 seeds are
   reported; no seed or progenitor is dropped or selected.
7. Decision per progenitor, with practical threshold δ = 5 % of the mean baseline RMSE:
   **"T/|W| better"** if the Holm-adjusted p < 0.05, the interval lies below 0 and
   |mean d| ≥ δ; **"no practical difference"** if the interval lies inside (−δ, +δ);
   otherwise **"inconclusive"**. Claim H is accepted if it is "T/|W| better" for all three
   progenitors on the full data.

## 8. Plan of runs (`python3 scripts/amp_experiment.py <step>`)

| Step | What runs | Condition to go on |
|---|---|---|
| `dry` | contract + properties, selection of runs | contract passes; each progenitor has ≥ 50 slow runs and all 18 EOS |
| `smoke` | one progenitor (15), seed 0, both models | both RMSEs finite and > 0; slope of `beta_ic_b` > 0 in every fold |
| `sweep` | 3 progenitors × 5 seeds × 2 models | all 30 RMSEs finite; folds of each seed are a partition (re-checked) |
| `full` | statistics and decision of §7 | writes `results/hw2/experiment_<data>.json` and `.md` |

Each step prints `PASSED` or exits with code 1. Runs are logged to `results/hw2/RUNLOG.md`.

**Subgoal tree**

```
Claim H holds on my data, and the numbers behind it can be trusted
├── the data are what they claim to be          — contract C1–C14 (checks/test_contract.py)
├── the data are physically consistent          — properties P1–P7 (checks/test_properties.py)
├── the evaluation cannot leak EOS information  — group_kfold partition and disjointness (checks/test_splits.py)
│   └── the statistics code is correct          — known values (checks/test_stats.py)
└── the difference is not seed noise            — 5 seeds, paired t, Holm, practical threshold (§7)
```

**Caught errors** (filled after runs; "before"/"after" outputs in `results/hw2/`)

| What was wrong | Real or injected | Caught by | Before | After |
|---|---|---|---|---|
| | | | | |

## 9. Revisions after the first run

(none yet)

## 10. Limitations known in advance

- The contract checks internal consistency of the published files, not that the
  simulations are physically correct (resolution, neutrino treatment, 2D symmetry).
- Derived parameters (`f_peak`, `dh_prebounce_max`, …) were computed from the full-length
  data and cannot be recomputed from the trimmed strain; only C14 relates the two.
- Claim H is tested within one simulation code and one family of initial rotation laws;
  "unseen EOS" means unseen among the 18 EOS of this dataset.
- The fragment (A ∈ {634, 1268} km) has less rotation variety than the full data, so the
  experiment on the fragment is a reproducibility check, not the main result.
