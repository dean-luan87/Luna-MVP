# -*- coding: utf-8 -*-
"""Upgrade v2 gated Evidence Packs to v1 with scan_observation / gate refs.

Phase-OCR-Evidence-Pack-Adapter-v1-ScanObservation-Alignment-001
"""

from __future__ import annotations

import copy
import json
import uuid
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Evidence-Pack-Adapter-v1-ScanObservation-Alignment-001"
PACK_SCHEMA_V0 = "ocr_text_evidence_pack_v0"
PACK_SCHEMA_V1 = "ocr_text_evidence_pack_v1"
ADAPTER_STEP = "ocr_evidence_pack_adapter_v1_scan_observation_alignment"
GATED_PHASE = "Mixed-Video-Poster-Batch-Smoke-v2-Gated-Path-Only-001"

SPATIAL_NULL: Dict[str, Any] = {
    "coordinate_source": "unknown",
    "gps_lat": None,
    "gps_lng": None,
    "gps_accuracy_m": None,
    "map_anchor_id": None,
    "place_candidate_id": None,
    "relative_position": {"distance_m": None, "bearing_deg": None, "height_relative_m": None},
    "spatial_confidence": None,
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _index_rows(rows: List[Any], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        if isinstance(r, dict) and r.get(key):
            out[str(r[key])] = r
    return out


def _upgrade_gated_pack(
    pack: Dict[str, Any],
    *,
    sq_row: Optional[Dict[str, Any]],
    read_row: Optional[Dict[str, Any]],
    req_row: Optional[Dict[str, Any]],
    trace_row: Optional[Dict[str, Any]],
    gated_path_root: str,
    linebox_trace_root: str,
) -> Dict[str, Any]:
    p = copy.deepcopy(pack)
    p["schema_version"] = PACK_SCHEMA_V1
    ic_ref = p.get("input_candidate_ref") or (p.get("source") or {}).get("input_candidate_ref")
    sq_grade = (sq_row or {}).get("source_quality_grade") or (p.get("source_quality") or {}).get("source_quality_grade")
    read_grade = (read_row or {}).get("readability_grade") or (p.get("readability_quality") or {}).get("readability_grade")
    ocr_ref = p.get("ocr_request_ref") or (p.get("source") or {}).get("ocr_request_ref") or {}

    scan_ref = None
    frame_id = (p.get("source") or {}).get("frame_id")
    if frame_id:
        scan_ref = f"scan_obs:{frame_id}"
    elif ic_ref and str(ic_ref).startswith("img_"):
        scan_ref = f"scan_obs:{ic_ref}"

    p["scan_observation_ref"] = scan_ref
    p["source_quality_grade"] = sq_grade
    p["readability_gate_ref"] = {
        "readability_grade": read_grade,
        "readability_gate_decision": (read_row or {}).get("readability_gate_decision"),
        "ocr_request_allowed": (read_row or {}).get("ocr_request_allowed"),
    }
    p["ocr_request_ref"] = ocr_ref
    p["gated_path_ref"] = {
        "phase": GATED_PHASE,
        "mixed_batch_v2_output_root": gated_path_root,
        "ocr_mainline_bridge_required": True,
        "provider_call_id": (trace_row or {}).get("provider_call_id"),
    }
    p["input_candidate_ref"] = ic_ref
    p["evidence_tier"] = "gated_ocr_primary"
    p["evidence_role"] = "primary_ocr_evidence_from_gated_submission"

    gov = p.get("governance") if isinstance(p.get("governance"), dict) else {}
    gov.update(
        {
            "scan_observation_not_primary_evidence": True,
            "full_frame_scan_primary": False,
            "primary_evidence_from_gated_ocr": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
    )
    p["governance"] = gov

    src = p.get("source") if isinstance(p.get("source"), dict) else {}
    chain = list(src.get("source_chain") or [])
    if ADAPTER_STEP not in chain:
        chain.append(ADAPTER_STEP)
    src["source_chain"] = chain
    src["ocr_request_ref"] = ocr_ref
    src["gated_path_ref"] = p["gated_path_ref"]
    src["scan_observation_ref"] = scan_ref
    p["source"] = src

    if "spatial_coordinates" not in p or not p["spatial_coordinates"]:
        p["spatial_coordinates"] = copy.deepcopy(SPATIAL_NULL)

    p["source_quality"] = {
        "source_quality_grade": sq_grade,
        "gate_decision": (sq_row or {}).get("gate_decision"),
        "reason_codes": (sq_row or {}).get("reason_codes") or [],
    }
    p["adapter_metadata"] = {
        "upgraded_from_schema": PACK_SCHEMA_V0,
        "linebox_trace_root": linebox_trace_root if scan_ref else None,
        "ocr_request_id": (req_row or {}).get("ocr_request_id"),
    }
    return p


def _scan_sidecar_entry(obs: Dict[str, Any], routing: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    route = (routing or {}).get("route") or "scan_observation_only"
    return {
        "sidecar_id": f"scan_sidecar_{obs.get('scan_observation_id', uuid.uuid4().hex[:8])}",
        "sidecar_type": "ScanObservationSidecar",
        "schema_version": "ocr_scan_observation_sidecar_v1",
        "scan_observation_ref": obs.get("scan_observation_id"),
        "scan_observation_id": obs.get("scan_observation_id"),
        "source_id": obs.get("source_id"),
        "frame_id": obs.get("frame_id"),
        "image_id": obs.get("image_id"),
        "ocr_preview_or_text_hint": obs.get("ocr_preview_or_text_hint"),
        "linebox_refs": obs.get("linebox_refs") or [],
        "source_quality_grade": obs.get("source_quality_grade"),
        "readability_gate_ref": {
            "readability_grade": "unknown",
            "note": "scan_only_no_gated_ocr_pack",
        },
        "ocr_request_ref": None,
        "gated_path_ref": {"phase": GATED_PHASE},
        "evidence_tier": "scan_observation_only",
        "evidence_role": "non_primary_scan_observation",
        "routing_ref": route,
        "reason_not_primary_evidence": obs.get("reason_not_primary_evidence"),
        "suggested_next_action": obs.get("suggested_next_action"),
        "governance": {
            "scan_observation_not_primary_evidence": True,
            "is_ocr_text_evidence_pack": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0(
    *,
    output_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    evidence_pack_contract_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    out = Path(output_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    contract = Path(evidence_pack_contract_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    for label, p in [("mixed_batch_v2", v2), ("contract", contract)]:
        if not p.is_dir():
            errs.append(f"missing_root:{label}")

    v2_packs_doc = _read_json(v2 / "mixed_batch_v2_ocr_evidence_pack_collection.json") or {}
    v2_packs = [p for p in (v2_packs_doc.get("packs") or []) if isinstance(p, dict)]
    scan_doc = _read_json(v2 / "mixed_batch_v2_scan_observation_report.json") or {}
    scan_obs = [s for s in (scan_doc.get("scan_observations") or []) if isinstance(s, dict)]
    routing_rows = (_read_json(v2 / "mixed_batch_v2_routing_matrix.json") or {}).get("rows") or []
    sq_rows = (_read_json(v2 / "mixed_batch_v2_source_quality_gate_decision_matrix.json") or {}).get("rows") or []
    read_rows = (_read_json(v2 / "mixed_batch_v2_readability_gate_decision_matrix.json") or {}).get("rows") or []
    req_rows = (_read_json(v2 / "mixed_batch_v2_ocr_request_candidate_matrix.json") or {}).get("rows") or []
    trace_rows = (_read_json(v2 / "mixed_batch_v2_ocr_request_gated_submission_trace.json") or {}).get("rows") or []
    vs_pf = _read_json(v2 / "mixed_batch_v2_visual_symbol_public_facility_routing_report.json") or {}

    sq_by_cid = _index_rows(sq_rows, "input_candidate_id")
    sq_by_cid.update(_index_rows(sq_rows, "candidate_id"))
    read_by_cid = _index_rows(read_rows, "candidate_id")
    route_by_cid = _index_rows(routing_rows, "candidate_id")
    req_by_ic = {r.get("input_candidate_id"): r for r in req_rows if isinstance(r, dict)}
    trace_by_ic = {t.get("input_candidate_id"): t for t in trace_rows if isinstance(t, dict)}

    # frame-level keys
    for r in sq_rows:
        if isinstance(r, dict) and r.get("input_candidate_id", "").startswith("frame_"):
            sq_by_cid[r["input_candidate_id"]] = r
    for r in read_rows:
        cid = r.get("candidate_id")
        if cid:
            read_by_cid[cid] = r
    for r in routing_rows:
        cid = r.get("candidate_id")
        if cid:
            route_by_cid[cid] = r

    gated_v1: List[Dict[str, Any]] = []
    for pack in v2_packs:
        ic = pack.get("input_candidate_ref") or ""
        if ic.startswith("frame_"):
            cid = ic
        else:
            cid = ic
        req = req_by_ic.get(ic) or req_by_ic.get(cid)
        ocr_id = (req or {}).get("ocr_request_id")
        trace = trace_by_ic.get(ic)
        if ocr_id:
            for t in trace_rows:
                if isinstance(t, dict) and t.get("ocr_request_id") == ocr_id:
                    trace = t
                    break
        gated_v1.append(
            _upgrade_gated_pack(
                pack,
                sq_row=sq_by_cid.get(ic) or sq_by_cid.get(cid),
                read_row=read_by_cid.get(ic) or read_by_cid.get(cid),
                req_row=req,
                trace_row=trace,
                gated_path_root=str(v2),
                linebox_trace_root=str(linebox),
            )
        )

    scan_sidecars: List[Dict[str, Any]] = []
    gated_ic_refs = {p.get("input_candidate_ref") for p in gated_v1}
    for obs in scan_obs:
        sid = obs.get("scan_observation_id", "")
        ic_guess = obs.get("source_id", "")
        if obs.get("image_id"):
            ic_guess = f"img_{obs['image_id']}"
        if ic_guess in gated_ic_refs:
            continue
        scan_sidecars.append(_scan_sidecar_entry(obs, route_by_cid.get(ic_guess)))

    visual_sidecars: List[Dict[str, Any]] = []
    pf_sidecars: List[Dict[str, Any]] = []
    for r in routing_rows:
        if not isinstance(r, dict):
            continue
        cid = r.get("candidate_id", "")
        if r.get("route") == "visual_symbol_candidate":
            visual_sidecars.append(
                {
                    "sidecar_id": f"vs_sidecar_{cid}",
                    "sidecar_type": "VisualSymbolCandidateSidecar",
                    "input_candidate_ref": cid,
                    "source_id": r.get("source_id"),
                    "source_quality_grade": (sq_by_cid.get(cid) or {}).get("source_quality_grade"),
                    "ocr_request_ref": None,
                    "evidence_tier": "visual_symbol_route",
                    "evidence_role": "non_ocr_visual_symbol",
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )
        elif r.get("route") == "public_facility_semantic_first":
            pf_sidecars.append(
                {
                    "sidecar_id": f"pf_sidecar_{cid}",
                    "sidecar_type": "PublicFacilitySemanticSidecar",
                    "input_candidate_ref": cid,
                    "source_id": r.get("source_id"),
                    "evidence_tier": "public_facility_semantic_first",
                    "ocr_request_ref": None,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )

    schema_delta = {
        "schema_version": "ocr_evidence_pack_v1_schema_delta_v0",
        "base_schema": PACK_SCHEMA_V0,
        "target_schema": PACK_SCHEMA_V1,
        "new_top_level_fields": [
            "scan_observation_ref",
            "source_quality_grade",
            "readability_gate_ref",
            "ocr_request_ref",
            "gated_path_ref",
            "input_candidate_ref",
            "evidence_tier",
            "evidence_role",
            "source_quality",
            "adapter_metadata",
        ],
        "governance_additions": [
            "scan_observation_not_primary_evidence",
            "primary_evidence_from_gated_ocr",
        ],
        "hierarchy": {
            "gated_ocr_primary": "OCRTextEvidencePack from ocr_mainline_bridge only",
            "scan_observation_only": "ScanObservationSidecar; not OCRTextEvidence primary",
            "visual_symbol_route": "VisualSymbolCandidateSidecar; no ordinary OCR pack",
            "public_facility_semantic_first": "semantic-first; OCR auxiliary only",
        },
    }

    hierarchy = {
        "schema_version": "ocr_scan_vs_gated_evidence_hierarchy_report_v0",
        "gated_ocr_primary_count": len(gated_v1),
        "scan_observation_sidecar_count": len(scan_sidecars),
        "visual_symbol_sidecar_count": len(visual_sidecars),
        "public_facility_sidecar_count": len(pf_sidecars),
        "full_frame_scan_not_primary_evidence": True,
        "scan_observation_is_not_ocr_text_evidence_pack": True,
        "gated_pack_must_have_ocr_request_ref": True,
        "rules": [
            "Only gated_ocr_primary tier may populate OCRTextEvidencePack.raw_ocr as primary evidence",
            "scan_observation_only tier must not create primary OCRTextEvidencePack without ocr_request_ref",
            "SQ_D routes to visual_symbol sidecar, not ordinary OCR pack",
            "SQ_E blocked; scan sidecar may retain preview hint only",
        ],
    }

    field_coverage = {
        "schema_version": "ocr_evidence_pack_v1_field_coverage_report_v0",
        "gated_pack_count": len(gated_v1),
        "with_scan_observation_ref": sum(1 for p in gated_v1 if p.get("scan_observation_ref") is not None),
        "with_source_quality_grade": sum(1 for p in gated_v1 if p.get("source_quality_grade")),
        "with_readability_gate_ref": sum(1 for p in gated_v1 if p.get("readability_gate_ref")),
        "with_ocr_request_ref": sum(1 for p in gated_v1 if (p.get("ocr_request_ref") or {}).get("request_id")),
        "with_gated_path_ref": sum(1 for p in gated_v1 if p.get("gated_path_ref")),
        "with_evidence_tier": sum(1 for p in gated_v1 if p.get("evidence_tier") == "gated_ocr_primary"),
        "all_gated_have_ocr_request_ref": all((p.get("ocr_request_ref") or {}).get("request_id") for p in gated_v1) if gated_v1 else True,
    }

    semantic_readiness = {
        "schema_version": "ocr_semantic_candidate_v1_readiness_report_v0",
        "ready_for_semantic_candidate_v1": True,
        "classification_rules": [
            {
                "tier": "gated_ocr_primary",
                "semantic_policy": "may_generate_meaning_candidate_with_review",
                "requires": ["ocr_request_ref", "evidence_pack_ref"],
            },
            {
                "tier": "scan_observation_only",
                "semantic_policy": "uncertain_or_deferred_only",
                "requires": ["scan_observation_ref"],
                "forbidden": ["strong_entity_candidate", "world_model_attach"],
            },
            {
                "tier": "visual_symbol_route",
                "semantic_policy": "route_visual_symbol_registry",
                "forbidden": ["ordinary_text_entity_candidate"],
            },
            {
                "tier": "sq_e_blocked",
                "semantic_policy": "no_strong_entity",
                "forbidden": ["world_model_attach"],
            },
        ],
        "distinction_matrix": {
            "scan_saw_but_not_ocr": "scan_observation_sidecar without matching gated pack",
            "gated_ocr_success": "gated_v1 pack with ocr_request_ref",
            "sq_d_visual_symbol": "visual_symbol_sidecar",
            "sq_e_blocked": "scan_sidecar or routing rejected_unreadable",
        },
    }

    routing_index = {
        "schema_version": "ocr_evidence_pack_v1_routing_alignment_index_v0",
        "row_count": len(routing_rows),
        "entries": [
            {
                "candidate_id": r.get("candidate_id"),
                "source_id": r.get("source_id"),
                "route": r.get("route"),
                "has_gated_pack": r.get("candidate_id") in gated_ic_refs or r.get("generated_ocr_request"),
                "has_scan_sidecar": any(s.get("source_id") == r.get("source_id") for s in scan_sidecars),
            }
            for r in routing_rows
            if isinstance(r, dict)
        ],
    }

    summary = {
        "schema_version": "ocr_evidence_pack_adapter_v1_scan_observation_alignment_summary_v0",
        "phase": PHASE_ID,
        "adapter_scope": "evidence_pack_v1_from_mixed_batch_v2_gated_only",
        "based_on_mixed_batch_v2": True,
        "based_on_linebox_sq_gate": linebox.is_dir(),
        "based_on_evidence_pack_contract": contract.is_dir(),
        "pack_schema_upgraded_to": PACK_SCHEMA_V1,
        "gated_pack_count": len(gated_v1),
        "scan_observation_sidecar_count": len(scan_sidecars),
        "visual_symbol_sidecar_count": len(visual_sidecars),
        "public_facility_sidecar_count": len(pf_sidecars),
        "every_gated_pack_has_ocr_request_ref": field_coverage["all_gated_have_ocr_request_ref"],
        "scan_observation_not_primary_evidence": True,
        "ocr_invoked": False,
        "semantic_candidate_generated": False,
        "world_model_attach_executed": False,
        "midplatform_fact_written": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if not errs and field_coverage["all_gated_have_ocr_request_ref"] else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    return {
        "summary": summary,
        "schema_delta": schema_delta,
        "gated_collection": {
            "schema_version": "ocr_evidence_pack_v1_gated_collection_v0",
            "pack_count": len(gated_v1),
            "every_pack_has_ocr_request_ref": field_coverage["all_gated_have_ocr_request_ref"],
            "packs": gated_v1,
        },
        "scan_sidecar_collection": {
            "schema_version": "ocr_evidence_pack_v1_scan_observation_sidecar_collection_v0",
            "sidecar_count": len(scan_sidecars),
            "scan_observations": scan_sidecars,
        },
        "routing_sidecar": {
            "schema_version": "ocr_evidence_pack_v1_routing_sidecar_index_v0",
            "visual_symbol_candidates": visual_sidecars,
            "public_facility_candidates": pf_sidecars,
        },
        "routing_index": routing_index,
        "hierarchy": hierarchy,
        "field_coverage": field_coverage,
        "semantic_readiness": semantic_readiness,
        "scan_ref_alignment": {
            "schema_version": "ocr_scan_observation_ref_alignment_report_v0",
            "scan_observation_count": len(scan_obs),
            "scan_sidecar_count": len(scan_sidecars),
            "gated_with_scan_ref_count": field_coverage["with_scan_observation_ref"],
            "scan_ref_on_gated_is_cross_link_only": True,
        },
        "gated_path_alignment": {
            "schema_version": "ocr_gated_path_ref_alignment_report_v0",
            "gated_path_phase": GATED_PHASE,
            "gated_path_root": str(v2),
            "packs_with_gated_path_ref": field_coverage["with_gated_path_ref"],
        },
        "unified_index": {
            "schema_version": "ocr_evidence_pack_v1_unified_index_v0",
            "gated_pack_ids": [p.get("evidence_id") for p in gated_v1],
            "scan_sidecar_ids": [s.get("sidecar_id") for s in scan_sidecars],
            "visual_symbol_sidecar_ids": [v.get("sidecar_id") for v in visual_sidecars],
        },
        "benchmark_link": {
            "schema_version": "ocr_evidence_pack_adapter_v1_benchmark_link_report_v0",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "ocr_evidence_pack_adapter_v1_system_health_link_report_v0",
            "system_health_governance_available": health.is_dir(),
            "provider_health_runtime_checked": False,
        },
        "boundary": {
            "schema_version": "ocr_evidence_pack_adapter_v1_no_write_boundary_report_v0",
            "boundary_ok": True,
            "violations": [],
            "adapter_only": True,
            "ocr_invoked": False,
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
        },
        "sim_report": {
            "schema_version": "ocr_evidence_pack_adapter_v1_simulation_context_report_v0",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get("simulation_profile_id") or "developer_full",
            "simulation_context_only": True,
        },
        "non_claims": {
            "schema_version": "ocr_evidence_pack_adapter_v1_non_claims_report_v0",
            "not_production_ocr": True,
            "not_accuracy_benchmark": True,
            "not_semantic_v1_executed": True,
            "adapter_aligns_structure_only": True,
        },
        "followups": {
            "schema_version": "ocr_evidence_pack_adapter_v1_open_followups_v0",
            "items": [
                "Semantic Candidate Generator v1 using evidence_tier",
                "Improve SQ_B poster ROI pass policy",
                "ROI Crop Proposal for blocked scan observations",
                "SystemHealth provider runtime dry-run",
                "Benchmark T2 collector with GT",
            ],
        },
        "audit": {
            "schema_version": "ocr_evidence_pack_adapter_v1_audit_report_v0",
            "adapter_v1_scan_observation_alignment_executed": True,
            "ocr_invoked": False,
            "gated_pack_count": len(gated_v1),
            "scan_sidecar_count": len(scan_sidecars),
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
        },
        "errs": errs,
    }
