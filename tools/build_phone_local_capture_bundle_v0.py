#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-DeviceEnv-005
Build a phone_local_controlled_capture bundle from a transferred phone video file.

v0 strategy: phone records video with system camera; user transfers video to Mac; Mac builds bundle.
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
    BundleBuildParams,
    build_phone_local_capture_bundle_v0,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-path", required=True)
    ap.add_argument("--bundle-root", required=True)
    ap.add_argument("--operator-id", required=True)
    ap.add_argument("--safety-observer-id", required=True)
    ap.add_argument("--record-owner-id", required=True)
    ap.add_argument("--entry-token", required=True)
    ap.add_argument("--timebox-ms", type=int, required=True)
    ap.add_argument("--device-id-or-label", default="phone_unknown")
    ap.add_argument("--camera-facing", default="environment", choices=["environment", "user"])
    args = ap.parse_args()

    res = build_phone_local_capture_bundle_v0(
        BundleBuildParams(
            video_path=args.video_path,
            bundle_root=args.bundle_root,
            operator_id=args.operator_id,
            safety_observer_id=args.safety_observer_id,
            record_owner_id=args.record_owner_id,
            entry_token=args.entry_token,
            timebox_ms=int(args.timebox_ms),
            device_id_or_label=args.device_id_or_label,
            camera_facing=args.camera_facing,
        )
    )

    print(
        json.dumps(
            {
                "tool": "build_phone_local_capture_bundle_v0",
                "phase": "Phase-DeviceEnv-005",
                "bundle_root": res.bundle_root,
                "bundle_id": res.bundle_id,
                "run_id": res.run_id,
                "media_rel_path": res.media_rel_path,
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

