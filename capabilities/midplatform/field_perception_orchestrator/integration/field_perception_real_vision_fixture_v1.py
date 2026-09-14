from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class S3FixtureCaseV1:
    case_id: str
    title: str
    information_need: str = "detect visual target"
    expected_evidence_kinds: Tuple[str, ...] = ("VISION_DETECTION",)
    requested_capability_kinds: Tuple[str, ...] = ("VISION_DETECTION",)
    provider_admitted: bool = True
    expected_accept: bool = True
    expected_error: str = ""
    provider_failure: bool = False
    budget_exhausted: bool = False
    contradiction: bool = False
    received_evidence: bool = False
    duplicate_inference: bool = False
    duplicate_evidence: bool = False


def build_s3_fixture_cases() -> Tuple[S3FixtureCaseV1, ...]:
    return (
        S3FixtureCaseV1("S3-01", "valid authorized vision demand"),
        S3FixtureCaseV1("S3-02", "no demand -> YOLO forbidden", information_need="", provider_admitted=False, expected_accept=False, expected_error="PROVIDER_NOT_ADMITTED"),
        S3FixtureCaseV1("S3-03", "raw frame arrival alone -> YOLO forbidden", information_need="", provider_admitted=False, expected_accept=False, expected_error="PROVIDER_NOT_ADMITTED"),
        S3FixtureCaseV1("S3-04", "model available alone -> YOLO forbidden", information_need="", provider_admitted=False, expected_accept=False, expected_error="PROVIDER_NOT_ADMITTED"),
        S3FixtureCaseV1("S3-05", "bounded provider session"),
        S3FixtureCaseV1("S3-06", "detection evidence mapping"),
        S3FixtureCaseV1("S3-07", "bbox preserved"),
        S3FixtureCaseV1("S3-08", "confidence preserved"),
        S3FixtureCaseV1("S3-09", "provider/model refs preserved"),
        S3FixtureCaseV1("S3-10", "frame ref preserved"),
        S3FixtureCaseV1("S3-11", "trace/provenance reverse lookup"),
        S3FixtureCaseV1("S3-12", "detection does not become fact"),
        S3FixtureCaseV1("S3-13", "detection does not mutate Field"),
        S3FixtureCaseV1("S3-14", "detection does not mutate Current World"),
        S3FixtureCaseV1("S3-15", "detection does not create Intent"),
        S3FixtureCaseV1("S3-16", "detection does not create Task"),
        S3FixtureCaseV1("S3-17", "detection does not call OCR"),
        S3FixtureCaseV1("S3-18", "detection does not call SLAM"),
        S3FixtureCaseV1("S3-19", "detection does not call VLM"),
        S3FixtureCaseV1("S3-20", "sufficient evidence -> STOP", received_evidence=True),
        S3FixtureCaseV1("S3-21", "insufficient evidence -> bounded CONTINUE"),
        S3FixtureCaseV1("S3-22", "contradiction -> reconsideration", contradiction=True, received_evidence=True),
        S3FixtureCaseV1("S3-23", "provider failure", provider_failure=True, expected_accept=False, expected_error="PROVIDER_INVOCATION_FAILED"),
        S3FixtureCaseV1("S3-24", "budget/session exhaustion", budget_exhausted=True, expected_accept=False, expected_error="SESSION_BUDGET_EXHAUSTED"),
        S3FixtureCaseV1("S3-25", "duplicate frame/inference guard", duplicate_inference=True, expected_accept=False, expected_error="DUPLICATE_INFERENCE_REQUEST"),
        S3FixtureCaseV1("S3-26", "duplicate evidence guard", duplicate_evidence=True, received_evidence=True),
        S3FixtureCaseV1("S3-27", "no semantic compression"),
        S3FixtureCaseV1("S3-28", "S0/S1/S2 regressions remain PASS"),
    )


__all__ = ["S3FixtureCaseV1", "build_s3_fixture_cases"]
