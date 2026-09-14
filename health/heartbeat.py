import time


def update_heartbeat(snapshot: dict) -> dict:
    snapshot["health"] = {
        "last_tick_time": time.time(),
        "loop_alive": True,
    }
    return snapshot
