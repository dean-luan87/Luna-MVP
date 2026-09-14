"""Metadata/evidence types for integrated baseline closure."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple


FREEZE_STATES = ("NOT_READY", "READY_TO_FREEZE", "FROZEN_BY_USER_DECISION")
VERIFICATION_STATUSES = ("PENDING", "VERIFIED", "BLOCKED")


@dataclass(frozen=True)
class RegressionEvidenceRecordV1:
    suite_id: str
    runner_ref: str
    verifier_ref: str
    expected_scenario_count: Any
    observed_scenario_count: Optional[int] = None
    all_cases_passed: Optional[bool] = None
    failed_case_ids: Tuple[str, ...] = ()
    blocker_count: Optional[int] = None
    verification_status: str = "PENDING"
    artifact_ref: Optional[str] = None
    verified_by_user_terminal: bool = False
    evidence_basis: str = "explicit_user_terminal_record"
    runner_stdout_observed: Optional[bool] = None
    coverage_mode: Optional[str] = None
    subscope_refs: Tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any], *, expected: Mapping[str, Any]) -> "RegressionEvidenceRecordV1":
        failed = raw.get("failed_case_ids")
        if not isinstance(failed, (list, tuple)):
            failed = ()
        return cls(
            suite_id=str(raw.get("suite_id", expected.get("id", ""))),
            runner_ref=str(raw.get("runner_ref", expected.get("runner", ""))),
            verifier_ref=str(raw.get("verifier_ref", expected.get("verifier", ""))),
            expected_scenario_count=expected.get("scenario_count"),
            observed_scenario_count=raw.get("observed_scenario_count"),
            all_cases_passed=raw.get("all_cases_passed"),
            failed_case_ids=tuple(str(value) for value in failed),
            blocker_count=raw.get("blocker_count"),
            verification_status=str(raw.get("verification_status", "PENDING")),
            artifact_ref=raw.get("artifact_ref"),
            verified_by_user_terminal=bool(raw.get("verified_by_user_terminal", False)),
            evidence_basis=str(raw.get("evidence_basis", "explicit_user_terminal_record")),
            runner_stdout_observed=raw.get("runner_stdout_observed"),
            coverage_mode=raw.get("coverage_mode"),
            subscope_refs=tuple(str(value) for value in raw.get("subscope_refs", ())),
        )


@dataclass(frozen=True)
class FreezeCandidateV1:
    state: str
    eligible: bool
    reasons: Tuple[str, ...]
    manifest_state_mutated: bool = False
