"""Make each topic folder importable (the folder names contain hyphens)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for folder in ("string-matching", "suffix-trees", "compression", "graphs", "number-theory"):
    sys.path.insert(0, str(ROOT / folder))
