from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict

from .types import ObservationPolicy


def save_policy(policy: ObservationPolicy, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(policy), f, indent=2)


def load_policy_raw(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
