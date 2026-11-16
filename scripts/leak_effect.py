"""Diagnostic: mean held-out RMSE per predictor with the current group_kfold (run on main and on
the branch hw2-injected-error to see the optimistic bias of row-level folds)."""
from pathlib import Path
import os; os.chdir(Path(__file__).resolve().parent.parent)
import sys; sys.path.insert(0, "src"); sys.path.insert(0, "scripts")
import ccsn_contract as cc, amp_experiment as ae
rows = cc.load(cc.data_dir())
for p in (15, 27, 40):
    sel = ae.select(rows, p)
    vals = {x: [ae.cv_rmse(sel, x, s)[0] for s in ae.SEEDS] for x in ae.PREDICTORS}
    print(f"s{p}: " + ", ".join(f"{x} mean RMSE {sum(v)/len(v):.2f} cm" for x, v in vals.items()))
