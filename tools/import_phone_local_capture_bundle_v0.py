#!/usr/bin/env python3
"""
Phase-DeviceEnv-005
Import a phone_local_controlled_capture bundle -> generate archive_root -> validate archive_valid.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from capabilities.device_env.phone_local_capture_bundle_v0 import (  # noqa: E402
    import_phone_local_capture_bundle_to_archive_v0,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle-root", required=True)
    ap.add_argument("--archive-root", required=True)
    args = ap.parse_args()
    out = import_phone_local_capture_bundle_to_archive_v0(args.bundle_root, args.archive_root)
    print(
        json.dumps(
            {
                "tool": "import_phone_local_capture_bundle_v0",
                "phase": "Phase-DeviceEnv-005",
                "bundle_root": args.bundle_root,
                "archive_root": out.get("archive_root"),
                "run_id": out.get("run_id"),
                "bundle_validation": out.get("bundle_validation"),
                "archive_validation": out.get("archive_validation"),
                "assertions": {
                    "realtime_upload": False,
                    "controlled_live_stream": False,
                    "evidence_type": "phone_local_controlled_capture",
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

