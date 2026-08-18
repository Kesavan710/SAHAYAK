import json
from pathlib import Path
from typing import Any

# TODO: Replace with vector similarity search (Pinecone/Chroma) when PINECONE_API_KEY is set

_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "schemes.json"


class SchemeRetriever:
    """In-memory scheme retriever backed by schemes.json.

    Applies basic context filters (state) and returns matching scheme dicts.
    Swap this class body for vector similarity search once a vector DB is
    configured via PINECONE_API_KEY.
    """

    def __init__(self) -> None:
        self._schemes: list[dict[str, Any]] = self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def retrieve(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        """Return schemes that match the given user *context*.

        Filters applied:
        - state: if context["state"] is provided, only schemes whose ``state``
          field is ``"all"`` or matches the requested state (case-insensitive)
          are returned.
        """
        requested_state = (context.get("state") or "").strip().lower()
        results: list[dict[str, Any]] = []

        for scheme in self._schemes:
            scheme_state = (scheme.get("state") or "all").lower()
            if requested_state and scheme_state not in ("all", requested_state):
                continue
            results.append(scheme)

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self) -> list[dict[str, Any]]:
        try:
            with _DATA_PATH.open(encoding="utf-8") as fh:
                return json.load(fh)
        except FileNotFoundError:
            return []
