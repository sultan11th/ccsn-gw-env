"""Physical properties P1-P7 of the simulation output (METHOD.md §5)."""
import unittest
from collections import defaultdict

from _common import rows


def offenders(pred):
    return [r["run_id"] for r in rows() if not pred(r)]


class Physics(unittest.TestCase):
    def check(self, pred, why):
        bad = offenders(pred)
        self.assertEqual(bad, [], f"{why}: {len(bad)} runs, e.g. {bad[:5]}")

    def test_P1_gravitational_mass_below_rest_mass(self):
        self.check(lambda r: r["mgrav_ic_b"] < r["mrest_ic_b"], "mgrav_ic_b >= mrest_ic_b")

    def test_P2_rotating_core_is_oblate(self):
        self.check(lambda r: r["r_pns_pole_b"] <= r["r_pns_eq_b"], "polar radius > equatorial radius")

    def test_P3_electron_fraction_neutron_rich(self):
        self.check(lambda r: 0 < r["ye_c_b"] < 0.5, "ye_c_b outside (0, 0.5)")

    def test_P4_lapse_between_0_and_1(self):
        self.check(lambda r: 0 < r["alpha_c_b"] < 1, "alpha_c_b outside (0, 1)")

    def test_P5_inner_core_is_part_of_the_grid(self):
        self.check(lambda r: r["mgrav_ic_b"] <= r["mgrav_b"] and r["j_ic_b"] <= r["j_b"],
                   "inner-core mass or angular momentum exceeds the total")

    def test_P6_below_bar_mode_threshold(self):
        self.check(lambda r: 0 < r["beta_ic_b"] < 0.27 and 0 < r["beta_b"] < 0.27, "T/|W| outside (0, 0.27)")

    def test_P7_rotation_at_bounce_grows_with_omega0_in_slow_regime(self):
        seq = defaultdict(list)
        for r in rows():
            seq[(r["progenitor_mass"], r["eos"], r["A"])].append(r)
        bad, n = [], 0
        for runs in seq.values():
            runs.sort(key=lambda r: r["omega_0"])
            for a, b in zip(runs, runs[1:]):
                if max(a["beta_ic_b"], b["beta_ic_b"]) >= 0.08:
                    continue
                n += 1
                if not (b["beta_ic_b"] > a["beta_ic_b"] and b["j_ic_b"] > a["j_ic_b"]):
                    bad.append(f"{a['run_id']} -> {b['run_id']}")
        self.assertGreater(n, 0, "no pairs to compare")
        self.assertEqual(bad, [], f"T/|W| or J_ic does not increase with omega_0 in {len(bad)} of {n} pairs: {bad[:5]}")


if __name__ == "__main__":
    unittest.main()
