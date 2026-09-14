"""Runner for the controlled Universal Capability Slot foundation.

The runner evaluates synthetic candidate fixtures only. It never imports a
provider, Model Manager runtime, downloader, installer, or executor.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve()
REPO_ROOT = next(
    candidate
    for candidate in (RUNNER_PATH, *RUNNER_PATH.parents)
    if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir()
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_fixture_v1 import (  # noqa: E402
    build_runner_result,
)


if __name__ == "__main__":
    print(json.dumps(build_runner_result(), indent=2, sort_keys=True))
