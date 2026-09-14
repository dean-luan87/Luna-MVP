from __future__ import annotations

import copy
import json
from pathlib import Path

from capabilities.cognitive_flow.cognitive_analysis.runtime_assessment.cognitive_analysis_runtime_assessment_runner_v1 import (
    run_runtime_capability_assessment_v1,
)
from capabilities.cognitive_flow.cognitive_analysis.runtime_assessment.cognitive_analysis_runtime_assessment_verifier_v1 import (
    verify_runtime_capability_assessment_v1,
)
from capabilities.cognitive_flow.cognitive_analysis.runtime_dryrun.cognitive_analysis_runtime_dryrun_runner_v1 import (
    run_runtime_skeleton_dryrun_v1,
)
from capabilities.cognitive_flow.cognitive_analysis.runtime_dryrun.cognitive_analysis_runtime_dryrun_verifier_v1 import (
    verify_runtime_skeleton_dryrun_v1,
)
from capabilities.cognitive_flow.cognitive_analysis.runtime_validation.cognitive_analysis_runtime_validation_runner_v1 import (
    run_runtime_validation_closure_v1,
)
from capabilities.cognitive_flow.cognitive_analysis.runtime_validation.cognitive_analysis_runtime_validation_verifier_v1 import (
    verify_runtime_validation_closure_v1,
)
from capabilities.evaluation.governance_verification_backbone_core_rules_controlled.engine_v1 import (
    GovernanceVerificationBackboneEvaluationEngineV1,
)
from capabilities.evaluation.governance_verification_backbone_core_rules_controlled.verifier_v1 import (
    _run_checks,
)
from capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.verifier_v1 import (
    verify as verify_provider_session_summary,
)
from tools.run_arch_guard import dcs_check_trace


def test_runtime_assessment_uses_independent_determinism_evidence(tmp_path: Path) -> None:
    report = run_runtime_capability_assessment_v1(tmp_path)
    assert report.determinism_status == "DETERMINISM_VERIFIED"
    assert report.determinism_evidence["reconstruction_a"] != report.determinism_evidence["reconstruction_b"]

    verification = verify_runtime_capability_assessment_v1(tmp_path)
    assert verification.determinism_status == "DETERMINISM_VERIFIED"
    assert verification.side_effect_evidence_status == "DECLARED_NOT_EXECUTED"
    assert verification.final_candidate_decision.endswith("BLOCKED")


def test_runtime_dryrun_uses_independent_reconstruction(tmp_path: Path) -> None:
    run_runtime_skeleton_dryrun_v1(tmp_path)
    verification = verify_runtime_skeleton_dryrun_v1(tmp_path)
    assert verification.determinism_status == "DETERMINISM_VERIFIED"
    assert verification.side_effect_evidence_status == "DECLARED_NOT_EXECUTED"
    assert verification.external_invocation_absent is False
    assert verification.final_candidate_decision.endswith("BLOCKED")


def test_runtime_validation_does_not_upgrade_single_artifact_to_determinism(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    validation_dir = tmp_path / "validation"
    run_runtime_skeleton_dryrun_v1(input_dir)
    result = run_runtime_validation_closure_v1(input_dir, validation_dir)
    assert result.determinism_status == "DETERMINISM_UNVERIFIED"

    verification = verify_runtime_validation_closure_v1(input_dir, validation_dir)
    assert verification.determinism_status == "DETERMINISM_UNVERIFIED"
    assert verification.final_candidate_decision.endswith("BLOCKED")


def test_provider_required_cases_fail_closed_for_missing_empty_wrong_type_duplicate_and_missing_expected() -> None:
    assert verify_provider_session_summary({})["all_checks_passed"] is False
    assert verify_provider_session_summary({"cases": []})["all_checks_passed"] is False
    assert verify_provider_session_summary({"cases": {}})["all_checks_passed"] is False
    duplicate = {"cases": [{"case_id": "DUP"}, {"case_id": "DUP"}]}
    assert verify_provider_session_summary(duplicate)["all_checks_passed"] is False
    missing_expected = {"cases": [{"case_id": "UNRELATED"}]}
    assert verify_provider_session_summary(missing_expected)["all_checks_passed"] is False


def test_provider_determinism_requires_independent_proof() -> None:
    summary = {"cases": [{"case_id": "DETERMINISTIC_SESSION_REF", "sessions": []}]}
    result = verify_provider_session_summary(summary)
    assert any(name == "session_ref_deterministic" for name in result["failed_checks"])


def test_provider_declared_side_effect_flags_are_not_observation_proof() -> None:
    summary = {
        "cases": [],
        "synthetic_only": True,
        "controlled": True,
        "no_real_runtime_effect": True,
        "no_real_provider_effect": True,
        "no_real_model_effect": True,
        "real_provider_invoked": False,
        "real_model_invoked": False,
        "network_called": False,
        "subprocess_started": False,
        "thread_started": False,
        "socket_used": False,
        "runtime_observation_created": False,
        "gateway_submission": False,
        "evidence_created": False,
        "truth_declared": False,
        "world_truth_declared": False,
    }
    result = verify_provider_session_summary(summary)
    assert "no_real_effects_verifier_observed" in result["failed_checks"]


def test_legacy_artifact_without_proof_fields_is_blocked(tmp_path: Path) -> None:
    run_runtime_skeleton_dryrun_v1(tmp_path)
    run_path = tmp_path / "cognitive_analysis_runtime_dryrun_run_result_v1.json"
    legacy = json.loads(run_path.read_text(encoding="utf-8"))
    legacy.pop("determinism_status", None)
    legacy.pop("determinism_evidence", None)
    legacy.pop("side_effect_evidence", None)
    run_path.write_text(json.dumps(legacy, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    verification = verify_runtime_skeleton_dryrun_v1(tmp_path)
    assert verification.determinism_status == "DETERMINISM_UNVERIFIED"
    assert verification.side_effect_evidence_status == "UNKNOWN"
    assert verification.final_candidate_decision.endswith("BLOCKED")


def test_governance_expected_result_tampering_is_detected() -> None:
    summary = GovernanceVerificationBackboneEvaluationEngineV1().run()
    tampered = copy.deepcopy(summary)
    target = next(case for case in tampered["cases"] if case["case_id"] == "GOVERNED_PHASE_VALID")
    target["expected"]["status"] = "WRONG"
    target["result"]["status"] = "WRONG"
    checks = _run_checks(tampered)
    assert any(item["check_id"] == "GOVERNED_PHASE_VALID:status" and not item["passed"] for item in checks)


def test_summary_aggregate_fields_do_not_override_governance_checks() -> None:
    summary = GovernanceVerificationBackboneEvaluationEngineV1().run()
    summary["all_checks_passed"] = True
    summary["passed_count"] = 10**9
    summary["final_decision"] = "GO"
    checks = _run_checks(summary)
    assert isinstance(checks, list)
    assert all("passed" in item for item in checks)


def test_architecture_guard_trace_states_fail_closed(tmp_path: Path) -> None:
    missing = dcs_check_trace(str(tmp_path / "missing.jsonl"))
    assert missing.ok is False
    assert missing.status == "TRACE_MISSING"

    empty_path = tmp_path / "empty.jsonl"
    empty_path.write_text("\n", encoding="utf-8")
    empty = dcs_check_trace(str(empty_path))
    assert empty.ok is False
    assert empty.status == "TRACE_EMPTY"

    invalid_path = tmp_path / "invalid.jsonl"
    invalid_path.write_text('{"not_time": true}\n', encoding="utf-8")
    invalid = dcs_check_trace(str(invalid_path))
    assert invalid.ok is False
    assert invalid.status == "TRACE_NO_VALID_RECORDS"
