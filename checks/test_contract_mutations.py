"""The contract must reject corrupted data: each mutation of a copy of the fragment
has to trigger its rule (METHOD.md §4). This is what makes a green contract meaningful."""
import csv
import gzip
import shutil
import tempfile
import unittest
from pathlib import Path

from _common import ROOT, cc

FRAGMENT = ROOT / "checks" / "fixtures" / "data"


def edit_params(d, fn):
    p = d / "parameters.csv"
    with open(p, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    rows = fn(rows)
    with open(p, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def edit_strain(d, fn):
    p = d / "timeseries" / "strain.csv.gz"
    with gzip.open(p, "rt", newline="") as f:
        rows = list(csv.reader(f))
    rows = fn(rows)
    with gzip.open(p, "wt", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def set_cell(col, value, row=1):
    def fn(rows):
        rows[row][rows[0].index(col)] = value(rows[row][rows[0].index(col)]) if callable(value) else value
        return rows
    return fn


def swap_rows(rows):
    rows[1], rows[2] = rows[2], rows[1]
    return rows


MUTATIONS = {
    "C1 columns": ("params", lambda rows: [r[:-1] for r in rows]),
    "C2 types": ("params", set_cell("f_peak", "")),
    "C3 units": ("dict", None),
    "C4 key": ("params", set_cell("omega_0", lambda v: str(float(v) + 0.5))),
    "C5 categories": ("params", lambda rows: [r[:2] + ["XYZ"] + r[3:] if i == 1 else r for i, r in enumerate(rows)]),
    "C6 grid": ("params", lambda rows: [r[:3] + ["700"] + r[4:] if i == 1 else r for i, r in enumerate(rows)]),
    "C7 rotation_scale": ("params", set_cell("rotation_scale", "1.5")),
    "C8 identities": ("params", set_cell("delta_dh", lambda v: str(float(v) * 1.01))),
    "C9 ranges": ("params", set_cell("f_peak", "80")),
    "C10 revision": ("params", lambda rows: rows[:-1]),
    "C11 strain alignment": ("strain", swap_rows),
    "C12 time grid": ("strain", lambda rows: [r[:60] + r[61:] for r in rows]),
    "C13 strain cells": ("strain", set_cell("0.00000000", "")),
    "C14 strain vs dh_bounce_min": ("strain", lambda rows: [r if i != 1 else [r[0]] + [str(float(x) - 5000)
                                    for x in r[1:]] for i, r in enumerate(rows)]),
}


class Mutations(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ccsn_mut_"))
        shutil.copytree(FRAGMENT, self.tmp / "data")
        self.d = self.tmp / "data"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_unmodified_copy_passes(self):
        bad = {k: v for k, v in cc.check(self.d).items() if v}
        self.assertEqual(bad, {})


def _make(rule, kind, fn):
    def test(self):
        if kind == "params":
            edit_params(self.d, fn)
        elif kind == "strain":
            edit_strain(self.d, fn)
        else:
            p = self.d / "data_dictionary.csv"
            p.write_text(p.read_text(encoding="utf-8").replace("parameters.csv,f_peak,Hz", "parameters.csv,f_peak,kHz"),
                         encoding="utf-8")
        res = cc.check(self.d)
        self.assertIn(rule, res, f"{rule} not evaluated; rules run: {list(res)}")
        self.assertTrue(res[rule], f"mutation for {rule} was NOT detected")
    return test


for _rule, (_kind, _fn) in MUTATIONS.items():
    setattr(Mutations, "test_detects_" + _rule.split()[0], _make(_rule, _kind, _fn))

if __name__ == "__main__":
    unittest.main()
