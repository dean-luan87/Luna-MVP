# -*- coding: utf-8 -*-
"""Dry-run verifier for Scene Delta write candidate from OCR (no executor, no writes).

Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

DRYRUN_SUMMARY_SCHEMA = "scene_delta_write_candidate_dryrun_summary_v0"
FIELD_COMPLETENESS_SCHEMA = "scene_delta_write_candidate_field_completeness_report_v0"
MAPPING_MATRIX_SCHEMA = "scene_delta_write_candidate_mapping_matrix_v0"
RISK_REPORT_SCHEMA = "scene_delta_write_candidate_risk_report_v0"
NO_WRITE_AUDIT_SCHEMA = "scene_delta_write_candidate_dryrun_no_write_audit_v0"

RISK_CODES_IN_ORDER = (
    "ocr_text_is_not_fact",
    "gate_not_evaluated",
    "ai_interpretation_not_invoked",
    "world_model_write_forbidden",
    "geometry_coordinate_space_source_image",
    "confidence_zero_or_unknown_allowed_as_candidate_only",
)


def _present(val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, str):
        return bool(val.strip())
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return True


def build_field_completeness_report_v0(
    *,
    candidate: Dict[str, Any],
    gate: Dict[str, Any],
    stub_audit: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str], bool]:
    """Returns (report, issues, overall_complete)."""
    issues: List[str] = []
    checks: Dict[str, Any] = {}

    def ck(name: str, ok: bool, detail: Optional[str] = None) -> None:
        checks[name] = {"ok": ok, "detail": detail}
        if not ok:
            issues.append(f"missing_or_invalid:{name}")

    ck("candidate_id", _present(candidate.get("candidate_id")))
    ck("candidate_scope", str(candidate.get("candidate_scope") or "") == "write_candidate_only")
    ck("source_type", _present(candidate.get("source_type")))
    items = candidate.get("evidence_items")
    ck("evidence_items", isinstance(items, list) and len(items) > 0, f"count={len(items) if isinstance(items, list) else 0}")
    sr = candidate.get("spatial_reference")
    ck("spatial_reference", isinstance(sr, dict) and _present(sr.get("geometry_source")) and _present(sr.get("coordinate_space")))
    scs = candidate.get("source_chain_summary")
    ck("source_chain_summary", isinstance(scs, dict))
    fa = candidate.get("forbidden_actions")
    ck(
        "forbidden_actions",
        isinstance(fa, dict)
        and all(k in fa for k in ("write_scene_delta", "write_midplatform_fact", "write_world_model", "invoke_ai_interpretation")),
    )
    ck("stub_audit_present", isinstance(stub_audit, dict) and bool(stub_audit))
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


def build_mapping_matrix_v0(candidate: Dict[str, Any], gate: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    items = candidate.get("evidence_items") if isinstance(candidate.get("evidence_items"), list) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        line = it.get("line_order")
        rows.append(
            {
                "line_order": line,
                "mappings": [
                    {
                        "ocr_path": "evidence_items[].text",
                        "scene_delta_path": "scene_delta.observed_text_candidate",
                        "value_preview": (str(it.get("text") or ""))[:80],
                    },
                    {
                        "ocr_path": "evidence_items[].roi_id|unit_id",
                        "scene_delta_path": "scene_delta.source_region_ref",
                        "roi_id": it.get("roi_id"),
                        "unit_id": it.get("unit_id"),
                    },
                    {
                        "ocr_path": "evidence_items[].original_bbox|original_polygon",
                        "scene_delta_path": "scene_delta.spatial_evidence",
                        "has_bbox": isinstance(it.get("original_bbox"), list),
                        "has_polygon": isinstance(it.get("original_polygon"), list),
                    },
                    {
                        "ocr_path": "evidence_items[].provider",
                        "scene_delta_path": "scene_delta.source_provider",
                        "value": it.get("provider"),
                    },
                    {
                        "ocr_path": "evidence_items[].fact_status",
                        "scene_delta_path": "scene_delta.fact_status_candidate",
                        "value": it.get("fact_status"),
                    },
                ],
            }
        )
    rows.append(
        {
            "line_order": None,
            "mappings": [
                {
                    "ocr_path": "gate_stub.gate_status",
                    "scene_delta_path": "scene_delta.write_gate_status",
                    "value": gate.get("gate_status"),
                }
            ],
        }
    )
    return {"schema": MAPPING_MATRIX_SCHEMA, "candidate_id": candidate.get("candidate_id"), "rows": rows}


def build_risk_report_v0(
    *,
    candidate: Dict[str, Any],
    gate: Dict[str, Any],
    completeness_issues: List[str],
) -> Dict[str, Any]:
    items = candidate.get("evidence_items") if isinstance(candidate.get("evidence_items"), list) else []
    confidences = [it.get("confidence") for it in items if isinstance(it, dict)]
    zero_or_unknown = all(c is None or c == 0.0 for c in confidences) if confidences else True

    risks: List[Dict[str, Any]] = []
    for code in RISK_CODES_IN_ORDER:
        if code == "ocr_text_is_not_fact":
            risks.append({"code": code, "severity": "info", "detail": "OCR lines are observed_text / not_fact only."})
        elif code == "gate_not_evaluated":
            risks.append(
                {
                    "code": code,
                    "severity": "info",
                    "detail": f"gate_status={gate.get('gate_status')!r}",
                }
            )
        elif code == "ai_interpretation_not_invoked":
            risks.append({"code": code, "severity": "info", "detail": "No semantic interpretation layer in candidate."})
        elif code == "world_model_write_forbidden":
            risks.append({"code": code, "severity": "info", "detail": "forbidden_actions includes write_world_model."})
        elif code == "geometry_coordinate_space_source_image":
            sr = candidate.get("spatial_reference") if isinstance(candidate.get("spatial_reference"), dict) else {}
            risks.append(
                {
                    "code": code,
                    "severity": "info",
                    "detail": f"coordinate_space={sr.get('coordinate_space')!r}",
                }
            )
        elif code == "confidence_zero_or_unknown_allowed_as_candidate_only":
            risks.append(
                {
                    "code": code,
                    "severity": "low",
                    "detail": f"all_zero_or_unknown={zero_or_unknown}",
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


def build_no_write_audit_v0() -> Dict[str, Any]:
    return {
        "schema": NO_WRITE_AUDIT_SCHEMA,
        "dry_run_executed": True,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
    }


def run_scene_delta_write_candidate_dryrun_v0(
    *,
    input_write_candidate_root: str,
    candidate: Dict[str, Any],
    evidence_matrix: Any,
    gate: Dict[str, Any],
    stub_audit: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    """
    Returns (summary, completeness_report, mapping_matrix, risk_report, no_write_audit, blocking_errors).

    ``blocking_errors`` non-empty means dry-run should be marked failed (still emit no-write audit).
    """
    blocking: List[str] = []

    items = candidate.get("evidence_items") if isinstance(candidate.get("evidence_items"), list) else []
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            continue
        if str(it.get("fact_status") or "") == "confirmed_fact":
            blocking.append(f"forbidden_confirmed_fact_at_evidence_{i}")

    comp_report, comp_issues, comp_ok = build_field_completeness_report_v0(candidate=candidate, gate=gate, stub_audit=stub_audit)
    if not isinstance(evidence_matrix, list):
        blocking.append("evidence_matrix_not_list")
    elif len(evidence_matrix) != len(items):
        blocking.append("evidence_matrix_row_count_mismatch")

    dry_run_status = "failed" if blocking else ("completed" if comp_ok else "completed_with_gaps")

    summary = {
        "schema": DRYRUN_SUMMARY_SCHEMA,
        "dry_run_id": f"dryrun_sd_ocr_{uuid.uuid4().hex}",
        "input_write_candidate_root": input_write_candidate_root,
        "source_candidate_id": str(candidate.get("candidate_id") or ""),
        "source_event_id": str(candidate.get("source_event_id") or ""),
        "source_ingest_candidate_id": str(candidate.get("source_ingest_candidate_id") or ""),
        "evidence_count": int(candidate.get("evidence_count") or len(items)),
        "dry_run_status": dry_run_status,
        "write_would_be_allowed": False,
        "executor_invoked": False,
        "database_write_invoked": False,
        "field_completeness_ok": comp_ok,
        "field_completeness_issue_count": len(comp_issues),
    }

    mapping = build_mapping_matrix_v0(candidate, gate)
    risks = build_risk_report_v0(candidate=candidate, gate=gate, completeness_issues=comp_issues)
    audit = build_no_write_audit_v0()

    return summary, comp_report, mapping, risks, audit, blocking
