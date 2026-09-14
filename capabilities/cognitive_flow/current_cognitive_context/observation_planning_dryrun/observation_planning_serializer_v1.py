import json
from pathlib import Path
from typing import Mapping

def canonical_json_dumps_v1(value: Mapping[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def write_canonical_json_v1(path: Path, value: Mapping[str, object]) -> None:
    path.write_text(canonical_json_dumps_v1(value) + "\n", encoding="utf-8")
