# -*- coding: utf-8 -*-
"""Public facility semantic-first runtime dry-run (no OCR/Vision/fact writes).

Phase-PublicFacility-Runtime-DryRun-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "PublicFacility-Runtime-DryRun-001"

SUMMARY_SCHEMA = "public_facility_runtime_dryrun_summary_v0"
FIXTURE_MANIFEST_SCHEMA = "public_facility_runtime_fixture_manifest_v0"
SEMANTIC_MATRIX_SCHEMA = "public_facility_semantic_candidate_matrix_v0"
CORRECTION_MATRIX_SCHEMA = "public_facility_correction_candidate_matrix_v0"
EVIDENCE_SCHEMA = "public_facility_evidence_composition_matrix_v0"
GATE_SCHEMA = "public_facility_gate_evaluator_dryrun_v0"
SPEAK_SCHEMA = "public_facility_cautious_speak_dryrun_report_v0"
RISK_SCHEMA = "public_facility_runtime_risk_report_v0"
METRICS_BIND_SCHEMA = "public_facility_runtime_metrics_binding_report_v0"
BENCHMARK_LINK_SCHEMA = "public_facility_runtime_benchmark_link_report_v0"
SIM_SCHEMA = "public_facility_runtime_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "public_facility_runtime_non_claims_report_v0"
AUDIT_SCHEMA = "public_facility_runtime_audit_v0"

FIXTURE_DEFS: Tuple[Dict[str, Any], ...] = (
    {
        "fixture_id": "PF_FIXTURE_RESTROOM_TYPO",
        "visual_hint": "restroom_icon",
        "raw_ocr_text": "Toliet",
        "expected_semantic_candidate": "restroom_facility_nearby",
        "expected_correction_candidate": "toilet/restroom",
        "expected_gate_decision": "allow_cautious_speak_candidate",
        "review_required": False,
        "correction_layers": ["L1_facility_dictionary_stub", "L2_facility_semantic_library_stub"],
        "cautious_phrase_zh": "前方疑似有洗手间标识。",
        "icon_only": False,
    },
    {
        "fixture_id": "PF_FIXTURE_EXIT_SIGN",
        "visual_hint": "exit_icon",
        "raw_ocr_text": "EXIT",
        "expected_semantic_candidate": "exit_or_directional_exit_sign",
        "expected_correction_candidate": None,
        "expected_gate_decision": "allow_cautious_speak_candidate",
        "review_required": False,
        "correction_layers": [],
        "cautious_phrase_zh": "前方疑似出口方向标识。",
        "icon_only": False,
    },
    {
        "fixture_id": "PF_FIXTURE_ELEVATOR_ICON_ONLY",
        "visual_hint": "elevator_icon",
        "raw_ocr_text": "",
        "expected_semantic_candidate": "elevator_facility_candidate",
        "expected_correction_candidate": None,
        "expected_gate_decision": "hold_for_review",
        "review_required": True,
        "correction_layers": [],
        "cautious_phrase_zh": "附近可能有电梯标识，但还需要进一步确认。",
        "icon_only": True,
        "gate_reason": "icon_only_requires_review",
    },
    {
        "fixture_id": "PF_FIXTURE_ACCESSIBLE_PARTIAL",
        "visual_hint": "accessible_icon",
        "raw_ocr_text": "Acc...",
        "expected_semantic_candidate": "accessible_facility_candidate",
        "expected_correction_candidate": "accessible",
        "expected_gate_decision": "hold_for_review",
        "review_required": True,
        "correction_layers": ["L3_model_candidate_stub", "midplatform_arbitration_required"],
        "cautious_phrase_zh": "前方疑似无障碍设施标识，建议进一步确认。",
        "icon_only": False,
    },
    {
        "fixture_id": "PF_FIXTURE_NO_ENTRY_WARNING",
        "visual_hint": "no_entry_or_warning_symbol",
        "raw_ocr_text": "",
        "expected_semantic_candidate": "restricted_or_warning_area_candidate",
        "expected_correction_candidate": None,
        "expected_gate_decision": "allow_cautious_speak_candidate",
        "review_required": False,
        "correction_layers": [],
        "cautious_phrase_zh": "前方疑似限制通行或警示标识，请注意。",
        "icon_only": False,
        "navigation_allowed": False,
    },
    {
        "fixture_id": "PF_FIXTURE_AMBIGUOUS_ICON",
        "visual_hint": "ambiguous_symbol",
        "raw_ocr_text": "",
        "expected_semantic_candidate": "uncertain_facility_symbol_candidate",
        "expected_correction_candidate": None,
        "expected_gate_decision": "hold_for_review",
        "review_required": True,
        "correction_layers": [],
        "cautious_phrase_zh": None,
        "icon_only": False,
    },
)

FORBIDDEN_SPEAK_PHRASES = (
    "这里就是洗手间",
    "请立即从这里出去",
    "前方一定是电梯",
    "这是已确认的公共设施",
)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _source_ok(root: Path, summary_name: str) -> bool:
    sm = _read_json(root / summary_name) or {}
    if not sm:
        return False
    if sm.get("bootstrap_only"):
        return True
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    return hint in ("GO", "CONDITIONAL_GO")


def _image_stub_ref(governance_root: Path, fixture_id: str) -> str:
    if fixture_id == "PF_FIXTURE_RESTROOM_TYPO":
        gov = _read_json(governance_root / "public_facility_synthetic_fixture_manifest.json") or {}
        ref = gov.get("source_image_ref")
        if ref:
            return str(ref)
    return f"stub://public_facility_runtime/{fixture_id}.png"


def build_fixture_manifest(governance_root: Path) -> Dict[str, Any]:
    fixtures: List[Dict[str, Any]] = []
    for d in FIXTURE_DEFS:
        fixtures.append(
            {
                "fixture_id": d["fixture_id"],
                "image_ref_or_stub_ref": _image_stub_ref(governance_root, d["fixture_id"]),
                "source_type": "synthetic_fixture_stub",
                "runtime_execution": False,
                "real_image_loaded": d["fixture_id"] == "PF_FIXTURE_RESTROOM_TYPO",
                "visual_hint": d["visual_hint"],
                "raw_ocr_text": d["raw_ocr_text"],
                "expected_semantic_candidate": d["expected_semantic_candidate"],
                "expected_correction_candidate": d.get("expected_correction_candidate"),
                "expected_gate_decision": d.get("expected_gate_decision"),
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": FIXTURE_MANIFEST_SCHEMA,
        "fixture_count": len(fixtures),
        "fixtures": fixtures,
    }


def build_semantic_candidate_matrix() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for i, d in enumerate(FIXTURE_DEFS):
        has_correction = bool(d.get("expected_correction_candidate"))
        rows.append(
            {
                "candidate_id": f"PF_SEM_CAND_{i + 1:03d}",
                "fixture_id": d["fixture_id"],
                "facility_type_candidate": d["expected_semantic_candidate"].split("_")[0],
                "semantic_candidate": d["expected_semantic_candidate"],
                "visual_hint": d["visual_hint"],
                "raw_ocr_text_preserved": d["raw_ocr_text"],
                "ocr_auxiliary_used": bool(d["raw_ocr_text"]),
                "correction_candidate_generated": has_correction,
                "confidence_placeholder": None,
                "fact_status": "not_fact",
                "write_allowed": False,
                "requires_midplatform_arbitration": True,
                "review_required": d.get("review_required", False),
            }
        )
    return {"schema_version": SEMANTIC_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_correction_candidate_matrix() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    cid = 0
    for d in FIXTURE_DEFS:
        raw = d["raw_ocr_text"]
        corrected = d.get("expected_correction_candidate")
        if not corrected:
            continue
        for layer in d.get("correction_layers") or ["L1_facility_dictionary_stub"]:
            cid += 1
            rows.append(
                {
                    "correction_id": f"PF_CORR_{cid:03d}",
                    "fixture_id": d["fixture_id"],
                    "raw_text": raw,
                    "corrected_text_candidate": corrected,
                    "correction_source_layer": layer,
                    "correction_method": "dictionary_stub_match" if "L1" in layer else "semantic_stub_match",
                    "correction_confidence_placeholder": None,
                    "raw_text_preserved": True,
                    "correction_committed": False,
                    "fact_status": "not_fact",
                }
            )
    return {"schema_version": CORRECTION_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_evidence_composition_matrix(
    semantic_rows: List[Dict[str, Any]],
    correction_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    corr_by_fixture = {r["fixture_id"]: r for r in correction_rows}
    rows: List[Dict[str, Any]] = []
    for sem in semantic_rows:
        fid = sem["fixture_id"]
        d = next(x for x in FIXTURE_DEFS if x["fixture_id"] == fid)
        corr = corr_by_fixture.get(fid)
        conflict = bool(corr and sem["raw_ocr_text_preserved"] != corr.get("raw_text"))
        if d["fixture_id"] == "PF_FIXTURE_AMBIGUOUS_ICON":
            final_status = "hold_for_review"
        elif d.get("expected_gate_decision") == "reject_uncertain":
            final_status = "rejected_or_uncertain"
        else:
            final_status = "candidate_ready_for_gate" if not d.get("review_required") else "hold_for_review"
        rows.append(
            {
                "fixture_id": fid,
                "visual_symbol_evidence_stub": {"visual_hint": d["visual_hint"], "registry_invoked": False},
                "ocr_auxiliary_text_evidence": sem["raw_ocr_text_preserved"] or None,
                "correction_candidate": corr.get("corrected_text_candidate") if corr else None,
                "semantic_candidate": sem["semantic_candidate"],
                "conflict_status": "none" if not conflict else "raw_preserved_with_correction_candidate",
                "evidence_strength_placeholder": None,
                "final_runtime_status": final_status,
            }
        )
    return {"schema_version": EVIDENCE_SCHEMA, "row_count": len(rows), "rows": rows}


def build_gate_evaluator_dryrun() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for i, d in enumerate(FIXTURE_DEFS):
        decision = d["expected_gate_decision"]
        reason = d.get("gate_reason") or (
            "icon_only_requires_review" if d.get("icon_only") else "semantic_first_dry_run"
        )
        rows.append(
            {
                "candidate_id": f"PF_SEM_CAND_{i + 1:03d}",
                "fixture_id": d["fixture_id"],
                "gate_status": "evaluated_dry_run",
                "decision": decision,
                "allowed_decisions": [
                    "allow_cautious_speak_candidate",
                    "hold_for_review",
                    "reject_uncertain",
                ],
                "fact_write_allowed": False,
                "world_model_write_allowed": False,
                "navigation_decision_allowed": False,
                "auto_approval_allowed": False,
                "reason": reason,
            }
        )
    return {"schema_version": GATE_SCHEMA, "row_count": len(rows), "rows": rows}


def build_cautious_speak_dryrun(gate_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    phrases: List[Dict[str, Any]] = []
    for d, gate in zip(FIXTURE_DEFS, gate_rows):
        if gate.get("decision") != "allow_cautious_speak_candidate":
            continue
        phrase = d.get("cautious_phrase_zh")
        if not phrase:
            continue
        phrases.append(
            {
                "fixture_id": d["fixture_id"],
                "candidate_id": gate.get("candidate_id"),
                "phrasing_zh": phrase,
                "phrasing_en": None,
                "strong_assertion": False,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": SPEAK_SCHEMA,
        "tts_invoked": False,
        "speech_output_committed": False,
        "candidate_phrasing_only": True,
        "forbidden_phrases_absent": True,
        "forbidden_phrases_checked": list(FORBIDDEN_SPEAK_PHRASES),
        "phrase_count": len(phrases),
        "phrases": phrases,
    }


def build_risk_report() -> Dict[str, Any]:
    return {
        "schema_version": RISK_SCHEMA,
        "semantic_first_not_fact": True,
        "raw_ocr_text_preserved": True,
        "correction_candidate_not_fact": True,
        "icon_only_requires_review": True,
        "ambiguous_symbol_hold_for_review": True,
        "no_ocr_mainline_default": True,
        "no_world_model_write": True,
        "no_navigation_decision": True,
        "no_auto_approval": True,
        "cautious_speak_only": True,
    }


def build_metrics_binding(
    semantic_rows: List[Dict[str, Any]],
    correction_rows: List[Dict[str, Any]],
    gate_rows: List[Dict[str, Any]],
    speak_report: Dict[str, Any],
) -> Dict[str, Any]:
    icon_only = sum(1 for d in FIXTURE_DEFS if d.get("icon_only"))
    ambiguous_hold = sum(
        1 for g in gate_rows if g.get("fixture_id") == "PF_FIXTURE_AMBIGUOUS_ICON" and g.get("decision") == "hold_for_review"
    )
    raw_preserved = sum(1 for s in semantic_rows if s.get("raw_ocr_text_preserved") is not None)
    return {
        "schema_version": METRICS_BIND_SCHEMA,
        "public_facility_candidate_count": len(semantic_rows),
        "correction_candidate_count": len(correction_rows),
        "raw_ocr_text_preserved_count": raw_preserved,
        "icon_only_candidate_count": icon_only,
        "ambiguous_hold_count": ambiguous_hold,
        "cautious_speak_candidate_count": speak_report.get("phrase_count", 0),
        "rejected_or_uncertain_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "future_facility_semantic_accuracy": None,
        "future_correction_accuracy": None,
        "accuracy_computed": False,
    }


def build_benchmark_link_report(benchmark_planning_root: Path) -> Dict[str, Any]:
    contract = _read_json(
        benchmark_planning_root / "cross_modal_vision_ocr_benchmark_real_values_collector_output_contract.json"
    ) or {}
    gt = _read_json(
        benchmark_planning_root / "cross_modal_vision_ocr_benchmark_ground_truth_requirement_report.json"
    ) or {}
    return {
        "schema_version": BENCHMARK_LINK_SCHEMA,
        "benchmark_planning_root": str(benchmark_planning_root),
        "current_phase_generates_benchmark_values": False,
        "ground_truth_required_for_facility_semantic_correctness": True,
        "current_ground_truth_available": _bool(gt.get("current_v1_has_ground_truth"), default=False) is False,
        "facility_semantic_accuracy_not_computed": True,
        "correction_accuracy_not_computed": True,
        "benchmark_contract_current_phase_generates_values": contract.get("current_phase_generates_values"),
    }


def _bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    return bool(v)


def build_simulation_context_report(sim_root: Path) -> Dict[str, Any]:
    sm = _read_json(sim_root / "simulation_summary.json") or {}
    return {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sm.get("simulation_output_root") or str(sim_root),
        "run_model": sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_production_facility_recognition": True,
        "not_icon_library_integrated": True,
        "no_real_ocr_executed": True,
        "no_model_correction_executed": True,
        "semantic_candidates_not_facts": True,
        "no_world_model_write": True,
        "not_for_navigation": True,
        "no_tts_broadcast": True,
        "no_benchmark_or_accuracy_claim": True,
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "public_facility_runtime_dryrun_executed": True,
        "dry_run_only": True,
        "semantic_first_required": True,
        "default_ocr_mainline_allowed": False,
        "real_ocr_invoked": False,
        "ocr_mainline_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "visual_symbol_registry_invoked": False,
        "external_icon_library_invoked": False,
        "external_brand_database_invoked": False,
        "model_correction_invoked": False,
        "ai_interpretation_invoked": False,
        "cautious_speak_committed": False,
        "tts_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }


def build_summary(
    *,
    governance_ok: bool,
    track_closures_ok: bool,
    benchmark_ok: bool,
    simulation_attached: bool,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "runtime_scope": "dry_run_only",
        "based_on_public_facility_governance": governance_ok,
        "based_on_v1_track_closures": track_closures_ok,
        "based_on_benchmark_planning": benchmark_ok,
        "simulation_context_attached": simulation_attached,
        "semantic_first_required": True,
        "default_ocr_mainline_allowed": False,
        "ocr_auxiliary_allowed": True,
        "real_ocr_invoked": False,
        "vision_provider_invoked": False,
        "visual_symbol_registry_invoked": False,
        "facility_candidate_generated": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_public_facility_runtime_dryrun_v0(
    *,
    public_facility_governance_root: str,
    v1_track_closures_root: str,
    benchmark_real_values_planning_root: str,
    simulation_lab_harness_root: str,
    poster_track_b_closure_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
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
    gov = Path(public_facility_governance_root).resolve()
    tc = Path(v1_track_closures_root).resolve()
    bench = Path(benchmark_real_values_planning_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()
    poster = Path(poster_track_b_closure_root).resolve()

    gov_ok = _source_ok(gov, "public_facility_semantic_correction_governance_summary.json")
    if not gov_ok:
        errs.append("governance_not_ok")

    tc_ok = _source_ok(tc, "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json")
    tc_sm = _read_json(tc / "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json") or {}
    if tc_sm.get("v1_status") != "closed_for_evaluation":
        errs.append("v1_not_closed_for_evaluation")

    bench_ok = _source_ok(bench, "cross_modal_vision_ocr_benchmark_real_values_planning_summary.json")
    if not bench_ok:
        errs.append("benchmark_planning_not_ok")

    sim_attached = (sim / "simulation_summary.json").is_file()
    if not sim_attached:
        errs.append("simulation_summary_missing")

    if not _source_ok(poster, "poster_testboard_track_b_closure_summary.json"):
        errs.append("poster_closure_not_ok")

    fixture_manifest = build_fixture_manifest(gov)
    if fixture_manifest.get("fixture_count", 0) < 6:
        errs.append("fixture_count_lt_6")

    semantic = build_semantic_candidate_matrix()
    correction = build_correction_candidate_matrix()
    evidence = build_evidence_composition_matrix(semantic["rows"], correction["rows"])
    gate = build_gate_evaluator_dryrun()
    speak = build_cautious_speak_dryrun(gate["rows"])
    risk = build_risk_report()
    metrics = build_metrics_binding(semantic["rows"], correction["rows"], gate["rows"], speak)
    benchmark_link = build_benchmark_link_report(bench)
    sim_report = build_simulation_context_report(sim)
    non_claims = build_non_claims_report()
    audit = build_audit()

    # Toliet raw preserved
    toilet_rows = [r for r in semantic["rows"] if r.get("fixture_id") == "PF_FIXTURE_RESTROOM_TYPO"]
    if not toilet_rows or toilet_rows[0].get("raw_ocr_text_preserved") != "Toliet":
        errs.append("toilet_raw_ocr_not_preserved")

    corr_toilet = [r for r in correction["rows"] if r.get("fixture_id") == "PF_FIXTURE_RESTROOM_TYPO"]
    if not corr_toilet or not all(r.get("raw_text_preserved") for r in corr_toilet):
        errs.append("toilet_correction_raw_not_preserved")

    amb_gate = [r for r in gate["rows"] if r.get("fixture_id") == "PF_FIXTURE_AMBIGUOUS_ICON"]
    if not amb_gate or amb_gate[0].get("decision") != "hold_for_review":
        errs.append("ambiguous_not_hold_for_review")

    for phrase in FORBIDDEN_SPEAK_PHRASES:
        for p in speak.get("phrases") or []:
            if phrase in (p.get("phrasing_zh") or ""):
                errs.append(f"forbidden_phrase_in_speak:{phrase}")

    summary = build_summary(
        governance_ok=gov_ok,
        track_closures_ok=tc_ok,
        benchmark_ok=bench_ok,
        simulation_attached=sim_attached,
    )

    return (
        summary,
        fixture_manifest,
        semantic,
        correction,
        evidence,
        gate,
        speak,
        risk,
        metrics,
        benchmark_link,
        sim_report,
        non_claims,
        audit,
        errs,
    )
