"""Compose semantic verification with canonical provenance binding."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .artifact_source_binding_v1 import (
    BindingVerificationResult,
    BINDING_INVALID,
    REVERIFY_REQUIRED,
    TRUSTED_CURRENT_EVIDENCE,
    UNBOUND_LEGACY_EVIDENCE,
    is_canonical_binding_result,
)


SEMANTIC_FAILED = "SEMANTIC_FAILED"
SEMANTIC_PASSED_UNBOUND = "SEMANTIC_PASSED_UNBOUND"


@dataclass(frozen=True)
class TrustCompositionResult:
    """Layered trust result; it does not recompute semantic truth."""

    state: str
    semantic_passed: bool
    trusted_current_evidence: bool
    binding_status: str | None

    def __getitem__(self, key: str) -> Any:
        return {
            "state": self.state,
            "semantic_passed": self.semantic_passed,
            "trusted_current_evidence": self.trusted_current_evidence,
            "binding_status": self.binding_status,
        }[key]


def compose_verification_trust(
    *,
    semantic_passed: bool,
    binding_result: BindingVerificationResult | None,
) -> TrustCompositionResult:
    """Require a canonical binding result before trusted-current evidence."""
    if not semantic_passed:
        return TrustCompositionResult(
            state=SEMANTIC_FAILED,
            semantic_passed=False,
            trusted_current_evidence=False,
            binding_status=getattr(binding_result, "status", None),
        )
    if binding_result is None:
        return TrustCompositionResult(
            state=SEMANTIC_PASSED_UNBOUND,
            semantic_passed=True,
            trusted_current_evidence=False,
            binding_status=None,
        )
    if not is_canonical_binding_result(binding_result):
        return TrustCompositionResult(
            state=BINDING_INVALID,
            semantic_passed=True,
            trusted_current_evidence=False,
            binding_status=None,
        )
    if binding_result.status == TRUSTED_CURRENT_EVIDENCE and binding_result.trusted:
        state = TRUSTED_CURRENT_EVIDENCE
    elif binding_result.status == REVERIFY_REQUIRED:
        state = REVERIFY_REQUIRED
    else:
        state = BINDING_INVALID
    return TrustCompositionResult(
        state=state,
        semantic_passed=True,
        trusted_current_evidence=state == TRUSTED_CURRENT_EVIDENCE,
        binding_status=binding_result.status,
    )


def legacy_provenance_status(trust: TrustCompositionResult) -> str:
    """Return the existing output vocabulary while exposing ``trust.state``."""
    if trust.state in {SEMANTIC_PASSED_UNBOUND, SEMANTIC_FAILED}:
        return UNBOUND_LEGACY_EVIDENCE
    return trust.state


__all__ = [
    "BINDING_INVALID",
    "SEMANTIC_FAILED",
    "SEMANTIC_PASSED_UNBOUND",
    "TRUSTED_CURRENT_EVIDENCE",
    "TrustCompositionResult",
    "compose_verification_trust",
    "legacy_provenance_status",
]
