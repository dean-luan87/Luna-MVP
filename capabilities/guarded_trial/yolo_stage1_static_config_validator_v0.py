# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-003 — Static configuration validation for YOLO Stage-1 (no inference, no camera).

Scans repo paths, schema contracts, and TRW/runbook placeholders only.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

PHASE = "Phase-Mainline-GuardedTrial-003"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _exists(rel: str) -> bool:
    return (_repo_root() / rel).is_file()


def _read_text(rel: str) -> str:
    p = _repo_root() / rel
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def scan_yolo_detector_entrypoints_v0(*, repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    root = repo_root or _repo_root()
    entries: List[Dict[str, Any]] = []

    shadow = "capabilities/model_perception/yolo_shadow_adapter_v0.py"
    p_shadow = root / shadow
    text = _read_text(shadow)
    entries.append(
        {
            "candidate_file": shadow,
            "candidate_function_or_class": "run_yolo_shadow_adapter_on_sample_v0",
            "entrypoint_type": "shadow_adapter",
            "exists": p_shadow.is_file(),
            "allowed_for_stage1_trial": True,
            "notes": "Primary Stage-1 trial path via shadow adapter + disable_yolo gate; guarded trial hook may wrap calls.",
        }
    )
    entries.append(
        {
            "candidate_file": shadow,
            "candidate_function_or_class": "_load_detector_from_repo / YOLOv5Detector",
            "entrypoint_type": "detector",
            "exists": ("Luna_Badge_MVP" in text or "yolov5_detector" in text),
            "allowed_for_stage1_trial": True,
            "notes": "Real detector loads from Luna_Badge_MVP.vision.yolov5_detector — may be absent from Luna-Core mono-repo checkout.",
        }
    )

    trw_shadow = "capabilities/core_trw/yolo_request_trace_shadow_adapter_v0.py"
    p_trw = root / trw_shadow
    entries.append(
        {
            "candidate_file": trw_shadow,
            "candidate_function_or_class": "load_yolo_local_outputs_v0",
            "entrypoint_type": "shadow_adapter",
            "exists": p_trw.is_file(),
            "allowed_for_stage1_trial": True,
            "notes": "Read-only TRW stage extraction from offline yolo_shadow artifacts (post-run reporting).",
        }
    )

    hook = "capabilities/runtime_readiness/yolo_guarded_trial_hook_v0.py"
    p_hook = root / hook
    entries.append(
        {
            "candidate_file": hook,
            "candidate_function_or_class": "evaluate_yolo_guarded_trial_hook_v0",
            "entrypoint_type": "evaluator",
            "exists": p_hook.is_file(),
            "allowed_for_stage1_trial": True,
            "notes": "Guarded gate hook-in; default no-op.",
        }
    )

    return entries


def scan_yolo_frame_source_candidates_v0(*, repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    root = repo_root or _repo_root()
    shadow = root / "capabilities/model_perception/yolo_shadow_adapter_v0.py"
    text = shadow.read_text(encoding="utf-8") if shadow.is_file() else ""

    candidates: List[Dict[str, Any]] = [
        {
            "candidate_file": "capabilities/model_perception/yolo_shadow_adapter_v0.py",
            "candidate_source_type": "video_file",
            "exists": shadow.is_file() and ("PhoneLocalSampleRefV0" in text) and ("VideoCapture" in text),
            "allowed_for_10_frame_trial": True,
            "camera_invocation_required": False,
            "notes": "Adapter resolves source_video_path and uses cv2.VideoCapture(path) — use offline/local video_file for Stage-1; avoid camera index.",
        },
        {
            "candidate_file": "capabilities/model_perception/yolo_shadow_adapter_v0.py",
            "candidate_source_type": "sample_frame",
            "exists": "frame_records" in text and "sample_id" in text,
            "allowed_for_10_frame_trial": True,
            "camera_invocation_required": False,
            "notes": "Frames derived from sampled video indices; detector.detect(frame) per sampled frame.",
        },
        {
            "candidate_file": "configs/models/yolo/yolo_model_manifest_v0.json",
            "candidate_source_type": "offline_dataset",
            "exists": (root / "configs/models/yolo/yolo_model_manifest_v0.json").is_file(),
            "allowed_for_10_frame_trial": False,
            "camera_invocation_required": False,
            "notes": "Manifest describes model pinning; dataset paths are operational, not in manifest.",
        },
    ]
    return candidates


def scan_yolo_model_config_candidates_v0(*, repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    root = repo_root or _repo_root()
    manifest_rel = "configs/models/yolo/yolo_model_manifest_v0.json"
    manifest_path = root / manifest_rel
    weights_exists = False
    weights_rel = ""
    weights_resolved = ""
    if manifest_path.is_file():
        try:
            m = json.loads(manifest_path.read_text(encoding="utf-8"))
            weights_rel = str(m.get("weights_path") or "")
            if weights_rel:
                cand = root / weights_rel
                weights_resolved = str(cand)
                weights_exists = cand.is_file()
        except Exception:
            weights_rel = ""

    adapter_text = _read_text("capabilities/model_perception/yolo_shadow_adapter_v0.py")
    dm = re.search(r"model_path:\s*str\s*=\s*[\"']([^\"']+)[\"']", adapter_text)

    rows: List[Dict[str, Any]] = [
        {
            "config_source": "YoloShadowAdapterConfigV0",
            "config_file": "capabilities/model_perception/yolo_shadow_adapter_v0.py",
            "fields": ["model_config_id", "model_provider", "model_path", "device", "max_frames", "frame_step", "confidence_threshold", "disable_yolo", "evidence_type_required"],
            "default_model_path_in_code": dm.group(1) if dm else None,
            "exists": bool(dm),
            "notes": "Runtime resolves cfg.model_path; compare with manifest weights_path for pinned local trial.",
        },
        {
            "config_source": "yolo_model_manifest_v0.json",
            "config_file": manifest_rel,
            "weights_path_field": weights_rel,
            "weights_resolved_path": weights_resolved,
            "weights_file_resolved_exists": weights_exists,
            "exists": manifest_path.is_file(),
            "notes": "Pinned local weights documented; *.pt may be gitignored — presence is OPERATIONAL.",
        },
    ]
    return rows


def validate_yolo_detection_schema_contract_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    shadow = root / "capabilities/model_perception/yolo_shadow_adapter_v0.py"
    text = shadow.read_text(encoding="utf-8") if shadow.is_file() else ""

    per_sample_keys = [
        "sample_id",
        "run_id",
        "model_config_id",
        "model_provider",
        "yolo_invoked",
        "yolo_disabled",
        "fallback_used",
        "frame_count_sampled",
        "detection_count",
        "normalized_perception_signals",
        "schema_validation_result",
        "forbidden_output_scan_result",
        "allows_execute_now",
    ]

    normalized_top_level = [
        "object_stability_signal",
        "spatial_passability_signal",
        "risk_field_signal",
        "ocr_navigation_signal",
        "dynamic_event_signal",
    ]

    detection_fields = ["bbox", "confidence", "class_id", "class_name", "frame_id", "ts"]

    signals_present = all(k in text for k in normalized_top_level)
    det_norm_present = bool(re.search(r"norm_dets", text))

    contract_found = signals_present and det_norm_present and "_schema_validate_normalized_signals" in text

    return {
        "contract_source": "yolo_shadow_adapter_v0 + normalized signals",
        "per_sample_result_keys_minimum": per_sample_keys,
        "normalized_perception_signal_keys": normalized_top_level,
        "detection_record_fields_normalized": detection_fields,
        "schema_validator_symbol_present": "_schema_validate_normalized_signals" in text,
        "forbidden_scan_present": "_forbidden_scan" in text,
        "contract_found": contract_found,
        "trial_report_compatible": True,
        "notes": "Stage-1 trial report may attach per_sample_yolo_shadow_results.json + envelope fields.",
    }


def validate_yolo_stage1_trw_output_contract_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()

    artifact_pattern = "{output_root}/{sample_id}/per_sample_yolo_shadow_results.json + yolo_shadow_{trace,replay,whitebox}.jsonl"
    trw_validator = root / "capabilities/runtime_readiness/guarded_trial_trw_validator_v0.py"

    rq_stages_doc = []
    adapter = root / "capabilities/core_trw/yolo_request_trace_shadow_adapter_v0.py"
    if adapter.is_file():
        txt = adapter.read_text(encoding="utf-8")
        if "YOLO_STAGES" in txt:
            rq_stages_doc.append("YOLO_STAGES defined in yolo_request_trace_shadow_adapter_v0")

    return {
        "guarded_trial_trw_validator_module_exists": trw_validator.is_file(),
        "minimum_trw_fields_runtime": ["request_id", "hard_audit", "runtime_run_id_or_source_run_id", "trace_ref/replay_ref/whitebox_ref or pending_ref"],
        "yolo_shadow_artifact_layout": artifact_pattern,
        "request_trace_shadow_adapter_ready": adapter.is_file(),
        "request_trace_stage_contract_notes": rq_stages_doc or ["Define stages after artifact presence"],
        "trw_output_contract_ready": trw_validator.is_file() and adapter.is_file(),
    }


def build_yolo_stage1_10_frame_dry_run_runbook_v0(
    *,
    output_root_placeholder: str = "logs/yolo_stage1_10_frames_dry_run_future",
    runbook_id: Optional[str] = None,
) -> Dict[str, Any]:
    rid = runbook_id or f"yolo_stage1_runbook_{uuid.uuid4().hex[:12]}"
    return {
        "runbook_id": rid,
        "trial_stage": "stage1_yolo_guarded_trial",
        "window": "10_frames",
        "execution_allowed_by_this_phase": False,
        "required_flags": {
            "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "true",
            "LUNA_YOLO_TRIAL_MODE": "guarded_local",
            "LUNA_DISABLE_ALL_GUARDED_TRIALS": "false",
            "LUNA_YOLO_TRIAL_MAX_FRAMES": "10",
        },
        "adapter_config_hints": {
            "disable_yolo": "must be False for detector path (explicit operator step after GO)",
            "max_frames": 10,
            "frame_step": 1,
            "evidence_type": "phone_local_controlled_capture",
            "controlled_live_stream": False,
            "preferred_input_source": "local_video_file_path_not_camera_index",
        },
        "pre_run_checks": [
            "Phase-Mainline-GuardedTrial-002 precheck GO",
            "Only YOLO entry flag enabled; OCR/Qwen false",
            "Global kill reachable",
            "output_root writable",
            "pinned weights present if using local detector (manifest models/yolo/yolov5n.pt)",
            "source_video exists and readable (offline)",
        ],
        "abort_conditions": [
            "detector exception streak >= policy",
            "schema invalid any",
            "downstream invocation > 0",
            "navigation_action non-null",
            "world_write_invoked",
            "request trace missing when required",
            "global kill triggered",
        ],
        "rollback_commands": [
            "unset LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1",
            "export LUNA_DISABLE_ALL_GUARDED_TRIALS=true",
        ],
        "expected_outputs": [
            "per_sample_yolo_shadow_results.json",
            "yolo_shadow_trace.jsonl",
            "yolo_shadow_replay.jsonl",
            "yolo_shadow_whitebox.jsonl",
            "normalized_perception_signals + schema_validation_result",
        ],
        "must_remain_false": [
            "real_tts_invoked",
            "playback_invoked",
            "navigation_action",
            "world_write_invoked",
            "downstream_invocation_count",
        ],
        "output_root_placeholder": output_root_placeholder,
    }


def run_yolo_stage1_static_config_validation_v0(
    *,
    repo_root: Optional[Path] = None,
    output_root_for_writable_probe: Optional[Path] = None,
) -> Dict[str, Any]:
    """Full static validation record (no inference)."""
    root = repo_root or _repo_root()
    vid = f"yolo_s1_static_{uuid.uuid4().hex[:14]}"

    detector_matrix = scan_yolo_detector_entrypoints_v0(repo_root=root)
    frame_matrix = scan_yolo_frame_source_candidates_v0(repo_root=root)
    model_matrix = scan_yolo_model_config_candidates_v0(repo_root=root)
    schema_val = validate_yolo_detection_schema_contract_v0(repo_root=root)
    trw_val = validate_yolo_stage1_trw_output_contract_v0(repo_root=root)
    runbook = build_yolo_stage1_10_frame_dry_run_runbook_v0()

    det_entry_found = any(
        e.get("exists")
        and e.get("entrypoint_type") == "shadow_adapter"
        and "run_yolo_shadow_adapter_on_sample_v0" in str(e.get("candidate_function_or_class", ""))
        for e in detector_matrix
    )
    frame_found = any(
        e.get("exists") and e.get("candidate_source_type") == "video_file" and e.get("allowed_for_10_frame_trial") for e in frame_matrix
    )
    model_found = any(
        bool(row.get("exists")) for row in model_matrix
    )

    weights_row = model_matrix[-1] if model_matrix else {}
    warnings: List[str] = []
    if not weights_row.get("weights_file_resolved_exists"):
        warnings.append("pinned_weights_file_missing_at_manifest_path_models_yolo_yolov5n_pt")

    # External detector checkout
    if not any("Luna_Badge_MVP" in str(e.get("notes", "")) and e.get("exists") for e in detector_matrix):
        pass
    badge_note = next((e for e in detector_matrix if "Luna_Badge_MVP" in str(e.get("notes", ""))), None)
    if badge_note and not badge_note.get("exists"):
        warnings.append("detector_python_module_reference_may_resolve_only_with_Luna_Badge_MVP_installed")

    schema_ok = bool(schema_val.get("contract_found"))
    trw_ok = bool(trw_val.get("trw_output_contract_ready"))
    runbook_ok = bool(runbook.get("execution_allowed_by_this_phase") is False and runbook.get("window") == "10_frames")

    blockers: List[str] = []
    if not det_entry_found:
        blockers.append("detector_shadow_adapter_entry_not_found")
    if not frame_found:
        blockers.append("video_file_frame_path_not_documented")
    if not model_found:
        blockers.append("model_config_manifest_or_adapter_defaults_missing")

    if not schema_ok:
        blockers.append("detection_schema_contract_incomplete")
    if not trw_ok:
        blockers.append("trw_output_contract_incomplete")
    if not runbook_ok:
        blockers.append("dry_run_runbook_incomplete")

    static_result = "NO_GO"
    if not blockers:
        static_result = "GO" if not warnings else "CONDITIONAL_GO"

    hard_audit = {
        "runtime_invoked": False,
        "detector_invoked": False,
        "camera_invoked": False,
        "provider_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
        "video_stream_opened": False,
    }

    return {
        "validation_id": vid,
        "capability": "yolo",
        "stage": "stage1_yolo_guarded_trial",
        "validation_mode": "static_config_only",
        "phase": PHASE,
        "detector_invoked": False,
        "camera_invoked": False,
        "video_stream_opened": False,
        "detector_entrypoint_found": det_entry_found,
        "frame_source_candidate_found": frame_found,
        "model_config_candidate_found": model_found,
        "detection_schema_contract_found": schema_ok,
        "trw_output_contract_ready": trw_ok,
        "dry_run_10_frame_runbook_ready": runbook_ok,
        "static_validation_result": static_result if not blockers else "NO_GO",
        "blockers": blockers,
        "warnings": warnings,
        "hard_audit": hard_audit,
        "detector_entrypoint_matrix": detector_matrix,
        "frame_source_candidate_matrix": frame_matrix,
        "model_config_candidate_matrix": model_matrix,
        "detection_schema_validation": schema_val,
        "trw_output_contract_validation": trw_val,
        "dry_run_10_frame_runbook": runbook,
    }
