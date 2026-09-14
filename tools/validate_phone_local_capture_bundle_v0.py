#!/usr/bin/env python3
"""
Phase-DeviceEnv-005
Validate a phone_local_controlled_capture bundle (bundle_valid).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from capabilities.device_env.phone_local_capture_bundle_v0 import (  # noqa: E402
    validate_phone_local_capture_bundle_v0,
)


def _now_ms() -> int:
    return int(time.time() * 1000)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle-root", required=True)
    args = ap.parse_args()
    out = validate_phone_local_capture_bundle_v0(args.bundle_root)
    report = {
        "tool": "validate_phone_local_capture_bundle_v0",
        "phase": "Phase-DeviceEnv-005",
        "generated_at_ms": _now_ms(),
        "bundle_root": args.bundle_root,
        "result": out,
        "assertions": {
            "default_path_enabled": False,
            "full_controlled_trial_entered": False,
            "real_side_effects_expanded": False,
            "open_user_testing": False,
            "scope_expanded": False,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

