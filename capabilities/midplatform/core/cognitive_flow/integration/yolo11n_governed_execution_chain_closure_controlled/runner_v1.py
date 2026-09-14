"""Compose the existing governed chain and stop at Provider Admission."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.yolo11n_producer_entry_v1 import (
    adapt_governed_bundle_to_canonical_yolo11n_records_v1,
    produce_yolo11n_governed_execution_records_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_binding_seam_v1 import (
    build_canonical_yolo11n_provider_admission_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_context_builder_v1 import (
    build_canonical_yolo11n_context_v1,
)


def _provider_admission(context: Any) -> Any:
    return build_canonical_yolo11n_provider_admission_v1(
        context=context,
        observation_demand_ref="observation-demand:closure-validation:v1",
        observation_request_ref="observation-request:closure-validation:v1",
        capability_requirement_ref="capability-requirement:object-detection:closure:v1",
        provider_session_ref="provider-session:closure-validation:v1",
        provider_candidate_ref="provider-candidate:yolo11n:closure-validation:v1",
        region_scope_candidate="bounded-single-frame",
        expected_evidence=("VISION_DETECTION",),
        bounded=True,
        trace_ref=context.trace_refs[0] if context and context.trace_refs else "trace:yolo11n:closure-validation:v1",
    )


def _compose(repo_root: Path) -> Dict[str, Any]:
    produced = produce_yolo11n_governed_execution_records_v1(repo_root)
    bundle = produced.bundle
    if bundle is None:
        return {
            "status": produced.status,
            "bundle": None,
            "records": None,
            "context": None,
            "provider_admission": None,
            "provider_invocation_executed": False,
            "failure": "GOVERNED_BUNDLE_MISSING",
        }
    records = adapt_governed_bundle_to_canonical_yolo11n_records_v1(bundle)
    if records is None:
        return {
            "status": produced.status,
            "bundle": bundle,
            "records": None,
            "context": None,
            "provider_admission": None,
            "provider_invocation_executed": False,
            "failure": "YOLO_RECORD_TRANSLATION_BLOCKED",
        }
    context_result = build_canonical_yolo11n_context_v1(records)
    if not context_result.validation.valid:
        return {
            "status": produced.status,
            "bundle": bundle,
            "records": records,
            "context": None,
            "context_result": context_result,
            "provider_admission": None,
            "provider_invocation_executed": False,
            "failure": "CANONICAL_CONTEXT_BLOCKED",
        }
    seam = _provider_admission(context_result.context)
    return {
        "status": produced.status,
        "bundle": bundle,
        "records": records,
        "context": context_result.context,
        "context_result": context_result,
        "provider_admission": seam,
        "provider_invocation_executed": False,
        "failure": None,
    }


def _negative_cases(composed: Dict[str, Any]) -> Tuple[Tuple[str, Optional[Any], str], ...]:
    bundle = composed.get("bundle")
    if bundle is None:
        return (("positive_bundle_missing", None, "GOVERNED_BUNDLE_MISSING"),)
    return (
        (
            "stale_capability_model_binding",
            replace(bundle, capability_model_binding=replace(bundle.capability_model_binding, lifecycle_status="STALE")),
            "CANONICAL_CONTEXT_BLOCKED",
        ),
        (
            "runtime_admission_blocked",
            replace(bundle, runtime_admission_assessment=replace(bundle.runtime_admission_assessment, admission_status="ADMISSION_BLOCKED_DEPENDENCY")),
            "CANONICAL_CONTEXT_BLOCKED",
        ),
        (
            "stale_executable_capability",
            replace(bundle, executable_capability=replace(bundle.executable_capability, expiry_staleness_refs=("stale:executable-capability",))),
            "CANONICAL_CONTEXT_BLOCKED",
        ),
        (
            "model_provider_mismatch",
            replace(bundle, model_provider_binding=replace(bundle.model_provider_binding, model_asset_ref="model-asset:mismatch:v1")),
            "CANONICAL_CONTEXT_BLOCKED",
        ),
        (
            "invalidation_propagation",
            replace(bundle, invalidation_refs=("invalidation:grant-revoked:closure",)),
            "YOLO_RECORD_TRANSLATION_BLOCKED",
        ),
        (
            "revoked_grant",
            replace(bundle, invalidation_refs=("grant:revoked:closure",)),
            "YOLO_RECORD_TRANSLATION_BLOCKED",
        ),
        (
            "source_version_mismatch",
            replace(bundle, executable_capability=replace(bundle.executable_capability, admitted_model_version_ref="model-version:mismatch:v1")),
            "CANONICAL_CONTEXT_BLOCKED",
        ),
    )


def _evaluate_negative(bundle: Any, expected: str) -> Dict[str, Any]:
    records = adapt_governed_bundle_to_canonical_yolo11n_records_v1(bundle)
    if records is None:
        actual = "YOLO_RECORD_TRANSLATION_BLOCKED"
    else:
        context_result = build_canonical_yolo11n_context_v1(records)
        if not context_result.validation.valid:
            actual = "CANONICAL_CONTEXT_BLOCKED"
        else:
            seam = _provider_admission(context_result.context)
            actual = "PROVIDER_ADMISSION_ALLOWED" if seam.validation.valid else "PROVIDER_ADMISSION_BLOCKED"
    return {"expected": expected, "actual": actual, "passed": actual == expected, "provider_invocation_executed": False}


def run_yolo11n_governed_execution_chain_closure_v1(repo_root: Path) -> Dict[str, Any]:
    composed = _compose(repo_root)
    bundle = composed.get("bundle")
    admission = composed.get("provider_admission")
    continuity = {
        "repository_bundle_status": composed.get("status") == "REPOSITORY_BACKED_VALIDATION_BUNDLE_PRODUCED",
        "bundle_source_refs_present": bool(bundle and bundle.source_refs),
        "bundle_to_yolo_records": composed.get("records") is not None,
        "records_to_context": composed.get("context") is not None,
        "context_to_provider_admission": bool(admission and admission.validation.valid),
        "provider_admission_candidate_created": admission is not None,
        "provider_invocation": False,
        "provider_invocation_authorized": bool(admission and admission.admission.provider_invocation_authorized),
        "capability_continuity": bool(bundle and bundle.capability_resolution and bundle.capability_model_binding and bundle.capability_resolution.module_ref == bundle.capability_model_binding.capability_ref),
        "model_identity_version_continuity": bool(bundle and bundle.capability_model_binding and bundle.model_provider_binding and bundle.capability_model_binding.model_asset_ref == bundle.model_provider_binding.model_asset_ref and bundle.capability_model_binding.model_version_ref == bundle.model_provider_binding.model_version_ref and bundle.capability_model_binding.weights_version_ref == bundle.model_provider_binding.weights_version_ref),
        "provider_continuity": bool(bundle and bundle.model_provider_binding and admission and admission.admission.canonical_model_provider_binding_ref == bundle.model_provider_binding.binding_id),
        "runtime_admission_continuity": bool(bundle and admission and admission.admission.canonical_runtime_admission_ref == bundle.runtime_admission_ref and admission.admission.canonical_runtime_admission_version == bundle.runtime_admission_version),
        "grant_constraint_continuity": bool(bundle and bundle.grant_refs and bundle.constraint_refs),
        "trace_continuity": bool(bundle and bundle.trace_refs and admission and admission.admission.trace_ref in bundle.trace_refs),
        "provenance_continuity": bool(bundle and bundle.provenance_refs and admission and set(bundle.provenance_refs).intersection(admission.admission.provenance_refs)),
        "source_version_continuity": bool(bundle and bundle.source_version_refs and admission and admission.validation.source_version_refs),
        "invalidation_continuity": bool(bundle and not bundle.invalidation_refs and admission and not admission.admission.canonical_invalidation_refs),
    }
    negative = []
    for case_id, negative_bundle, expected in _negative_cases(composed):
        negative.append({"case_id": case_id, **(_evaluate_negative(negative_bundle, expected) if negative_bundle else {"expected": expected, "actual": "GOVERNED_BUNDLE_MISSING", "passed": False, "provider_invocation_executed": False})})
    forbidden_execution_guards = {
        "provider_invocation": continuity["provider_invocation"],
    }
    continuity_positive_checks = {
        key: value
        for key, value in continuity.items()
        if key not in forbidden_execution_guards
    }
    forbidden_execution_guards_ok = all(value is False for value in forbidden_execution_guards.values())
    continuity_positive_checks_ok = all(continuity_positive_checks.values())
    return {
        "phase": "Phase-P1-Midplatform-YOLO11n-Governed-Execution-Chain-NoRuntime-Integration-Closure-v1-001",
        "chain_status": composed.get("status"),
        "continuity": continuity,
        "negative_cases": negative,
        "negative_cases_all_passed": all(item["passed"] for item in negative),
        "continuity_positive_checks_ok": continuity_positive_checks_ok,
        "forbidden_execution_guards_ok": forbidden_execution_guards_ok,
        "provider_admission_candidate_created": admission is not None,
        "provider_invocation": False,
        "model_loading": False,
        "observation_execution": False,
        "action_execution": False,
        "source_mutation": False,
        "world_truth_declared": False,
        "all_cases_passed": continuity_positive_checks_ok and forbidden_execution_guards_ok and all(item["passed"] for item in negative),
    }


def main() -> None:
    root = Path(__file__).resolve().parents[6]
    print(json.dumps(run_yolo11n_governed_execution_chain_closure_v1(root), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
