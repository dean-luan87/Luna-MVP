# -*- coding: utf-8 -*-
"""Document Surface — iteration validation v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_validation_v1 import (
    validate_controlled_outputs,
)


def validate_iteration_outputs(outputs: Dict[str, Any]) -> Dict[str, Any]:
    base = validate_controlled_outputs(outputs)
    relations = outputs.get("relation_hint_candidates") or []
    fake = any(r.get("fake_relation") for r in relations)
    forced = outputs.get("overlap_strategy", {}).get("forced_two_surface") is True
    no_evidence = [r for r in relations if not r.get("evidence_basis")]
    if fake:
        base["abort_reason"] = "fake_relation_detected"
        base["validation_status_candidate"] = "aborted"
    if forced:
        base["abort_reason"] = "forced_multi_surface_detected"
        base["validation_status_candidate"] = "aborted"
    if no_evidence:
        base["validation_status_candidate"] = "aborted"
        base["abort_reason"] = "relation_without_evidence"
    base["fake_relation_rate"] = 1.0 if fake else 0.0
    base["forced_multi_surface_rate"] = 1.0 if forced else 0.0
    base["relation_without_evidence_count"] = len(no_evidence)
    return base
