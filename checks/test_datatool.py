"""Properties of src/data.py, the agent's data tool (METHOD.md §6)."""
import csv
import os
import shutil
import subprocess
import sys
import unittest

from _common import DATA, ROOT

TMP = ROOT / "results" / ".check_tmp"


def run(*args):
    env = dict(os.environ, CCSN_DATA=str(DATA))
    r = subprocess.run([sys.executable, str(ROOT / "src" / "data.py"), *args], capture_output=True, text=True,
                       env=env, cwd=ROOT)
    if r.returncode:
        raise AssertionError(f"data.py {' '.join(args)} failed: {r.stderr}")
    return r.stdout


def ids(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {row["run_id"] for row in csv.DictReader(f)}


class DataTool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TMP.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP, ignore_errors=True)

    def out(self, name, *where):
        args = ["params"] + [x for w in where for x in ("--where", w)] + ["--out", f"results/.check_tmp/{name}.csv"]
        run(*args)
        return TMP / f"{name}.csv"

    def test_two_filters_are_the_intersection(self):
        for w1, w2 in [("eos==SFHo", "A==634"), ("progenitor_mass==27", "beta_ic_b>=0.05"),
                       ("eos in LS220,HSDD2", "omega_0<5")]:
            a, b, ab = self.out("a", w1), self.out("b", w2), self.out("ab", w1, w2)
            self.assertEqual(ids(ab), ids(a) & ids(b), f"{w1} AND {w2}")
            self.assertTrue(ids(ab), f"empty selection for {w1} AND {w2}")

    def test_out_is_idempotent(self):
        p = self.out("once", "eos==HShen")
        first = p.read_bytes()
        self.assertEqual(self.out("once", "eos==HShen").read_bytes(), first)

    def test_printed_rows_are_capped(self):
        text = run("params", "--limit", "500")
        self.assertIn("showing 50", text)


if __name__ == "__main__":
    unittest.main()
