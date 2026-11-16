"""EOS-grouped split and statistics for the HW2 experiment (METHOD.md §6-7). Standard library only."""
import math
import random


# ----------------------------------------------------------------------------- EOS families
# METHOD.md §9, revision R1: the 10 EOS with distinguishable bounce signals
# (literature/md/akhmetali2026_networkeos.md:L79-L81) and the EOS whose GWs are very similar
# to one of them (literature/md/abylkairov2025_distance.md:L185-L185 and the author).
DISTINGUISHABLE = ("LS180", "LS220", "LS375", "HSTM1", "HSDD2", "HSIUF", "SFHo", "GShenNL3", "GShenFSU2.1", "HShen")
EOS_FAMILY = {
    "LS180": "LS180", "LS220": "LS220", "LS375": "LS375", "GShenNL3": "GShenNL3",
    "HSDD2": "HSDD2", "BHBl": "HSDD2", "BHBlp": "HSDD2", "HSTMA": "HSDD2",
    "HShen": "HShen", "HShenH": "HShen",
    "GShenFSU2.1": "GShenFSU2.1", "GShenFSU1.7": "GShenFSU2.1",
    "SFHo": "SFHo", "SFHx": "SFHo",
    "HSTM1": "HSTM1", "HSNL3": "HSTM1",
    "HSIUF": "HSIUF", "HSFSG": "HSIUF",
}


# ----------------------------------------------------------------------------- split
def group_kfold(groups, k, seed):
    """Split row indices into k folds so that no group (e.g. EOS) is in both train and test.

    The distinct groups are shuffled with random.Random(seed) and dealt to the folds in turn.
    Returns a list of (train_indices, test_indices), one per fold.
    """
    names = sorted(set(groups))
    if not 2 <= k <= len(names):
        raise ValueError(f"need 2 <= k <= number of groups ({len(names)}), got k={k}")
    random.Random(seed).shuffle(names)
    fold_of = {g: i % k for i, g in enumerate(names)}
    folds = []
    for f in range(k):
        test = [i for i, g in enumerate(groups) if fold_of[g] == f]
        train = [i for i, g in enumerate(groups) if fold_of[g] != f]
        folds.append((train, test))
    return folds


# ----------------------------------------------------------------------------- models
def ols(x, y):
    """Least-squares line y = a + b x; returns (a, b)."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    if sxx == 0:
        raise ValueError("x has zero variance")
    b = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sxx
    return my - b * mx, b


def rmse(y, yhat):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(y, yhat)) / len(y))


# ----------------------------------------------------------------------------- statistics
def _betacf(a, b, x, itmax=300, eps=3e-16):
    """Continued fraction of the regularised incomplete beta function (modified Lentz)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1) < eps:
            break
    return h


def betai(a, b, x):
    """Regularised incomplete beta function I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lbt) * _betacf(a, b, x) / a
    return 1 - math.exp(lbt) * _betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    """CDF of Student's t distribution."""
    tail = 0.5 * betai(df / 2, 0.5, df / (df + t * t))
    return 1 - tail if t >= 0 else tail


def t_quantile(p, df):
    """Inverse CDF of Student's t (bisection)."""
    lo, hi = -1e3, 1e3
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def paired_t(d, level=0.95):
    """Two-sided one-sample t-test of mean(d) = 0 and the t-interval for the mean.

    Returns dict(n, mean, sd, t, p, ci=(lo, hi)). With zero spread, p is 0 for a nonzero mean.
    """
    n = len(d)
    if n < 2:
        raise ValueError("need at least 2 paired values")
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    q = t_quantile(0.5 + level / 2, n - 1)
    if se == 0:
        t, p = (math.inf if mean else 0.0), (0.0 if mean else 1.0)
    else:
        t = mean / se
        p = 2 * (1 - t_cdf(abs(t), n - 1))
    return {"n": n, "mean": mean, "sd": sd, "t": t, "p": p, "ci": (mean - q * se, mean + q * se)}


def holm(pvalues):
    """Holm step-down adjusted p-values, in the input order."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adj, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvalues[i])
        adj[i] = min(1.0, running)
    return adj


def decide(ci, mean, p_adj, delta, alpha=0.05):
    """Decision of METHOD.md §7 rule 7."""
    if p_adj < alpha and ci[1] < 0 and abs(mean) >= delta:
        return "T/|W| better"
    if -delta < ci[0] and ci[1] < delta:
        return "no practical difference"
    return "inconclusive"
