import json
from typing import Dict, Any

from ..interfaces.bus import EnvelopeBus


def write_envelope_trace(path: str, bus: EnvelopeBus) -> None:
    record = {"signals": [signal.__dict__ for signal in bus.signals]}
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
