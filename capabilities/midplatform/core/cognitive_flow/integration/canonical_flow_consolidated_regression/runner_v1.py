"""Controlled consolidated regression Runner.

This process invokes only the three existing synthetic child Runners.  It
keeps child output in memory, binds it to the current attempt, and invokes a
child Verifier only after that child's Runner has produced a valid summary.
"""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .cross_module_checks_v1 import build_cross_module_cases, evaluate_cross_module_cases
from .manifest_v1 import CHILD_MODULES, DOCUMENT_FILES, PHASE
from .normalizers_v1 import normalize_runner_output, normalize_verifier_output


DOC_ROOT = Path(__file__).resolve().parents[6] / "docs" / "architecture" / "phase_luna_canonical_flow_consolidated_regression_v1"


def _attempt_id() -> str:
    return f"attempt:{uuid.uuid4().hex}"


def _run_child(spec: Any, attempt_id: str) -> Dict[str, Any]:
    runner = subprocess.run(
        [sys.executable, "-m", spec.runner_module],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    child = normalize_runner_output(
        spec,
        attempt_id=attempt_id,
        returncode=runner.returncode,
        stdout=runner.stdout,
        stderr=runner.stderr,
    )
    if not child["runner_passed"]:
        return child
    verifier = subprocess.run(
        [
            sys.executable,
            "-c",
            "import json,sys; from " + spec.verifier_module + " import verify_summary; print(json.dumps(verify_summary(json.load(sys.stdin))))",
        ],
        input=runner.stdout,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    return normalize_verifier_output(
        child,
        attempt_id=attempt_id,
        returncode=verifier.returncode,
        stdout=verifier.stdout,
        stderr=verifier.stderr,
    )


def _child_passed(child: Dict[str, Any]) -> bool:
    return bool(child.get("runner_passed") and child.get("verifier_passed"))


def _required_child_checks_ok(child: Dict[str, Any], spec: Any) -> bool:
    checks = child.get("verifier_checks", {})
    return all(checks.get(name) is True for name in spec.required_checks)


def _documentation_set_ok() -> bool:
    return all((DOC_ROOT / name).is_file() for name in DOCUMENT_FILES)


def _guard_violation(summary: Any, *, positive: str, negative: str) -> bool:
    return any(
        item.get("guards", {}).get(positive) is True
        or item.get("guards", {}).get(negative) is False
        or item.get("handoff_flags", {}).get(positive) is True
        for item in (summary or {}).get("case_results", ())
    )


def run_consolidated_regression() -> Dict[str, Any]:
    attempt_id = _attempt_id()
    children = {spec.module_id: _run_child(spec, attempt_id) for spec in CHILD_MODULES}
    child_pass_count = sum(_child_passed(child) for child in children.values())
    child_verifier_pass_count = sum(child.get("verifier_passed") is True for child in children.values())
    failed_children = [
        spec.module_id
        for spec in CHILD_MODULES
        if not _child_passed(children[spec.module_id]) or not _required_child_checks_ok(children[spec.module_id], spec)
    ]
    cross_cases = build_cross_module_cases(children, attempt_id)
    cross = evaluate_cross_module_cases(cross_cases)
    child_summaries = {module_id: child.get("summary") for module_id, child in children.items()}
    runtime_execution_observed = any(
        (summary or {}).get("runtime_execution_count", 0) > 0
        or _guard_violation(summary, positive="runtime_execution", negative="no_runtime_execution")
        for summary in child_summaries.values()
    )
    model_loading_observed = (child_summaries.get("CAPABILITY_MODEL_PROVIDER_BINDING") or {}).get("model_loading_count", 0) > 0 or _guard_violation(child_summaries.get("CAPABILITY_MODEL_PROVIDER_BINDING"), positive="model_loading_executed", negative="no_model_loading")
    provider_invocation_observed = any(
        (summary or {}).get("provider_invocation_count", 0) > 0
        or _guard_violation(summary, positive="provider_invocation_executed", negative="no_provider_invocation")
        for summary in child_summaries.values()
    )
    execution_summary = child_summaries.get("EXECUTION_HANDOFF_ADAPTERS")
    observation_execution_observed = (execution_summary or {}).get("observation_execution_count", 0) > 0 or _guard_violation(execution_summary, positive="observation_execution_executed", negative="no_observation_execution")
    action_execution_observed = (execution_summary or {}).get("action_execution_count", 0) > 0 or _guard_violation(execution_summary, positive="action_execution_executed", negative="no_action_execution")
    source_mutation_observed = any((summary or {}).get("source_mutation_count", 0) > 0 or _guard_violation(summary, positive="source_mutation_executed", negative="no_source_mutation") for summary in child_summaries.values())
    world_truth_declared = any(
        item.get("guards", {}).get("world_truth_declared") is True
        or item.get("guards", {}).get("no_world_truth") is False
        or item.get("handoff_flags", {}).get("world_truth_declared") is True
        for summary in child_summaries.values()
        for item in (summary or {}).get("case_results", ())
    )
    child_regressions_ok = not failed_children and child_pass_count == len(CHILD_MODULES) and child_verifier_pass_count == len(CHILD_MODULES)
    doc_ok = _documentation_set_ok()
    summary = {
        "phase": PHASE,
        "attempt_id": attempt_id,
        "child_module_count": len(CHILD_MODULES),
        "child_runner_pass_count": child_pass_count,
        "child_verifier_pass_count": child_verifier_pass_count,
        "failed_child_ids": failed_children,
        "child_results": children,
        "cross_module_case_count": cross["cross_module_case_count"],
        "cross_module_pass_count": cross["cross_module_pass_count"],
        "failed_cross_module_case_ids": cross["failed_cross_module_case_ids"],
        "authority_continuity_ok": cross["authority_continuity_ok"],
        "responsibility_continuity_ok": cross["responsibility_continuity_ok"],
        "reference_continuity_ok": cross["reference_continuity_ok"],
        "version_domain_continuity_ok": cross["version_domain_continuity_ok"],
        "invalidation_continuity_ok": cross["invalidation_continuity_ok"],
        "constraint_continuity_ok": cross["constraint_continuity_ok"],
        "candidate_admission_execution_separation_ok": cross["candidate_binding_admission_execution_separation_ok"],
        "source_state_return_continuity_ok": cross["source_state_return_continuity_ok"],
        "failure_return_continuity_ok": cross["failure_return_continuity_ok"],
        "outcome_brain_boundary_ok": cross["outcome_brain_boundary_ok"],
        "loop_mechanical_boundary_ok": cross["loop_mechanical_boundary_ok"],
        "legacy_bypass_audit_ok": cross["active_bypass_count"] == 0,
        "legacy_audit": cross["legacy_audit"],
        "active_bypass_count": cross["active_bypass_count"],
        "active_bypass_ids": cross["active_bypass_ids"],
        "trace_provenance_ok": cross["trace_provenance_ok"],
        "runtime_execution_observed": runtime_execution_observed,
        "model_loading_observed": model_loading_observed,
        "provider_invocation_observed": provider_invocation_observed,
        "observation_execution_observed": observation_execution_observed,
        "action_execution_observed": action_execution_observed,
        "source_mutation_observed": source_mutation_observed,
        "world_truth_declared": world_truth_declared,
        "attempt_freshness_ok": all(child.get("attempt_id") == attempt_id and child.get("artifact_mode") == "current_in_memory_stdout" for child in children.values()),
        "no_stale_child_artifact_ok": all(child.get("stale_artifact_used") is False for child in children.values()),
        "documentation_set_ok": doc_ok,
        "cross_module_cases": cross["cases"],
        "child_regressions_ok": child_regressions_ok,
        "all_regressions_passed": bool(child_regressions_ok and doc_ok and not cross["failed_cross_module_case_ids"] and cross["active_bypass_count"] == 0 and not runtime_execution_observed and not model_loading_observed and not provider_invocation_observed and not observation_execution_observed and not action_execution_observed and not source_mutation_observed and not world_truth_declared),
    }
    return summary


if __name__ == "__main__":
    print(json.dumps(run_consolidated_regression(), indent=2, ensure_ascii=False))
