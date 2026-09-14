"""Controlled synthetic Runner for the Luna V1 Visual Capability System."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from .visual_capability_system_fixture_v1 import build_runner_result
except ImportError:  # direct user-terminal script execution
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from capabilities.vision.registry.visual_capability_system_controlled.visual_capability_system_fixture_v1 import build_runner_result


if __name__ == "__main__":
    print(json.dumps(build_runner_result(), indent=2, ensure_ascii=False))
