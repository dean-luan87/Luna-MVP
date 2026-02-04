"""Tag definitions and helpers for ObjectCard classification."""

from typing import List


SAFETY_CRITICAL = "safety_critical"
INDOOR = "indoor"
OUTDOOR = "outdoor"
TRANSIT = "transit"


def normalize_tags(tags: List[str]) -> List[str]:
    """Return tags in a stable, de-duplicated order."""
    seen = set()
    out: List[str] = []
    for t in tags:
        if t not in seen:
            out.append(t)
            seen.add(t)
    return out
