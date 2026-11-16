"""Data contract C1-C14 (METHOD.md §4): one test per rule."""
import unittest

from _common import DATA, cc

_result = None


def result():
    global _result
    if _result is None:
        _result = cc.check(DATA)
    return _result


def _make(rule):
    def test(self):
        bad = result().get(rule)
        self.assertIsNotNone(bad, f"{rule} was not evaluated (an earlier rule failed: {list(result())})")
        self.assertEqual(bad, [], f"{rule} violated on {DATA}: {cc._first(bad, 5)}")
    return test


class Contract(unittest.TestCase):
    pass


for _rule in ["C1 columns", "C2 types", "C3 units", "C4 key", "C5 categories", "C6 grid", "C7 rotation_scale",
              "C8 identities", "C9 ranges", "C10 revision", "C11 strain alignment", "C12 time grid",
              "C13 strain cells", "C14 strain vs dh_bounce_min"]:
    setattr(Contract, "test_" + _rule.replace(" ", "_").replace("/", "_"), _make(_rule))

if __name__ == "__main__":
    unittest.main()
