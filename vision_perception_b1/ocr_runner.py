from __future__ import annotations

from typing import Any, List, Dict


class OCRRunner:
    def run(self, image: Any) -> List[Dict[str, Any]]:
        return [
            {"text": "EXIT", "confidence": 0.42}
        ]
