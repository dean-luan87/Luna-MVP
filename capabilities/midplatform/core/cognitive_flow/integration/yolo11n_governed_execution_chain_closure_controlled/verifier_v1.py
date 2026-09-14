"""Independent closure checks for the repository-backed no-runtime chain."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.field_perception_orchestrator.integration.yolo11n_single_frame_execution.real_yolo11n_caller_aware_verification_v1 import (
    inspect_real_yolo11n_caller_wiring_v1,
)

from .runner_v1 import run_yolo11n_governed_execution_chain_closure_v1


ENTRYPOINT_RELATIVE = Path("capabilities/midplatform/field_perception_orchestrator/integration/yolo11n_single_frame_execution/run_yolo11n_real_single_frame_provider_execution_v1.py")
AROUTE_RELATIVE = Path("capabilities/midplatform/field_perception_orchestrator/integration/run_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1.py")
PROVIDER_RELATIVE = Path("capabilities/midplatform/field_perception_orchestrator/integration/field_perception_real_vision_provider_adapter_v1.py")
CLOSURE_RELATIVE = Path("capabilities/midplatform/core/cognitive_flow/integration/yolo11n_governed_execution_chain_closure_controlled")


def _text(repo_root: Path, relative: Path) -> str:
    path = repo_root / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def verify_yolo11n_governed_execution_chain_closure_v1(repo_root: Path) -> Dict[str, Any]:
    run = run_yolo11n_governed_execution_chain_closure_v1(repo_root)
    caller = inspect_real_yolo11n_caller_wiring_v1(repo_root)
    entrypoint = _text(repo_root, ENTRYPOINT_RELATIVE)
    aroute = _text(repo_root, AROUTE_RELATIVE)
    provider = _text(repo_root, PROVIDER_RELATIVE)
    closure_files = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (repo_root / CLOSURE_RELATIVE).glob("*.py")
        if path.is_file() and path.name != "verifier_v1.py"
    )
    continuity = run["continuity"]
    checks = {
        "repository_backed_origin_ok": continuity["repository_bundle_status"] and continuity["bundle_source_refs_present"],
        "runtime_admission_continuity_ok": continuity["runtime_admission_continuity"],
        "governed_bundle_continuity_ok": continuity["bundle_to_yolo_records"],
        "yolo_translation_continuity_ok": continuity["records_to_context"],
        "canonical_context_continuity_ok": continuity["records_to_context"],
        "provider_admission_candidate_created": run["provider_admission_candidate_created"],
        "provider_invocation_false": run["provider_invocation"] is False,
        "model_loading_false": run["model_loading"] is False,
        "observation_action_false": run["observation_execution"] is False and run["action_execution"] is False,
        "source_mutation_false": run["source_mutation"] is False,
        "world_truth_false": run["world_truth_declared"] is False,
        "identity_owner_and_version_continuity_ok": continuity["capability_continuity"] and continuity["model_identity_version_continuity"] and continuity["provider_continuity"],
        "grant_constraint_continuity_ok": continuity["grant_constraint_continuity"],
        "trace_provenance_continuity_ok": continuity["trace_continuity"] and continuity["provenance_continuity"],
        "source_version_continuity_ok": continuity["source_version_continuity"],
        "invalidation_continuity_ok": continuity["invalidation_continuity"],
        "negative_integration_cases_ok": run["negative_cases_all_passed"],
        "real_entrypoint_requires_context": "context=canonical_binding" in entrypoint and "build_canonical_yolo11n_provider_admission_v1" in entrypoint,
        "a_route_requires_context_before_provider_admission": "build_canonical_yolo11n_context_v1(canonical_upstream_records)" in aroute and "context=canonical_binding" in aroute,
        "provider_shared_guard_present": "canonical_chain_validated" in provider and "canonical_invalidation_refs" in provider,
        "real_callers_no_low_level_yolo_bypass": "run_yolo_on_unit_v0" not in entrypoint and "run_yolo_on_unit_v0" not in aroute,
        "closure_does_not_invoke_provider": "run_authorized_vision_provider_v1" not in closure_files and "run_yolo_on_unit_v0" not in closure_files,
        "existing_caller_wiring_reported": bool(caller.get("checks")),
        "runner_all_cases_passed": run["all_cases_passed"] is True,
        "caller_aware_required_wiring_ok": bool(
            caller.get("all_checks_passed") is True
            and caller.get("checks", {}).get("governed_upstream_record_producer_found") is True
        ),
    }
    all_checks_passed = bool(
        all(checks.values())
        and run["all_cases_passed"] is True
        and caller.get("all_checks_passed") is True
        and caller.get("checks", {}).get("governed_upstream_record_producer_found") is True
    )
    return {
        "phase": "Phase-P1-Midplatform-YOLO11n-Governed-Execution-Chain-NoRuntime-Integration-Closure-v1-001",
        "checks": checks,
        "all_checks_passed": all_checks_passed,
        "runner": run,
        "existing_caller_aware_wiring": caller,
        "active_bypass_count": 0 if checks["real_entrypoint_requires_context"] and checks["a_route_requires_context_before_provider_admission"] and checks["provider_shared_guard_present"] else 1,
        "f001_proposed_status": "CLOSED_FOR_TARGETED_REAL_PATH" if all(checks.values()) else "MITIGATED_FAIL_CLOSED",
        "f004_proposed_status": "CLOSED_FOR_TARGETED_REAL_PATH" if checks["source_version_continuity_ok"] and checks["invalidation_continuity_ok"] else "PARTIALLY_REMEDIATED",
        "runtime_executed": False,
        "model_loaded": False,
        "provider_invoked": False,
        "observation_executed": False,
        "action_executed": False,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[6]
    print(json.dumps(verify_yolo11n_governed_execution_chain_closure_v1(root), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
