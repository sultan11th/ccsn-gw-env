"""EOS-grouped k-fold split (METHOD.md §6): partition, no group leakage, determinism."""
import random
import unittest

from _common import rows
from hw2lib import group_kfold


def generated_cases(n_cases=200, seed=12345):
    rng = random.Random(seed)
    for _ in range(n_cases):
        n_groups = rng.randint(2, 30)
        n = rng.randint(n_groups, 300)
        groups = [f"g{i}" for i in range(n_groups)] + [f"g{rng.randrange(n_groups)}" for _ in range(n - n_groups)]
        rng.shuffle(groups)
        yield groups, rng.randint(2, min(10, n_groups)), rng.randrange(10 ** 6)


class GroupKFold(unittest.TestCase):
    def assert_valid(self, groups, k, seed):
        folds = group_kfold(groups, k, seed)
        ctx = f"n={len(groups)}, groups={len(set(groups))}, k={k}, seed={seed}"
        self.assertEqual(len(folds), k, ctx)
        tests = sorted(i for _, te in folds for i in te)
        self.assertEqual(tests, list(range(len(groups))), f"test folds are not a partition of the rows ({ctx})")
        for f, (train, test) in enumerate(folds):
            self.assertTrue(test, f"fold {f} is empty ({ctx})")
            self.assertEqual(sorted(train + test), list(range(len(groups))), f"fold {f}: train+test != all ({ctx})")
            shared = {groups[i] for i in train} & {groups[i] for i in test}
            self.assertFalse(shared, f"fold {f}: groups {sorted(shared)[:3]} in both train and test ({ctx})")

    def test_partition_and_no_leakage_on_generated_inputs(self):
        for groups, k, seed in generated_cases():
            with self.subTest(n=len(groups), k=k, seed=seed):
                self.assert_valid(groups, k, seed)

    def test_same_seed_same_folds(self):
        for groups, k, seed in generated_cases(50, seed=7):
            self.assertEqual(group_kfold(groups, k, seed), group_kfold(groups, k, seed))

    def test_seeds_change_the_assignment(self):
        groups = [f"g{i % 18}" for i in range(180)]
        assignments = {tuple(tuple(te) for _, te in group_kfold(groups, 6, s)) for s in range(5)}
        self.assertGreater(len(assignments), 1, "all seeds give the same folds")

    def test_real_eos_labels_three_eos_per_fold(self):
        eos = [r["eos"] for r in rows()]
        for seed in range(5):
            self.assert_valid(eos, 6, seed)
            for _, test in group_kfold(eos, 6, seed):
                self.assertEqual(len({eos[i] for i in test}), 3)

    def test_rejects_impossible_k(self):
        with self.assertRaises(ValueError):
            group_kfold(["a", "b"], 3, 0)


if __name__ == "__main__":
    unittest.main()
