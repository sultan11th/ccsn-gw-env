"""Text normalisation and tokenisation shared by build_index.py and search.py.

Physics notation is mapped to stable tokens before tokenising, so that
"T/|W|", "$T/|W|$" and "T/W" all become ``tw_ratio``, and "f_\\mathrm{peak}",
"f_{peak}" and "f_peak" all become ``f_peak``. Standard library only.
"""
import re

_PATTERNS = [
    (re.compile(r"T\s*/\s*\\?\|\s*W\s*\\?\|", re.I), " tw_ratio "),   # T/|W|, T/\|W\|
    (re.compile(r"\bT\s*/\s*W\b"), " tw_ratio "),                      # T/W
    (re.compile(r"β|\\beta\b"), " beta "),
    (re.compile(r"f_\{?\s*\\?(?:mathrm|rm|text|textrm)?\s*\{?\s*peak\s*\}?\s*\}?", re.I), " f_peak "),
    (re.compile(r"\bf\s*peak\b|\bfpeak\b", re.I), " f_peak "),
    (re.compile(r"√|\\sqrt\b"), " sqrt "),
    (re.compile(r"<[^>]{1,300}>"), " "),                               # HTML tags left by pandoc
    (re.compile(r"\\[a-zA-Z]+"), " "),                                 # remaining LaTeX commands
]
_TOKEN = re.compile(r"[a-z0-9]+(?:[_.+\-][a-z0-9]+)*")
STOPWORDS = frozenset("""
a an and are as at be been but by can do does for from had has have how i if in into is it
its may more most no not of on or our over such than that the their them then there these
they this those through to was we were what when where which while who why will with within
would you your et al also using used use between than both each other same only very
""".split())


def normalize(text: str) -> str:
    for pat, rep in _PATTERNS:
        text = pat.sub(rep, text)
    return text.lower()


def _stem(tok: str) -> str:
    """Very light plural stripping: 'signals' -> 'signal', keeps 'loss', 'sasi'."""
    if len(tok) > 4 and tok.endswith("ies"):
        return tok[:-3] + "y"
    if len(tok) > 3 and tok.endswith("s") and not tok.endswith(("ss", "us", "is")) and not tok[-2].isdigit():
        return tok[:-1]
    return tok


def tokenize(text: str) -> list[str]:
    """Normalise, split, drop stopwords; hyphenated terms also yield their parts."""
    out = []
    for tok in _TOKEN.findall(normalize(text)):
        if tok in STOPWORDS:
            continue
        out.append(_stem(tok))
        if "-" in tok:
            out.extend(_stem(p) for p in tok.split("-") if p and p not in STOPWORDS)
    return out
