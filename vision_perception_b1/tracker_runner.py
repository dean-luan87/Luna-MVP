from __future__ import annotations

from typing import Any, List, Dict


class TrackerRunner:
    def run(self, image: Any) -> List[Dict[str, Any]]:
        return [
            {"label": "person", "confidence": 0.61}
        ]
