"""Interrupt control candidate types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class InterruptCandidateV1:
    cycle_id: str
    trigger: str
    related_refs: Tuple[str, ...]
    candidate_only: bool = True
    runtime_interrupt_executed: bool = False
    trace_ref: str = ""


@dataclass(frozen=True)
class SuspendCandidateV1:
    cycle_id: str
    reason: str
    related_refs: Tuple[str, ...]
    candidate_only: bool = True
    runtime_suspend_executed: bool = False
    trace_ref: str = ""


@dataclass(frozen=True)
class ResumeCandidateV1:
    cycle_id: str
    reason: str
    related_refs: Tuple[str, ...]
    candidate_only: bool = True
    runtime_resume_executed: bool = False
    trace_ref: str = ""


@dataclass(frozen=True)
class AbortCandidateV1:
    cycle_id: str
    reason: str
    related_refs: Tuple[str, ...]
    candidate_only: bool = True
    runtime_abort_executed: bool = False
    trace_ref: str = ""
