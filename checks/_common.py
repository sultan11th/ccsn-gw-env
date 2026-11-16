"""Shared set-up for checks/: import path and the data directory under test."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import ccsn_contract as cc  # noqa: E402

DATA = cc.data_dir()          # $CCSN_DATA, else data/data (full, local), else checks/fixtures/data
_rows = None


def rows():
    global _rows
    if _rows is None:
        _rows = cc.load(DATA)
    return _rows
