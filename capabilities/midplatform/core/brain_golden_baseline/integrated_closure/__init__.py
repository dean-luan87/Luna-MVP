"""Thin integrated closure surface for the Brain Golden Baseline."""

from .integrated_closure_governance_v1 import (
    build_closure_result,
    evaluate_freeze_candidate,
    load_terminal_evidence,
)

__all__ = ["build_closure_result", "evaluate_freeze_candidate", "load_terminal_evidence"]
