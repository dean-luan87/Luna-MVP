# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-004 — Dependency / weight / runbook freeze for YOLO Stage-1 approval gate.

No detector execution, no model inference, no camera, no video stream decode.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE = "Phase-Mainline-GuardedTrial-004"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def compute_file_sha256_v0(path: Path) -> Tuple[str, int]:
    """Read file in chunks; returns (hex sha256, size_bytes)."""
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def check_python_import_available_v0(module_name: str) -> Dict[str, Any]:
    """Import-only check; does not run detector or load weights."""
    out: Dict[str, Any] = {"name": module_name, "import_available": False, "version": None, "error": None}
    try:
        m = importlib.import_module(module_name)
        out["import_available"] = True
        ver = getattr(m, "__version__", None)
        if ver is None and hasattr(m, "version"):
            ver = getattr(m.version, "__version__", None)
        out["version"] = str(ver) if ver is not None else None
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}:{e}"
    return out


def _import_shadow_adapter_module_v0() -> Dict[str, Any]:
    try:
        importlib.import_module("capabilities.model_perception.yolo_shadow_adapter_v0")
        return {"importable": True, "module": "capabilities.model_perception.yolo_shadow_adapter_v0", "error": None}
    except Exception as e:  # noqa: BLE001
        return {"importable": False, "module": None, "error": f"{type(e).__name__}:{e}"}


def _import_luna_badge_detector_v0() -> Dict[str, Any]:
    try:
        importlib.import_module("Luna_Badge_MVP.vision.yolov5_detector")
        return {"importable": True, "module": "Luna_Badge_MVP.vision.yolov5_detector", "error": None}
    except Exception as e:  # noqa: BLE001
        return {"importable": False, "module": None, "error": f"{type(e).__name__}:{e}"}


def validate_yolo_weight_snapshot_v0(*, repo_root: Path) -> Dict[str, Any]:
    manifest = repo_root / "configs/models/yolo/yolo_model_manifest_v0.json"
    out: Dict[str, Any] = {
        "path": "",
        "exists": False,
        "sha256": None,
        "size_bytes": 0,
        "manifest_sha256_expected": None,
        "sha256_matches_manifest": None,
    }
    if not manifest.is_file():
        return out
    try:
        m = json.loads(manifest.read_text(encoding="utf-8"))
        rel = str(m.get("weights_path") or "")
        out["manifest_sha256_expected"] = m.get("weights_sha256")
        if not rel:
            return out
        wp = (repo_root / rel).resolve()
        out["path"] = rel
        if not wp.is_file():
            return out
        out["exists"] = True
        sha, sz = compute_file_sha256_v0(wp)
        out["sha256"] = sha
        out["size_bytes"] = sz
        exp = out["manifest_sha256_expected"]
        if isinstance(exp, str) and len(exp) == 64:
            out["sha256_matches_manifest"] = exp.lower() == sha.lower()
        else:
            out["sha256_matches_manifest"] = None
    except Exception as e:  # noqa: BLE001
        out["error"] = str(e)
    return out


def validate_yolo_dependency_snapshot_v0() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for mod in ("numpy", "cv2", "torch"):
        r = check_python_import_available_v0(mod)
        r["required_for_phase"] = "next_phase_005_dry_run"
        rows.append(r)
    ultra = check_python_import_available_v0("ultralytics")
    ultra["required_for_phase"] = "optional_torch_hub_path"
    rows.append(ultra)
    return rows


def _is_camera_index_path(p: str) -> bool:
    s = (p or "").strip()
    if not s:
        return False
    return s.isdigit() and len(s) <= 2


def validate_yolo_input_source_snapshot_v0(*, input_video_path: Optional[str]) -> Dict[str, Any]:
    """
    Validates file existence only; never opens VideoCapture.
    Camera index paths (e.g. '0') => not allowed as 10-frame default.
    """
    out: Dict[str, Any] = {
        "source_type": "unknown",
        "path": "",
        "exists": False,
        "will_open_stream": False,
        "camera_like_path": False,
        "approval_note": "",
    }
    if not input_video_path or not str(input_video_path).strip():
        out["approval_note"] = "no_input_video_path_supplied_human_specification_required"
        return out

    raw = str(input_video_path).strip()
    out["path"] = raw

    if _is_camera_index_path(raw) or raw.lower() in {"camera", "webcam"}:
        out["source_type"] = "camera"
        out["camera_like_path"] = True
        out["approval_note"] = "camera_index_or_camera_alias_forbidden_for_default_10_frame_gate"
        return out

    p = Path(raw)
    if not p.is_file():
        out["source_type"] = "video_file"
        out["exists"] = False
        out["approval_note"] = "path_not_found"
        return out

    # Heuristic: treat as video_file for offline trial
    out["source_type"] = "video_file"
    out["exists"] = True
    out["approval_note"] = "offline_video_file_candidate_ok"
    return out


def validate_yolo_10_frame_runbook_snapshot_v0(runbook_path: Path) -> Dict[str, Any]:
    if not runbook_path.is_file():
        return {"exists": False, "valid": False, "error": "runbook_missing"}
    try:
        data = json.loads(runbook_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"exists": True, "valid": False, "error": str(e)}
    need = {"runbook_id", "window", "execution_allowed_by_this_phase", "required_flags", "rollback_commands"}
    missing = sorted(need - set(data.keys()))
    return {
        "exists": True,
        "valid": len(missing) == 0 and data.get("window") == "10_frames",
        "missing_fields": missing,
        "frozen_runbook": data,
    }


def build_yolo_stage1_abort_rollback_snapshot_v0(*, frozen_runbook: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    rb = frozen_runbook or {}
    cmds = rb.get("rollback_commands") if isinstance(rb, dict) else None
    abort = rb.get("abort_conditions") if isinstance(rb, dict) else None
    pre = rb.get("pre_run_checks") if isinstance(rb, dict) else None
    return {
        "rollback_commands": list(cmds) if isinstance(cmds, list) else [],
        "abort_conditions": list(abort) if isinstance(abort, list) else [],
        "pre_run_checks": list(pre) if isinstance(pre, list) else [],
        "source": "frozen_10_frame_runbook_v0",
    }


def build_yolo_stage1_env_flag_snapshot_v0(*, frozen_runbook: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    rb = frozen_runbook or {}
    req = rb.get("required_flags") if isinstance(rb, dict) else {}
    return {
        "env_flags_for_next_phase": dict(req) if isinstance(req, dict) else {},
        "freeze_policy": "values_documented_for_005_only_not_applied_by_this_tool",
    }


def build_yolo_stage1_approval_gate_v0(
    *,
    weight_snap: Dict[str, Any],
    dep_snap: List[Dict[str, Any]],
    shadow_import: Dict[str, Any],
    backend_import: Dict[str, Any],
    input_snap: Dict[str, Any],
    runbook_snap: Dict[str, Any],
    abort_snap: Dict[str, Any],
    env_snap: Dict[str, Any],
) -> Dict[str, Any]:
    blockers: List[str] = []
    warnings: List[str] = []

    if not weight_snap.get("exists"):
        blockers.append("weights_file_missing")
    elif not weight_snap.get("sha256"):
        blockers.append("weights_sha256_failed")

    if not shadow_import.get("importable"):
        blockers.append("shadow_adapter_entrypoint_not_importable")

    if input_snap.get("source_type") == "camera" or input_snap.get("camera_like_path"):
        blockers.append("camera_only_or_camera_index_input_forbidden")

    if not input_snap.get("exists") and input_snap.get("source_type") == "video_file":
        blockers.append("input_video_path_missing_or_not_a_file")

    if not input_snap.get("path"):
        warnings.append("input_source_requires_human_path_for_full_GO")

    if not runbook_snap.get("valid"):
        blockers.append("runbook_invalid_or_incomplete")

    if not isinstance(abort_snap.get("rollback_commands"), list) or len(abort_snap.get("rollback_commands") or []) == 0:
        blockers.append("rollback_commands_missing")

    if not isinstance(abort_snap.get("abort_conditions"), list) or len(abort_snap.get("abort_conditions") or []) == 0:
        blockers.append("abort_conditions_missing")

    env_flags = env_snap.get("env_flags_for_next_phase") or {}
    for k in ("LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1", "LUNA_YOLO_TRIAL_MODE", "LUNA_YOLO_TRIAL_MAX_FRAMES"):
        if k not in env_flags:
            blockers.append(f"env_flag_missing_in_runbook:{k}")

    if not backend_import.get("importable"):
        warnings.append("luna_badge_yolov5_detector_import_failed_next_phase_may_fail")

    core_deps = [d for d in dep_snap if d.get("name") in {"numpy", "cv2", "torch"}]
    for d in core_deps:
        if not d.get("import_available"):
            warnings.append(f"dependency_missing:{d.get('name')}")

    if weight_snap.get("sha256_matches_manifest") is False:
        warnings.append("weights_sha256_mismatch_vs_manifest")

    verdict = "NO_GO"
    if not blockers:
        if warnings:
            verdict = "CONDITIONAL_GO"
        else:
            verdict = "GO"
    else:
        verdict = "NO_GO"

    return {
        "approval_gate_result": verdict,
        "blockers": blockers,
        "warnings": warnings,
    }


def run_yolo_stage1_dependency_snapshot_v0(
    *,
    repo_root: Path,
    static_config_root: Path,
    input_video_path: Optional[str] = None,
) -> Dict[str, Any]:
    snapshot_id = f"yolo_s1_snap_{uuid.uuid4().hex[:14]}"

    weight_snap = validate_yolo_weight_snapshot_v0(repo_root=repo_root)
    dep_snap = validate_yolo_dependency_snapshot_v0()
    shadow = _import_shadow_adapter_module_v0()
    backend = _import_luna_badge_detector_v0()
    input_snap = validate_yolo_input_source_snapshot_v0(input_video_path=input_video_path)

    runbook_path = static_config_root / "yolo_stage1_10_frame_dry_run_runbook.json"
    runbook_snap = validate_yolo_10_frame_runbook_snapshot_v0(runbook_path)
    frozen = runbook_snap.get("frozen_runbook") if isinstance(runbook_snap.get("frozen_runbook"), dict) else {}

    abort_snap = build_yolo_stage1_abort_rollback_snapshot_v0(frozen_runbook=frozen)
    env_snap = build_yolo_stage1_env_flag_snapshot_v0(frozen_runbook=frozen)

    gate = build_yolo_stage1_approval_gate_v0(
        weight_snap=weight_snap,
        dep_snap=dep_snap,
        shadow_import=shadow,
        backend_import=backend,
        input_snap=input_snap,
        runbook_snap=runbook_snap,
        abort_snap=abort_snap,
        env_snap=env_snap,
    )

    hard_audit = {
        "detector_invoked": False,
        "model_inference_invoked": False,
        "camera_invoked": False,
        "video_stream_opened": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
    }

    detector_entry = {
        "file": "capabilities/model_perception/yolo_shadow_adapter_v0.py",
        "function_or_class": "run_yolo_shadow_adapter_on_sample_v0",
        "shadow_adapter_module_importable": bool(shadow.get("importable")),
        "detector_backend_module": "Luna_Badge_MVP.vision.yolov5_detector",
        "detector_backend_importable": bool(backend.get("importable")),
        "importable": bool(shadow.get("importable")),
        "will_execute": False,
    }

    return {
        "snapshot_id": snapshot_id,
        "capability": "yolo",
        "stage": "stage1_yolo_guarded_trial",
        "snapshot_mode": "pre_execution_approval_gate",
        "phase": PHASE,
        "real_yolo_execution_allowed_by_this_phase": False,
        "ten_frame_dry_run_allowed_by_this_phase": False,
        "yolo_stage1_trial_preparation_status": "ready_for_10_frame_dry_run_review",
        "real_yolo_execution": "NO_GO",
        "ten_frame_dry_run_execution": "NO_GO",
        "weights": {
            "path": weight_snap.get("path", ""),
            "exists": bool(weight_snap.get("exists")),
            "sha256": weight_snap.get("sha256"),
            "size_bytes": int(weight_snap.get("size_bytes") or 0),
            "sha256_matches_manifest": weight_snap.get("sha256_matches_manifest"),
        },
        "dependencies": dep_snap,
        "detector_entrypoint": detector_entry,
        "input_source": {
            "source_type": input_snap.get("source_type"),
            "path": input_snap.get("path", ""),
            "exists": bool(input_snap.get("exists")),
            "will_open_stream": False,
            "camera_like_path": bool(input_snap.get("camera_like_path")),
            "approval_note": input_snap.get("approval_note"),
        },
        "env_flags_for_next_phase": env_snap.get("env_flags_for_next_phase", {}),
        "output_root_naming_rule_next_phase": "logs/yolo_stage1_10_frame_dry_run_execution_005_<UTC>",
        "abort_rollback_snapshot": abort_snap,
        "runbook_snapshot": runbook_snap,
        "approval_gate_result": gate["approval_gate_result"],
        "blockers": gate["blockers"],
        "warnings": gate["warnings"],
        "hard_audit": hard_audit,
        "static_config_root": str(static_config_root.resolve()),
    }
