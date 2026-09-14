# -*- coding: utf-8 -*-
"""Real Chain DryRun Adapter — full collaboration orchestration loop v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.collaboration.real_chain.dryrun.evidence_package_builder_v1 import (
    build_fusion_evidence_package,
    build_packages_from_executions,
)
from capabilities.midplatform.model_manager.collaboration.real_chain.dryrun.execution_trace_graph_v1 import (
    build_execution_trace_graph,
)
from capabilities.midplatform.model_manager.collaboration.real_chain.dryrun.fusion_validation_adapter_v1 import (
    run_context_challenge_validation,
    run_evidence_conflict_validation,
    run_fusion_and_validation,
    run_ocr_failure_validation,
)
from capabilities.midplatform.model_manager.collaboration.real_chain.dryrun.provider_binding_dryrun_v1 import (
    bind_providers_for_dryrun,
    upgrade_slot_provider,
)
from capabilities.midplatform.model_manager.collaboration.real_chain.dryrun.slot_execution_simulator_v1 import (
    simulate_pipeline_chain,
)
from capabilities.midplatform.model_manager.collaboration.real_chain.slot_provider_binding_v1 import (
    bind_slot_providers,
    get_shopfront_chain_slots,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_BLOCKED"
CHAIN_ID = "shopfront_text_detection_ocr_qwen_context_v1"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _l1_shopfront() -> Dict[str, Any]:
    return {
        "situation_id": _uid("sit"),
        "scene_profile_candidate": {"scene_type": "shopfront_sign"},
        "missing_information_candidates": [{"info_type": "text_identity"}],
        "candidate_only": True,
    }


def _l2_identify_place() -> Dict[str, Any]:
    return {
        "plan_id": _uid("plan"),
        "plan_goal_candidate": {"goal_type": "identify_place"},
        "collaboration_plan": {
            "slot_1": "text_detection",
            "slot_2": "text_recognition",
            "slot_3": "context_reasoning",
        },
        "candidate_only": True,
    }


def _collaboration_plan_candidate(goal_id: str) -> Dict[str, Any]:
    return {
        "collaboration_plan_id": _uid("cpl"),
        "goal_id": goal_id,
        "collaboration_type": "pipeline",
        "slots": get_shopfront_chain_slots(),
        "collaboration_plan_candidate": True,
        "not_model_pipeline": True,
        "slot_driven": True,
        "candidate_only": True,
    }


def run_standard_shopfront_dryrun() -> Dict[str, Any]:
    """Case A: standard shopfront chain — fusion is evidence package, not fact."""
    situation = _l1_shopfront()
    plan = _l2_identify_place()
    goal_id = _uid("goal")
    collab_plan = _collaboration_plan_candidate(goal_id)

    binding = bind_providers_for_dryrun()
    bound = binding["bound_slots"]
    executions = simulate_pipeline_chain(
        bound_slots=bound,
        fixture_map={
            "slot_1": "detection_success",
            "slot_2": "ocr_success_ashu",
            "slot_3": "qwen_context_commercial",
        },
    )
    packages = build_packages_from_executions(executions)
    fusion_summary = build_fusion_evidence_package(packages)
    fv = run_fusion_and_validation(evidence_packages=packages)
    trace = build_execution_trace_graph(
        goal_id=goal_id,
        collaboration_plan_id=collab_plan["collaboration_plan_id"],
        situation=situation,
        plan=plan,
        bound_slots=bound,
        slot_executions=executions,
        evidence_packages=packages,
        validation_id=fv["validation_review"]["validation_id"],
        fusion_id=fv["fusion_candidate"].get("fusion_id"),
    )

    return {
        "case": "case_a_standard_shopfront_chain",
        "l1_situation": situation,
        "l2_plan": plan,
        "collaboration_plan": collab_plan,
        "slot_binding": binding,
        "slot_executions": executions,
        "evidence_packages": packages,
        "fusion_evidence_package": fusion_summary,
        "fusion_candidate": fv["fusion_candidate"],
        "validation_review": fv["validation_review"],
        "execution_trace_graph": trace,
        "slot_driven_not_model_pipeline": collab_plan.get("slot_driven") is True,
        "not_merged_fact": fusion_summary.get("not_merged_fact") is True,
        "three_slots_executed": len(executions) == 3,
        "candidate_only": True,
        "not_fact": True,
    }


def run_slot_provider_upgrade_dryrun() -> Dict[str, Any]:
    """Case B: ocr_v1 → ocr_v2 — only binding changes."""
    binding = bind_providers_for_dryrun()
    original_map = binding["slot_provider_binding"]
    upgrade = upgrade_slot_provider(
        slot_id="slot_2",
        new_provider_id="paddleocr_v1",
        original_binding=original_map,
    )
    upgraded_binding = bind_providers_for_dryrun(
        provider_overrides=upgrade["slot_provider_binding_after"],
    )
    return {
        "case": "case_b_slot_provider_upgrade",
        "original_binding": original_map,
        "upgrade": upgrade,
        "upgraded_binding": upgraded_binding,
        "slot_2_provider_changed": upgraded_binding["slot_provider_binding"].get("slot_2") == "paddleocr_v1",
        "l1_unchanged": upgrade.get("l1_unchanged") is True,
        "l2_unchanged": upgrade.get("l2_unchanged") is True,
        "collaboration_plan_unchanged": upgrade.get("collaboration_plan_unchanged") is True,
        "candidate_only": True,
    }


def run_ocr_failure_chain_dryrun() -> Dict[str, Any]:
    """Case C: OCR failure → incomplete evidence → replan."""
    binding = bind_providers_for_dryrun()
    bound = binding["bound_slots"]
    executions = simulate_pipeline_chain(
        bound_slots=bound,
        fixture_map={"slot_1": "detection_success", "slot_2": "ocr_failure_blurry", "slot_3": "skip"},
    )
    packages = build_packages_from_executions(executions)
    ocr_fail = next((p for p in packages if p.get("evidence_type") == "ocr_failure_candidate"), {})
    validation = run_ocr_failure_validation(ocr_failure_package=ocr_fail)

    return {
        "case": "case_c_ocr_failure_chain",
        "slot_executions": executions,
        "ocr_failure_candidate": ocr_fail,
        "validation_review": validation,
        "detection_succeeded": any(e.get("status") == "completed" and e.get("slot_id") == "slot_1" for e in executions),
        "ocr_failed": ocr_fail.get("status") == "failed",
        "qwen_not_invoked_for_guess": len([e for e in executions if e.get("slot_id") == "slot_3"]) == 0,
        "l2_replan_candidate": validation.get("l2_replan_candidate") is True,
        "not_qwen_guess": validation.get("not_qwen_guess") is True,
        "candidate_only": True,
    }


def run_context_challenge_dryrun() -> Dict[str, Any]:
    """Case D: OCR text + Qwen restaurant context — candidate only."""
    binding = bind_providers_for_dryrun()
    executions = simulate_pipeline_chain(
        bound_slots=binding["bound_slots"],
        fixture_map={
            "slot_1": "detection_success",
            "slot_2": "ocr_success_ashu",
            "slot_3": "qwen_context_restaurant",
        },
    )
    ocr_ex = next(e for e in executions if e.get("slot_id") == "slot_2")
    ctx_ex = next(e for e in executions if e.get("slot_id") == "slot_3")
    validation = run_context_challenge_validation(
        ocr_text=ocr_ex.get("payload", {}).get("text", ""),
        context_payload=ctx_ex.get("payload", {}),
    )

    return {
        "case": "case_d_context_challenge",
        "ocr_text": ocr_ex.get("payload", {}).get("text"),
        "context_evidence": ctx_ex.get("payload"),
        "validation_review": validation,
        "context_allowed": validation.get("context_evidence_allowed") is True,
        "restaurant_fact_forbidden": validation.get("restaurant_fact_forbidden") is True,
        "candidate_only": True,
    }


def run_evidence_conflict_dryrun() -> Dict[str, Any]:
    """Case E: OCR 嘉会湖 vs Qwen 机场 — no confidence override."""
    binding = bind_providers_for_dryrun()
    executions = simulate_pipeline_chain(
        bound_slots=binding["bound_slots"],
        fixture_map={
            "slot_1": "detection_success",
            "slot_2": "ocr_success_jiahui",
            "slot_3": "qwen_hypothesis_airport",
        },
    )
    ocr_ex = next(e for e in executions if e.get("slot_id") == "slot_2")
    qwen_ex = next(e for e in executions if e.get("slot_id") == "slot_3")
    result = run_evidence_conflict_validation(
        ocr_text=ocr_ex.get("payload", {}).get("text", ""),
        qwen_hypothesis=qwen_ex.get("payload", {}).get("hypothesis", ""),
        qwen_confidence=qwen_ex.get("payload", {}).get("confidence", 0.9),
    )

    return {
        "case": "case_e_evidence_conflict",
        "ocr_text": ocr_ex.get("payload", {}).get("text"),
        "qwen_hypothesis": qwen_ex.get("payload", {}).get("hypothesis"),
        **result,
        "not_confidence_override": result["evidence_conflict"].get("not_confidence_override") is True,
        "candidate_only": True,
    }


def run_full_trace_dryrun() -> Dict[str, Any]:
    """Case F: complete trace graph — goal → plan → slot → provider → evidence → validation."""
    base = run_standard_shopfront_dryrun()
    trace = base.get("execution_trace_graph") or {}
    slot_traces = trace.get("slot_traces") or []

    ids_present = {
        "goal_id": bool(trace.get("goal_id")),
        "collaboration_plan_id": bool(trace.get("collaboration_plan_id")),
        "slot_ids": all(st.get("slot_id") for st in slot_traces),
        "provider_execution_ids": all(st.get("provider_execution_id") for st in slot_traces),
        "evidence_ids": all(st.get("evidence_id") for st in slot_traces),
        "validation_id": bool(trace.get("validation_id")),
    }

    ocr_trace = next((st for st in slot_traces if st.get("capability") == "text_recognition"), {})
    why = ocr_trace.get("why_called") or {}

    return {
        "case": "case_f_full_execution_trace",
        "execution_trace_graph": trace,
        "ids_present": ids_present,
        "trace_complete": trace.get("trace_complete") is True,
        "self_explainable": trace.get("self_explainable") is True,
        "ocr_why_called": why,
        "why_has_situation_goal_capability": all(k in why for k in ("situation", "goal", "capability_required", "provider_selected", "reason")),
        "candidate_only": True,
    }


def run_real_chain_dryrun(*, case_id: Optional[str] = None) -> Dict[str, Any]:
    dispatch = {
        "case_a_standard_shopfront_chain": run_standard_shopfront_dryrun,
        "case_b_slot_provider_upgrade": run_slot_provider_upgrade_dryrun,
        "case_c_ocr_failure_chain": run_ocr_failure_chain_dryrun,
        "case_d_context_challenge": run_context_challenge_dryrun,
        "case_e_evidence_conflict": run_evidence_conflict_dryrun,
        "case_f_full_execution_trace": run_full_trace_dryrun,
    }
    if case_id and case_id in dispatch:
        return dispatch[case_id]()
    return {"phase": "Real-Multi-Model-Chain-DryRun", "dryrun_only": True}
