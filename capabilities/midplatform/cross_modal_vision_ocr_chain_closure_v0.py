# -*- coding: utf-8 -*-
"""CrossModal Vision→OCR→Scene Delta evaluation chain closure (archive only).

Phase-CrossModal-Vision-OCR-Evaluation-Chain-Closure-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SUMMARY_SCHEMA = "cross_modal_vision_ocr_chain_closure_summary_v0"
PHASE_MATRIX_SCHEMA = "cross_modal_vision_ocr_phase_matrix_v0"
LINEAGE_MATRIX_SCHEMA = "cross_modal_vision_ocr_lineage_matrix_v0"
NO_WRITE_SCHEMA = "cross_modal_vision_ocr_no_write_boundary_matrix_v0"
CAPABILITY_SCHEMA = "cross_modal_vision_ocr_capability_closure_report_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "cross_modal_vision_ocr_open_followups_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_chain_closure_audit_v0"

DEFAULT_CHAIN_ROOTS: Dict[str, str] = {
    "Vision-ROI-to-OCR-Request-Bridge": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0",
    "OCR-Request-Submission-Gated-Smoke": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_request_submission_from_vision_roi_smoke_v0",
    "Vision-OCR-Evidence-ReadOnly-Consumer": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_triggered_ocr_evidence_readonly_consumer_smoke_v0",
    "RapidOCR-Submission-From-Vision-ROI": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/rapidocr_submission_from_vision_roi_smoke_v0",
    "RapidOCR-ReadOnly-Consumer": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_triggered_rapidocr_evidence_readonly_consumer_smoke_v0",
    "CrossModal-RapidOCR-Reference-Only": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_reference_only_rapidocr_smoke_v0",
    "Text-Bearing-OCR-Sample": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_roi_text_bearing_ocr_sample_smoke_v0",
    "Fusion-Candidate-DryRun": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0",
    "Review-Queue": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_fusion_review_queue_smoke_v0",
    "AI-Interpretation-DryRun": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_ai_interpretation_dryrun_smoke_v0",
    "Scene-Delta-Candidate-DryRun": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_scene_delta_candidate_dryrun_smoke_v0",
    "Gate-Evaluator-DryRun": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_scene_delta_gate_evaluator_dryrun_smoke_v0",
    "Executor-Trace-Stub": "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_scene_delta_executor_trace_stub_smoke_v0",
}

PHASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_key": "Vision-ROI-to-OCR-Request-Bridge",
        "phase_id": "Phase-Vision-ROI-to-OCR-Request-Bridge-001",
        "verifier_file": "vision_roi_to_ocr_request_bridge_verifier_report.json",
        "audit_file": "vision_roi_to_ocr_request_bridge_audit_report.json",
        "boundary": "Vision ROI → OCRRequest candidate; no OCR provider invoke.",
        "critical": True,
    },
    {
        "phase_key": "OCR-Request-Submission-Gated-Smoke",
        "phase_id": "Phase-OCR-Request-Submission-Gated-Smoke-001",
        "verifier_file": "ocr_request_submission_from_vision_roi_verifier_report.json",
        "audit_file": "ocr_request_submission_from_vision_roi_audit_report.json",
        "boundary": "Stub OCR via mainline bridge; evaluation-only.",
        "critical": False,
    },
    {
        "phase_key": "Vision-OCR-Evidence-ReadOnly-Consumer",
        "phase_id": "Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001",
        "verifier_file": "vision_triggered_ocr_evidence_readonly_consumer_verifier_report.json",
        "audit_file": "vision_triggered_ocr_evidence_readonly_consumer_audit_report.json",
        "boundary": "Read-only stub submission consumer.",
        "critical": False,
    },
    {
        "phase_key": "RapidOCR-Submission-From-Vision-ROI",
        "phase_id": "Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001",
        "verifier_file": "rapidocr_submission_from_vision_roi_verifier_report.json",
        "audit_file": "rapidocr_submission_from_vision_roi_audit_report.json",
        "boundary": "RapidOCR via bridge on video ROI; empty text valid.",
        "critical": True,
    },
    {
        "phase_key": "RapidOCR-ReadOnly-Consumer",
        "phase_id": "Phase-Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001",
        "verifier_file": "vision_triggered_rapidocr_evidence_readonly_consumer_verifier_report.json",
        "audit_file": "vision_triggered_rapidocr_evidence_readonly_consumer_audit_report.json",
        "boundary": "Read-only RapidOCR submission consumer.",
        "critical": True,
    },
    {
        "phase_key": "CrossModal-RapidOCR-Reference-Only",
        "phase_id": "Phase-CrossModal-Vision-OCR-Reference-Only-002",
        "verifier_file": "cross_modal_vision_ocr_reference_only_rapidocr_verifier_report.json",
        "audit_file": "cross_modal_vision_ocr_reference_only_rapidocr_audit_report.json",
        "boundary": "Reference-only alignment; not fusion.",
        "critical": True,
    },
    {
        "phase_key": "Text-Bearing-OCR-Sample",
        "phase_id": "Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001",
        "verifier_file": "vision_roi_text_bearing_ocr_sample_verifier_report.json",
        "audit_file": "vision_roi_text_bearing_ocr_sample_audit_report.json",
        "boundary": "Local text-bearing ROI; non-empty RapidOCR via bridge.",
        "critical": True,
    },
    {
        "phase_key": "Fusion-Candidate-DryRun",
        "phase_id": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001",
        "verifier_file": "cross_modal_vision_ocr_fusion_dryrun_verifier_report.json",
        "audit_file": "cross_modal_vision_ocr_fusion_dryrun_audit_report.json",
        "boundary": "Fusion candidate dry-run; not fact.",
        "critical": True,
    },
    {
        "phase_key": "Review-Queue",
        "phase_id": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001",
        "verifier_file": "cross_modal_fusion_review_queue_verifier_report.json",
        "audit_file": "cross_modal_fusion_review_queue_audit_report.json",
        "boundary": "pending_review queue; no auto-approve.",
        "critical": True,
    },
    {
        "phase_key": "AI-Interpretation-DryRun",
        "phase_id": "Phase-CrossModal-Vision-OCR-AI-Interpretation-DryRun-001",
        "verifier_file": "cross_modal_ai_interpretation_dryrun_verifier_report.json",
        "audit_file": "cross_modal_ai_interpretation_dryrun_audit_report.json",
        "boundary": "template_stub interpretation; no external LLM.",
        "critical": True,
    },
    {
        "phase_key": "Scene-Delta-Candidate-DryRun",
        "phase_id": "Phase-CrossModal-Vision-OCR-Scene-Delta-Candidate-DryRun-001",
        "verifier_file": "cross_modal_scene_delta_dryrun_verifier_report.json",
        "audit_file": "cross_modal_scene_delta_dryrun_audit_report.json",
        "boundary": "Scene Delta candidate only; gate not evaluated.",
        "critical": True,
    },
    {
        "phase_key": "Gate-Evaluator-DryRun",
        "phase_id": "Phase-CrossModal-Vision-OCR-Scene-Delta-Gate-Evaluator-DryRun-001",
        "verifier_file": "cross_modal_scene_delta_gate_evaluator_verifier_report.json",
        "audit_file": "cross_modal_scene_delta_gate_evaluator_audit_report.json",
        "boundary": "hold_for_review; write_allowed=false.",
        "critical": True,
    },
    {
        "phase_key": "Executor-Trace-Stub",
        "phase_id": "Phase-CrossModal-Vision-OCR-Scene-Delta-Executor-Trace-Stub-001",
        "verifier_file": "cross_modal_scene_delta_executor_trace_stub_verifier_report.json",
        "audit_file": "cross_modal_scene_delta_executor_trace_stub_audit_report.json",
        "boundary": "blocked_by_gate trace; no real executor.",
        "critical": True,
    },
)

NO_WRITE_CHECK_KEYS = (
    "midplatform_fact_written",
    "scene_delta_written",
    "world_model_written",
    "navigation_decision_invoked",
    "database_write_invoked",
    "wal_append_invoked",
    "ai_interpretation_committed",
    "auto_approve_invoked",
    "approval_granted",
    "cross_modal_fusion_committed",
    "scene_delta_executor_invoked",
    "real_scene_delta_executor_invoked",
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _safe_read(p: Path) -> Optional[Any]:
    if not p.is_file():
        return None
    try:
        return _read_json(p)
    except Exception:
        return None


def _verdict_from_root(root: Path, verifier_file: str) -> Tuple[Optional[str], List[str]]:
    vp = root / verifier_file
    if not vp.is_file():
        return None, [f"missing_verifier:{verifier_file}"]
    rep = _safe_read(vp)
    if not isinstance(rep, dict):
        return None, ["verifier_invalid"]
    blockers = list(rep.get("blockers") or []) if isinstance(rep.get("blockers"), list) else []
    return str(rep.get("verdict") or ""), blockers


def build_phase_matrix_v0(roots: Dict[str, Path]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for spec in PHASE_SPECS:
        key = spec["phase_key"]
        root = roots.get(key)
        if root is None:
            rows.append(
                {
                    "phase_name": key,
                    "phase_id": spec["phase_id"],
                    "input_root": None,
                    "verifier_verdict": None,
                    "blockers": ["missing_root"],
                    "status": "missing",
                    "boundary": spec["boundary"],
                }
            )
            continue
        verdict, blockers = _verdict_from_root(root, str(spec["verifier_file"]))
        if verdict in ("GO", "CONDITIONAL_GO") and not blockers:
            status = "ok"
        elif verdict in ("GO", "CONDITIONAL_GO"):
            status = "ok_with_notes"
        else:
            status = "check_required"
        rows.append(
            {
                "phase_name": key,
                "phase_id": spec["phase_id"],
                "input_root": str(root.resolve()),
                "verifier_verdict": verdict,
                "blockers": blockers,
                "status": status,
                "boundary": spec["boundary"],
                "critical": spec.get("critical", False),
            }
        )
    return {"schema_version": PHASE_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def _first_item(items: Any) -> Optional[Dict[str, Any]]:
    if isinstance(items, list) and items and isinstance(items[0], dict):
        return items[0]
    return None


def build_lineage_matrix_v0(roots: Dict[str, Path]) -> Dict[str, Any]:
    tb = roots.get("Text-Bearing-OCR-Sample")
    fusion = roots.get("Fusion-Candidate-DryRun")
    queue = roots.get("Review-Queue")
    ai = roots.get("AI-Interpretation-DryRun")
    sd = roots.get("Scene-Delta-Candidate-DryRun")
    gate = roots.get("Gate-Evaluator-DryRun")
    trace = roots.get("Executor-Trace-Stub")
    bridge = roots.get("Vision-ROI-to-OCR-Request-Bridge")

    lineage: Dict[str, Any] = {
        "chain": "text_bearing_primary",
        "frame_id": None,
        "roi_id": None,
        "roi_type": "upper_sign_roi",
        "ocr_request_candidate_id": None,
        "ocr_request_id": None,
        "ocr_provider": "rapidocr_candidate",
        "rapidocr_provider_status": "invoked_non_empty_text",
        "text_joined": None,
        "fusion_candidate_id": None,
        "queue_item_id": None,
        "interpretation_id": None,
        "scene_delta_candidate_id": None,
        "gate_eval_id": None,
        "executor_trace_id": None,
        "final_execution_status": "blocked_by_gate",
        "final_fact_status": "not_fact",
    }

    if tb and tb.is_dir():
        ref = _safe_read(tb / "vision_roi_text_bearing_cross_modal_reference_candidate.json")
        sub = _safe_read(tb / "vision_roi_text_bearing_rapidocr_submission_result.json")
        cand = _safe_read(tb / "vision_roi_text_bearing_ocr_request_candidate.json")
        if isinstance(ref, dict):
            lineage["frame_id"] = ref.get("frame_id")
            lineage["roi_id"] = ref.get("roi_id")
            ocr_refs = ref.get("ocr_refs") if isinstance(ref.get("ocr_refs"), dict) else {}
            lineage["text_joined"] = ocr_refs.get("ocr_text_joined")
            lineage["ocr_request_id"] = ocr_refs.get("ocr_request_id")
        if isinstance(cand, dict):
            lineage["ocr_request_candidate_id"] = cand.get("candidate_id")
            ocr_req = cand.get("ocr_request") if isinstance(cand.get("ocr_request"), dict) else {}
            if not lineage["ocr_request_id"]:
                lineage["ocr_request_id"] = ocr_req.get("request_id")
        if isinstance(sub, dict):
            if not lineage["text_joined"]:
                lineage["text_joined"] = sub.get("text_joined") or sub.get("evidence_text_joined")

    if fusion and fusion.is_dir():
        doc = _safe_read(fusion / "cross_modal_vision_ocr_fusion_candidates.json")
        fc = _first_item(doc.get("candidates") if isinstance(doc, dict) else None)
        if fc:
            lineage["fusion_candidate_id"] = fc.get("candidate_id")

    if queue and queue.is_dir():
        doc = _safe_read(queue / "cross_modal_fusion_review_queue_candidates.json")
        qi = _first_item(doc.get("items") if isinstance(doc, dict) else None)
        if qi:
            lineage["queue_item_id"] = qi.get("queue_item_id")

    if ai and ai.is_dir():
        doc = _safe_read(ai / "cross_modal_ai_interpretation_candidates.json")
        interp = _first_item(doc.get("interpretations") if isinstance(doc, dict) else None)
        if interp:
            lineage["interpretation_id"] = interp.get("interpretation_id")

    if sd and sd.is_dir():
        doc = _safe_read(sd / "cross_modal_scene_delta_candidates.json")
        sc = _first_item(doc.get("candidates") if isinstance(doc, dict) else None)
        if sc:
            lineage["scene_delta_candidate_id"] = sc.get("candidate_id")

    if gate and gate.is_dir():
        doc = _safe_read(gate / "cross_modal_scene_delta_gate_evaluation_result.json")
        gr = _first_item(doc.get("results") if isinstance(doc, dict) else None)
        if gr:
            lineage["gate_eval_id"] = gr.get("gate_eval_id")

    if trace and trace.is_dir():
        doc = _safe_read(trace / "cross_modal_scene_delta_executor_trace_stub.json")
        tr = _first_item(doc.get("traces") if isinstance(doc, dict) else None)
        if tr:
            lineage["executor_trace_id"] = tr.get("trace_id")
            lineage["final_execution_status"] = tr.get("execution_status") or lineage["final_execution_status"]

    video_note = {
        "chain": "video_roi_stub_path",
        "rapidocr_provider_status": "invoked_empty_text_x10",
        "text_joined": "",
        "reference_only_root": str(roots["CrossModal-RapidOCR-Reference-Only"].resolve())
        if roots.get("CrossModal-RapidOCR-Reference-Only")
        else None,
        "bridge_root": str(bridge.resolve()) if bridge else None,
    }

    return {
        "schema_version": LINEAGE_MATRIX_SCHEMA,
        "primary_lineage": lineage,
        "supplemental_paths": [video_note],
    }


def build_no_write_boundary_matrix_v0(roots: Dict[str, Path]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    all_ok = True
    for spec in PHASE_SPECS:
        key = spec["phase_key"]
        root = roots.get(key)
        row: Dict[str, Any] = {"phase_name": key, "phase_id": spec["phase_id"]}
        if root is None or not root.is_dir():
            row["audit_present"] = False
            row["boundary_ok"] = False
            all_ok = False
            rows.append(row)
            continue
        aud = _safe_read(root / str(spec["audit_file"]))
        row["audit_present"] = isinstance(aud, dict)
        row["input_root"] = str(root.resolve())
        boundary_ok = isinstance(aud, dict)
        if isinstance(aud, dict):
            for bk in NO_WRITE_CHECK_KEYS:
                if bk in aud:
                    val = aud.get(bk)
                    row[bk] = val
                    if val is not False:
                        boundary_ok = False
        else:
            boundary_ok = False
        row["boundary_ok"] = boundary_ok
        if not boundary_ok:
            all_ok = False
        rows.append(row)
    return {
        "schema_version": NO_WRITE_SCHEMA,
        "all_phases_boundary_ok": all_ok,
        "rows": rows,
    }


def build_capability_closure_report_v0(lineage: Dict[str, Any]) -> Dict[str, Any]:
    primary = lineage.get("primary_lineage") if isinstance(lineage.get("primary_lineage"), dict) else {}
    return {
        "schema_version": CAPABILITY_SCHEMA,
        "proven_capabilities": [
            "vision_roi_generates_ocr_request_candidate",
            "ocr_request_submittable_via_mainline_bridge_stub",
            "vision_triggered_ocr_evidence_readonly_consumer_stub",
            "rapidocr_gated_submission_from_vision_roi",
            "rapidocr_readonly_consumer_with_empty_text_valid",
            "cross_modal_vision_ocr_reference_only_rapidocr",
            "text_bearing_roi_produces_non_empty_rapidocr_evidence",
            "fusion_candidate_dry_run_generatable",
            "review_queue_accepts_fusion_candidate_pending_review",
            "ai_interpretation_dryrun_template_stub",
            "scene_delta_candidate_dry_run_generatable",
            "gate_evaluator_hold_for_review",
            "executor_trace_stub_blocked_by_gate",
            "no_write_throughout_evaluation_chain",
            "fact_status_not_fact_throughout",
        ],
        "lineage_snapshot": primary,
    }


def build_non_claims_report_v0() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_cross_modal_fused_fact": True,
        "not_ai_interpretation_approved": True,
        "no_scene_delta_write": True,
        "no_world_model_write": True,
        "not_navigation_ready": True,
        "not_production_executor": True,
        "not_real_scene_quality_eval": True,
        "not_performance_eval": True,
        "not_multi_video_long_run": True,
        "not_auto_approve": True,
        "claims": [
            "Does NOT claim CrossModal fusion is confirmed fact.",
            "Does NOT claim AI interpretation was approved.",
            "Does NOT claim Scene Delta may be written.",
            "Does NOT claim WorldModel may be written.",
            "Does NOT claim outputs may drive navigation.",
            "Does NOT claim production Scene Delta executor was invoked.",
            "Does NOT claim real-scene OCR/vision quality was fully evaluated.",
            "Does NOT claim performance or long-run stability was evaluated.",
            "Does NOT claim multi-video / long-run testing is complete.",
            "Does NOT claim auto-approval is enabled.",
        ],
    }


def build_open_followups_v0() -> Dict[str, Any]:
    return {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": [
            {"id": "cross_modal_fusion_policy_gate", "title": "CrossModal fusion policy gate real rules"},
            {"id": "human_policy_review_workflow", "title": "Human / policy review workflow"},
            {"id": "scene_delta_production_schema", "title": "Scene Delta production schema alignment"},
            {"id": "executor_openapi_proto", "title": "Executor OpenAPI/proto import"},
            {"id": "multi_text_bearing_roi_samples", "title": "Diverse text-bearing ROI samples"},
            {"id": "real_video_text_roi_discovery", "title": "Text ROI discovery on real video frames"},
            {"id": "vision_roi_text_bearing_detector", "title": "Vision ROI quality / text-bearing detector"},
            {"id": "performance_controller", "title": "Performance Controller integration"},
            {"id": "test_board_scenarios", "title": "Test Board scenario set integration"},
            {"id": "worldmodel_write_readiness_gate", "title": "WorldModel write readiness gate"},
            {"id": "user_disclosure_policy", "title": "User disclosure policy for OCR/fusion candidates"},
        ],
    }


def build_final_closure_summary_v0() -> Dict[str, Any]:
    return {
        "chain_status": "closed_for_evaluation",
        "final_write_status": "no_write",
        "final_executor_status": "blocked_by_gate",
        "final_fact_status": "not_fact",
        "recommended_next_decision": "policy_review_or_testboard_expansion",
    }


def build_closure_audit_v0(*, no_write_verified: bool) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_vision_ocr_chain_closure_executed": True,
        "evaluation_only": True,
        "no_write_boundary_verified": no_write_verified,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "scene_delta_executor_invoked": False,
        "database_write_invoked": False,
        "wal_append_invoked": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def run_cross_modal_vision_ocr_chain_closure_v0(
    *,
    chain_roots: Dict[str, str],
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    roots: Dict[str, Path] = {}
    for spec in PHASE_SPECS:
        key = spec["phase_key"]
        path_str = chain_roots.get(key) or DEFAULT_CHAIN_ROOTS.get(key, "")
        if not path_str:
            errs.append(f"missing_root_config:{key}")
            continue
        rp = Path(path_str).resolve()
        roots[key] = rp
        if not rp.is_dir():
            errs.append(f"input_root_not_found:{key}:{rp}")

    phase_matrix = build_phase_matrix_v0(roots)
    lineage = build_lineage_matrix_v0(roots)
    no_write = build_no_write_boundary_matrix_v0(roots)
    capability = build_capability_closure_report_v0(lineage)
    non_claims = build_non_claims_report_v0()
    followups = build_open_followups_v0()
    final_closure = build_final_closure_summary_v0()
    audit = build_closure_audit_v0(no_write_verified=bool(no_write.get("all_phases_boundary_ok")))

    critical_go = 0
    critical_total = 0
    for row in phase_matrix.get("rows") or []:
        if not isinstance(row, dict):
            continue
        if row.get("critical"):
            critical_total += 1
            if row.get("verifier_verdict") in ("GO", "CONDITIONAL_GO"):
                critical_go += 1

    phase_verdict = "GO"
    if errs and critical_go < critical_total:
        phase_verdict = "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"
    elif not no_write.get("all_phases_boundary_ok"):
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Evaluation-Chain-Closure-001",
        "input_roots": {k: str(v.resolve()) for k, v in roots.items()},
        "phase_matrix_row_count": phase_matrix.get("row_count"),
        "critical_phases_go": critical_go,
        "critical_phases_total": critical_total,
        "no_write_all_phases_ok": no_write.get("all_phases_boundary_ok"),
        "final_closure": final_closure,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, phase_matrix, lineage, no_write, capability, non_claims, followups, audit, errs
