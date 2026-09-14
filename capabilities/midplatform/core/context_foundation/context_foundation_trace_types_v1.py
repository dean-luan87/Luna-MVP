# -*- coding: utf-8 -*-
"""Trace types for Context Foundation controlled skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class ContextFoundationTraceV1:
    trace_id: str
    input_projection_refs: Tuple[str, ...]
    assembly_steps: Tuple[str, ...]
    output_context_reference: str
    timestamp: str
    status: str
    provenance: Tuple[str, ...] = field(default_factory=tuple)
    skeleton_only: bool = True
    runtime_executed: bool = False
    state_mutation_executed: bool = False

