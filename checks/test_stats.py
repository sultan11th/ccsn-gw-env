"""Statistics code of the experiment against known values (METHOD.md §6)."""
import random
import unittest

from _common import ROOT  # noqa: F401  (sets the import path)
from hw2lib import decide, holm, ols, paired_t, rmse, t_cdf, t_quantile


class Stats(unittest.TestCase):
    def test_ols_recovers_exact_line(self):
        x = [0.5 * i for i in range(20)]
        a, b = ols(x, [3.0 - 2.5 * xi for xi in x])
        self.assertAlmostEqual(a, 3.0, places=10)
        self.assertAlmostEqual(b, -2.5, places=10)

    def test_rmse(self):
        self.assertEqual(rmse([1, 2, 3], [1, 2, 3]), 0.0)
        self.assertAlmostEqual(rmse([0, 0], [3, 4]), (12.5) ** 0.5)

    def test_t_cdf_known_quantiles(self):
        for t, df, p in [(2.776445, 4, 0.975), (2.570582, 5, 0.975), (12.706205, 1, 0.975),
                         (1.959964, 10 ** 6, 0.975), (1.533206, 4, 0.9), (0.0, 7, 0.5)]:
            self.assertAlmostEqual(t_cdf(t, df), p, places=5, msg=f"t={t}, df={df}")

    def test_t_cdf_symmetry_and_inverse(self):
        for df in (1, 2, 4, 9, 30):
            for t in (0.3, 1.0, 2.5, 6.0):
                self.assertAlmostEqual(t_cdf(-t, df), 1 - t_cdf(t, df), places=12)
                self.assertAlmostEqual(t_quantile(t_cdf(t, df), df), t, places=6)

    def test_paired_t_known_value(self):
        r = paired_t([1, 2, 3, 4, 5])
        self.assertAlmostEqual(r["mean"], 3.0)
        self.assertAlmostEqual(r["t"], 4.242641, places=5)
        self.assertAlmostEqual(r["p"], 0.013236, places=5)
        self.assertAlmostEqual(r["ci"][0], 3 - 2.776445 * (2.5 ** 0.5) / (5 ** 0.5), places=5)

    def test_holm_known_and_properties(self):
        self.assertEqual([round(x, 10) for x in holm([0.01, 0.04, 0.03])], [0.03, 0.06, 0.06])
        rng = random.Random(1)
        for _ in range(200):
            p = [rng.random() for _ in range(rng.randint(1, 8))]
            adj = holm(p)
            self.assertTrue(all(a >= q and a <= 1 for a, q in zip(adj, p)))
            order = sorted(range(len(p)), key=lambda i: p[i])
            self.assertEqual([adj[i] for i in order], sorted(adj[i] for i in order))

    def test_decision_rule(self):
        self.assertEqual(decide((-30, -20), -25, 0.001, 5), "T/|W| better")
        self.assertEqual(decide((-30, -20), -25, 0.2, 5), "inconclusive")
        self.assertEqual(decide((-3, -1), -2, 0.001, 5), "no practical difference")
        self.assertEqual(decide((-8, 2), -3, 0.3, 5), "inconclusive")


if __name__ == "__main__":
    unittest.main()
