"""Adapter/device/provider reference candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdapterReferenceCandidateV1:
    adapter_ref: str
    capability_match: bool
    mismatch_reason: str | None
    real_adapter_call_executed: bool = False
    real_device_call_executed: bool = False
    real_provider_call_executed: bool = False
    candidate_only: bool = True
