"""Shared project root and import path."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ensure_on_path() -> Path:
    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    return ROOT
