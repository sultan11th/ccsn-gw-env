# HW2 report "Verification": a verifier for the CCSN bounce dataset and the amplitude–T/|W| claim

Authorship marks follow the course rules: `[written]` — written by me, `[generated: model]`
— produced by the AI assistant, `[source: …]` — taken from a source. The summary table is in §9.

| Field | Value |
|---|---|
| Direction | computational |
| Verifier variant | data check (contract with schema, units, ranges, key, identities, file alignment, revision) + property tests (7 physical properties, split and statistics properties) + an experiment with repeats |
| Repository | https://github.com/sultan11th/ccsn-gw-env |
| Git tag | `hw2` |
| Verifier command | `python3 -m unittest discover -s checks -v` (also `make check`; `AGENTS.md` §6) |

## 1. Task and the place of the verifier

`[generated: Claude Opus 5.5]` The project is a research environment for an AI agent that
answers questions about gravitational waves (GWs) from rotating core collapse, from a
library of 48 papers and from my dataset of 7,438 two-dimensional general-relativistic
simulations (3 progenitors × 18 nuclear equations of state (EOS) × 138 rotation profiles).
Every number that the agent or I take from the dataset passes through `src/data.py` and
through derived analyses, such as the ML studies in the library that classify the EOS
from bounce signals.

The verified piece is the **data and the evaluation built on it**. If a row of the
strain file is shifted against the parameter table, an identity such as
Δh = h_max − h_min is broken, a unit is mislabelled or the grid is truncated, every answer
built on the data is wrong while looking plausible. If an evaluation lets waveforms of the
same EOS into training and test data ("template leakage"), EOS-inference results are
inflated: under leave-one-EOS-out validation the models of
`literature/md/mitra2026_generalization.md:L17-L17` become worse than predicting the mean.
On top of this the verifier tests one literature claim on the data with repeats:
in the slow-rotation regime the bounce amplitude follows T/|W| of the inner core
(`[source: Richers et al. 2017, Phys. Rev. D 95, 063019; literature/md/richers2017.md:L237-L247]`).

## 2. Method

`[generated: Claude Opus 5.5]` Summary of `METHOD.md`, committed **before the first run**:
`cd62f8a 2026-11-17 01:12:19 +0500` (`git log --reverse --format="%h %ad" -- METHOD.md | head -1`);
the first HW2 result in `results/hw2/` is from 01:16:55 the same day (`RUNLOG.md`). Files in
`results/` outside `results/hw2/` (agent transcripts of the earlier homework) predate the
method and are not part of this work.

- **Idea:** check that the data are what they claim to be, that they are physically
  consistent, that the EOS-grouped split cannot leak, and test Claim H with a fixed rule.
- **Claim H:** for 0.02 ≤ T/|W| ≤ 0.06, the bounce amplitude D·Δh is predicted on *unseen EOS*
  better by a line in T/|W| (`beta_ic_b`) than by a line in the grid label Ω₀ (baseline).
- **Setup:** varied — predictor (T/|W| vs Ω₀), progenitor (15, 27, 40 M☉), seed (0–4);
  fixed — regime, OLS line fitted on training folds only, 6 folds of 3 EOS each;
  measured — pooled held-out RMSE of D·Δh [cm] and the paired difference
  d = RMSE(T/|W|) − RMSE(Ω₀).
- **Data and revision:** full data local only (MD5 of `parameters.csv`
  `ce3c743c…71`, `strain.csv.gz` `295790fc…b1`, `data_dictionary.csv` `89db9011…7d`), and a
  committed fragment (A ∈ {634, 1268} km, 810 runs) built deterministically by
  `scripts/make_fragment.py`; both revisions are in `checks/data_revision.json`.
- **Acceptance rule (7 points, `METHOD.md` §7):** contract and properties pass; per
  progenitor all slow runs; OLS on training folds; the same EOS-grouped folds for both models
  (paired); pooled RMSE; two-sided paired t-test over 5 seeds with Holm correction over 3
  progenitors at α = 0.05 and a 95 % t-interval; decision "T/|W| better" only if
  p_Holm < 0.05, the interval is below 0 and |mean d| ≥ δ = 5 % of the baseline RMSE.
- **Revision R1 (`METHOD.md` §9, commit `8d76f0e`, 01:52, before any run with it):** after
  reviewing the method I pointed out that only 10 of the 18 EOS give distinguishable bounce
  signals and each of the other 8 is a near-twin of one of them. EOS-grouped folds therefore
  still leak: 28 of the 30 test folds of the original analysis have a family twin in the
  training folds. R1 groups the folds by these 10 families (5 folds of 2 families) and keeps
  every other point of the rule. R1 was written after the original result was known; both
  results are reported.
- **Plan of runs:** `dry` (contract, ≥ 50 slow runs and 18 EOS per progenitor) → `smoke`
  (s15, seed 0; finite RMSEs, positive slopes) → `sweep` (30 RMSEs; folds re-checked as
  partitions) → `full` (statistics and decision). Each step prints `PASSED` or exits 1.

## 3. Verifier

`[generated: Claude Opus 5.5]`

- **What it checks:** the dataset satisfies a 14-rule contract; the contract itself rejects
  each kind of corruption; 7 physical properties hold for every simulation; the EOS-grouped
  k-fold split is a partition with no EOS on both sides; the statistics code reproduces known
  values; the agent's data tool filters and writes files correctly.
- **How it is built:** 55 `unittest` checks in `checks/` on the standard library only
  (`src/ccsn_contract.py`, `src/hw2lib.py`); the experiment in `scripts/amp_experiment.py`.
- **What it does not check:** listed in §8.

**Data contract** (`checks/test_contract.py`, rules of `METHOD.md` §4):

| Rule | Content | Known violations |
|---|---|---|
| C1–C2 | 31 columns in fixed order; types; no empty cells | none |
| C3 | units in the data dictionary equal the contract units | none |
| C4–C5 | `run_id` unique and equal to `s<M>_A<A>_w<Ω₀>_<EOS>`; categories | none |
| C6–C7 | (A, Ω₀) on the simulation grid, ≤ 138 runs per (progenitor, EOS); rotation scale per progenitor | none |
| C8 | identities A_eff = s·A, Ω₀,eff = Ω₀/s², Δh = h_max − h_min (rel. 1e-3) | none |
| C9 | physical ranges (|D·h| ≤ 2000 cm, 500 ≤ f_peak ≤ 1500 Hz, densities, masses, radii, …) | none |
| C10 | row count and MD5 equal a known revision | none |
| C11–C13 | strain file: same `run_id` order, 131 samples on a uniform 1/16384 s grid with t = 0, finite values | none |
| C14 | min(strain) ≥ 1.01 · `dh_bounce_min` | 8 rapid rotators dip 0.1–0.6 % below (resampling overshoot), inside the tolerance set in `METHOD.md` §3 |

**Strength of the contract** (`checks/test_contract_mutations.py`): for each rule a copy of
the fragment is corrupted in one way — a column dropped, an empty cell, a unit changed to
kHz, Ω₀ shifted by 0.5 so the key no longer matches, an unknown EOS, an off-grid A, a wrong
rotation scale, Δh × 1.01, f_peak = 80 Hz, a row removed, two strain rows swapped, a time
column removed, an empty strain cell, a strain dip of −5000 cm — and the test requires the
corresponding rule to fire; the unmodified copy must pass. All 14 mutations are detected.

**Properties** (`checks/test_properties.py`, `test_splits.py`, `test_stats.py`, `test_datatool.py`):

| № | Property | Why it must hold | Test |
|---|---|---|---|
| P1 | M_grav,ic < M_rest,ic | gravitational binding energy is negative | `test_P1_…` |
| P2 | R_pole ≤ R_eq of the PNS | centrifugal support makes a rotating core oblate | `test_P2_…` |
| P3 | 0 < Y_e,c < 0.5 | charge neutrality; the collapsed centre is neutron-rich | `test_P3_…` |
| P4 | 0 < α_c < 1 | the lapse is below 1 in a gravitational well, positive without a horizon | `test_P4_…` |
| P5 | M_ic ≤ M_total, J_ic ≤ J_total | the inner core is part of the grid | `test_P5_…` |
| P6 | 0 < T/\|W\| < 0.27 | cores at bounce stay below the dynamical bar-mode threshold | `test_P6_…` |
| P7 | T/\|W\| and J_ic strictly increase with Ω₀ at fixed (progenitor, EOS, A) while T/\|W\| < 0.08 | more initial rotation gives more rotation at bounce in the slow regime; the trend reverses only for rapid rotation `[source: literature/md/richers2017.md:L573-L575]` | `test_P7_…` |
| S1 | every row is in exactly one test fold; train + test = all rows | a split must not lose or repeat data | 200 generated inputs |
| S2 | no group (EOS) in both train and test of a fold | otherwise "unseen EOS" is not unseen | 200 generated inputs + real EOS labels |
| S3 | same seed ⇒ same folds; different seeds change the folds; impossible k rejected | reproducibility and real randomisation | `test_same_seed_…`, `test_seeds_…` |
| S4 | OLS recovers an exact line; Student-t CDF matches tables (t₀.₉₇₅,₄ = 2.776, …); paired t of (1…5) gives p = 0.0132; Holm ≥ raw, monotone, ≤ 1 | the decision depends on this code | `test_stats.py` |
| S6 | the family map covers the 18 EOS once, has 10 families, each with exactly one distinguishable EOS; family-grouped folds have no family (hence no EOS) on both sides; EOS-grouped folds do split families | revision R1: "unseen" must mean unseen family | `test_splits.EOSFamilies` |
| S5 | `data.py --where X --where Y` = intersection of the single filters; `--out` is idempotent; printed rows capped at 50 | the agent's data tool must return what it claims | `test_datatool.py` |

## 4. Decomposition of the check

`[generated: Claude Opus 5.5]`

```
Claim H holds on my data, and the numbers behind it can be trusted
├── the data are what they claim to be            — closed: contract C1–C14, 1 attempt
│   └── the contract can fail                     — closed: 14 mutation tests, 2 attempts
├── the data are physically consistent            — closed: properties P1–P7, 1 attempt
├── the evaluation cannot leak EOS information    — closed: S1–S3 on 200 generated inputs + real labels, 1 attempt;
│   │                                               injected leak caught (§6)
│   └── the statistics code is correct            — closed: S4 against tabulated values, 1 attempt
├── the difference is not seed noise              — closed: 5 seeds, paired t, Holm, threshold δ (§5), 2 attempts
└── the result survives near-identical EOS        — closed: revision R1, family-grouped folds (S6, §5), 1 attempt
```

Attempt log:

| Subgoal | Attempt | What was tried (who) | Result | Rule of three attempts |
|---|---|---|---|---|
| contract C1–C14 | 1 | rules of `METHOD.md` §4 on the full data and the fragment (agent) | all pass, no rule changed | — |
| the contract can fail | 1 | run `test_contract_mutations.py` as a single file (agent) | import error: `checks/` not on the path when run by file name | 1 of 3 |
| the contract can fail | 2 | run through the official command `unittest discover -s checks` (agent) | 15/15 pass: every mutation detected, clean copy passes | closed |
| properties P1–P7 | 1 | tests on all 7,438 runs (agent) | pass | — |
| split S1–S3 | 1 | 200 generated inputs, real labels (agent) | pass; on the injected branch 201 failures | — |
| statistics S4 | 1 | known quantiles and examples (agent) | pass | — |
| seed noise / decision | 1 | `smoke` on the branch with the injected leak (agent) | `smoke` passed but did not stop, ran into `sweep`, whose partition guard failed: a real bug in the step runner | 1 of 3 |
| seed noise / decision | 2 | each step exits after `PASSED`; `dry → smoke → sweep → full` on `main` (agent) | all steps pass; decision in §5 | closed |

| survives near-identical EOS | 1 | revision R1 from my review; family map from the library and from me; `--group family` (agent) | all steps pass; Claim H accepted for all progenitors | closed |

No subgoal needed a third attempt, so no subgoal had to be split or re-planned.

## 5. Results of the runs

`[generated: Claude Opus 5.5]` Numbers from `results/hw2/experiment_full.md`,
`results/hw2/experiment_fragment.md` and `results/hw2/RUNLOG.md`.

**Depth steps (full data):** `dry` PASSED in 0.5 s (contract OK; 808 / 844 / 846 slow runs for
s15 / s27 / s40, all with 18 EOS) → `smoke` PASSED in 0.5 s (s15, seed 0: RMSE 39.85 cm for
T/|W| vs 95.44 cm for Ω₀; T/|W| slopes 9063–9544 cm in all 6 folds) → `sweep` PASSED in 0.6 s
(30 RMSEs finite; every fold set a partition with disjoint EOS) → `full` PASSED.
The verifier itself takes about 3 s (55 checks).

**Repeats:** 5 seeds (0, 1, 2, 3, 4); every seed is reported, none is selected.

| Variant | Progenitor | Mean RMSE [cm] | SD over seeds [cm] | 95 % interval [cm] |
|---|---|---|---|---|
| Ω₀ baseline | s15 | 95.11 | 0.406 | [94.61; 95.62] |
| T/\|W\| | s15 | 38.79 | 1.133 | [37.39; 40.20] |
| Ω₀ baseline | s27 | 101.00 | 0.352 | [100.57; 101.44] |
| T/\|W\| | s27 | 40.33 | 1.050 | [39.02; 41.63] |
| Ω₀ baseline | s40 | 114.84 | 0.474 | [114.25; 115.43] |
| T/\|W\| | s40 | 51.60 | 1.052 | [50.29; 52.90] |

**Paired comparison with the baseline** (d = RMSE(T/|W|) − RMSE(Ω₀) per seed, Holm over 3 progenitors):

| Progenitor | Mean d [cm] | SD [cm] | 95 % interval [cm] | p | p (Holm) | δ [cm] | Decision |
|---|---|---|---|---|---|---|---|
| s15 | −56.32 | 0.744 | [−57.25; −55.40] | 7.3e-09 | 8.9e-09 | 4.76 | T/\|W\| better |
| s27 | −60.68 | 0.708 | [−61.56; −59.80] | 4.5e-09 | 8.9e-09 | 5.05 | T/\|W\| better |
| s40 | −63.24 | 0.581 | [−63.96; −62.52] | 1.7e-09 | 5.1e-09 | 5.74 | T/\|W\| better |

**Conclusion by the acceptance rule:** Claim H is accepted. For all three progenitors the
difference is significant after the Holm correction, its interval lies below zero, and the
effect (56–63 cm, i.e. the held-out error drops from ≈ 95–115 cm to ≈ 39–52 cm, by 59 %, 60 %
and 55 %) is more than ten times the practical threshold δ ≈ 5 cm. The seed-to-seed spread
of d (SD 0.58–0.74 cm) is small compared with the effect. In words: on unseen EOS the inner-core
T/|W| at bounce explains the bounce amplitude far better than the initial rotation rate,
which ignores differential rotation and EOS-dependent core structure. This agrees with the
linear dependence reported by Richers et al.

**Revision R1: folds grouped by EOS family** (`results/hw2/experiment_full_family.md`;
5 folds of 2 families, same seeds and rule):

| Variant | Progenitor | Mean RMSE [cm] | SD over seeds [cm] | 95 % interval [cm] |
|---|---|---|---|---|
| Ω₀ baseline | s15 | 95.67 | 0.725 | [94.77; 96.57] |
| T/\|W\| | s15 | 40.10 | 2.054 | [37.55; 42.65] |
| Ω₀ baseline | s27 | 101.12 | 0.806 | [100.12; 102.12] |
| T/\|W\| | s27 | 40.52 | 2.083 | [37.93; 43.10] |
| Ω₀ baseline | s40 | 114.66 | 0.746 | [113.73; 115.59] |
| T/\|W\| | s40 | 50.85 | 1.549 | [48.93; 52.77] |

| Progenitor | Mean d [cm] | SD [cm] | 95 % interval [cm] | p | p (Holm) | δ [cm] | Decision |
|---|---|---|---|---|---|---|---|
| s15 | −55.57 | 1.331 | [−57.22; −53.92] | 7.9e-08 | 9.8e-08 | 4.78 | T/\|W\| better |
| s27 | −60.60 | 1.287 | [−62.20; −59.00] | 4.9e-08 | 9.8e-08 | 5.06 | T/\|W\| better |
| s40 | −63.81 | 0.812 | [−64.82; −62.80] | 6.3e-09 | 1.9e-08 | 5.73 | T/\|W\| better |

Claim H is also accepted in the revised sense. Holding out whole families changes the
effect by less than 1 cm (−55.57 vs −56.32 cm for s15). The spread over seeds roughly
doubles (SD of d 0.8–1.3 cm instead of 0.6–0.7 cm), because fewer and larger groups are
dealt to the folds. The amplitude–T/|W| relation therefore does not depend on having a
near-identical EOS in the training data. That is expected: the relation is driven by
rotation, and the EOS enters only weakly through the core structure.

**Fragment** (what a reviewer reproduces from the clean clone; 122–126 slow runs per
progenitor): mean d = −14.79 cm [−15.33; −14.26] (s15), −20.69 cm [−21.19; −20.18] (s27),
−26.65 cm [−27.11; −26.18] (s40); Holm-adjusted p ≤ 1.7e-07; δ = 2.99 / 3.25 / 3.95 cm;
decision "T/|W| better" for all three; with family folds (R1) mean d = −14.52 / −20.51 /
−27.08 cm, also "T/|W| better" for all three (`results/hw2/experiment_fragment_family.md`).
The effect is smaller, probably because the fragment keeps
only two values of A, so the differential rotation that Ω₀ ignores varies less; the verdict is the same.

## 6. Caught error

`[generated: Claude Opus 5.5]`

| What was wrong | Real or injected | Caught by | Output "before" | Output "after" |
|---|---|---|---|---|
| `group_kfold` dealt *rows* to folds (a plain shuffled k-fold), so waveforms of one EOS were in train and test | injected, branch `hw2-injected-error` | `checks/test_splits.py`: all 200 generated inputs and the real EOS labels; also the `sweep` guard | `results/hw2/caught_error_before.txt`: `FAILED (failures=201)`, exit 1 | `results/hw2/caught_error_after.txt`: `Ran 51 tests … OK`, exit 0 (recorded before R1 added 4 checks; now 55) |
| a passed step of `scripts/amp_experiment.py` did not exit, so `smoke` ran on into `sweep` and `full` | real | running the step plan on the branch (`RUNLOG.md` rows 1–2) | `RUNLOG.md` row 2: `full … FAILED – sweep condition not met` after a `smoke` command | fix commit "each experiment step stops after it passes"; all later rows end at their own step |

Why the injected error matters: with row-level folds the T/|W| model looks better than it
is. Its mean held-out RMSE is 35.94 / 37.51 / 48.36 cm instead of 38.79 / 40.33 / 51.60 cm
(s15 / s27 / s40), i.e. about 7 % optimistic (`python3 scripts/leak_effect.py` on both branches).
This is the same optimistic bias that the leave-one-EOS-out validation of the library warns about.

Reproduce "before": `git checkout hw2-injected-error && python3 -m unittest discover -s checks -v`.

## 7. Reproduction

```bash
git clone https://github.com/sultan11th/ccsn-gw-env && cd ccsn-gw-env && git checkout hw2
python3 -m unittest discover -s checks -v                                   # 55 checks, ~2 s on the fragment
for s in dry smoke sweep full; do python3 scripts/amp_experiment.py $s; done                 # original analysis
for s in dry smoke sweep full; do python3 scripts/amp_experiment.py $s --group family; done  # revision R1
```

Environment: Python 3.10.12 on Linux 6.8 (`results/hw2/ENVIRONMENT.txt`). The verifier and
the experiment use only the Python standard library (≥ 3.10), so nothing has to be installed.
Seeds are fixed in the code (folds: 0–4; generated test inputs: 12345, 7 and 1). Running time:
about 2 s for the checks on the fragment, 3 s on the full data, under 1 s per experiment step.
Data: in a clean clone the checks and the experiment run on the committed fragment
`checks/fixtures/data/` (810 of my own simulations, CC BY 4.0) and must reproduce
`results/hw2/experiment_fragment.md` exactly. The full dataset (7,438 runs) is local only.
Its MD5 sums are in `METHOD.md` §3 and `checks/data_revision.json`, and the contract
rejects any other revision.

## 8. Limitations

`[generated: Claude Opus 5.5]`

- The contract checks **internal consistency** of the published files. It does not check
  that the simulations are physically right (resolution, leakage neutrino scheme, 2D
  axisymmetry). Properties P1–P7 are necessary conditions, not a validation of the physics.
- Derived parameters (`f_peak`, `dh_prebounce_max`, the averages over 6 ms after bounce) were
  computed from the full-length time series. They cannot be recomputed from the trimmed
  strain, so only C14 links a derived value to the waveform.
- The ranges of C9 are physical bounds chosen before the run. They catch gross errors (unit
  mix-ups, sign flips), not small numerical drifts inside the bounds.
- C14 allows a 1 % overshoot, which was justified by the exploration of the full data
  *before* the method (`METHOD.md` §3). A real error smaller than 1 % of the bounce minimum
  would pass.
- Claim H is tested within one code, one rotation law and 18 EOS. "Unseen EOS" means unseen
  among these 18, which is not a test of generalisation to other physics. The models are
  one-variable lines; a better baseline (e.g. Ω₀ and A together) could narrow the gap. Claim
  H compares two predictors and makes no causal statement.
- The EOS families of R1 come partly from the library (the 10 distinguishable EOS and three
  pairings in `abylkairov2025_distance`) and partly from my earlier work (SFHx, HSNL3, HSFSG,
  HSTMA). The grouping is based on how distinguishable the waveforms are for EOS
  classification, not on the amplitude itself. R1 was written after the original result was
  known, so it is a robustness check, not a blind pre-registration.
- The randomness that the 5 seeds sample is only the assignment of EOS to folds. The
  simulations are deterministic, so the intervals describe the split, not simulation noise.
- On a clean clone the reviewer reproduces the fragment results. The full-data numbers in §5
  can be checked only by someone who has the full dataset.
- The course self-check `check_week6.py` (week 6 starter kit) was not available locally, so
  it was not run. The checklist of the assignment was followed by hand.

## 9. Use of AI assistants

`[generated: Claude Opus 5.5]` The work was done with Claude Code (model Claude Opus 5.5) in
one session. I chose the topic among the options proposed, decided that a small real
fragment of the data goes into the repository, the report language, and permission to
commit and push. The agent wrote the code, the method and this report. Session transcript:
https://claude.ai/code/session_01LUYjwu1kHox2WJLiYjbvTn.

| Fragment or file | Mark | Tool or model | How it was checked |
|---|---|---|---|
| `METHOD.md` (§1–§8 before the first run, §9 after) | `[generated]` | Claude Code, Claude Opus 5.5 | commit order (`git log`); rules applied unchanged; author review: read and checked by the author on 2026-11-16 |
| `src/ccsn_contract.py` (rules C1–C14) | `[generated]` | Claude Code, Claude Opus 5.5 | passes on the full data and the fragment; 14 mutation tests show each rule can fail |
| `src/hw2lib.py` (`group_kfold`, OLS, Student t, Holm, decision) | `[generated]` | Claude Code, Claude Opus 5.5 | `test_splits.py`, `test_stats.py` against tabulated values; the injected leak is caught |
| `checks/*.py` (55 checks) | `[generated]` | Claude Code, Claude Opus 5.5 | each fails on its injected fault (mutations, branch `hw2-injected-error`); locked by `make lock` |
| `scripts/amp_experiment.py`, `scripts/make_fragment.py`, `scripts/leak_effect.py` | `[generated]` | Claude Code, Claude Opus 5.5 | step conditions; fragment byte-identical on rebuild (MD5 in `checks/data_revision.json`); one real bug found and fixed (§6) |
| `src/data.py` (data tool, `CCSN_DATA`) | `[generated]` | Claude Code, Claude Opus 5.5 | `test_datatool.py` |
| the dataset (`data/`, `checks/fixtures/data/`) | `[written]` | — (my simulations) | contract C1–C14, properties P1–P7 |
| choice of topic, data fragment, language | `[written]` | — | — |
| revision R1: the comment that 8 of the 18 EOS are near-twins of the 10 distinguishable ones, and the family of SFHx, HSNL3, HSFSG and HSTMA | `[written]` | — (my earlier work) | `test_splits.EOSFamilies`; the other pairings from `abylkairov2025_distance` L185 |
| `METHOD.md` §9 R1 text, `EOS_FAMILY` in `src/hw2lib.py`, `--group family` | `[generated]` | Claude Code, Claude Opus 5.5 | committed before the family runs (`8d76f0e`); 4 new checks |
| this report | `[generated]` | Claude Code, Claude Opus 5.5 | numbers compared with `results/hw2/`; author review: read and checked by the author on 2026-11-16 |
| Claim H, the regime 0.02 ≤ T/\|W\| ≤ 0.06 and property P7 | `[source]` | Richers et al. 2017, `literature/md/richers2017.md:L237-L247`, `L348-L356`, `L573-L575` | passages read in the library |
