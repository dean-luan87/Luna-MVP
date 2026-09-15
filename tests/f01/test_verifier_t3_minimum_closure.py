from __future__ import annotations

import copy
import subprocess
from pathlib import Path

import pytest

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
from capabilities.evaluation.common.artifact_source_binding_v1 import (
    BINDING_INCOMPLETE,
    REVERIFY_REQUIRED,
    SOURCE_MISMATCH,
    TRUSTED_CURRENT_EVIDENCE,
    UNBOUND_LEGACY_EVIDENCE,
    sha256_file,
    verify_binding,
)
from capabilities.evaluation.common.verification_trust_composition_v1 import (
    BINDING_INVALID,
    SEMANTIC_FAILED,
    SEMANTIC_PASSED_UNBOUND,
    TRUSTED_CURRENT_EVIDENCE as COMPOSED_TRUSTED_CURRENT_EVIDENCE,
    compose_verification_trust,
)
from capabilities.evaluation.common.side_effect_observation_v1 import (
    CONTROLLED_WITHHOLD,
    OBSERVED_NOT_EXECUTED,
    classify_observer_record,
    classify_side_effect_map,
)
from capabilities.evaluation.provider_binding_runtime_allocation_execution_instance_controlled.engine_v1 import (
    ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1,
)
from capabilities.evaluation.provider_binding_runtime_allocation_execution_instance_controlled.verifier_v1 import (
    verify as verify_binding_allocation,
)
from capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.verifier_v1 import (
    verify as verify_provider_session,
)


ROOT = Path(__file__).resolve().parents[2]
RUNNER = "capabilities/evaluation/common/side_effect_observation_v1.py"
VERIFIER = "capabilities/evaluation/common/artifact_source_binding_v1.py"
FIXTURE = "capabilities/evaluation/provider_session_controlled_invocation_multiscenario_sandbox/fixtures_v1.py"
CONTRACT = "docs/architecture/governance/luna_repository_rebaseline_v1/artifact_source_binding_contract_v1.json"


def _head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def _binding(tmp_path: Path) -> tuple[dict[str, object], Path]:
    artifact = tmp_path / "runner_summary.json"
    artifact.write_text('{"status":"PASS"}\n', encoding="utf-8")
    binding = {
        "schema_version": "v1",
        "git_commit_sha": _head(),
        "worktree_state": "CLEAN",
        "baseline_source_manifest_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
        "runner_path": RUNNER,
        "runner_sha256": sha256_file(ROOT / RUNNER),
        "verifier_path": VERIFIER,
        "verifier_sha256": sha256_file(ROOT / VERIFIER),
        "fixture_paths": [{"path": FIXTURE, "sha256": sha256_file(ROOT / FIXTURE)}],
        "contract_paths": [{"path": CONTRACT, "sha256": sha256_file(ROOT / CONTRACT)}],
        "input_manifest_sha256": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
        "runner_artifact_sha256": sha256_file(artifact),
        "verification_timestamp": "2026-09-14T00:00:00Z",
        "verification_status": "PASS",
        "proof_scope": "F01_P3_CONTROLLED",
        "proof_tier": "T2",
        "provenance_status": TRUSTED_CURRENT_EVIDENCE,
    }
    return binding, artifact


def test_forged_observed_status_is_withheld() -> None:
    record = {
        "status": OBSERVED_NOT_EXECUTED,
        "values": {"network": False},
        "evidence_refs": ["producer:claim"],
    }
    assert classify_observer_record(record) == CONTROLLED_WITHHOLD


def test_controlled_no_request_status_remains_distinct() -> None:
    assert classify_side_effect_map({"provider": "REQUEST_NOT_ISSUED"}) == "REQUEST_NOT_ISSUED"


def test_missing_external_observation_is_unknown() -> None:
    assert classify_observer_record({}) == "UNKNOWN"


def test_runtime_assessment_keeps_controlled_scope_but_withholds_observation(tmp_path: Path) -> None:
    run_runtime_capability_assessment_v1(tmp_path)
    result = verify_runtime_capability_assessment_v1(tmp_path)
    assert result.controlled_scope_passed is True
    assert result.actual_side_effect_observation_status == "DECLARED_NOT_EXECUTED"
    assert result.final_candidate_decision.endswith("BLOCKED")


def test_runtime_dryrun_keeps_controlled_scope_but_withholds_observation(tmp_path: Path) -> None:
    run_runtime_skeleton_dryrun_v1(tmp_path)
    result = verify_runtime_skeleton_dryrun_v1(tmp_path)
    assert result.controlled_scope_passed is True
    assert result.actual_side_effect_observation_status == "DECLARED_NOT_EXECUTED"
    assert result.external_invocation_absent is False


def test_provider_session_producer_observation_is_not_external_proof() -> None:
    summary = {
        "verifier_observed_side_effects": {
            "status": OBSERVED_NOT_EXECUTED,
            "values": {"network": False},
            "independent_observer": True,
            "observer_ref": "forged:observer",
            "evidence_refs": ["runner:claim"],
        },
        "cases": [],
    }
    result = verify_provider_session(summary)
    assert result["actual_side_effect_observation_status"] == CONTROLLED_WITHHOLD
    assert result["all_checks_passed"] is False
    assert result["provenance_status"] == UNBOUND_LEGACY_EVIDENCE
    assert result["trusted_current_evidence"] is False


def test_forged_observer_record_with_all_metadata_is_withheld() -> None:
    record = {
        "status": OBSERVED_NOT_EXECUTED,
        "values": {"network": False, "provider": False},
        "independent_observer": True,
        "observer_ref": "forged:observer",
        "evidence_refs": ["forged:evidence"],
    }
    assert classify_observer_record(record) == CONTROLLED_WITHHOLD
    assert classify_observer_record(record) != OBSERVED_NOT_EXECUTED


def test_forged_binding_mapping_cannot_establish_trust() -> None:
    forged = {
        "trusted": True,
        "status": TRUSTED_CURRENT_EVIDENCE,
        "provenance_status": TRUSTED_CURRENT_EVIDENCE,
    }
    result = compose_verification_trust(semantic_passed=True, binding_result=forged)  # type: ignore[arg-type]
    assert result.state == BINDING_INVALID
    assert result.trusted_current_evidence is False


def test_provider_verifier_ignores_caller_binding_result() -> None:
    forged = {
        "trusted": True,
        "status": TRUSTED_CURRENT_EVIDENCE,
        "provenance_status": TRUSTED_CURRENT_EVIDENCE,
    }
    result = verify_provider_session({}, binding_result=forged)
    assert result["trusted_current_evidence"] is False
    assert result["provenance_status"] == UNBOUND_LEGACY_EVIDENCE


def test_semantic_pass_without_binding_is_explicitly_unbound() -> None:
    result = compose_verification_trust(semantic_passed=True, binding_result=None)
    assert result.state == SEMANTIC_PASSED_UNBOUND
    assert result.trusted_current_evidence is False


def test_semantic_pass_with_invalid_binding_is_not_trusted(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["runner_artifact_sha256"] = "sha256:" + "0" * 64
    invalid = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    result = compose_verification_trust(semantic_passed=True, binding_result=invalid)
    assert result.state == BINDING_INVALID
    assert result.trusted_current_evidence is False


def test_semantic_pass_with_canonical_valid_binding_is_trusted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    binding, artifact = _binding(tmp_path)
    import capabilities.evaluation.common.artifact_source_binding_v1 as binding_module

    monkeypatch.setattr(binding_module, "_tracked_worktree_clean", lambda _: True)
    verified = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    result = compose_verification_trust(semantic_passed=True, binding_result=verified)
    assert result.state == COMPOSED_TRUSTED_CURRENT_EVIDENCE
    assert result.trusted_current_evidence is True


def test_semantic_failure_cannot_become_trusted_with_valid_binding(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    binding, artifact = _binding(tmp_path)
    import capabilities.evaluation.common.artifact_source_binding_v1 as binding_module

    monkeypatch.setattr(binding_module, "_tracked_worktree_clean", lambda _: True)
    verified = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    result = compose_verification_trust(semantic_passed=False, binding_result=verified)
    assert result.state == SEMANTIC_FAILED
    assert result.trusted_current_evidence is False


def test_aggregate_pass_cannot_override_invalid_binding() -> None:
    invalid = compose_verification_trust(
        semantic_passed=True,
        binding_result={"trusted": True, "status": TRUSTED_CURRENT_EVIDENCE},  # type: ignore[arg-type]
    )
    assert invalid.state == BINDING_INVALID
    assert invalid.trusted_current_evidence is False


def test_valid_source_binding_succeeds(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    binding, artifact = _binding(tmp_path)
    import capabilities.evaluation.common.artifact_source_binding_v1 as binding_module

    monkeypatch.setattr(binding_module, "_tracked_worktree_clean", lambda _: True)
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is True
    assert result["status"] == TRUSTED_CURRENT_EVIDENCE


def test_wrong_commit_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["git_commit_sha"] = "0" * 40
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["status"] == SOURCE_MISMATCH
    assert result["trusted"] is False


def test_wrong_verifier_digest_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["verifier_sha256"] = "sha256:" + "0" * 64
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False


def test_wrong_runner_digest_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["runner_sha256"] = "sha256:" + "0" * 64
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False


def test_wrong_fixture_digest_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["fixture_paths"][0]["sha256"] = "sha256:" + "0" * 64
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False


def test_missing_required_file_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["fixture_paths"] = [{"path": "missing/fixture.py", "sha256": "sha256:" + "0" * 64}]
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False
    assert any("file_unavailable" in error for error in result["errors"])


def test_duplicate_bound_path_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["contract_paths"] = [{"path": RUNNER, "sha256": sha256_file(ROOT / RUNNER)}]
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False


def test_path_traversal_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["fixture_paths"] = [{"path": "../outside.py", "sha256": "sha256:" + "0" * 64}]
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False


def test_artifact_digest_mismatch_fails(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["runner_artifact_sha256"] = "sha256:" + "0" * 64
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False


def test_legacy_unbound_artifact_requires_reverification() -> None:
    assert UNBOUND_LEGACY_EVIDENCE != TRUSTED_CURRENT_EVIDENCE
    assert REVERIFY_REQUIRED != TRUSTED_CURRENT_EVIDENCE


def test_dirty_tracked_source_withholds_trust(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    binding, artifact = _binding(tmp_path)
    import capabilities.evaluation.common.artifact_source_binding_v1 as binding_module

    monkeypatch.setattr(binding_module, "_tracked_worktree_clean", lambda _: False)
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False
    assert result["status"] == "WORKTREE_DIRTY"


def test_unrelated_untracked_scope_does_not_fail_clean_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    binding, artifact = _binding(tmp_path)
    import capabilities.evaluation.common.artifact_source_binding_v1 as binding_module

    monkeypatch.setattr(binding_module, "_tracked_worktree_clean", lambda _: True)
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["tracked_worktree_clean"] is True


def test_duplicate_case_identity_fails_before_dict_collapse() -> None:
    summary = ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1().run()
    duplicate = copy.deepcopy(summary)
    duplicate["cases"].append(copy.deepcopy(duplicate["cases"][0]))
    assert verify_binding_allocation(duplicate)["all_checks_passed"] is False


def test_unbound_provider_binding_cannot_return_trusted_go() -> None:
    summary = ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1().run()
    result = verify_binding_allocation(summary)
    assert result["controlled_scope_passed"] is True
    assert result["provenance_status"] == UNBOUND_LEGACY_EVIDENCE
    assert result["trusted_current_evidence"] is False
    assert result["final_decision"] != "GO"


def test_aggregate_pass_cannot_override_binding_failure(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["runner_artifact_sha256"] = "sha256:" + "0" * 64
    binding["verification_status"] = "PASS"
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is False


def test_claimed_commit_cannot_override_observed_head(tmp_path: Path) -> None:
    binding, artifact = _binding(tmp_path)
    binding["git_commit_sha"] = "f" * 40
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["actual_git_commit_sha"] == _head()
    assert result["trusted"] is False


def test_baseline_hash_is_lineage_metadata_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    binding, artifact = _binding(tmp_path)
    binding["baseline_source_manifest_hash"] = "sha256:" + "f" * 64
    import capabilities.evaluation.common.artifact_source_binding_v1 as binding_module

    monkeypatch.setattr(binding_module, "_tracked_worktree_clean", lambda _: True)
    result = verify_binding(binding, repo_root=ROOT, artifact_path=artifact)
    assert result["trusted"] is True
    assert result["baseline_source_manifest_hash"] == "sha256:" + "f" * 64
