"""
Scheme loader utility.
Reads all scheme JSON files from knowledge/schemes/ and provides
lookup helpers used by the eligibility, documents, and application tools.
Person 2 drops new scheme files into knowledge/schemes/ — no code changes needed.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

# Resolve knowledge/schemes/ relative to this file's location
_SCHEMES_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "schemes"

# In-memory cache — loaded once per process
_scheme_cache: Dict[str, dict] = {}


def _load_all() -> Dict[str, dict]:
    """Load all *.json files from the schemes directory into a dict keyed by scheme_id."""
    global _scheme_cache
    if _scheme_cache:
        return _scheme_cache

    if not _SCHEMES_DIR.exists():
        raise FileNotFoundError(f"Schemes directory not found: {_SCHEMES_DIR}")

    loaded: Dict[str, dict] = {}
    for path in sorted(_SCHEMES_DIR.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            scheme_id = data.get("scheme_id")
            if not scheme_id:
                continue  # skip malformed files silently
            loaded[scheme_id] = data
        except (json.JSONDecodeError, OSError):
            continue  # skip unreadable files; log in production

    _scheme_cache = loaded
    return _scheme_cache


def get_all_schemes() -> List[dict]:
    """Return all loaded schemes as a list."""
    return list(_load_all().values())


def get_scheme_by_id(scheme_id: str) -> Optional[dict]:
    """Return a single scheme by its scheme_id, or None if not found."""
    return _load_all().get(scheme_id)


def reload_schemes() -> None:
    """Force a cache reload — useful during development or after Person 2 adds new files."""
    global _scheme_cache
    _scheme_cache = {}
    _load_all()
