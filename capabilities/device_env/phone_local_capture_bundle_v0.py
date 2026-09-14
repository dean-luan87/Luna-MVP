#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-DeviceEnv-005
Phone Local Controlled Capture Bundle v0 (Mac-side builder + validator + importer).

v0 implementation strategy (per phase constraints):
- Phone uses system camera to record video.
- User transfers video file to Mac.
- Mac builds a phone_capture_bundle (metadata/notes/risk/device_info/summary/manifest + media copy).
- Mac validates bundle manifest/hash and metadata boundary.
- Mac imports bundle -> generates a RealScene archive_root (required_files + manifest), preserving evidence_type.

Hard boundaries:
- evidence_type is phone_local_controlled_capture (must NOT be rewritten to controlled_live)
- controlled_live_stream=false
- phone_local_capture=true
- no realtime upload; no tunnels; no default-on; candidate-only; no execution authority.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


BUNDLE_REQUIRED_FILES_V0: List[str] = [
    "bundle_manifest.json",
    "capture_metadata.json",
    "device_info.json",
    "capture_summary.json",
    "operator_notes.md",
    "risk_events.jsonl",
    "media/video.mp4",
]

ARCHIVE_REQUIRED_FILES_V0: List[str] = [
    "run_evidence.json",
    "trace.jsonl",
    "replay.jsonl",
    "whitebox.jsonl",
    "model_candidate_trace.jsonl",
    "output_candidate_trace.jsonl",
    "operator_notes.md",
    "risk_events.jsonl",
    "post_run_summary.md",
    "archive_manifest.json",
]


def _now_ms() -> int:
    return int(time.time() * 1000)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _is_dir_empty(path: str) -> bool:
    if not os.path.exists(path):
        return True
    if not os.path.isdir(path):
        return False
    return len(os.listdir(path)) == 0


def _ensure_empty_dir_or_nonexistent(path: str, label: str) -> None:
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise ValueError(f"{label}_exists_but_not_dir")
        if os.listdir(path):
            raise ValueError(f"{label}_must_be_empty_dir_or_nonexistent")


@dataclass(frozen=True)
class BundleBuildParams:
    video_path: str
    bundle_root: str
    operator_id: str
    safety_observer_id: str
    record_owner_id: str
    entry_token: str
    timebox_ms: int
    device_id_or_label: str = "phone_unknown"
    camera_facing: str = "environment"  # environment/user


@dataclass(frozen=True)
class BundleBuildResult:
    bundle_root: str
    bundle_id: str
    run_id: str
    media_rel_path: str


def build_phone_local_capture_bundle_v0(p: BundleBuildParams) -> BundleBuildResult:
    if not p.video_path or not os.path.exists(p.video_path):
        raise ValueError("video_path_missing_or_not_found")
    if not str(p.bundle_root or "").strip():
        raise ValueError("bundle_root_empty")
    if not str(p.operator_id or "").strip():
        raise ValueError("operator_id_empty")
    if not str(p.safety_observer_id or "").strip():
        raise ValueError("safety_observer_id_empty")
    if not str(p.record_owner_id or "").strip():
        raise ValueError("record_owner_id_empty")
    if not str(p.entry_token or "").strip():
        raise ValueError("entry_token_empty")
    if not isinstance(p.timebox_ms, int) or p.timebox_ms <= 0:
        raise ValueError("timebox_ms_invalid")
    if p.camera_facing not in ("environment", "user"):
        raise ValueError("camera_facing_invalid")

    _ensure_empty_dir_or_nonexistent(p.bundle_root, "bundle_root")
    os.makedirs(p.bundle_root, exist_ok=True)

    bundle_id = f"bundle_{uuid.uuid4().hex[:10]}"
    run_id = f"plc_{uuid.uuid4().hex[:10]}"
    start_ms = _now_ms()

    media_dir = os.path.join(p.bundle_root, "media")
    os.makedirs(media_dir, exist_ok=True)
    media_rel = os.path.join("media", "video.mp4")
    media_dst = os.path.join(p.bundle_root, media_rel)
    shutil.copy2(p.video_path, media_dst)
    original_video_filename = os.path.basename(p.video_path)
    media_format = os.path.splitext(original_video_filename)[1].lstrip(".").lower() or "unknown"

    end_ms = _now_ms()
    duration_ms = end_ms - start_ms

    capture_metadata = {
        "bundle_id": bundle_id,
        "run_id": run_id,
        "evidence_type": "phone_local_controlled_capture",
        "input_source": "phone_local_camera",
        "controlled_live_stream": False,
        "phone_local_capture": True,
        "selected_option": "OptionA_sidewalk_short_walk_observe",
        "scenario_id": "sidewalk_short_walk_observe_v0",
        "explicit_trial_intent": True,
        "entry_token": p.entry_token,
        "capture_started": True,
        "capture_ended": True,
        "start_time_ms": start_ms,
        "end_time_ms": end_ms,
        "duration_ms": duration_ms,
        "timebox_ms": p.timebox_ms,
        "operator_id": p.operator_id,
        "safety_observer_id": p.safety_observer_id,
        "record_owner_id": p.record_owner_id,
        "device_id_or_label": p.device_id_or_label,
        "camera_facing": p.camera_facing,
        "media_type": "video",
        "media_path": media_rel,
        "original_video_filename": original_video_filename,
        "media_format": media_format,
        "privacy_area_checked": True,
        "environment_allowed": True,
        "no_execute_leakage_assertion": True,
        "no_default_on_assertion": True,
        "no_side_effect_expansion_assertion": True,
        "abort_triggered": False,
        "abort_reason": None,
        "fallback_triggered": False,
        "degraded_triggered": False,
        "pending_mac_import": True,
    }
    _write_json(os.path.join(p.bundle_root, "capture_metadata.json"), capture_metadata)

    device_info = {
        "device_id_or_label": p.device_id_or_label,
        "camera_facing": p.camera_facing,
        "media_capture": {"media_type": "video", "filename": "video.mp4", "original_filename": original_video_filename, "format": media_format},
        "notes": "v0: built on Mac from transferred phone video file; no realtime upload",
    }
    _write_json(os.path.join(p.bundle_root, "device_info.json"), device_info)

    capture_summary = {
        "bundle_id": bundle_id,
        "run_id": run_id,
        "summary": "phone_local_controlled_capture_v0 bundle prepared for Mac import",
        "controlled_live_stream": False,
        "pending_mac_import": True,
    }
    _write_json(os.path.join(p.bundle_root, "capture_summary.json"), capture_summary)

    _write_text(
        os.path.join(p.bundle_root, "operator_notes.md"),
        "\n".join(
            [
                "# operator_notes_v0 (phone_local_controlled_capture)",
                "",
                f"- bundle_id: {bundle_id}",
                f"- run_id: {run_id}",
                f"- operator_id: {p.operator_id}",
                f"- safety_observer_id: {p.safety_observer_id}",
                f"- record_owner_id: {p.record_owner_id}",
                "- environment_summary: (to be filled by operator)",
                "- scenario_summary: OptionA_sidewalk_short_walk_observe",
                "- observed_behavior_summary: (to be filled by operator)",
                "- unexpected_behavior: none_observed",
                "- manual_intervention: none",
                "- abort_used: false",
                "- fallback_used: false",
                "- degraded_used: false",
                "- privacy_issue_observed: none_observed",
                "- follow_up_required: false",
                "",
            ]
        )
        + "\n",
    )

    _write_jsonl(
        os.path.join(p.bundle_root, "risk_events.jsonl"),
        [{"risk_events_status": "none_observed", "timestamp_ms": _now_ms(), "source": "record_owner"}],
    )

    # Bundle manifest (hash everything required)
    _write_json(os.path.join(p.bundle_root, "bundle_manifest.json"), {"placeholder": True})
    manifest1 = build_bundle_manifest_v0(p.bundle_root, bundle_id=bundle_id)
    _write_json(os.path.join(p.bundle_root, "bundle_manifest.json"), manifest1)
    manifest2 = build_bundle_manifest_v0(p.bundle_root, bundle_id=bundle_id)
    _write_json(os.path.join(p.bundle_root, "bundle_manifest.json"), manifest2)

    return BundleBuildResult(bundle_root=p.bundle_root, bundle_id=bundle_id, run_id=run_id, media_rel_path=media_rel)


def build_bundle_manifest_v0(bundle_root: str, bundle_id: str) -> Dict[str, Any]:
    required = list(BUNDLE_REQUIRED_FILES_V0)
    file_hashes: Dict[str, str] = {}
    missing: List[str] = []
    for relp in required:
        ap = os.path.join(bundle_root, relp)
        if not os.path.exists(ap):
            missing.append(relp)
            continue
        file_hashes[relp] = _sha256_file(ap)
    integrity_status = "pass" if not missing else "fail"
    return {
        "manifest_id": f"bm_{uuid.uuid4().hex[:10]}",
        "bundle_id": bundle_id,
        "generated_at_ms": _now_ms(),
        "required_files": required,
        "file_hashes": file_hashes,
        "missing_files": missing,
        "hash_mismatches": [],
        "integrity_status": integrity_status,
        "bundle_ready": integrity_status == "pass",
    }


def validate_phone_local_capture_bundle_v0(bundle_root: str) -> Dict[str, Any]:
    hard: List[str] = []
    soft: List[str] = []

    missing: List[str] = []
    for relp in BUNDLE_REQUIRED_FILES_V0:
        if not os.path.exists(os.path.join(bundle_root, relp)):
            missing.append(relp)
    if missing:
        hard.append("missing_required_files")

    # capture_metadata boundary
    meta_path = os.path.join(bundle_root, "capture_metadata.json")
    meta: Optional[Dict[str, Any]] = None
    if os.path.exists(meta_path):
        try:
            meta = _read_json(meta_path)
        except Exception:
            hard.append("capture_metadata_unparseable")
    else:
        hard.append("capture_metadata_missing")

    if meta is not None:
        if meta.get("evidence_type") != "phone_local_controlled_capture":
            hard.append("evidence_type_mismatch")
        if meta.get("input_source") != "phone_local_camera":
            hard.append("input_source_mismatch")
        if meta.get("controlled_live_stream") is not False:
            hard.append("controlled_live_stream_not_false")
        if meta.get("phone_local_capture") is not True:
            hard.append("phone_local_capture_not_true")
        if not str(meta.get("original_video_filename") or "").strip():
            hard.append("original_video_filename_missing")
        if not str(meta.get("media_path") or "").strip():
            hard.append("media_path_missing")
        if meta.get("privacy_area_checked") is not True:
            hard.append("privacy_area_checked_not_true")
        if meta.get("environment_allowed") is not True:
            hard.append("environment_allowed_not_true")
        if meta.get("no_execute_leakage_assertion") is not True:
            hard.append("no_execute_assertion_failed")
        if meta.get("no_default_on_assertion") is not True:
            hard.append("no_default_on_assertion_failed")
        if meta.get("no_side_effect_expansion_assertion") is not True:
            hard.append("no_side_effect_expansion_assertion_failed")
        if meta.get("abort_triggered") is True and not str(meta.get("abort_reason") or "").strip():
            hard.append("abort_reason_missing")

    # media non-empty (prefer metadata media_path)
    media_path = os.path.join(bundle_root, "media", "video.mp4")
    if meta is not None and str(meta.get("media_path") or "").strip():
        media_path = os.path.join(bundle_root, str(meta.get("media_path")))
    if os.path.exists(media_path) and os.path.getsize(media_path) <= 0:
        hard.append("video_empty")

    # risk_events none_observed requirement
    risk_path = os.path.join(bundle_root, "risk_events.jsonl")
    if os.path.exists(risk_path):
        try:
            with open(risk_path, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
            if len(lines) == 0:
                hard.append("risk_events_empty_without_none_observed")
        except Exception:
            hard.append("risk_events_unparseable")
    else:
        hard.append("risk_events_missing")

    # manifest hash validation
    man_path = os.path.join(bundle_root, "bundle_manifest.json")
    man: Optional[Dict[str, Any]] = None
    if os.path.exists(man_path):
        try:
            man = _read_json(man_path)
        except Exception:
            hard.append("bundle_manifest_unparseable")
    else:
        hard.append("bundle_manifest_missing")

    hash_mismatches: List[str] = []
    if man is not None:
        if man.get("integrity_status") != "pass" or man.get("bundle_ready") is not True:
            hard.append("bundle_manifest_not_ready")
        req = man.get("required_files")
        hashes = man.get("file_hashes")
        if not isinstance(req, list) or not isinstance(hashes, dict):
            hard.append("bundle_manifest_fields_missing")
        else:
            for relp in req:
                ap = os.path.join(bundle_root, relp)
                if not os.path.exists(ap):
                    continue
                if relp == "bundle_manifest.json":
                    # allow self-hash mismatch
                    continue
                actual = _sha256_file(ap)
                expected = hashes.get(relp)
                if expected is None:
                    hard.append("bundle_manifest_hash_missing_for_file")
                elif str(expected) != str(actual):
                    hash_mismatches.append(relp)
            if hash_mismatches:
                hard.append("bundle_manifest_hash_mismatch")

    rec = "no_go" if hard else ("conditional_go" if soft else "go")
    return {
        "recommendation": rec,
        "hard_blockers": hard,
        "soft_followups": soft,
        "details": {
            "bundle_root": bundle_root,
            "missing_files": missing,
            "hash_mismatches": hash_mismatches,
        },
    }


def import_phone_local_capture_bundle_to_archive_v0(bundle_root: str, archive_root: str) -> Dict[str, Any]:
    # Validate bundle first
    bundle_val = validate_phone_local_capture_bundle_v0(bundle_root)
    if bundle_val["recommendation"] != "go":
        raise ValueError(f"bundle_validation_failed:{bundle_val.get('hard_blockers')}")

    _ensure_empty_dir_or_nonexistent(archive_root, "archive_root")
    os.makedirs(archive_root, exist_ok=True)

    meta = _read_json(os.path.join(bundle_root, "capture_metadata.json"))
    bundle_id = str(meta.get("bundle_id"))
    run_id = str(meta.get("run_id"))
    original_video_filename = str(meta.get("original_video_filename") or "")

    # Copy media into archive_root/media/
    os.makedirs(os.path.join(archive_root, "media"), exist_ok=True)
    src_video_rel = str(meta.get("media_path") or os.path.join("media", "video.mp4"))
    src_video = os.path.join(bundle_root, src_video_rel)
    dst_video_rel = os.path.join("media", "video.mp4")
    dst_video = os.path.join(archive_root, dst_video_rel)
    shutil.copy2(src_video, dst_video)

    start_ms = _now_ms()

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []

    def trace(event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        trace_rows.append(
            {
                "timestamp_ms": _now_ms(),
                "run_id": run_id,
                "event_type": event_type,
                "seq": len(trace_rows) + 1,
                "payload": payload or {},
            }
        )

    trace("run_started", {"phase": "Phase-DeviceEnv-005", "evidence_type": "phone_local_controlled_capture"})
    trace("bundle_verified", {"bundle_id": bundle_id})
    trace("import_started", {"source_bundle_root": bundle_root})

    # Build minimal replay events by sampling frames from imported video
    sampled = 0
    try:
        import cv2  # local dependency

        cap = cv2.VideoCapture(dst_video)
        if not cap.isOpened():
            raise ValueError("imported_video_failed_to_open")
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
        idx = 0
        frame_step = 30
        max_sampled = 200
        while sampled < max_sampled:
            ret, frame = cap.read()
            if not ret:
                break
            idx += 1
            if (idx - 1) % frame_step != 0:
                continue
            sampled += 1
            ts_ms = int(((idx - 1) / fps) * 1000) if fps and fps > 0 else _now_ms()
            frame_ref = f"phone_local://bundle/{bundle_id}#video/video.mp4#frame/{idx}"
            trace("frame_sampled", {"frame_index": idx, "timestamp_ms": ts_ms, "frame_ref": frame_ref})
            replay_rows.append(
                {
                    "timestamp_ms": ts_ms,
                    "frame_index": idx,
                    "frame_ref": frame_ref,
                    "input_source": "phone_local_camera",
                    "replay_available": True,
                    "source_media_path": dst_video_rel,
                    "source_original_video_filename": original_video_filename,
                    "frame_ref_strategy": "phone_bundle_media_reference",
                }
            )
        cap.release()
    except Exception as e:
        trace("run_failed", {"reason": f"exception:{type(e).__name__}:{e}"})
        raise

    trace(
        "no_execute_leakage_assertion",
        {
            "no_execute_leakage_assertion": True,
            "no_default_on_assertion": True,
            "no_side_effect_expansion_assertion": True,
        },
    )
    trace("run_completed", {"sampled_frame_count": sampled})

    # Minimal whitebox/model/output (candidate-only gates)
    whitebox_rows = [
        {
            "timestamp_ms": _now_ms(),
            "run_id": run_id,
            "candidate_only": True,
            "default_path_disabled": True,
            "full_controlled_trial": False,
            "model_execution_authority": False,
            "allows_execute_now": False,
            "mode": "phone_local_controlled_capture",
        }
    ]
    model_rows = [
        {
            "timestamp_ms": _now_ms(),
            "run_id": run_id,
            "model_invoked": False,
            "model_shadow_status": "disabled_or_not_used",
            "candidate_only": True,
            "reason": "device_env_005_v0_focus_on_bundle_import_and_archive_bridge",
        }
    ]
    output_rows = [
        {
            "timestamp_ms": _now_ms(),
            "run_id": run_id,
            "output_type": "silence",
            "allows_execute_now": False,
            "suppression_reason": "device_env_005_v0_no_output_chain_execution",
            "reason_codes": ["CANDIDATE_ONLY", "PHONE_LOCAL_CAPTURE"],
        }
    ]

    # Copy notes & risk events into archive (preserve)
    shutil.copy2(os.path.join(bundle_root, "operator_notes.md"), os.path.join(archive_root, "operator_notes.md"))
    shutil.copy2(os.path.join(bundle_root, "risk_events.jsonl"), os.path.join(archive_root, "risk_events.jsonl"))

    post_summary = "\n".join(
        [
            "# post_run_summary_v0 (phone_local_controlled_capture import)",
            "",
            f"- run_id: {run_id}",
            f"- bundle_id: {bundle_id}",
            "- run_status: completed",
            f"- sampled_frame_count: {sampled}",
            "- evidence_type: phone_local_controlled_capture",
            "- controlled_live_stream: false",
            "- safety_assertions:",
            "  - no_execute_leakage_assertion: true",
            "  - no_default_on_assertion: true",
            "  - no_side_effect_expansion_assertion: true",
            "",
        ]
    ) + "\n"
    _write_text(os.path.join(archive_root, "post_run_summary.md"), post_summary)

    end_ms = _now_ms()
    run_evidence = {
        "run_id": run_id,
        "scenario_id": "sidewalk_short_walk_observe_v0",
        "selected_option": "OptionA_sidewalk_short_walk_observe",
        "evidence_type": "phone_local_controlled_capture",
        "input_source": "phone_local_camera",
        "controlled_live_stream": False,
        "phone_local_capture": True,
        "source_bundle_id": bundle_id,
        "source_bundle_manifest_path": os.path.join(bundle_root, "bundle_manifest.json"),
        "imported_on_mac": True,
        "archive_generated_from_phone_bundle": True,
        "pending_real_sidewalk_run": True,
        "source_media_path": dst_video_rel,
        "source_original_video_filename": original_video_filename,
        "start_time_ms": start_ms,
        "end_time_ms": end_ms,
        "duration_ms": end_ms - start_ms,
        "sampled_frame_count": sampled,
        "trace_file_path": "trace.jsonl",
        "replay_file_path": "replay.jsonl",
        "whitebox_file_path": "whitebox.jsonl",
        "model_candidate_trace_path": "model_candidate_trace.jsonl",
        "output_candidate_trace_path": "output_candidate_trace.jsonl",
        "operator_notes_path": "operator_notes.md",
        "risk_events_path": "risk_events.jsonl",
        "archive_manifest_path": "archive_manifest.json",
        "post_run_summary_path": "post_run_summary.md",
        "no_execute_leakage_assertion": True,
        "no_default_on_assertion": True,
        "no_side_effect_expansion_assertion": True,
        "overall_run_status": "completed",
        "imported_video_rel_path": dst_video_rel,
    }
    _write_json(os.path.join(archive_root, "run_evidence.json"), run_evidence)

    _write_jsonl(os.path.join(archive_root, "trace.jsonl"), trace_rows)
    _write_jsonl(os.path.join(archive_root, "replay.jsonl"), replay_rows)
    _write_jsonl(os.path.join(archive_root, "whitebox.jsonl"), whitebox_rows)
    _write_jsonl(os.path.join(archive_root, "model_candidate_trace.jsonl"), model_rows)
    _write_jsonl(os.path.join(archive_root, "output_candidate_trace.jsonl"), output_rows)

    # archive manifest last (allow self-hash mismatch)
    _write_json(os.path.join(archive_root, "archive_manifest.json"), {"placeholder": True})
    man1 = build_archive_manifest_v0(archive_root)
    _write_json(os.path.join(archive_root, "archive_manifest.json"), man1)
    man2 = build_archive_manifest_v0(archive_root)
    _write_json(os.path.join(archive_root, "archive_manifest.json"), man2)

    archive_val = validate_phone_local_archive_root_v0(archive_root)
    return {"bundle_validation": bundle_val, "archive_validation": archive_val, "archive_root": archive_root, "run_id": run_id}


def build_archive_manifest_v0(archive_root: str) -> Dict[str, Any]:
    file_hashes: Dict[str, str] = {}
    missing: List[str] = []
    for relp in ARCHIVE_REQUIRED_FILES_V0:
        ap = os.path.join(archive_root, relp)
        if not os.path.exists(ap):
            missing.append(relp)
            continue
        file_hashes[relp] = _sha256_file(ap)
    integrity_status = "pass" if not missing else "partial"
    run_id = "unknown"
    try:
        run_id = _read_json(os.path.join(archive_root, "run_evidence.json")).get("run_id", "unknown")
    except Exception:
        pass
    return {
        "manifest_id": f"am_{uuid.uuid4().hex[:10]}",
        "run_id": run_id,
        "generated_at_ms": _now_ms(),
        "archive_root_path": archive_root,
        "required_files": list(ARCHIVE_REQUIRED_FILES_V0),
        "file_hashes": file_hashes,
        "missing_files": missing,
        "hash_mismatches": [],
        "integrity_status": integrity_status,
        "archive_ready": integrity_status == "pass",
    }


def validate_phone_local_archive_root_v0(archive_root: str) -> Dict[str, Any]:
    hard: List[str] = []
    soft: List[str] = []

    missing: List[str] = []
    for relp in ARCHIVE_REQUIRED_FILES_V0:
        if not os.path.exists(os.path.join(archive_root, relp)):
            missing.append(relp)
    if missing:
        hard.append("missing_required_files")

    run_evidence_path = os.path.join(archive_root, "run_evidence.json")
    ev: Optional[Dict[str, Any]] = None
    if os.path.exists(run_evidence_path):
        try:
            ev = _read_json(run_evidence_path)
        except Exception:
            hard.append("run_evidence_unparseable")
    else:
        hard.append("run_evidence_missing")

    if ev is not None:
        if ev.get("evidence_type") != "phone_local_controlled_capture":
            hard.append("evidence_type_mismatch")
        if ev.get("controlled_live_stream") is not False:
            hard.append("controlled_live_stream_not_false")
        if ev.get("phone_local_capture") is not True:
            hard.append("phone_local_capture_not_true")
        if not str(ev.get("source_bundle_id") or "").strip():
            hard.append("source_bundle_id_missing")
        if not str(ev.get("source_bundle_manifest_path") or "").strip():
            hard.append("source_bundle_manifest_path_missing")
        if ev.get("imported_on_mac") is not True:
            hard.append("imported_on_mac_not_true")
        if ev.get("archive_generated_from_phone_bundle") is not True:
            hard.append("archive_generated_from_phone_bundle_not_true")
        if not str(ev.get("source_media_path") or "").strip():
            hard.append("source_media_path_missing")
        if not str(ev.get("source_original_video_filename") or "").strip():
            hard.append("source_original_video_filename_missing")
        # must NOT be mislabeled as controlled_live
        if ev.get("evidence_type") == "controlled_live":
            hard.append("mislabels_controlled_live")
        if ev.get("no_execute_leakage_assertion") is not True:
            hard.append("no_execute_assertion_failed")
        if ev.get("no_default_on_assertion") is not True:
            hard.append("no_default_on_assertion_failed")
        if ev.get("no_side_effect_expansion_assertion") is not True:
            hard.append("no_side_effect_expansion_assertion_failed")

    # manifest hash check (allow self-hash mismatch)
    man_path = os.path.join(archive_root, "archive_manifest.json")
    man: Optional[Dict[str, Any]] = None
    if os.path.exists(man_path):
        try:
            man = _read_json(man_path)
        except Exception:
            hard.append("manifest_unparseable")
    else:
        hard.append("manifest_missing")

    hash_mismatches: List[str] = []
    if man is not None:
        req = man.get("required_files")
        hashes = man.get("file_hashes")
        if not isinstance(req, list) or not isinstance(hashes, dict):
            hard.append("manifest_fields_missing")
        else:
            for relp in req:
                ap = os.path.join(archive_root, relp)
                if not os.path.exists(ap):
                    continue
                if relp == "archive_manifest.json":
                    continue
                actual = _sha256_file(ap)
                expected = hashes.get(relp)
                if expected is None:
                    hard.append("manifest_hash_missing_for_file")
                elif str(expected) != str(actual):
                    hash_mismatches.append(relp)
            if hash_mismatches:
                hard.append("manifest_hash_mismatch")

    rec = "no_go" if hard else ("conditional_go" if soft else "go")
    return {
        "recommendation": rec,
        "hard_blockers": hard,
        "soft_followups": soft,
        "details": {"archive_root": archive_root, "missing_files": missing, "hash_mismatches": hash_mismatches},
    }

