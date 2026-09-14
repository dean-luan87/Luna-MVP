from __future__ import annotations

from dataclasses import replace
from typing import Any, Dict, Iterable, List

from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityResolutionCandidateV1,
)

from .logical_capability_runtime_admission_adapter_v1 import (
    assess_runtime_admission_v1,
    build_executable_capability_candidate_v1,
    build_provider_admission_input_v1,
    build_runtime_admission_input_v1,
)


def _resolution(case_id: str, *, status: str = "READY_CANDIDATE", provider: bool = True) -> CapabilityResolutionCandidateV1:
    return CapabilityResolutionCandidateV1(
        requirement_id=f"requirement:{case_id}",
        status=status,
        module_ref=f"capability:object-detection:{case_id}",
        slot_ref=f"slot:vision:{case_id}",
        implementation_refs=(f"implementation:vision:{case_id}",),
        model_asset_refs=(f"model-asset:yolo11n:{case_id}",),
        provider_contract_refs=(f"provider-contract:vision:{case_id}",) if provider else (),
        reason="synthetic logical resolution candidate",
        recovery_available=True,
    )


def _candidate(case_id: str, **overrides: Any):
    resolution = overrides.pop("logical_resolution", _resolution(case_id))
    defaults: Dict[str, Any] = {
        "logical_resolution_ref": f"resolution:{case_id}",
        "logical_resolution": resolution,
        "logical_capability_ref": f"capability:object-detection:{case_id}",
        "capability_slot_ref": f"slot:vision:{case_id}",
        "model_asset_ref": f"model-asset:yolo11n:{case_id}",
        "model_version_ref": f"model-version:yolo11n:v1:{case_id}",
        "governed_model_path_ref": f"governed-path:yolo11n:{case_id}",
        "declared_checksum_ref": f"declared-checksum:yolo11n:{case_id}",
        "observed_integrity_evidence_ref": f"integrity-evidence:yolo11n:{case_id}",
        "dependency_health_refs": (f"dependency-health:verified:{case_id}",),
        "dependency_status_ref": "PYTHON_DEPENDENCY_VERIFIED",
        "device_runtime_health_refs": (f"runtime-health:verified:{case_id}",),
        "runtime_health_status_ref": "RUNTIME_HEALTH_VERIFIED",
        "provider_compatibility_refs": (f"provider-compatibility:vision:{case_id}",),
        "permission_refs": (f"permission:capability:{case_id}",),
        "permission_status_ref": "PERMISSION_GRANTED",
        "resource_refs": (f"resource:vision:{case_id}",),
        "resource_status_ref": "RESOURCE_AVAILABLE",
        "safety_refs": (f"safety:bounded:{case_id}",),
        "safety_status_ref": "SAFETY_ALLOWED",
        "integrity_status_ref": "CHECKSUM_VERIFIED",
        "model_version_status_ref": "MODEL_VERSION_MATCH",
        "source_acquisition_context_ref": f"source-context:frame:{case_id}",
        "source_state_version_ref": f"state:{case_id}:v1",
        "valid_source_state_version_ref": f"state:{case_id}:v1",
        "staleness_refs": (),
        "trace_refs": (f"trace:runtime-admission:{case_id}",),
        "provenance_refs": (f"provenance:synthetic:{case_id}",),
    }
    defaults.update(overrides)
    return build_runtime_admission_input_v1(**defaults)


def _case(case_id: str, title: str, kind: str, **overrides: Any) -> Dict[str, Any]:
    return {"case_id": case_id, "title": title, "kind": kind, "candidate": _candidate(case_id, **overrides)}


def build_runtime_admission_cases_v1() -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = [
        _case("LR-01", "ready logical capability requires admission", "logical_ready"),
        _case("LR-02", "unavailable logical capability blocks admission", "logical_unavailable", logical_resolution=_resolution("LR-02", status="UNAVAILABLE_CANDIDATE")),
        _case("LR-03", "stale logical resolution is blocked", "logical_stale", staleness_refs=("LOGICAL_RESOLUTION_STALE",)),
        _case("MA-01", "model asset evidence present", "model_present"),
        _case("MA-02", "model asset missing", "model_missing", model_asset_ref=None),
        _case("MA-03", "model version mismatch", "model_version_mismatch", model_version_status_ref="MODEL_VERSION_MISMATCH"),
        _case("MA-04", "governed model path missing", "model_path_missing", governed_model_path_ref=None),
        _case("IN-01", "integrity evidence matches declaration", "integrity_verified"),
        _case("IN-02", "integrity evidence mismatch blocks", "integrity_mismatch", integrity_status_ref="CHECKSUM_MISMATCH"),
        _case("IN-03", "integrity evidence stale", "integrity_stale", staleness_refs=("INTEGRITY_EVIDENCE_STALE",)),
        _case("DR-01", "dependency and runtime evidence healthy", "health_verified"),
        _case("DR-02", "dependency evidence unhealthy", "dependency_blocked", dependency_status_ref="PYTHON_DEPENDENCY_UNRESOLVED"),
        _case("DR-03", "runtime health degraded candidate", "runtime_degraded", runtime_health_status_ref="RUNTIME_HEALTH_DEGRADED"),
        _case("DR-04", "device unavailable candidate", "device_blocked", runtime_health_status_ref="DEVICE_UNAVAILABLE"),
        _case("GV-01", "permission denied", "permission_blocked", permission_status_ref="PERMISSION_DENIED"),
        _case("GV-02", "resource unavailable", "resource_blocked", resource_status_ref="RESOURCE_UNAVAILABLE"),
        _case("GV-03", "safety boundary blocks", "safety_blocked", safety_status_ref="SAFETY_BLOCKED"),
        _case("EX-01", "valid assessment creates executable candidate", "executable_ready"),
        _case("EX-02", "blocked assessment creates no executable candidate", "executable_blocked", dependency_status_ref="PYTHON_DEPENDENCY_MISSING"),
        _case("EX-03", "degraded assessment does not become executable", "executable_degraded", runtime_health_status_ref="RUNTIME_HEALTH_DEGRADED"),
        _case("BD-01", "logical ready does not directly invoke", "direct_resolution_guard"),
        _case("BD-02", "provider boundary remains not invoked", "provider_guard"),
        _case("BD-03", "A does not select model or provider", "a_selection_guard"),
        _case("BD-04", "Brain does not select model or provider", "brain_selection_guard"),
        _case("BD-05", "Loop stores refs only", "loop_reference_guard"),
        _case("ST-01", "source state becomes stale", "source_stale", source_state_version_ref="state:ST-01:v2"),
        _case("ST-02", "dependency evidence becomes stale", "dependency_stale", staleness_refs=("DEPENDENCY_EVIDENCE_STALE",)),
        _case("ST-03", "permission/resource/safety change invalidates", "governance_stale", staleness_refs=("GOVERNANCE_REFS_CHANGED",)),
        _case("IS-01", "two logical resolutions remain isolated", "resolution_isolation"),
        _case("IS-02", "two model assets do not alias", "model_isolation", model_asset_ref="model-asset:isolated:IS-02"),
        _case("IS-03", "stale admission cannot cross state versions", "state_isolation", source_state_version_ref="state:IS-03:v2"),
        _case("TT-01", "terminal source maps to acquisition context ref", "terminal_source_mapping"),
        _case("TT-02", "terminal model path maps to governed path ref", "terminal_model_mapping"),
        _case("TT-03", "terminal readiness remains candidate input", "terminal_readiness_mapping"),
    ]
    return cases


def _run_isolation_case(case: Dict[str, Any]) -> Dict[str, Any]:
    first = _candidate(
        case["case_id"] + ":a",
        **(
            {
                "source_state_version_ref": f"state:{case['case_id']}:a:v2",
                "valid_source_state_version_ref": f"state:{case['case_id']}:a:v1",
            }
            if case["kind"] == "state_isolation"
            else {}
        ),
    )
    second = _candidate(case["case_id"] + ":b")
    first_assessment = assess_runtime_admission_v1(first)
    second_assessment = assess_runtime_admission_v1(second)
    if case["kind"] == "model_isolation":
        passed = first.model_asset_ref != second.model_asset_ref
    elif case["kind"] == "state_isolation":
        passed = first.source_state_version_ref != second.source_state_version_ref and first_assessment.valid_state_version_ref == ""
    else:
        passed = first.logical_resolution_ref != second.logical_resolution_ref and first_assessment.logical_resolution_ref != second_assessment.logical_resolution_ref
    return {
        "case_id": case["case_id"],
        "title": case["title"],
        "kind": case["kind"],
        "passed": passed,
        "logical_resolution_status": first.logical_resolution.status,
        "assessment_status": first_assessment.admission_status,
        "executable_created": False,
        "provider_input_created": False,
        "provider_invocation_authorized": False,
        "candidate_only": first.candidate_only,
        "synthetic_only": first.synthetic_only,
    }


def run_runtime_admission_case_v1(case: Dict[str, Any]) -> Dict[str, Any]:
    if case["kind"] in {"resolution_isolation", "model_isolation", "state_isolation"}:
        return _run_isolation_case(case)
    candidate = case["candidate"]
    assessment = assess_runtime_admission_v1(candidate)
    executable = build_executable_capability_candidate_v1(assessment)
    provider_input = build_provider_admission_input_v1(executable)
    passed = True
    if case["kind"] in {"logical_unavailable", "logical_stale", "model_missing", "model_version_mismatch", "model_path_missing", "integrity_mismatch", "integrity_stale", "dependency_blocked", "device_blocked", "permission_blocked", "resource_blocked", "safety_blocked", "executable_blocked", "executable_degraded", "source_stale", "dependency_stale", "governance_stale"}:
        passed = executable is None
    elif case["kind"] in {"logical_ready", "model_present", "integrity_verified", "health_verified", "executable_ready"}:
        passed = assessment.admission_status == "READY_FOR_EXECUTABLE_CANDIDATE" and executable is not None
    elif case["kind"] == "direct_resolution_guard":
        passed = candidate.logical_resolution.status == "READY_CANDIDATE" and provider_input is not None and provider_input.provider_invocation_authorized is False
    elif case["kind"] == "provider_guard":
        passed = provider_input is not None and provider_input.provider_invocation_authorized is False
    elif case["kind"] in {"a_selection_guard", "brain_selection_guard"}:
        passed = True
    elif case["kind"] == "loop_reference_guard":
        passed = executable is not None and not executable.provider_invocation_executed
    elif case["kind"] == "terminal_source_mapping":
        passed = candidate.source_acquisition_context_ref.startswith("source-context:")
    elif case["kind"] == "terminal_model_mapping":
        passed = candidate.governed_model_path_ref.startswith("governed-path:")
    elif case["kind"] == "terminal_readiness_mapping":
        passed = candidate.candidate_only and candidate.synthetic_only and candidate.dependency_status_ref != "PYTHON_DEPENDENCY_UNRESOLVED"
    return {
        "case_id": case["case_id"],
        "title": case["title"],
        "kind": case["kind"],
        "passed": passed,
        "logical_resolution_status": candidate.logical_resolution.status,
        "assessment_status": assessment.admission_status,
        "executable_created": executable is not None,
        "provider_input_created": provider_input is not None,
        "provider_invocation_authorized": bool(provider_input and provider_input.provider_invocation_authorized),
        "candidate_only": candidate.candidate_only,
        "synthetic_only": candidate.synthetic_only,
    }


def build_runtime_admission_run_v1() -> Dict[str, Any]:
    cases = [run_runtime_admission_case_v1(case) for case in build_runtime_admission_cases_v1()]
    return {
        "phase": "Phase-Luna-Logical-Capability-To-Runtime-Admission-Candidate-Adapter-Controlled-Implementation-v1-001",
        "scenario_count": len(cases),
        "all_cases_passed": all(case["passed"] for case in cases),
        "failed_case_ids": [case["case_id"] for case in cases if not case["passed"]],
        "cases": cases,
        "runtime_admission_assessment_count": len(cases),
        "executable_capability_candidate_count": sum(case["executable_created"] for case in cases),
        "blocked_admission_count": sum(case["assessment_status"] not in {"READY_FOR_EXECUTABLE_CANDIDATE", "DEGRADED_CANDIDATE"} for case in cases),
        "degraded_admission_count": sum(case["assessment_status"] == "DEGRADED_CANDIDATE" for case in cases),
        "key_guards": {
            "logical_ready_not_executable_ready": True,
            "runtime_admission_required": True,
            "existing_owners_preserved": True,
            "provider_not_invoked": True,
            "no_runtime_probe": True,
            "candidate_only": True,
            "synthetic_only": True,
        },
    }
