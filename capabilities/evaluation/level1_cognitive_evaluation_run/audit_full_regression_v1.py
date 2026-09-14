"""Read-only Level-1 full-regression and data-conformance audit.

This module deliberately uses only the Python standard library.  It reads
declared transient outputs and durable archive records; it never imports or
executes cognition, provider, model, observation, action, or archive-writer
code.  The only writes are audit reports below ``_eval_out``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple


PHASE = "Phase-P1-Luna-Level1-Internal-Full-Regression-And-Data-Conformance-Audit-v1-001"
DEFAULT_OUTPUT = Path("_eval_out/level1_internal_full_regression_and_data_conformance_audit_v1")
ARCHIVE_RELATIVE_ROOT = Path("evaluation_archive/level1_cognitive_runs")
DEFAULT_SESSION_MANIFEST = DEFAULT_OUTPUT / "session_manifest_v1.json"

FORBIDDEN_FLAGS = (
    "model_invocation",
    "provider_invocation",
    "live_observation_execution",
    "observation_execution",
    "action_execution",
    "field_mutation",
    "world_truth_declared",
    "memory_promotion",
    "knowledge_promotion",
    "experience_promotion",
)
METRIC_KEYS = {
    "latency",
    "resource_usage",
    "evidence_consumed_count",
    "observation_cycle_count",
    "reobservation_count",
    "cognitive_transition_count",
}
EXPECTED_GOVERNANCE_PREFIXES = tuple(f"G{index:02d}_" for index in range(1, 21))
RESOLVED_FINDINGS: Tuple[Mapping[str, Any], ...] = (
    {
        "finding_id": "CROSS-RUN-None",
        "severity": "MAJOR",
        "category": "AUDIT_INFRASTRUCTURE",
        "component": "A-Route controlled replay runtime",
        "stage": "Stage 6",
        "status": "RESOLVED",
        "cause": "archive applicability was not consulted for a runtime-only component",
        "observed": "archive_ref_missing",
        "resolution": "cross-reference validation is now NOT_APPLICABLE when archive_required is false",
    },
    {
        "finding_id": "Dataset Registry / declaration:phase_present",
        "severity": "MAJOR",
        "category": "AUDIT_INFRASTRUCTURE",
        "component": "Dataset Registry / declaration",
        "stage": "Stage 7",
        "status": "RESOLVED",
        "cause": "generic phase presence check was applied to a durable registry declaration",
        "observed": "phase field absent",
        "resolution": "phase presence is now NOT_APPLICABLE when phase_required is false",
    },
)
STATIC_PRECHECK_ASSETS = (
    "capabilities/midplatform/core/execution_mode_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/__init__.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_io_types_v1.py",
    "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_engine_v1.py",
    "capabilities/midplatform/core/observation_gateway/observation_gateway_engine_v1.py",
    "capabilities/midplatform/core/a_route_orchestration/a_route_orchestration_engine_v1.py",
    "capabilities/evaluation/level1_cognitive_evaluation_run/types_v1.py",
    "capabilities/evaluation/level1_cognitive_evaluation_run/run_boundary_v1.py",
    "capabilities/evaluation/level1_cognitive_evaluation_run/archive_v1.py",
    "capabilities/evaluation/a_route_cognitive_whitebox_foundation/types_v1.py",
    "capabilities/evaluation/a_route_cognitive_whitebox_foundation/runtime_collector_v1.py",
    "capabilities/evaluation/level1_cognitive_evaluation_run/preflight_full_regression_v1.py",
)


REGRESSION_MANIFEST: Tuple[Mapping[str, Any], ...] = (
    {
        "component": "Dataset Registry / declaration",
        "source": "dataset_registry",
        "runner_module": None,
        "verifier_module": None,
        "output_path": "capabilities/evaluation/dataset_registry/registry_declaration_v1.json",
        "priority": "P0",
        "dependency": "none; exercised by Evaluation Run Boundary",
        "archive_writing": False,
        "archive_required": False,
        "phase_required": False,
        "rerun_safe": "read-only/static",
        "execution_mode": "contract-only",
    },
    {
        "component": "Synthetic Evaluation Run Boundary",
        "source": "Phase-P1-Luna-Level1-Cognitive-Evaluation-Run-Boundary-And-Durable-Archive-Bridge-v1-001",
        "runner_module": "capabilities.evaluation.level1_cognitive_evaluation_run.runner_v1",
        "verifier_module": "capabilities.evaluation.level1_cognitive_evaluation_run.verifier_v1",
        "output_path": "_eval_out/level1_cognitive_evaluation_run_boundary_v1/runner_summary_v1.json",
        "priority": "P1",
        "dependency": "Dataset Registry / Level-1 case contracts",
        "archive_writing": True,
        "archive_required": True,
        "phase_required": True,
        "rerun_safe": "yes; per-execution Evaluation Run identity",
        "execution_mode": "SYNTHETIC_CONTROLLED",
    },
    {
        "component": "Observation Gateway controlled integration",
        "source": "Observation Gateway canonical integration",
        "runner_module": "capabilities.midplatform.core.observation_gateway.run_observation_gateway_controlled_integration_v1",
        "verifier_module": None,
        "output_path": "_eval_out/a_route_perception_observation_gateway_controlled_integration_v1/observation_gateway_result_v1.json",
        "priority": "P1",
        "dependency": "execution mode and gateway contracts",
        "archive_writing": False,
        "archive_required": False,
        "phase_required": True,
        "rerun_safe": "yes; transient output replacement",
        "execution_mode": "SYNTHETIC_CONTROLLED plus replay cases",
    },
    {
        "component": "Cognitive State Formation controlled implementation",
        "source": "Cognitive State Formation canonical implementation",
        "runner_module": "capabilities.midplatform.core.cognitive_state_formation.run_cognitive_state_formation_controlled_implementation_v1",
        "verifier_module": None,
        "output_path": "_eval_out/cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_result_v1.json",
        "priority": "P1",
        "dependency": "Observation / cognition contracts",
        "archive_writing": False,
        "archive_required": False,
        "phase_required": True,
        "rerun_safe": "yes; transient output replacement",
        "execution_mode": "SYNTHETIC_CONTROLLED and controlled replay",
    },
    {
        "component": "A-Route controlled replay runtime",
        "source": "Phase-P1-Luna-A-Route-Controlled-Replay-Runtime-Enablement-v1-001",
        "runner_module": "capabilities.midplatform.core.a_route_orchestration.run_a_route_controlled_replay_runtime_enablement_v1",
        "verifier_module": "capabilities.midplatform.core.a_route_orchestration.verify_a_route_controlled_replay_runtime_enablement_v1",
        "output_path": "_eval_out/a_route_controlled_replay_runtime_enablement_v1/runner_summary_v1.json",
        "priority": "P0",
        "dependency": "Observation Gateway; Cognitive State Formation",
        "archive_writing": False,
        "archive_required": False,
        "phase_required": True,
        "rerun_safe": "yes; transient output only",
        "execution_mode": "CONTROLLED_REPLAY_RUNTIME",
    },
    {
        "component": "White-box V1 foundation",
        "source": "Phase-P1-Luna-A-Route-Cognitive-Whitebox-Trace-And-Execution-Profile-Foundation-v1-001",
        "runner_module": "capabilities.evaluation.a_route_cognitive_whitebox_foundation.runner_v1",
        "verifier_module": "capabilities.evaluation.a_route_cognitive_whitebox_foundation.verifier_v1",
        "output_path": "_eval_out/a_route_cognitive_whitebox_trace_and_execution_profile_foundation_v1/synthetic_cognitive_whitebox_runner_v1.json",
        "priority": "P1",
        "dependency": "White-box V1 contracts",
        "archive_writing": False,
        "archive_required": False,
        "phase_required": True,
        "rerun_safe": "yes; synthetic transient output",
        "execution_mode": "synthetic",
    },
    {
        "component": "Replay Evaluation / White-box / Governance integration",
        "source": "Phase-P1-Luna-Level1-Replay-Evaluation-Whitebox-Archive-And-Governance-Integration-v1-001",
        "runner_module": "capabilities.evaluation.level1_cognitive_evaluation_run.run_controlled_replay_integration_v1",
        "verifier_module": "capabilities.evaluation.level1_cognitive_evaluation_run.verify_controlled_replay_integration_v1",
        "output_path": "_eval_out/level1_replay_evaluation_whitebox_archive_governance_integration_v1/runner_summary_v1.json",
        "priority": "P0",
        "dependency": "A-Route replay; Evaluation Run Boundary; White-box V1; Plane G",
        "archive_writing": True,
        "archive_required": True,
        "phase_required": True,
        "governance_required": True,
        "rerun_safe": "yes only with execution-instance identity",
        "execution_mode": "CONTROLLED_REPLAY_RUNTIME",
    },
    {
        "component": "Minimum Sufficient Cognition Loop",
        "source": "Phase-P1-Luna-Level1-Minimum-Sufficient-Cognition-Loop-Controlled-Replay-v1-001",
        "runner_module": "capabilities.evaluation.level1_cognitive_evaluation_run.run_minimum_sufficient_cognition_loop_controlled_replay_v1",
        "verifier_module": "capabilities.evaluation.level1_cognitive_evaluation_run.verify_minimum_sufficient_cognition_loop_controlled_replay_v1",
        "output_path": "_eval_out/level1_minimum_sufficient_cognition_loop_controlled_replay_v1/runner_summary_v1.json",
        "priority": "P0",
        "dependency": "Replay Evaluation integration; canonical loop owners",
        "archive_writing": True,
        "archive_required": True,
        "phase_required": True,
        "governance_required": True,
        "rerun_safe": "yes only with execution-instance identity",
        "execution_mode": "CONTROLLED_REPLAY_RUNTIME",
    },
)


def _finding(
    finding_id: str,
    severity: str,
    category: str,
    component: str,
    description: str,
    expected: Any = None,
    observed: Any = None,
    *,
    run_ref: str | None = None,
    evidence_ref: str | None = None,
    remediation_required: bool = False,
) -> Dict[str, Any]:
    return {
        "finding_id": finding_id,
        "severity": severity,
        "category": category,
        "component": component,
        "run_ref": run_ref,
        "description": description,
        "expected": expected,
        "observed": observed,
        "evidence_ref": evidence_ref,
        "remediation_required": remediation_required,
    }


def _check(
    checks: MutableMapping[str, List[Dict[str, Any]]],
    layer: str,
    check_id: str,
    passed: bool | None,
    component: str,
    *,
    notes: str = "",
    status: str | None = None,
) -> None:
    checks.setdefault(layer, []).append(
        {
            "check_id": check_id,
            "status": status or ("PASS" if passed is True else "FAIL" if passed is False else "WARNING"),
            "passed": passed,
            "component": component,
            "notes": notes,
        }
    )


def _load_json(path: Path) -> Tuple[Dict[str, Any] | List[Any] | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "missing_file"
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_session_manifest(repository_root: Path, session_manifest_path: Path | None) -> Tuple[Dict[str, Any] | None, str | None]:
    if session_manifest_path is None:
        return None, "session_manifest_not_provided"
    path = session_manifest_path if session_manifest_path.is_absolute() else repository_root / session_manifest_path
    payload, error = _load_json(path)
    if error:
        return None, error
    manifest = _dict(payload)
    if manifest.get("schema") != "full-regression-session-manifest-v1":
        return None, "invalid_session_manifest_schema"
    if manifest.get("repository_root") != str(repository_root):
        return None, "session_manifest_repository_mismatch"
    if not isinstance(manifest.get("baseline_files"), dict):
        return None, "session_manifest_baseline_missing"
    return manifest, None


def _session_status(path: Path, repository_root: Path, session_manifest: Mapping[str, Any] | None) -> str:
    if session_manifest is None:
        return "SESSION_EVIDENCE_NOT_PROVIDED"
    if not path.is_file():
        return "MISSING"
    relative = str(path.relative_to(repository_root))
    baseline = _dict(_dict(session_manifest).get("baseline_files")).get(relative)
    if not isinstance(baseline, dict):
        return "CURRENT_SESSION"
    stat = path.stat()
    changed = (
        baseline.get("sha256") != _sha256_file(path)
        or baseline.get("size") != stat.st_size
        or baseline.get("mtime_ns") != stat.st_mtime_ns
    )
    return "CURRENT_SESSION" if changed else "HISTORICAL_OR_UNCHANGED"


def _safe_archive_name(run_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", run_id).strip("_") or "invalid-run-id"


def _dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _all_false(value: Mapping[str, Any], fields: Iterable[str]) -> bool:
    """Return false only for an explicit forbidden true claim.

    Missing flags are handled by the surrounding contract audit as
    unavailable metadata; they must not be mistaken for executed capability.
    """
    return all(value.get(field) is not True for field in fields)


def _nested_metric_findings(value: Any, path: str = "") -> List[Tuple[str, Any]]:
    findings: List[Tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key in METRIC_KEYS and isinstance(child, (int, float)) and child == 0:
                findings.append((child_path, child))
            if key == "value" and isinstance(child, (int, float)) and child == 0 and path.rsplit(".", 1)[-1] in METRIC_KEYS:
                availability = value.get("availability")
                if availability in {"unavailable", "not_observed", "not_instrumented", "planned"}:
                    findings.append((path, child))
            findings.extend(_nested_metric_findings(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_nested_metric_findings(child, f"{path}[{index}]"))
    return findings


def _audit_governance(case: Mapping[str, Any], component: str, run_ref: str, findings: List[Dict[str, Any]], checks: MutableMapping[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    plane_g = _dict(case.get("plane_g_result"))
    assertions = _list(plane_g.get("assertion_results"))
    ids = [str(item.get("assertion_id", "")) for item in assertions if isinstance(item, dict)]
    expected = [f"G{index:02d}_" for index in range(1, 21)]
    present_prefixes = [next((prefix for prefix in expected if item.startswith(prefix)), item) for item in ids]
    complete = len(assertions) == 20 and all(prefix in present_prefixes for prefix in expected)
    _check(checks, "runtime_data_conformance", f"{component}:plane_g_assertion_set", complete, component, notes="G01-G20 must be present for the current loop integration")
    for item in assertions:
        if not isinstance(item, dict):
            continue
        assertion_id = str(item.get("assertion_id", "unknown"))
        evidence = _list(item.get("evidence_refs"))
        target_refs = _list(item.get("target_refs"))
        if item.get("status") == "PASS" and not evidence:
            findings.append(_finding(
                f"GOV-EVIDENCE-{assertion_id}", "MAJOR", "governance", component,
                "Governance assertion claims PASS without evidence refs.",
                expected="non-empty evidence_refs", observed=item, run_ref=run_ref,
                remediation_required=True,
            ))
        if item.get("status") == "PASS" and item.get("passed") is not True:
            findings.append(_finding(
                f"GOV-STATUS-{assertion_id}", "MAJOR", "governance", component,
                "Governance assertion status/passed fields disagree.",
                expected={"status": "PASS", "passed": True}, observed=item, run_ref=run_ref,
                remediation_required=True,
            ))
        if target_refs and not any(run_ref == ref for ref in target_refs):
            findings.append(_finding(
                f"GOV-TARGET-{assertion_id}", "MAJOR", "governance", component,
                "Governance assertion target does not include its Evaluation Run.",
                expected=run_ref, observed=target_refs, run_ref=run_ref,
                remediation_required=True,
            ))
        if item.get("contract_ref") is None and item.get("contract_ref_availability") != "unavailable":
            findings.append(_finding(
                f"GOV-CONTRACT-AVAIL-{assertion_id}", "MINOR", "governance", component,
                "Missing contract ref lacks explicit unavailable status.",
                expected="contract_ref_availability=unavailable", observed=item, run_ref=run_ref,
            ))
    compliance = plane_g.get("compliance_status")
    _check(checks, "runtime_data_conformance", f"{component}:plane_g_compliance_status", compliance in {"COMPLIANT", "NON_COMPLIANT", "INCOMPLETE", "NOT_EVALUATED"}, component, notes=str(compliance))
    return {"status": compliance, "assertion_count": len(assertions), "assertion_ids": ids}


def _audit_case(
    case: Mapping[str, Any],
    component: str,
    findings: List[Dict[str, Any]],
    checks: MutableMapping[str, List[Dict[str, Any]]],
    repository_root: Path,
    *,
    archive_expected: bool = False,
    governance_expected: bool = False,
) -> Dict[str, Any]:
    case_id = str(case.get("case_id", "unknown"))
    run_ref = str(case.get("evaluation_run_id", "")) or None
    prefix = f"{component}:{case_id}"
    for flag in FORBIDDEN_FLAGS:
        value = case.get(flag)
        if value is True:
            findings.append(_finding(f"RUNTIME-FORBIDDEN-{case_id}-{flag}", "BLOCKER", "negative_guard", component, f"Forbidden runtime flag is true: {flag}.", expected=False, observed=value, run_ref=run_ref, remediation_required=True))
    _check(checks, "runtime_data_conformance", f"{prefix}:forbidden_capabilities", _all_false(case, FORBIDDEN_FLAGS), component)
    validation = _list(case.get("validation_errors")) + _list(case.get("boundary_errors"))
    _check(checks, "runtime_data_conformance", f"{prefix}:validation_clean", not validation, component, notes=";".join(str(item) for item in validation))
    archive_location = str(case.get("archive_location", ""))
    archive_path = repository_root / archive_location if archive_location else None
    archive = _load_archive_for_case(case, repository_root) if archive_expected else None
    mode = case.get("execution_mode")
    if mode is None and archive:
        mode = _dict(archive.get("evaluation_run")).get("execution_mode")
    mode_valid = mode in {"SYNTHETIC_CONTROLLED", "CONTROLLED_REPLAY_RUNTIME", "LIVE_RUNTIME"}
    mode_valid = mode_valid or (archive_expected and mode == "synthetic_candidate")
    _check(
        checks,
        "runtime_data_conformance",
        f"{prefix}:execution_mode",
        mode_valid,
        component,
        notes=str(mode),
    )
    if archive_expected:
        _check(checks, "artifact_conformance", f"{prefix}:archive_path", bool(archive_path and archive_path.is_file() and "_eval_out" not in archive_location), component, notes=archive_location)
        if archive and mode == "CONTROLLED_REPLAY_RUNTIME":
            _audit_archived_payload(case, component, archive, findings, checks)
        elif archive:
            _check(checks, "artifact_conformance", f"{prefix}:archive_record_readable", True, component)
    if case_id == "sufficient-and-stop":
        sufficiency = _list(case.get("sufficiency"))
        _check(checks, "runtime_data_conformance", f"{prefix}:sufficient_stop_chain", len(sufficiency) == 1 and _dict(sufficiency[0]).get("status") == "SUFFICIENT" and bool(_list(case.get("stop_refs"))) and not _list(case.get("information_gap_refs")) and not _list(case.get("reobservation_refs")), component)
        if _list(case.get("information_gap_refs")) or _list(case.get("reobservation_refs")):
            findings.append(_finding(f"CHAIN-CASE-A-{case_id}", "BLOCKER", "causal_chain", component, "Sufficient Case A contains a gap or re-observation.", expected="no gap/re-observation", observed=case, run_ref=run_ref, remediation_required=True))
    if case_id.startswith("identify-gap"):
        sufficiency = _list(case.get("sufficiency"))
        good_shape = (
            len(sufficiency) == 2
            and _dict(sufficiency[0]).get("status") == "INSUFFICIENT"
            and _dict(sufficiency[1]).get("status") == "SUFFICIENT"
            and len(_list(case.get("information_gap_refs"))) == 1
            and len(_list(case.get("reobservation_refs"))) == 1
            and len(_list(case.get("next_cycle_ingress_refs"))) == 1
            and len(_list(case.get("hypothesis_revision_refs"))) == 1
            and len(_list(case.get("stop_refs"))) == 1
        )
        _check(checks, "runtime_data_conformance", f"{prefix}:two_cycle_shape", good_shape, component)
        archive = _load_archive_for_case(case, repository_root)
        if archive:
            metadata = _dict(archive.get("bounded_metadata"))
            proofs = _list(metadata.get("canonical_cognition_proofs"))
            replays = _list(metadata.get("replay_inputs"))
            if len(proofs) >= 2 and len(replays) >= 2:
                first, second = _dict(proofs[0]), _dict(proofs[1])
                first_gap = first.get("information_gap_ref")
                first_reobs = first.get("reobservation_ref")
                first_next = first.get("next_cycle_ingress_ref")
                revision_gap = second.get("hypothesis_revision_information_gap_ref")
                revision_reobs = second.get("hypothesis_revision_reobservation_ref")
                replay_second = _dict(replays[1])
                causal = (
                    first_gap == revision_gap
                    and first_reobs == revision_reobs
                    and replay_second.get("prior_information_gap_ref") == first_gap
                    and replay_second.get("prior_reobservation_ref") == first_reobs
                    and replay_second.get("prior_next_cycle_ingress_ref") == first_next
                    and set(_list(_dict(replays[0]).get("evidence_refs"))).isdisjoint(set(_list(replay_second.get("evidence_refs"))))
                )
                _check(checks, "runtime_data_conformance", f"{prefix}:causal_identity_continuity", causal, component)
                if not causal:
                    findings.append(_finding(f"CHAIN-CASE-B-{case_id}", "BLOCKER", "causal_chain", component, "Cycle 2 gap/re-observation/next-cycle identity continuity failed.", expected="exact Cycle 1 refs carried into Cycle 2", observed={"cycle_1_gap": first_gap, "cycle_1_reobservation": first_reobs, "cycle_1_next": first_next, "cycle_2_revision_gap": revision_gap, "cycle_2_revision_reobservation": revision_reobs, "cycle_2_prior_gap": replay_second.get("prior_information_gap_ref"), "cycle_2_prior_reobservation": replay_second.get("prior_reobservation_ref"), "cycle_2_prior_next": replay_second.get("prior_next_cycle_ingress_ref")}, run_ref=run_ref, remediation_required=True))
    if governance_expected:
        _audit_governance(case, component, run_ref or "", findings, checks)
    else:
        _check(
            checks,
            "runtime_data_conformance",
            f"{prefix}:plane_g_applicability",
            None,
            component,
            notes="NOT_APPLICABLE: component contract does not produce Plane G",
            status="NOT_APPLICABLE",
        )
    for path, value in _nested_metric_findings(case):
        findings.append(_finding(f"METRIC-ZERO-{case_id}-{path.replace('.', '-')}", "MAJOR", "availability", component, "Metric appears zero-filled without a trustworthy observed status.", expected="explicit unavailable/not_observed/not_instrumented or observed provenance", observed={"path": path, "value": value}, run_ref=run_ref, remediation_required=True))
    return {"case_id": case_id, "evaluation_run_id": run_ref, "execution_mode": mode, "archive_location": archive_location}


def _load_archive_for_case(case: Mapping[str, Any], repository_root: Path) -> Dict[str, Any] | None:
    location = str(case.get("archive_location", ""))
    if not location:
        return None
    payload, error = _load_json(repository_root / location)
    return _dict(payload) if error is None else None


def _audit_archived_payload(
    case: Mapping[str, Any],
    component: str,
    archive: Mapping[str, Any],
    findings: List[Dict[str, Any]],
    checks: MutableMapping[str, List[Dict[str, Any]]],
) -> None:
    """Inspect archived White-box, Plane B, and run-level cross references."""
    case_id = str(case.get("case_id", "unknown"))
    run_ref = str(case.get("evaluation_run_id", ""))
    prefix = f"{component}:{case_id}"
    run = _dict(archive.get("evaluation_run"))
    identity_ok = True
    for case_field, archive_field in (
        ("evaluation_run_id", "evaluation_run_id"),
        ("whitebox_trace_ref", "trace_ref"),
        ("whitebox_profile_ref", "execution_profile_ref"),
        ("a_route_execution_ref", "a_route_execution_ref"),
    ):
        expected = case.get(case_field)
        if expected is None:
            continue
        observed = run.get(archive_field)
        matches = observed == expected
        identity_ok = identity_ok and matches
        if not matches:
            findings.append(_finding(
                f"ARCHIVE-REF-{case_id}-{archive_field}", "MAJOR", "cross_reference", component,
                "Archived Evaluation Run reference disagrees with the transient case output.",
                expected=expected, observed=observed, run_ref=run_ref or None, remediation_required=True,
            ))
    _check(checks, "artifact_conformance", f"{prefix}:archive_run_refs", identity_ok, component)
    metadata = _dict(archive.get("bounded_metadata"))
    trace = _dict(metadata.get("whitebox_trace"))
    profile = _dict(metadata.get("whitebox_profile"))
    trace_ref = trace.get("trace_id")
    profile_ref = profile.get("execution_profile_id")
    trace_ok = bool(trace_ref and trace.get("nodes") and trace_ref == run.get("trace_ref"))
    profile_ok = bool(profile_ref and profile.get("cognitive_trace_ref") == trace_ref and profile_ref == run.get("execution_profile_ref"))
    _check(checks, "artifact_conformance", f"{prefix}:whitebox_trace_payload", trace_ok, component)
    _check(checks, "artifact_conformance", f"{prefix}:whitebox_profile_payload", profile_ok, component)
    if not trace_ok or not profile_ok:
        findings.append(_finding(
            f"WHITEBOX-LINK-{case_id}", "MAJOR", "whitebox", component,
            "Archived White-box Trace/Profile payload is absent or cross-linked incorrectly.",
            expected={"trace_ref": run.get("trace_ref"), "profile_ref": run.get("execution_profile_ref")},
            observed={"trace_id": trace_ref, "profile_id": profile_ref, "profile_trace_ref": profile.get("cognitive_trace_ref")},
            run_ref=run_ref or None, remediation_required=True,
        ))
    nodes = _list(trace.get("nodes"))
    node_ids = [item.get("trace_node_id") for item in nodes if isinstance(item, dict)]
    node_ok = bool(nodes) and len(node_ids) == len(set(node_ids)) and all(
        item.get("candidate_only") is True and item.get("authoritative") is False
        for item in nodes if isinstance(item, dict)
    )
    _check(checks, "runtime_data_conformance", f"{prefix}:whitebox_nodes", node_ok, component, notes=f"{len(nodes)} nodes")
    transition_refs = tuple(trace.get("transition_refs") or ())
    expected_transitions = tuple(case.get("cognitive_transition_refs") or ())
    transition_ok = bool(transition_refs) and (not expected_transitions or transition_refs == expected_transitions)
    _check(checks, "runtime_data_conformance", f"{prefix}:whitebox_transitions", transition_ok, component)
    if not node_ok or not transition_ok:
        findings.append(_finding(
            f"WHITEBOX-NODES-{case_id}", "MAJOR", "whitebox", component,
            "White-box nodes or transition linkage is duplicated, authoritative, or inconsistent with the case.",
            expected={"unique_candidate_nodes": True, "transition_refs": list(expected_transitions)},
            observed={"node_ids": node_ids, "transition_refs": list(transition_refs)},
            run_ref=run_ref or None, remediation_required=True,
        ))
    plane_b = _dict(metadata.get("plane_b_result"))
    plane_b_ok = plane_b.get("status") == "NOT_EVALUATED" and plane_b.get("evaluation_only") is True
    _check(checks, "runtime_data_conformance", f"{prefix}:plane_b_not_evaluated", plane_b_ok, component, notes=str(plane_b.get("reason", "")))
    if plane_b and not plane_b_ok:
        findings.append(_finding(
            f"PLANE-B-REPLAY-{case_id}", "MAJOR", "evaluation", component,
            "Replay archive reports external capability fitness despite no model/provider execution.",
            expected="NOT_EVALUATED", observed=plane_b, run_ref=run_ref or None, remediation_required=True,
        ))
    for path, value in _nested_metric_findings(profile):
        findings.append(_finding(
            f"PROFILE-ZERO-{case_id}-{path.replace('.', '-')}", "MAJOR", "availability", component,
            "Archived White-box profile contains a zero-filled unavailable metric.",
            expected="explicit unavailable/not_observed/not_instrumented or observed provenance",
            observed={"path": path, "value": value}, run_ref=run_ref or None, remediation_required=True,
        ))


def _audit_output(
    manifest: Mapping[str, Any],
    repository_root: Path,
    findings: List[Dict[str, Any]],
    checks: MutableMapping[str, List[Dict[str, Any]]],
    *,
    session_manifest: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    component = str(manifest["component"])
    relative = Path(str(manifest["output_path"]))
    path = repository_root / relative
    payload, error = _load_json(path)
    priority = str(manifest["priority"])
    severity = "BLOCKER" if priority == "P0" else "MAJOR" if priority == "P1" else "MINOR"
    session_status = _session_status(path, repository_root, session_manifest)
    archive_required = bool(manifest.get("archive_required", manifest.get("archive_writing", False)))
    governance_required = bool(manifest.get("governance_required", False))
    if error:
        _check(checks, "execution_health", f"{component}:output_readable", False, component, notes=error)
        findings.append(_finding(f"OUTPUT-{component.replace(' ', '-')}", severity, "execution_health", component, "Declared canonical output is missing or unreadable.", expected=str(relative), observed=error, remediation_required=True))
        return {"component": component, "path": str(relative), "status": "MISSING_OR_UNREADABLE", "priority": priority, "session_evidence": session_status}
    _check(checks, "execution_health", f"{component}:output_readable", True, component)
    if isinstance(payload, dict):
        phase = payload.get("phase")
        phase_required = bool(manifest.get("phase_required", True))
        if phase_required:
            _check(checks, "artifact_conformance", f"{component}:phase_present", bool(phase), component, notes=str(phase))
        else:
            _check(
                checks,
                "artifact_conformance",
                f"{component}:phase_present",
                None,
                component,
                notes="NOT_APPLICABLE: durable declaration contract has no phase field",
                status="NOT_APPLICABLE",
            )
        errors = _list(payload.get("phase_validation_errors")) + _list(payload.get("validation_errors")) + _list(payload.get("boundary_errors"))
        if errors:
            findings.append(_finding(f"OUTPUT-ERRORS-{component.replace(' ', '-')}", "MAJOR", "artifact", component, "Output contains validation or boundary errors.", expected=[], observed=errors, remediation_required=True))
        cases = _list(payload.get("case_results"))
        if cases:
            case_results = [
                _audit_case(
                    _dict(case),
                    component,
                    findings,
                    checks,
                    repository_root,
                    archive_expected=archive_required,
                    governance_expected=governance_required,
                )
                for case in cases
            ]
        else:
            case_results = []
            if payload.get("evaluation_run_id") or payload.get("cognition_execution") is not None:
                case_results.append(
                    _audit_case(
                        payload,
                        component,
                        findings,
                        checks,
                        repository_root,
                        archive_expected=archive_required,
                        governance_expected=governance_required,
                    )
                )
            for flag in FORBIDDEN_FLAGS:
                if payload.get(flag) is True:
                    findings.append(_finding(f"OUTPUT-FORBIDDEN-{component.replace(' ', '-')}-{flag}", "BLOCKER", "negative_guard", component, f"Forbidden flag is true: {flag}.", expected=False, observed=True, remediation_required=True))
            _check(checks, "runtime_data_conformance", f"{component}:forbidden_capabilities", _all_false(payload, FORBIDDEN_FLAGS), component)
        return {"component": component, "path": str(relative), "status": "READABLE", "priority": priority, "phase": phase, "case_results": case_results, "session_evidence": session_status}
    _check(checks, "artifact_conformance", f"{component}:object_payload", False, component, notes="top-level JSON is not an object")
    findings.append(_finding(f"OUTPUT-SHAPE-{component.replace(' ', '-')}", severity, "artifact", component, "Declared output is not a JSON object.", expected="object", observed=type(payload).__name__, remediation_required=True))
    return {"component": component, "path": str(relative), "status": "INVALID_SHAPE", "priority": priority, "session_evidence": session_status}


def _audit_archives(
    repository_root: Path,
    current_run_ids: Sequence[str],
    findings: List[Dict[str, Any]],
    checks: MutableMapping[str, List[Dict[str, Any]]],
    *,
    session_manifest: Mapping[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    root = repository_root / ARCHIVE_RELATIVE_ROOT
    records: List[Dict[str, Any]] = []
    by_run: Dict[str, List[Tuple[str, str]]] = {}
    paths = sorted(root.glob("*.json")) if root.is_dir() else []
    _check(checks, "artifact_conformance", "archive:directory_present", root.is_dir(), "Durable Archive", notes=str(root))
    if not root.is_dir():
        findings.append(_finding("ARCHIVE-DIRECTORY", "BLOCKER", "archive", "Durable Archive", "Canonical archive directory is missing.", expected=str(ARCHIVE_RELATIVE_ROOT), observed="missing", remediation_required=True))
        return records
    for path in paths:
        payload, error = _load_json(path)
        session_status = _session_status(path, repository_root, session_manifest)
        if error:
            classification = "INVALID_RECORD"
            findings.append(_finding(f"ARCHIVE-READ-{path.name}", "BLOCKER", "archive", "Durable Archive", "Archive JSON is unreadable.", expected="readable JSON", observed=error, evidence_ref=str(path), remediation_required=True))
            records.append({"path": str(path.relative_to(repository_root)), "classification": classification, "error": error, "session_evidence": session_status})
            continue
        raw = _dict(payload)
        run = _dict(raw.get("evaluation_run"))
        run_id = str(run.get("evaluation_run_id", ""))
        record_id = str(raw.get("record_id", ""))
        classification = "VALID_HISTORICAL_RUN"
        if not run_id or not record_id:
            classification = "INVALID_RECORD"
            findings.append(_finding(f"ARCHIVE-IDENTITY-{path.name}", "BLOCKER", "archive", "Durable Archive", "Archive record lacks record or Evaluation Run identity.", expected="record_id and evaluation_run.evaluation_run_id", observed=raw, evidence_ref=str(path), remediation_required=True))
        expected_path = root / f"{_safe_archive_name(run_id)}.json" if run_id else path
        if path != expected_path:
            classification = "ORPHANED_REFERENCE"
            findings.append(_finding(f"ARCHIVE-PATH-{path.name}", "MAJOR", "archive", "Durable Archive", "Archive filename does not correspond to its Evaluation Run identity.", expected=str(expected_path), observed=str(path), run_ref=run_id or None, evidence_ref=str(path), remediation_required=True))
        if raw.get("immutable_by_identity") is not True or raw.get("append_or_supersede_only") is not True:
            classification = "INVALID_RECORD"
            findings.append(_finding(f"ARCHIVE-IMMUTABILITY-{path.name}", "BLOCKER", "archive", "Durable Archive", "Archive record does not declare immutable append/supersede semantics.", expected=True, observed={"immutable_by_identity": raw.get("immutable_by_identity"), "append_or_supersede_only": raw.get("append_or_supersede_only")}, run_ref=run_id or None, evidence_ref=str(path), remediation_required=True))
        if run.get("result_status") in {"INCOMPLETE", "BLOCKED"}:
            classification = "VALID_PARTIAL_HISTORY" if classification == "VALID_HISTORICAL_RUN" else classification
        if run_id in current_run_ids and session_status == "CURRENT_SESSION":
            classification = "VALID_CURRENT_RUN" if classification == "VALID_HISTORICAL_RUN" else classification
        digest = hashlib.sha256(json.dumps(raw, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        by_run.setdefault(run_id, []).append((str(path), digest))
        records.append({"path": str(path.relative_to(repository_root)), "classification": classification, "evaluation_run_id": run_id, "record_id": record_id, "session_evidence": session_status})
    for run_id, items in by_run.items():
        if run_id and len(items) > 1:
            digests = {digest for _, digest in items}
            severity = "BLOCKER" if len(digests) > 1 else "MAJOR"
            findings.append(_finding(f"ARCHIVE-DUPLICATE-{_safe_archive_name(run_id)}", severity, "archive", "Durable Archive", "Evaluation Run identity appears in multiple archive records.", expected="one immutable path per execution identity", observed=items, run_ref=run_id, remediation_required=True))
    _check(checks, "artifact_conformance", "archive:records_readable", all(item.get("classification") != "INVALID_RECORD" for item in records), "Durable Archive", notes=f"{len(records)} records")
    return records


def _audit_cross_references(
    output_results: Sequence[Mapping[str, Any]],
    repository_root: Path,
    findings: List[Dict[str, Any]],
    checks: MutableMapping[str, List[Dict[str, Any]]],
    manifest_by_component: Mapping[str, Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for output in output_results:
        component = str(output.get("component", "unknown"))
        archive_required = bool(manifest_by_component.get(component, {}).get("archive_required", False))
        for case in output.get("case_results", []) if isinstance(output.get("case_results"), list) else []:
            run_id = str(case.get("evaluation_run_id", ""))
            location = str(case.get("archive_location", ""))
            if not archive_required:
                _check(
                    checks,
                    "artifact_conformance",
                    f"cross-reference:{component}:archive_applicability",
                    None,
                    component,
                    notes="NOT_APPLICABLE: runtime-only component has no durable Evaluation Archive contract",
                    status="NOT_APPLICABLE",
                )
                results.append({
                    "run_ref": run_id or None,
                    "archive_location": location or None,
                    "archive_applicability": "NOT_APPLICABLE",
                    "archive_run_identity_matches": None,
                })
                continue
            payload, error = _load_json(repository_root / location) if location else (None, "archive_ref_missing")
            archive_run = _dict(_dict(payload).get("evaluation_run")) if error is None else {}
            matches = bool(run_id and archive_run.get("evaluation_run_id") == run_id)
            _check(checks, "artifact_conformance", f"cross-reference:{run_id}:run_identity", matches, component, notes=location)
            if not matches:
                findings.append(_finding(f"CROSS-RUN-{run_id or 'missing'}", "BLOCKER", "cross_reference", component, "Runner case and archive Evaluation Run identities disagree.", expected=run_id, observed=archive_run.get("evaluation_run_id") or error, run_ref=run_id or None, remediation_required=True))
            results.append({"run_ref": run_id, "archive_location": location, "archive_applicability": "REQUIRED", "archive_run_identity_matches": matches})
    return results


def _summarize_checks(checks: Mapping[str, Sequence[Mapping[str, Any]]]) -> Dict[str, Dict[str, int]]:
    result: Dict[str, Dict[str, int]] = {}
    for layer, items in checks.items():
        result[layer] = {
            "total_checks": len(items),
            "passed": sum(item.get("status") == "PASS" for item in items),
            "failed": sum(item.get("status") == "FAIL" for item in items),
            "warnings": sum(item.get("status") == "WARNING" for item in items),
        }
    return result


def build_audit_report_v1(
    repository_root: Path,
    *,
    session_manifest_path: Path | None = None,
) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    checks: Dict[str, List[Dict[str, Any]]] = {}
    session_manifest, session_error = _load_session_manifest(repository_root, session_manifest_path)
    session_status = "PROVIDED" if session_manifest is not None else "NOT_PROVIDED"
    _check(
        checks,
        "execution_health",
        "session:baseline_manifest",
        session_manifest is not None,
        "Full-regression session evidence",
        notes=session_error or str(session_manifest_path),
    )
    if session_manifest is None:
        findings.append(_finding(
            "SESSION-EVIDENCE-MISSING",
            "BLOCKER",
            "execution_health",
            "Full-regression session evidence",
            "A historical output/archive cannot prove that the current full-regression command executed without a pre-run session baseline.",
            expected="valid full-regression-session-manifest-v1",
            observed=session_error,
            remediation_required=True,
        ))
    component_results = [
        _audit_output(item, repository_root, findings, checks, session_manifest=session_manifest)
        for item in REGRESSION_MANIFEST
    ]
    if session_manifest is not None:
        for item in component_results:
            manifest_item = next(
                (entry for entry in REGRESSION_MANIFEST if entry.get("component") == item.get("component")),
                {},
            )
            if (
                item.get("priority") == "P0"
                and manifest_item.get("runner_module") is not None
                and item.get("session_evidence") != "CURRENT_SESSION"
            ):
                findings.append(_finding(
                    f"SESSION-P0-NOT-CURRENT-{str(item.get('component')).replace(' ', '-')}",
                    "BLOCKER",
                    "execution_health",
                    str(item.get("component")),
                    "P0 output is present but was not changed after the session baseline; it cannot prove current-session execution.",
                    expected="session_evidence=CURRENT_SESSION",
                    observed=item.get("session_evidence"),
                    evidence_ref=str(item.get("path")),
                    remediation_required=True,
                ))
    current_run_ids = [
        str(case.get("evaluation_run_id"))
        for item in component_results
        for case in item.get("case_results", [])
        if case.get("evaluation_run_id")
    ]
    archive_results = _audit_archives(repository_root, current_run_ids, findings, checks, session_manifest=session_manifest)
    manifest_by_component = {str(item["component"]): item for item in REGRESSION_MANIFEST}
    cross_reference_results = _audit_cross_references(component_results, repository_root, findings, checks, manifest_by_component)
    for path in STATIC_PRECHECK_ASSETS:
        present = (repository_root / path).is_file()
        _check(checks, "execution_health", f"static:{path}", present, "Static import/runtime precheck", notes="canonical asset present")
    duplicate_ids = [item for item in findings if item["category"] == "archive" and item["finding_id"].startswith("ARCHIVE-DUPLICATE-")]
    _check(checks, "artifact_conformance", "archive:duplicate_execution_identity", not duplicate_ids, "Durable Archive")
    for item in REGRESSION_MANIFEST:
        if item["runner_module"] is None:
            _check(checks, "execution_health", f"inventory:{item['component']}:contract_only", True, str(item["component"]), notes="no executable pair; covered by dependent canonical runner")
        elif item["verifier_module"] is None:
            _check(checks, "execution_health", f"inventory:{item['component']}:verifier_coverage", None, str(item["component"]), notes="GUARD_PRESENT_TEST_COVERAGE_MISSING unless runner has embedded checks")
    summaries = _summarize_checks(checks)
    severity_counts = {severity: sum(item["severity"] == severity for item in findings) for severity in ("BLOCKER", "MAJOR", "MINOR", "INFO")}
    execution = summaries.get("execution_health", {"total_checks": 0, "passed": 0, "failed": 0, "warnings": 0})
    runtime = summaries.get("runtime_data_conformance", {"total_checks": 0, "passed": 0, "failed": 0, "warnings": 0})
    artifact = summaries.get("artifact_conformance", {"total_checks": 0, "passed": 0, "failed": 0, "warnings": 0})
    return {
        "phase": PHASE,
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(repository_root),
        "session_evidence": {
            "status": session_status,
            "manifest_path": str(session_manifest_path) if session_manifest_path else None,
            "session_id": session_manifest.get("session_id") if session_manifest else None,
            "current_session_outputs": [item.get("path") for item in component_results if item.get("session_evidence") == "CURRENT_SESSION"],
            "historical_or_unchanged_outputs": [item.get("path") for item in component_results if item.get("session_evidence") == "HISTORICAL_OR_UNCHANGED"],
            "unproven_outputs": [item.get("path") for item in component_results if item.get("session_evidence") != "CURRENT_SESSION"],
            "current_session_archives": [item.get("path") for item in archive_results if item.get("session_evidence") == "CURRENT_SESSION"],
            "historical_archives": [item.get("path") for item in archive_results if item.get("session_evidence") != "CURRENT_SESSION"],
        },
        "execution_health": {"total": execution["total_checks"], "passed": execution["passed"], "failed": execution["failed"], "blocked": severity_counts["BLOCKER"]},
        "runtime_data_conformance": {"total_checks": runtime["total_checks"], "passed": runtime["passed"], "failed": runtime["failed"], "warnings": runtime["warnings"]},
        "artifact_conformance": {"total_checks": artifact["total_checks"], "passed": artifact["passed"], "failed": artifact["failed"], "warnings": artifact["warnings"]},
        "component_results": component_results,
        "run_results": [case for item in component_results for case in item.get("case_results", [])],
        "archive_results": archive_results,
        "cross_reference_results": cross_reference_results,
        "governance_results": [item for item in findings if item["category"] == "governance"],
        "negative_guard_results": [item for item in findings if item["category"] == "negative_guard"],
        "resolved_findings": list(RESOLVED_FINDINGS),
        "backward_compatibility_results": {
            "synthetic_controlled": "covered by manifest and synthetic boundary output",
            "controlled_replay_single_cycle": "covered by A-Route replay and replay integration outputs",
            "controlled_replay_two_cycle": "covered by minimum sufficient loop output",
            "previous_archive_records": "classified without deletion or overwrite",
        },
        "checks": checks,
        "finding_severity_counts": severity_counts,
        "findings": findings,
        "final_decision_candidate": (
            "BLOCKED_PENDING_SESSION_EVIDENCE"
            if session_manifest is None
            else "BLOCKED_PENDING_TERMINAL_FULL_REGRESSION"
            if findings
            else "GO_CANDIDATE_PENDING_TERMINAL_FULL_REGRESSION"
        ),
    }


def _markdown_report(report: Mapping[str, Any]) -> str:
    counts = report.get("finding_severity_counts", {})
    lines = [
        f"# {report.get('phase')}",
        "",
        "Read-only audit report generated from declared `_eval_out` outputs and durable archive records.",
        "",
        f"- Audit timestamp: `{report.get('audit_timestamp')}`",
        f"- Repository root: `{report.get('repository_root')}`",
        f"- Session evidence: `{_dict(report.get('session_evidence')).get('status')}`",
        f"- Decision candidate: `{report.get('final_decision_candidate')}`",
        f"- Findings: BLOCKER={counts.get('BLOCKER', 0)}, MAJOR={counts.get('MAJOR', 0)}, MINOR={counts.get('MINOR', 0)}, INFO={counts.get('INFO', 0)}",
        "",
        "## Component results",
        "",
        "| Component | Output | Status | Priority |",
        "|---|---|---|---|",
    ]
    for item in report.get("component_results", []):
        lines.append(f"| {item.get('component')} | `{item.get('path')}` | {item.get('status')} | {item.get('priority')} |")
    lines.extend(["", "## Findings", ""])
    findings = report.get("findings", [])
    if not findings:
        lines.append("No findings were emitted by the read-only audit.")
    else:
        for finding in findings:
            lines.append(f"- `{finding.get('severity')}` `{finding.get('finding_id')}` — {finding.get('description')}")
    lines.extend(["", "## Resolved audit-infrastructure findings", ""])
    resolved = report.get("resolved_findings", [])
    if not resolved:
        lines.append("None.")
    else:
        for finding in resolved:
            lines.append(f"- `{finding.get('status')}` `{finding.get('finding_id')}` — {finding.get('resolution')}")
    lines.extend(["", "## Archive classifications", "", "| Path | Classification | Evaluation Run |", "|---|---|---|"])
    for item in report.get("archive_results", []):
        lines.append(f"| `{item.get('path')}` | {item.get('classification')} | `{item.get('evaluation_run_id', '')}` |")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Level-1 runtime/data/artifact conformance audit")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--session-manifest", type=Path, default=DEFAULT_SESSION_MANIFEST)
    args = parser.parse_args(argv)
    repository_root = args.repo_root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else repository_root / args.output_dir
    report = build_audit_report_v1(repository_root, session_manifest_path=args.session_manifest)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "full_regression_audit_report_v1.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "full_regression_audit_report_v1.md").write_text(_markdown_report(report), encoding="utf-8")
    print(json.dumps({"phase": PHASE, "final_decision_candidate": report["final_decision_candidate"], "finding_severity_counts": report["finding_severity_counts"], "status": "WAITING_FOR_USER_TERMINAL_FULL_REGRESSION"}, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
