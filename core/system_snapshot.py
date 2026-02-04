import time
from typing import Any, Dict


def create_snapshot() -> Dict[str, Any]:
    return {
        "time": time.time(),
        "self_state": {},
        "perception_facts": {},
        "navigation_state": {},
        "device_state": {},
        "task_state": {},
        "health": {},
    }


def update_snapshot(snapshot: Dict[str, Any], updates: Dict[str, Any] = None) -> Dict[str, Any]:
    if updates:
        for key, value in updates.items():
            snapshot[key] = value
    snapshot["time"] = time.time()
    return snapshot
