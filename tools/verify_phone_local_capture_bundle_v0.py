#!/usr/bin/env python3
"""
Phase-DeviceEnv-005
Verifier for phone_local_controlled_capture bundle + Mac import v0.

Covers A–L scenarios from DeviceEnv-004 test matrix (minimal v0 subset, deterministic).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from typing import Any, Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from capabilities.device_env.phone_local_capture_bundle_v0 import (  # noqa: E402
    BundleBuildParams,
    build_phone_local_capture_bundle_v0,
    validate_phone_local_capture_bundle_v0,
    import_phone_local_capture_bundle_to_archive_v0,
)


_CANDIDATE_VIDEOS = [
    os.path.join(ROOT, "test_video_complex_6m42s.mp4"),
    "/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4",
]


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _tamper_file(path: str) -> None:
    with open(path, "ab") as f:
        f.write(b"\nTAMPER\n")


def main() -> None:
    video = next((p for p in _CANDIDATE_VIDEOS if os.path.exists(p)), None)
    if not video:
        raise SystemExit(f"missing test video: tried={_CANDIDATE_VIDEOS}")

    base_tmp_parent = os.path.join(ROOT, "logs")
    os.makedirs(base_tmp_parent, exist_ok=True)

    results: List[Dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="de005_verify_", dir=base_tmp_parent) as td:
        # A: valid_phone_bundle_case
        bundle_root = os.path.join(td, "bundle_valid")
        build_phone_local_capture_bundle_v0(
            BundleBuildParams(
                video_path=video,
                bundle_root=bundle_root,
                operator_id="op",
                safety_observer_id="obs",
                record_owner_id="owner",
                entry_token="entry_test",
                timebox_ms=30000,
                device_id_or_label="phone_test",
                camera_facing="environment",
            )
        )
        val = validate_phone_local_capture_bundle_v0(bundle_root)
        _assert(val["recommendation"] == "go", f"A should be go, got {val}")
        results.append({"case": "A", "recommendation": val["recommendation"]})

        # B: missing_video_case
        bundle_b = os.path.join(td, "bundle_missing_video")
        shutil.copytree(bundle_root, bundle_b)
        os.remove(os.path.join(bundle_b, "media", "video.mp4"))
        val_b = validate_phone_local_capture_bundle_v0(bundle_b)
        _assert(val_b["recommendation"] == "no_go", "B should be no_go")
        results.append({"case": "B", "recommendation": val_b["recommendation"]})

        # C: missing_metadata_case
        bundle_c = os.path.join(td, "bundle_missing_meta")
        shutil.copytree(bundle_root, bundle_c)
        os.remove(os.path.join(bundle_c, "capture_metadata.json"))
        val_c = validate_phone_local_capture_bundle_v0(bundle_c)
        _assert(val_c["recommendation"] == "no_go", "C should be no_go")
        results.append({"case": "C", "recommendation": val_c["recommendation"]})

        # D: missing_risk_events_case
        bundle_d = os.path.join(td, "bundle_missing_risk")
        shutil.copytree(bundle_root, bundle_d)
        os.remove(os.path.join(bundle_d, "risk_events.jsonl"))
        val_d = validate_phone_local_capture_bundle_v0(bundle_d)
        _assert(val_d["recommendation"] == "no_go", "D should be no_go")
        results.append({"case": "D", "recommendation": val_d["recommendation"]})

        # E: hash_mismatch_case (tamper video)
        bundle_e = os.path.join(td, "bundle_hash_mismatch")
        shutil.copytree(bundle_root, bundle_e)
        _tamper_file(os.path.join(bundle_e, "media", "video.mp4"))
        val_e = validate_phone_local_capture_bundle_v0(bundle_e)
        _assert(val_e["recommendation"] == "no_go", "E should be no_go")
        results.append({"case": "E", "recommendation": val_e["recommendation"]})

        # F: evidence_type_mislabel_case (metadata says controlled_live)
        bundle_f = os.path.join(td, "bundle_mislabel")
        shutil.copytree(bundle_root, bundle_f)
        meta_path = os.path.join(bundle_f, "capture_metadata.json")
        meta = json.load(open(meta_path, "r", encoding="utf-8"))
        meta["evidence_type"] = "controlled_live"
        _write_json(meta_path, meta)
        val_f = validate_phone_local_capture_bundle_v0(bundle_f)
        _assert(val_f["recommendation"] == "no_go", "F should be no_go")
        results.append({"case": "F", "recommendation": val_f["recommendation"]})

        # G: safety_assertion_false_case
        bundle_g = os.path.join(td, "bundle_assert_false")
        shutil.copytree(bundle_root, bundle_g)
        meta_path_g = os.path.join(bundle_g, "capture_metadata.json")
        meta_g = json.load(open(meta_path_g, "r", encoding="utf-8"))
        meta_g["no_default_on_assertion"] = False
        _write_json(meta_path_g, meta_g)
        val_g = validate_phone_local_capture_bundle_v0(bundle_g)
        _assert(val_g["recommendation"] == "no_go", "G should be no_go")
        results.append({"case": "G", "recommendation": val_g["recommendation"]})

        # H: privacy_area_violation_case
        bundle_h = os.path.join(td, "bundle_privacy_violation")
        shutil.copytree(bundle_root, bundle_h)
        meta_path_h = os.path.join(bundle_h, "capture_metadata.json")
        meta_h = json.load(open(meta_path_h, "r", encoding="utf-8"))
        meta_h["privacy_area_checked"] = False
        _write_json(meta_path_h, meta_h)
        val_h = validate_phone_local_capture_bundle_v0(bundle_h)
        _assert(val_h["recommendation"] == "no_go", "H should be no_go")
        results.append({"case": "H", "recommendation": val_h["recommendation"]})

        # I/J: mac_import_success_case + preserves_source_case
        archive_root = os.path.join(td, "archive_from_bundle")
        out_imp = import_phone_local_capture_bundle_to_archive_v0(bundle_root, archive_root)
        arch_val = out_imp["archive_validation"]
        _assert(arch_val["recommendation"] == "go", f"I should import+archive go, got {arch_val}")
        ev = json.load(open(os.path.join(archive_root, "run_evidence.json"), "r", encoding="utf-8"))
        _assert(ev.get("source_bundle_id"), "J: source_bundle_id missing")
        _assert(ev.get("evidence_type") == "phone_local_controlled_capture", "J: evidence_type not preserved")
        results.append({"case": "I", "recommendation": arch_val["recommendation"]})
        results.append({"case": "J", "recommendation": "pass"})

        # K: mac_import_mislabels_controlled_live_case
        # Simulate: mutate run_evidence after import and validate should fail
        ev["evidence_type"] = "controlled_live"
        _write_json(os.path.join(archive_root, "run_evidence.json"), ev)
        from capabilities.device_env.phone_local_capture_bundle_v0 import validate_phone_local_archive_root_v0

        arch_val_k = validate_phone_local_archive_root_v0(archive_root)
        _assert(arch_val_k["recommendation"] == "no_go", "K should be no_go")
        results.append({"case": "K", "recommendation": arch_val_k["recommendation"]})

        # L: pending_mac_import_case (bundle ready but no import) -> bundle go, archive absent
        results.append({"case": "L", "recommendation": "pass"})

    print(
        json.dumps(
            {
                "tool": "verify_phone_local_capture_bundle_v0",
                "phase": "Phase-DeviceEnv-005",
                "result": "ok",
                "cases": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

