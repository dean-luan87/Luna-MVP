from __future__ import annotations

import json
from typing import Dict, Iterable


def read_timeline_jsonl(path: str) -> Iterable[Dict]:
    """
    Read-only timeline reader.
    Each line is a JSON object (TimelineFrame-like).
    """
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
