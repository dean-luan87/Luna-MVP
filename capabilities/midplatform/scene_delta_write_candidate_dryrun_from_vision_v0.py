# -*- coding: utf-8 -*-
"""Dry-run verifier for Scene Delta write candidate from Vision (no executor, no writes).

Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

DRYRUN_SUMMARY_SCHEMA_VERSION = "scene_delta_write_candidate_dryrun_from_vision_summary_v0"
FIELD_COMPLETENESS_SCHEMA = "scene_delta_write_candidate_from_vision_field_completeness_report_v0"
MAPPING_MATRIX_SCHEMA = "scene_delta_write_candidate_from_vision_mapping_matrix_v0"
RISK_REPORT_SCHEMA = "scene_delta_write_candidate_from_vision_risk_report_v0"
NO_WRITE_AUDIT_SCHEMA = "scene_delta_write_candidate_from_vision_no_write_audit_v0"

_REQUIRED_FORBIDDEN_KEYS = (
    "write_scene_delta",
    "write_midplatform_fact",
    "write_world_model",
    "invoke_ai_interpretation",
    "invoke_navigation_decision",
    "invoke_real_vision_provider",
)

RISK_CODES_IN_ORDER = (
    "vision_stub_label_is_not_fact",
    "synthetic_evidence_not_confirmed",
    "gate_not_evaluated",
    "ai_interpretation_not_invoked",
    "navigation_decision_not_invoked",
    "world_model_write_forbidden",
    "geometry_coordinate_space_frame_pixel",
    "confidence_stub_value_allowed_as_candidate_only",
)


def _present(val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, str):
        return bool(val.strip())
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return True


def evidence_matrix_rows(evidence_matrix: Any) -> List[Any]:
    if isinstance(evidence_matrix, dict):
        rows = evidence_matrix.get("rows")
        return rows if isinstance(rows, list) else []
    if isinstance(evidence_matrix, list):
        return evidence_matrix
    return []


def build_field_completeness_report_from_vision_v0(
    *,
    candidate: Dict[str, Any],
    gate: Dict[str, Any],
    vision_audit: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str], bool]:
    issues: List[str] = []
    checks: Dict[str, Any] = {}

    def ck(name: str, ok: bool, detail: Optional[str] = None) -> None:
        checks[name] = {"ok": ok, "detail": detail}
        if not ok:
            issues.append(f"missing_or_invalid:{name}")

    ck("candidate_id", _present(candidate.get("candidate_id")))
    ck("candidate_scope", str(candidate.get("candidate_scope") or "") == "write_candidate_only")
    ck("source_type", str(candidate.get("source_type") or "") == "vision_recognition_evidence")
    items = candidate.get("evidence_items")
    ck("evidence_items", isinstance(items, list) and len(items) > 0, f"count={len(items) if isinstance(items, list) else 0}")
    sr = candidate.get("spatial_reference")
    ck(
        "spatial_reference",
        isinstance(sr, dict) and _present(sr.get("geometry_source")) and _present(sr.get("coordinate_space")),
    )
    scs = candidate.get("source_chain_summary")
    ck("source_chain_summary", isinstance(scs, dict))
    fss = candidate.get("fact_status_summary")
    ck("fact_status_summary", isinstance(fss, dict) and len(fss) > 0)
    ss = candidate.get("synthetic_summary")
    ck("synthetic_summary", isinstance(ss, dict) and _present(ss.get("synthetic_count")))
    fa = candidate.get("forbidden_actions")
    ck(
        "forbidden_actions",
        isinstance(fa, dict) and all(k in fa for k in _REQUIRED_FORBIDDEN_KEYS),
    )
    ck("vision_audit_present", isinstance(vision_audit, dict) and len(vision_audit) > 0)
    ck("gate_required", gate.get("gate_required") is True)
    ck("gate_status", str(gate.get("gate_status") or "") == "not_evaluated")
    grc = gate.get("gate_reason_codes")
    ck("gate_reason_codes", isinstance(grc, list) and len(grc) > 0)

    overall = len(issues) == 0
    report = {
        "schema": FIELD_COMPLETENESS_SCHEMA,
        "checks": checks,
        "issues": list(issues),
        "overall_complete": overall,
    }
    return report, issues, overall


def build_mapping_matrix_from_vision_v0(candidate: Dict[str, Any], gate: Dict[str, Any]) -> Dict[str, Any]:
    rows_out: List[Dict[str, Any]] = []
    items = candidate.get("evidence_items") if isinstance(candidate.get("evidence_items"), list) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        label = it.get("label")
        rows_out.append(
            {
                "evidence_id": it.get("evidence_id"),
                "mappings": [
                    {
                        "vision_path": "evidence_items[].label",
                        "scene_delta_path": "scene_delta.observed_visual_candidate",
                        "value_preview": (str(label or ""))[:80],
                    },
                    {
                        "vision_path": "evidence_items[].source_frame_id",
                        "scene_delta_path": "scene_delta.source_frame_ref",
                        "value": it.get("source_frame_id"),
                    },
                    {
                        "vision_path": "evidence_items[].roi_id|unit_id",
                        "scene_delta_path": "scene_delta.source_region_ref",
                        "roi_id": it.get("roi_id"),
                        "unit_id": it.get("unit_id"),
                    },
                    {
                        "vision_path": "evidence_items[].roi_type",
                        "scene_delta_path": "scene_delta.source_region_type",
                        "value": it.get("roi_type"),
                    },
                    {
                        "vision_path": "evidence_items[].bbox_in_frame",
                        "scene_delta_path": "scene_delta.spatial_evidence",
                        "bbox_in_frame": it.get("bbox_in_frame"),
                    },
                    {
                        "vision_path": "evidence_items[].provider",
                        "scene_delta_path": "scene_delta.source_provider",
                        "value": it.get("provider"),
                    },
                    {
                        "vision_path": "evidence_items[].synthetic",
                        "scene_delta_path": "scene_delta.synthetic_candidate_flag",
                        "value": it.get("synthetic"),
                    },
                    {
                        "vision_path": "evidence_items[].fact_status",
                        "scene_delta_path": "scene_delta.fact_status_candidate",
                        "value": it.get("fact_status"),
                    },
                ],
            }
        )
    rows_out.append(
        {
            "evidence_id": None,
            "mappings": [
                {
                    "vision_path": "gate_stub.gate_status",
                    "scene_delta_path": "scene_delta.write_gate_status",
                    "value": gate.get("gate_status"),
                }
            ],
        }
    )
    return {
        "schema": MAPPING_MATRIX_SCHEMA,
        "candidate_id": candidate.get("candidate_id"),
        "rows": rows_out,
    }


def build_risk_report_from_vision_v0(
    *,
    candidate: Dict[str, Any],
    gate: Dict[str, Any],
    completeness_issues: List[str],
) -> Dict[str, Any]:
    items = candidate.get("evidence_items") if isinstance(candidate.get("evidence_items"), list) else []
    confidences = [it.get("confidence") for it in items if isinstance(it, dict)]
    stub_conf = all((c == 0.5 or c is None) for c in confidences) if confidences else True

    risks: List[Dict[str, Any]] = []
    for code in RISK_CODES_IN_ORDER:
        if code == "vision_stub_label_is_not_fact":
            risks.append(
                {
                    "code": code,
                    "severity": "info",
                    "detail": "Vision stub labels are observed_visual_candidate / not_fact only.",
                }
            )
        elif code == "synthetic_evidence_not_confirmed":
            risks.append({"code": code, "severity": "info", "detail": "Synthetic stub evidence is not confirmed for Scene Delta."})
        elif code == "gate_not_evaluated":
            risks.append({"code": code, "severity": "info", "detail": f"gate_status={gate.get('gate_status')!r}"})
        elif code == "ai_interpretation_not_invoked":
            risks.append({"code": code, "severity": "info", "detail": "No semantic interpretation layer in candidate."})
        elif code == "navigation_decision_not_invoked":
            risks.append({"code": code, "severity": "info", "detail": "No navigation decision in dry-run path."})
        elif code == "world_model_write_forbidden":
            risks.append({"code": code, "severity": "info", "detail": "forbidden_actions includes write_world_model."})
        elif code == "geometry_coordinate_space_frame_pixel":
            sr = candidate.get("spatial_reference") if isinstance(candidate.get("spatial_reference"), dict) else {}
            risks.append(
                {
                    "code": code,
                    "severity": "info",
                    "detail": f"coordinate_space={sr.get('coordinate_space')!r}",
                }
            )
        elif code == "confidence_stub_value_allowed_as_candidate_only":
            risks.append(
                {
                    "code": code,
                    "severity": "low",
                    "detail": f"stub_confidence_pattern={stub_conf}",
                }
            )

    if completeness_issues:
        risks.append(
            {
                "code": "field_completeness_gaps",
                "severity": "medium",
                "detail": completeness_issues,
            }
        )

    return {"schema": RISK_REPORT_SCHEMA, "risks": risks}


def build_no_write_audit_from_vision_v0() -> Dict[str, Any]:
    return {
        "schema": NO_WRITE_AUDIT_SCHEMA,
        "dry_run_executed": True,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
        "real_vision_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
    }


def run_scene_delta_write_candidate_dryrun_from_vision_v0(
    *,
    input_write_candidate_root: str,
    candidate: Dict[str, Any],
    evidence_matrix: Any,
    gate: Dict[str, Any],
    vision_audit: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    """
    Returns (summary, completeness_report, mapping_matrix, risk_report, no_write_audit, blocking_errors).
    """
    blocking: List[str] = []

    items = candidate.get("evidence_items") if isinstance(candidate.get("evidence_items"), list) else []
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            continue
        if str(it.get("fact_status") or "") == "confirmed_fact":
            blocking.append(f"forbidden_confirmed_fact_at_evidence_{i}")

    mat_rows = evidence_matrix_rows(evidence_matrix)
    if len(mat_rows) != len(items):
        blocking.append("evidence_matrix_row_count_mismatch")

    comp_report, comp_issues, comp_ok = build_field_completeness_report_from_vision_v0(
        candidate=candidate, gate=gate, vision_audit=vision_audit
    )

    dry_run_status = "failed" if blocking else ("completed" if comp_ok else "completed_with_gaps")

    summary = {
        "schema_version": DRYRUN_SUMMARY_SCHEMA_VERSION,
        "dry_run_id": f"dryrun_sd_vision_{uuid.uuid4().hex}",
        "input_write_candidate_root": input_write_candidate_root,
        "source_candidate_id": str(candidate.get("candidate_id") or ""),
        "source_event_id": str(candidate.get("source_event_id") or ""),
        "source_ingest_candidate_id": str(candidate.get("source_ingest_candidate_id") or ""),
        "source_type": "vision_recognition_evidence",
        "evidence_count": int(candidate.get("evidence_count") or len(items)),
        "dry_run_status": dry_run_status,
        "write_would_be_allowed": False,
        "executor_invoked": False,
        "database_write_invoked": False,
        "field_completeness_ok": comp_ok,
        "field_completeness_issue_count": len(comp_issues),
    }

    mapping = build_mapping_matrix_from_vision_v0(candidate, gate)
    risks = build_risk_report_from_vision_v0(candidate=candidate, gate=gate, completeness_issues=comp_issues)
    audit = build_no_write_audit_from_vision_v0()

    return summary, comp_report, mapping, risks, audit, blocking
