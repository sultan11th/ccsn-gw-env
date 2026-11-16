# HW2 run log

| Time | Step | Data | Revision | Result | Note |
|---|---|---|---|---|---|
| 2026-11-17 01:16:55 | smoke | checks/fixtures/data | fragment | PASSED | s15 seed 0: RMSE beta 42.009 cm, omega_0 58.103 cm; beta slopes 8177..8670 cm |
| 2026-11-17 01:16:56 | full | checks/fixtures/data | fragment | FAILED | sweep condition not met |
| 2026-11-17 01:17:34 | dry | data/data | full | PASSED | contract OK; slow runs (n, EOS) per progenitor: s15: 808, 18, s27: 844, 18, s40: 846, 18 |
| 2026-11-17 01:17:35 | smoke | data/data | full | PASSED | s15 seed 0: RMSE beta 39.847 cm, omega_0 95.443 cm; beta slopes 9063..9544 cm |
| 2026-11-17 01:17:36 | sweep | data/data | full | PASSED | 30 RMSEs finite: True; folds are partitions with disjoint EOS: True |
| 2026-11-17 01:17:36 | full | data/data | full | PASSED | claim H accepted; s15: T/\|W\| better; s27: T/\|W\| better; s40: T/\|W\| better |
| 2026-11-17 01:17:41 | dry | checks/fixtures/data | fragment | PASSED | contract OK; slow runs (n, EOS) per progenitor: s15: 122, 18, s27: 126, 18, s40: 126, 18 |
| 2026-11-17 01:17:41 | smoke | checks/fixtures/data | fragment | PASSED | s15 seed 0: RMSE beta 46.102 cm, omega_0 60.455 cm; beta slopes 8142..8658 cm |
| 2026-11-17 01:17:41 | sweep | checks/fixtures/data | fragment | PASSED | 30 RMSEs finite: True; folds are partitions with disjoint EOS: True |
| 2026-11-17 01:17:42 | full | checks/fixtures/data | fragment | PASSED | claim H accepted; s15: T/\|W\| better; s27: T/\|W\| better; s40: T/\|W\| better |

Rows 1-2 (01:16:55-56) were run on the branch `hw2-injected-error` (row-level folds): `smoke`
passed but did not stop and ran on into `sweep`, whose partition guard rejected the leaky
folds ("sweep condition not met"). This exposed a real bug in `scripts/amp_experiment.py`
(a passed step did not exit), fixed in commit "each experiment step stops after it passes".
All later rows are on `main` after the fix.
| 2026-11-17 01:18:38 | full | data/data | full | PASSED | claim H accepted; s15: T/\|W\| better; s27: T/\|W\| better; s40: T/\|W\| better |
| 2026-11-17 01:18:38 | full | checks/fixtures/data | fragment | PASSED | claim H accepted; s15: T/\|W\| better; s27: T/\|W\| better; s40: T/\|W\| better |
| 2026-11-17 01:18:45 | dry | checks/fixtures/data | fragment | PASSED | contract OK; slow runs (n, EOS) per progenitor: s15: 122, 18, s27: 126, 18, s40: 126, 18 |
| 2026-11-17 01:53:17 | dry | data/data | full | PASSED | contract OK; [groups: family] slow runs (n, family groups) per progenitor: s15: 808, 10, s27: 844, 10, s40: 846, 10 |
| 2026-11-17 01:53:17 | smoke | data/data | full | PASSED | [groups: family] s15 seed 0: RMSE beta 37.349 cm, omega_0 94.719 cm; beta slopes 9070..9428 cm |
| 2026-11-17 01:53:18 | sweep | data/data | full | PASSED | [groups: family] 30 RMSEs finite: True; folds are partitions with disjoint family groups: True |
| 2026-11-17 01:53:18 | full | data/data | full | PASSED | [groups: family] claim H accepted; s15: T/\|W\| better; s27: T/\|W\| better; s40: T/\|W\| better |
| 2026-11-17 01:53:18 | dry | checks/fixtures/data | fragment | PASSED | contract OK; [groups: family] slow runs (n, family groups) per progenitor: s15: 122, 10, s27: 126, 10, s40: 126, 10 |
| 2026-11-17 01:53:18 | smoke | checks/fixtures/data | fragment | PASSED | [groups: family] s15 seed 0: RMSE beta 42.982 cm, omega_0 58.506 cm; beta slopes 8025..8495 cm |
| 2026-11-17 01:53:18 | sweep | checks/fixtures/data | fragment | PASSED | [groups: family] 30 RMSEs finite: True; folds are partitions with disjoint family groups: True |
| 2026-11-17 01:53:19 | full | checks/fixtures/data | fragment | PASSED | [groups: family] claim H accepted; s15: T/\|W\| better; s27: T/\|W\| better; s40: T/\|W\| better |
