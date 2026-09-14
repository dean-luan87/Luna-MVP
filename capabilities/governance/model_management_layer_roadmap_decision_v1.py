# -*- coding: utf-8 -*-
"""Model Management Layer Roadmap Decision v1 — route selection only, B-lite selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.model_management_layer_recovery_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
    PHASE_ID as POST_REVIEW_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Model-Management-Layer-Roadmap-Decision-v1-001"
SCOPE = "model_management_layer_roadmap_decision_only"
SOURCE_CHAIN = "model_management_layer_roadmap_decision_v1"

UPSTREAM_REQUIRED_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_NEXT_PHASE = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = "MODEL_MANAGEMENT_LAYER_ROADMAP_DECISION_READY_FOR_MODEL_REGISTRY_CANONICALIZATION_PLANNING"
FINAL_DECISION_HOLD = "MODEL_MANAGEMENT_LAYER_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Registry-Canonicalization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Management-Layer-Recovery-Issue-Review-v1-001"

ROUTE_A = "Route A — Vision / OCR / Voice Controlled Optimization"
ROUTE_B_LITE = "Route B-lite — Model Registry Canonicalization v0"
ROUTE_C = "Route C — Health Management Layer Integration"
ROUTE_D = "Route D — Skill Registry Expansion Later"

SELECTED_ROUTE = ROUTE_B_LITE
NEXT_ROUTE = ROUTE_C
DEFERRED_ROUTE_A = ROUTE_A
DEFERRED_ROUTE_D = ROUTE_D

REGISTRY_VERSION = "model_registry_canonical_v0"
SCHEMA_VERSION = "model_registry_schema_v0"
VERSION_STATUS = "baseline"
VERSION_SCOPE = "mock_fixture_and_contract_only"

SCHEMA_V0_FIELDS: Tuple[str, ...] = (
    "model_id",
    "domain",
    "provider_type",
    "runtime_mode",
    "capability_tags",
    "input_contract",
    "output_contract",
    "health_ref",
    "fallback_ref",
)

V0_MODEL_IDS: Tuple[str, ...] = (
    "vision_perspective_model_mock",
    "ocr_model_mock",
    "voice_asr_model_mock",
    "voice_tts_model_mock",
    "emotion_model_mock",
    "face_recognition_model_mock",
    "scan_model_mock",
)

V0_NOT_COVERED: Tuple[str, ...] = (
    "real OCR provider",
    "real vision provider",
    "real ASR/TTS provider",
    "map model / map skill",
    "library / hive skill",
    "external tool skill",
    "production runtime model",
)

UPDATE_TRIGGERS: Tuple[str, ...] = (
    "new model domain added",
    "real provider added",
    "controlled provider planning added",
    "health management integration added",
    "skill registry expanded",
    "map/library/hive skill added",
    "external tool provider added",
    "model output contract changed",
    "fallback strategy changed",
    "runtime boundary changed",
)

FUTURE_VERSIONS: Tuple[Dict[str, str], ...] = (
    {"version": "v0.1", "description": "field completion, naming fixes, documentation reference fixes — no new real provider"},
    {"version": "v0.2", "description": "Health Management Integration — add health fields"},
    {"version": "v0.3", "description": "Controlled Provider Planning — add provider readiness fields"},
    {"version": "v1.0", "description": "first controlled provider registry inclusion — not default real runtime"},
    {"version": "v1.1", "description": "map / library / hive / external tool Skill registry expansion"},
    {"version": "v2.0", "description": "multi-provider / multi-endpoint / local+cloud hybrid governance"},
)

B_LITE_GOALS: Tuple[str, ...] = (
    "normalize model_id naming",
    "normalize model_domain",
    "normalize provider_type",
    "normalize runtime_mode",
    "normalize capability_tags",
    "normalize input/output contract",
    "normalize health_state_ref",
    "normalize fallback_model_ref",
    "default invocation_allowed=false",
    "bind candidate output contract",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "selected_route_execution_started_now",
    "model_registry_canonicalization_started_now",
    "health_management_integration_started_now",
    "model_optimization_started_now",
    "skill_registry_expansion_started_now",
    "model_runtime_invoked_now",
    "model_provider_invoked_now",
    "ocr_provider_invoked_now",
    "vision_model_invoked_now",
    "voice_model_invoked_now",
    "emotion_model_invoked_now",
    "face_recognition_model_invoked_now",
    "scan_model_invoked_now",
    "model_switch_executed_now",
    "model_update_executed_now",
    "model_repair_executed_now",
    "runtime_enabled_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
    "world_model_written_now",
    "memory_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ model registry canonical table implemented",
    "Route B-lite selected ≠ model invocation enabled",
    "Route B-lite selected ≠ provider or runtime started",
    "Route A deferred ≠ Vision/OCR/Voice optimization abandoned",
    "Route C next_after_b_lite ≠ health monitor enabled now",
    "Route D deferred_later ≠ skill registry expansion started",
    "Canonicalization planning next ≠ real model calls",
    "model_registry_canonical_v0 ≠ final model registry",
    "model_registry_canonical_v0 ≠ real provider enabled",
    "model_registry_canonical_v0 ≠ production runtime ready",
    "schema_version_v0 may be upgraded later",
    "future Skill / map / library / hive integration may require version bump",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "model_management_layer_roadmap_decision_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _version_meta() -> Dict[str, Any]:
    return {
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "selected_registry_baseline_version": REGISTRY_VERSION,
        "selected_schema_version": SCHEMA_VERSION,
        "version_status": VERSION_STATUS,
        "version_scope": VERSION_SCOPE,
        "future_update_expected": True,
        "real_provider_included": False,
        "production_runtime_included": False,
    }


def _version_note_markdown() -> str:
    return f"""# Model Registry Version Note — {REGISTRY_VERSION}

**Version:** `{REGISTRY_VERSION}`

## 含义

Luna 模型管理层第一版 canonical registry baseline。该版本只归一化当前已存在的 mock/fixture model registry、skill registry dryrun、capability descriptor、model output contract、health_state_ref、fallback_model_ref。不启用真实模型，不接真实 provider，不代表最终模型体系。

## 双层版号

| 层 | 版号 | 说明 |
|---|---|---|
| 内容版本 | `{REGISTRY_VERSION}` | 当前 7 个 mock/fixture model entry + 6 个 skill dryrun entry 的归一化台账 |
| 结构版本 | `{SCHEMA_VERSION}` | 字段结构：{' / '.join(SCHEMA_V0_FIELDS)} |

## 适用范围（v0 覆盖）

{chr(10).join(f'- `{mid}`' for mid in V0_MODEL_IDS)}

## 不覆盖

{chr(10).join(f'- {item}' for item in V0_NOT_COVERED)}

## 后续版本预留

{chr(10).join(f'- **{fv["version"]}**：{fv["description"]}' for fv in FUTURE_VERSIONS)}

## Non-Claims

- `{REGISTRY_VERSION}` ≠ final model registry
- `{REGISTRY_VERSION}` ≠ real provider enabled
- `{REGISTRY_VERSION}` ≠ production runtime ready
- `{SCHEMA_VERSION}` may be upgraded later
- future Skill / map / library / hive integration may require version bump
"""


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_model_management_layer_roadmap_decision_v1(
    *,
    model_management_layer_recovery_post_dryrun_review_root: str,
    model_management_layer_recovery_dryrun_root: Optional[str] = None,
    model_management_layer_recovery_planning_root: Optional[str] = None,
    midplatform_module_gap_and_roadmap_planning_root: Optional[str] = None,
    midplatform_backbone_definition_alignment_root: Optional[str] = None,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(model_management_layer_recovery_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    next_opt = _try_read_json(post_root / "next_model_optimization_readiness_decision_v1.json") or {}

    dryrun_root = Path(
        model_management_layer_recovery_dryrun_root
        or post_sm.get("upstream_dryrun_root")
        or post_root.parent / "model_management_layer_recovery_dryrun"
    ).expanduser().resolve()
    planning_root = Path(
        model_management_layer_recovery_planning_root
        or post_root.parent / "model_management_layer_recovery_planning"
    ).expanduser().resolve()
    gap_root = Path(
        midplatform_module_gap_and_roadmap_planning_root
        or post_root.parent / "midplatform_module_gap_and_roadmap_planning"
    ).expanduser().resolve()
    backbone_root = Path(
        midplatform_backbone_definition_alignment_root
        or post_root.parent / "midplatform_backbone_definition_alignment"
    ).expanduser().resolve()

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else post_root.parent / "model_management_layer_roadmap_decision"
    )

    meta = {
        **_boundary_meta(),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_planning_root": str(planning_root),
        "upstream_gap_planning_root": str(gap_root),
        "upstream_backbone_alignment_root": str(backbone_root),
        "output_root": str(out_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    planning_sm = _try_read_json(planning_root / "summary.json") or {}
    gap_sm = _try_read_json(gap_root / "summary.json") or {}
    backbone_sm = _try_read_json(backbone_root / "summary.json") or {}
    registry = _try_read_json(dryrun_root / "mock_fixture_model_registry_v1.json") or {}

    verifier_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not verifier_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("post-review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("post-review recommended_next_phase mismatch")
    if post_sm.get("governance_skeleton_consumable") is not True:
        blockers.append("governance_skeleton_consumable must be true")
    if post_sm.get("boundary_ok") is not True:
        blockers.append("post-review boundary_ok must be true")

    counts = {
        "mock_fixture_model_registry": dryrun_sm.get("model_registry_entry_count", len(registry.get("entries") or [])),
        "skill_registry_dryrun": dryrun_sm.get("skill_registry_entry_count", 0),
        "model_health_state_candidate": dryrun_sm.get("health_candidate_count", 0),
        "model_switching_candidate": dryrun_sm.get("switching_candidate_count", 0),
        "output_contract": len(
            (_try_read_json(dryrun_root / "model_output_contract_integration_result_v1.json") or {}).get(
                "output_types"
            )
            or []
        ),
    }
    expected = {
        "mock_fixture_model_registry": 7,
        "skill_registry_dryrun": 6,
        "model_health_state_candidate": 6,
        "model_switching_candidate": 6,
        "output_contract": 7,
    }
    for key, exp in expected.items():
        if counts[key] != exp:
            blockers.append(f"{key} count must be {exp}")

    for field in (
        "model_runtime_invoked_now",
        "model_provider_invoked_now",
        "model_switch_executed_now",
    ):
        if dryrun_sm.get(field) is True or post_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    for field in BOUNDARY_FALSE:
        if post_sm.get(field) is True:
            blockers.append(f"post-review {field} must be false")

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("dryrun verifier should be GO")
    if planning_sm.get("boundary_ok") is not True:
        blockers.append("planning upstream should be boundary_ok")

    input_review = {
        "review_id": "model_management_post_review_input_review_v1",
        "upstream_post_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_planning_root": str(planning_root),
        "upstream_gap_planning_root": str(gap_root),
        "upstream_backbone_alignment_root": str(backbone_root),
        "upstream_verifier_go": verifier_go,
        "upstream_final_decision": post_sm.get("final_decision"),
        "governance_skeleton_consumable": post_sm.get("governance_skeleton_consumable"),
        "counts": counts,
        "b_foundation_exists": dryrun_sm.get("model_registry_entry_count", 0) >= 7,
        "c_partial_only": True,
        "d_deferred_until_map_library_hive": True,
        "prior_preferred_route_a": next_opt.get("preferred_route"),
        "user_selected_route_b_lite": True,
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_vision_ocr_voice_optimization_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "deferred",
        "business_value": "high",
        "defer_reasons": [
            "depends on canonical model registry ledger",
            "depends on health/degradation mechanisms",
            "must not enable real provider directly",
            "starts from mock to controlled provider planning after B-lite and C",
        ],
        "resume_entry": "mock_to_controlled_provider_planning",
        **meta,
    }

    route_b_lite = {
        "assessment_id": "route_b_lite_model_registry_canonicalization_assessment_v1",
        "route_id": "B-lite",
        "route_label": ROUTE_B_LITE,
        "status": "selected",
        "selection_reasons": [
            "B foundation already exists from recovery dryrun — not greenfield",
            "mock/fixture registry, IO specs, capability descriptor, output contract already present",
            "consolidate scattered definitions into Model Registry Canonical Table v0 (model_registry_canonical_v0)",
            "versioned baseline — not final model system; schema_version model_registry_schema_v0",
            "no model invocation, no runtime, no provider implementation",
            "user explicitly selected B-lite over Route A for this cycle",
        ],
        "b_lite_goals": list(B_LITE_GOALS),
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "version_status": VERSION_STATUS,
        "not_in_scope": [
            "deep model registry implementation",
            "real provider enablement",
            "model optimization execution",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_health_management_integration_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "next_after_b_lite",
        "partial_coverage_note": "health candidate matrix exists; full layer integration not done",
        "focus_after_b_lite": [
            "health_warning to survival_drive_candidate",
            "model failure to fallback candidate",
            "hardware pressure to degradation candidate",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_skill_registry_expansion_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred_later",
        "defer_reasons": [
            "avoid premature abstraction",
            "wait until map, library, hive, external tools integration prep",
            "skill registry dryrun sufficient for governance skeleton",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "model_management_route_selection_matrix_v1",
        "routes": [
            {"route_id": "A", "label": ROUTE_A, "status": "deferred"},
            {"route_id": "B-lite", "label": ROUTE_B_LITE, "status": "selected"},
            {"route_id": "C", "label": ROUTE_C, "status": "next_after_b_lite"},
            {"route_id": "D", "label": ROUTE_D, "status": "deferred_later"},
        ],
        "selected_route": SELECTED_ROUTE,
        "next_route": NEXT_ROUTE,
        "deferred_route_a": DEFERRED_ROUTE_A,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "decision_basis": [
            "post-dryrun review GO and governance skeleton consumable",
            "mock registry 7 + skill 6 + health 6 + switching 6 + output 7 verified",
            "B foundation from recovery dryrun/planning",
            "user selection B-lite",
        ],
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions_met": input_review.get("review_pass") is True,
        "requires": [
            "post_dryrun_review GO",
            "dryrun mock_fixture_model_registry and contracts trusted",
            "roadmap decision selects B-lite only",
            "canonicalization planning is next — still no invocation",
        ],
        "must_remain_false_until_canonicalization_planning": list(BOUNDARY_FALSE),
        "recommended_next_phase": NEXT_PHASE_GO,
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_routes": [
            {
                "route": DEFERRED_ROUTE_A,
                "status": "deferred",
                "earliest_resume": "after B-lite v0 canonical baseline and Route C health integration planning",
            },
            {
                "route": ROUTE_C,
                "status": "next_after_b_lite",
                "note": "not deferred — scheduled immediately after B-lite planning closure",
            },
            {
                "route": DEFERRED_ROUTE_D,
                "status": "deferred_later",
                "earliest_resume": "before map/library/hive external tool integration",
            },
        ],
        **meta,
    }

    decision_ok = input_review.get("review_pass") is True

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_model_registry_canonicalization_planning": decision_ok,
        "selected_route": SELECTED_ROUTE,
        "next_route": NEXT_ROUTE,
        "recommended_next_phase": NEXT_PHASE_GO if decision_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if decision_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "model_management_roadmap_decision_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "principles": [
            "decision_only_no_implementation",
            "B_lite_selected_A_deferred_C_next_after_b_lite_D_deferred_later",
            "no_model_no_provider_no_runtime",
        ],
        "selected_route": SELECTED_ROUTE,
        "next_route": NEXT_ROUTE,
        **meta,
    }

    versioning_policy = {
        "policy_id": "model_registry_versioning_policy_v1",
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        "version_status": VERSION_STATUS,
        "version_scope": VERSION_SCOPE,
        "future_update_expected": True,
        "real_provider_included": False,
        "production_runtime_included": False,
        "schema_v0_fields": list(SCHEMA_V0_FIELDS),
        "v0_model_ids": list(V0_MODEL_IDS),
        "v0_not_covered": list(V0_NOT_COVERED),
        "update_triggers": list(UPDATE_TRIGGERS),
        "future_versions": list(FUTURE_VERSIONS),
        "dual_version_semantics": {
            "registry_version": "content version of canonical model registry ledger",
            "schema_version": "field structure version of registry schema",
        },
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary_out = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": decision_ok,
        "violations": blockers,
        "final_decision": next_readiness["final_decision"],
        "recommended_next_phase": next_readiness["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "next_route": NEXT_ROUTE,
        "deferred_route_a": DEFERRED_ROUTE_A,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "high_risk_count": 0 if decision_ok else 1,
        "counts": counts,
        **_version_meta(),
        **meta,
    }

    return {
        "model_management_roadmap_decision_policy": policy,
        "model_management_post_review_input_review": input_review,
        "route_a_vision_ocr_voice_optimization_assessment": route_a,
        "route_b_lite_model_registry_canonicalization_assessment": route_b_lite,
        "route_c_health_management_integration_assessment": route_c,
        "route_d_skill_registry_expansion_assessment": route_d,
        "model_management_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "model_registry_versioning_policy": versioning_policy,
        "model_registry_version_note_v0_md": _version_note_markdown(),
        "non_claims_register": non_claims,
        "summary": summary_out,
    }
