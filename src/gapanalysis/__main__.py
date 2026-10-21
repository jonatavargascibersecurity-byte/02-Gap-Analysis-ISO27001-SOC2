"""Allow ``python -m gapanalysis ...``."""

from __future__ import annotations

from .cli import main

raise SystemExit(main())
