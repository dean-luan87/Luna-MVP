from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    not_fact,
)


def build_protocol_manager_impact_analysis_candidate_v1(
    input_candidate: Mapping[str, Any],
    compatibility_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    change_set = dict(input_candidate.get("change_set") or {})
    affected_capabilities = tuple(change_set.get("affected_capability_ids") or ())
    affected_protocols = tuple(change_set.get("affected_protocol_ids") or ())
    affected_manifests = tuple(change_set.get("affected_manifest_refs") or ())
    affected_baselines = tuple(change_set.get("affected_baseline_refs") or ())
    breaking = bool(compatibility_candidate.get("breaking_change_candidate"))
    migration_required = compatibility_candidate.get("compatibility_result") in {
        "migration_required",
        "incompatible",
    }

    recommended_actions = []
    if breaking:
        recommended_actions.append("prepare_breaking_change_review_candidate")
    if migration_required:
        recommended_actions.append("prepare_migration_plan_candidate")
    if affected_capabilities:
        recommended_actions.append("schedule_retest_for_affected_capabilities")
    if not recommended_actions:
        recommended_actions.append("no_change")

    return {
        "schema_version": "protocol_manager_impact_analysis_candidate_v1",
        "affected_capability_ids": affected_capabilities,
        "affected_protocol_ids": affected_protocols,
        "affected_manifest_refs": affected_manifests,
        "affected_baseline_refs": affected_baselines,
        "breaking_change_candidate": breaking,
        "migration_required": migration_required,
        "retest_required": bool(affected_capabilities),
        "recommended_actions": tuple(recommended_actions),
        **not_fact(),
    }
