# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-011 — OCR Stage-2 Controlled Provider Invocation v0.

Scope:
- Single frozen input image from Phase-010 approval root
- One controlled local OCR provider invocation (no network)
- Output raw_text candidate only + TRW (trace/replay/whitebox) + post-trial report

Hard boundaries:
- semantic_interpretation_enabled MUST be False
- MUST NOT enter MidPlatform / SceneDelta / WorldContextEvidence
- MUST NOT trigger navigation / TTS / Qwen / world write / hive upload
- MUST NOT open camera / video streams
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.guarded_trial.ocr_stage2_provider_approval_gate_v0 import compute_file_sha256_v0


PHASE = "Phase-Mainline-GuardedTrial-011"


@dataclass(frozen=True)
class ApprovalSnapshotV0:
    approval_root: str
    input_image_path: str
    input_sha256: Optional[str]
    input_size_bytes: int
    secret_values_logged: bool


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_ocr_stage2_approval_snapshot_v0(*, approval_root: str) -> ApprovalSnapshotV0:
    root = Path(approval_root).expanduser().resolve()
    snap_path = root / "ocr_stage2_input_sample_snapshot.json"
    cred_path = root / "ocr_stage2_provider_credentials_snapshot.json"
    if not snap_path.is_file():
        raise FileNotFoundError(f"missing_input_sample_snapshot:{snap_path}")
    s = _read_json(snap_path) if snap_path.is_file() else {}
    c = _read_json(cred_path) if cred_path.is_file() else {}
    p = str(s.get("path") or "")
    return ApprovalSnapshotV0(
        approval_root=str(root),
        input_image_path=p,
        input_sha256=s.get("sha256"),
        input_size_bytes=int(s.get("size_bytes") or 0),
        secret_values_logged=bool(c.get("secret_values_logged") is True),
    )


def validate_ocr_input_matches_approval_snapshot_v0(
    *,
    approval: ApprovalSnapshotV0,
    input_image: str,
) -> Dict[str, Any]:
    p_in = Path(input_image).expanduser().resolve()
    p_ap = Path(approval.input_image_path).expanduser().resolve()
    exists = p_in.is_file()
    sha = compute_file_sha256_v0(p_in) if exists else None
    size = int(p_in.stat().st_size) if exists else 0
    path_match = str(p_in) == str(p_ap)
    sha_match = (approval.input_sha256 is None) or (sha == approval.input_sha256)
    size_match = (approval.input_size_bytes == 0) or (size == approval.input_size_bytes)
    ok = bool(exists and path_match and sha_match and size_match)
    return {
        "approval_input_path": str(p_ap),
        "resolved_input_path": str(p_in),
        "exists": exists,
        "path_match": path_match,
        "sha256": sha,
        "sha256_match": sha_match,
        "size_bytes": size,
        "size_bytes_match": size_match,
        "input_snapshot_match": ok,
        "blockers": [] if ok else ["input_snapshot_mismatch_or_missing"],
    }


def select_ocr_stage2_controlled_provider_v0() -> Dict[str, Any]:
    """
    Prefer cross-platform local offline providers (mainline):
    1) RapidOCR ONNXRuntime (local)
    2) PaddleOCR (local)

    NOTE: macOS Vision / Tesseract are intentionally NOT selected in the mainline
    controlled trial path (dev-only or fallback elsewhere), to avoid binding the
    guarded trial to macOS/system providers.
    """
    candidates: List[Dict[str, Any]] = []

    # RapidOCR default adapter
    try:
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        a = RapidOCRAdapterV0()
        ok, err = a.is_available()
        candidates.append(
            {
                "provider_name": a.provider_id,
                "provider_type": "local_ocr",
                "available": bool(ok),
                "requires_network": False,
                "requires_credentials": False,
                "error": err,
                "adapter": a,
            }
        )
    except Exception as e:
        candidates.append(
            {
                "provider_name": "rapidocr_onnxruntime_v0",
                "provider_type": "local_ocr",
                "available": False,
                "requires_network": False,
                "requires_credentials": False,
                "error": repr(e),
                "adapter": None,
            }
        )

    try:
        from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

        a = PaddleOCRAdapterV0(enable_real_inference=True)
        rd = a.evaluate_readiness()
        ok = bool(rd.get("provider_available"))
        err = None if ok else ";".join([str(x) for x in (rd.get("hard_blockers") or [])])[:400] or "not_ready"
        candidates.append(
            {
                "provider_name": a.provider_id,
                "provider_type": "local_ocr",
                "available": bool(ok),
                "requires_network": False,
                "requires_credentials": False,
                "error": err,
                "adapter": a,
            }
        )
    except Exception as e:
        candidates.append(
            {
                "provider_name": "paddleocr_ppocrv5_lightweight_v0",
                "provider_type": "local_ocr",
                "available": False,
                "requires_network": False,
                "requires_credentials": False,
                "error": repr(e),
                "adapter": None,
            }
        )

    selected = next((c for c in candidates if c.get("available") and c.get("adapter") is not None), None)
    if selected is None:
        return {
            "provider_selected": "not_available",
            "provider_type": "mock_ocr",
            "provider_invoked": False,
            "ocr_model_invoked": False,
            "network_request_invoked": False,
            "fallback_used": True,
            "not_available": True,
            "provider_error": "no_local_provider_available",
            "candidates": [{k: v for k, v in c.items() if k != "adapter"} for c in candidates],
            "adapter": None,
        }

    return {
        "provider_selected": str(selected["provider_name"]),
        "provider_type": str(selected["provider_type"]),
        "provider_invoked": False,
        "ocr_model_invoked": False,
        "network_request_invoked": False,
        "fallback_used": False,
        "not_available": False,
        "provider_error": None,
        "candidates": [{k: v for k, v in c.items() if k != "adapter"} for c in candidates],
        "adapter": selected["adapter"],
    }


def invoke_ocr_provider_controlled_v0(
    *,
    adapter: Any,
    input_image_path: str,
    frame_id: str = "img_001",
) -> Dict[str, Any]:
    """
    Calls adapter.recognize_image once. This is the only allowed real provider invocation.
    """
    ts_ms = int(time.time() * 1000.0)
    out = adapter.recognize_image(image_path=input_image_path, frame_id=frame_id, timestamp_ms=ts_ms)
    return out if isinstance(out, dict) else {"hard_blockers": ["provider_return_not_dict"], "raw_text_joined": ""}


def _confidence_from_candidates(raw_candidates: Any) -> float:
    vals: List[float] = []
    if isinstance(raw_candidates, list):
        for c in raw_candidates:
            if not isinstance(c, dict):
                continue
            v = c.get("confidence")
            try:
                if v is not None:
                    vals.append(float(v))
            except Exception:
                continue
    if not vals:
        return 0.0
    return max(0.0, min(1.0, sum(vals) / float(len(vals))))


def build_ocr_raw_text_candidate_v0(
    *,
    approval: ApprovalSnapshotV0,
    source_image_ref: str,
    provider_name: str,
    provider_type: str,
    provider_payload: Dict[str, Any],
    not_available: bool,
    provider_error: Optional[str],
) -> Dict[str, Any]:
    raw_joined = str(provider_payload.get("raw_text_joined") or "")
    raw_candidates = provider_payload.get("raw_text_candidates")
    latency_ms = provider_payload.get("latency_ms")
    conf = _confidence_from_candidates(raw_candidates)

    err_state = None
    if not_available:
        err_state = "not_available"
    elif provider_error:
        err_state = str(provider_error)

    return {
        "candidate_id": f"ocr_raw_{uuid.uuid4().hex[:16]}",
        "source_image_ref": source_image_ref,
        "source_approval_ref": approval.approval_root,
        "provider_name": provider_name,
        "provider_type": provider_type,
        "raw_text": raw_joined if not err_state else "",
        "confidence": float(conf),
        "reading_order": [],
        "bbox_or_region": None,
        "provider_metadata": {
            "latency_ms": latency_ms,
            "provider_details": provider_payload.get("provider_details"),
            "ocr_runtime_mode": provider_payload.get("ocr_runtime_mode"),
            "provider_id": provider_payload.get("provider_id"),
            "model_config_id": provider_payload.get("model_config_id"),
        },
        "error_or_not_available_state": err_state,
        "allows_execute_now": False,
        "semantic_interpretation_enabled": False,
        "midplatform_forward_enabled": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "real_tts_invoked": False,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
    }


def validate_ocr_raw_text_candidate_v0(candidate: Dict[str, Any]) -> Dict[str, Any]:
    blockers: List[str] = []
    required = [
        "candidate_id",
        "source_image_ref",
        "source_approval_ref",
        "provider_name",
        "provider_type",
        "raw_text",
        "confidence",
        "allows_execute_now",
        "semantic_interpretation_enabled",
        "downstream_invocation_count",
    ]
    for k in required:
        if k not in candidate:
            blockers.append(f"missing:{k}")
    if candidate.get("semantic_interpretation_enabled") is not False:
        blockers.append("semantic_must_be_false")
    if candidate.get("downstream_invocation_count") != 0:
        blockers.append("downstream_must_be_zero")
    if candidate.get("allows_execute_now") is not False:
        blockers.append("allows_execute_now_must_be_false")
    ok = not blockers
    return {"schema_valid": ok, "blockers": blockers}


def build_ocr_stage2_provider_post_trial_report_v0(
    *,
    trial: Dict[str, Any],
    candidate_schema_valid: bool,
) -> Dict[str, Any]:
    details = trial.get("details") if isinstance(trial.get("details"), dict) else {}
    cand = details.get("raw_text_candidate") if isinstance(details.get("raw_text_candidate"), dict) else {}
    raw_txt = str(cand.get("raw_text") or "").strip()

    if trial.get("abort_triggered"):
        rec = "NO_GO_rollback_and_fix"
    elif trial.get("provider_invoked") and candidate_schema_valid and not trial.get("not_available"):
        # Empty OCR output is still schema-valid but not a full GO for Stage-2 trials.
        rec = "CONDITIONAL_GO_repeat" if not raw_txt else "GO_next_window"
    else:
        rec = "CONDITIONAL_GO_repeat"
    return {
        "phase": PHASE,
        "trial_id": trial.get("trial_id"),
        "post_trial_recommendation": rec,
        "notes": [
            "Phase-011 allows a single controlled local OCR provider invocation on the frozen input image only.",
            "No semantic interpretation; no MidPlatform/SceneDelta/WorldContext; raw_text only.",
        ],
    }


def run_ocr_stage2_controlled_provider_invocation_v0(
    *,
    approval_root: str,
    input_image_override: Optional[str] = None,
) -> Dict[str, Any]:
    trial_id = f"ocr_s2_trial_{uuid.uuid4().hex[:16]}"
    approval = load_ocr_stage2_approval_snapshot_v0(approval_root=approval_root)

    if approval.secret_values_logged:
        # hard stop
        return {
            "trial_id": trial_id,
            "capability": "ocr",
            "stage": "stage2_ocr_guarded_trial",
            "execution_mode": "controlled_provider_single_image",
            "approval_root": approval.approval_root,
            "input_image": approval.input_image_path,
            "input_snapshot_match": False,
            "provider_selected": "not_available",
            "provider_invoked": False,
            "ocr_model_invoked": False,
            "network_request_invoked": False,
            "fallback_used": True,
            "not_available": True,
            "raw_text_candidate_generated": False,
            "raw_text_candidate_schema_valid": False,
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "abort_triggered": True,
            "abort_reason": "secret_values_logged_true",
            "hard_audit": {
                "ocr_provider_invoked": False,
                "ocr_model_invoked": False,
                "network_request_invoked": False,
                "semantic_interpretation_enabled": False,
                "midplatform_invoked": False,
                "scene_delta_invoked": False,
                "world_context_invoked": False,
                "qwen_invoked": False,
                "real_tts_invoked": False,
                "playback_invoked": False,
                "downstream_invocation_count": 0,
                "navigation_action": None,
                "world_write_invoked": False,
                "hive_upload_invoked": False,
            },
            "details": {"blockers": ["secret_values_logged_true_abort"]},
        }

    input_image = input_image_override or approval.input_image_path
    match = validate_ocr_input_matches_approval_snapshot_v0(approval=approval, input_image=input_image)
    if not match.get("input_snapshot_match"):
        return {
            "trial_id": trial_id,
            "capability": "ocr",
            "stage": "stage2_ocr_guarded_trial",
            "execution_mode": "controlled_provider_single_image",
            "approval_root": approval.approval_root,
            "input_image": str(Path(input_image).expanduser().resolve()),
            "input_snapshot_match": False,
            "provider_selected": "not_available",
            "provider_invoked": False,
            "ocr_model_invoked": False,
            "network_request_invoked": False,
            "fallback_used": True,
            "not_available": True,
            "raw_text_candidate_generated": False,
            "raw_text_candidate_schema_valid": False,
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "abort_triggered": True,
            "abort_reason": "input_snapshot_mismatch",
            "hard_audit": {
                "ocr_provider_invoked": False,
                "ocr_model_invoked": False,
                "network_request_invoked": False,
                "semantic_interpretation_enabled": False,
                "midplatform_invoked": False,
                "scene_delta_invoked": False,
                "world_context_invoked": False,
                "qwen_invoked": False,
                "real_tts_invoked": False,
                "playback_invoked": False,
                "downstream_invocation_count": 0,
                "navigation_action": None,
                "world_write_invoked": False,
                "hive_upload_invoked": False,
            },
            "details": {"input_snapshot_match": match},
        }

    sel = select_ocr_stage2_controlled_provider_v0()
    adapter = sel.get("adapter")
    provider_selected = str(sel.get("provider_selected"))
    provider_type = str(sel.get("provider_type"))

    provider_invoked = False
    ocr_model_invoked = False
    fallback_used = bool(sel.get("fallback_used"))
    not_available = bool(sel.get("not_available"))
    provider_error = sel.get("provider_error")
    payload: Dict[str, Any] = {}

    if adapter is not None and not not_available:
        try:
            provider_invoked = True
            payload = invoke_ocr_provider_controlled_v0(adapter=adapter, input_image_path=match["resolved_input_path"])
            # Adapter semantics: if provider returns hard_blockers it may still have invoked model; treat as invoked when adapter called.
            ocr_model_invoked = True
            hb = payload.get("hard_blockers") if isinstance(payload.get("hard_blockers"), list) else []
            if hb:
                fallback_used = True
                not_available = True
                provider_error = ";".join([str(x) for x in hb])[:400]
        except Exception as e:
            provider_invoked = True
            ocr_model_invoked = True
            fallback_used = True
            not_available = True
            provider_error = f"provider_exception:{e!r}"
            payload = {"raw_text_joined": "", "raw_text_candidates": [], "hard_blockers": ["exception"]}

    candidate = build_ocr_raw_text_candidate_v0(
        approval=approval,
        source_image_ref=match["resolved_input_path"],
        provider_name=provider_selected,
        provider_type=provider_type,
        provider_payload=payload,
        not_available=not_available,
        provider_error=provider_error if not_available else None,
    )
    cand_val = validate_ocr_raw_text_candidate_v0(candidate)

    trial = {
        "trial_id": trial_id,
        "capability": "ocr",
        "stage": "stage2_ocr_guarded_trial",
        "execution_mode": "controlled_provider_single_image",
        "phase": PHASE,
        "approval_root": approval.approval_root,
        "input_image": match["resolved_input_path"],
        "input_snapshot_match": True,
        "provider_selected": provider_selected,
        "provider_type": provider_type,
        "provider_invoked": provider_invoked,
        "ocr_model_invoked": ocr_model_invoked,
        "network_request_invoked": False,
        "fallback_used": fallback_used,
        "not_available": not_available,
        "provider_error": provider_error,
        "raw_text_candidate_generated": True,
        "raw_text_candidate_schema_valid": bool(cand_val.get("schema_valid")),
        "semantic_interpretation_enabled": False,
        "midplatform_invoked": False,
        "scene_delta_invoked": False,
        "world_context_invoked": False,
        "abort_triggered": False,
        "abort_reason": None,
        "hard_audit": {
            "ocr_provider_invoked": provider_invoked,
            "ocr_model_invoked": ocr_model_invoked,
            "network_request_invoked": False,
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "qwen_invoked": False,
            "real_tts_invoked": False,
            "playback_invoked": False,
            "downstream_invocation_count": 0,
            "navigation_action": None,
            "world_write_invoked": False,
            "hive_upload_invoked": False,
        },
        "details": {
            "input_snapshot_match": match,
            "provider_selection": {k: v for k, v in sel.items() if k != "adapter"},
            "provider_payload": payload,
            "raw_text_candidate": candidate,
            "raw_text_candidate_validation": cand_val,
        },
    }
    post = build_ocr_stage2_provider_post_trial_report_v0(trial=trial, candidate_schema_valid=bool(cand_val.get("schema_valid")))
    trial["post_trial_report"] = post
    return trial

