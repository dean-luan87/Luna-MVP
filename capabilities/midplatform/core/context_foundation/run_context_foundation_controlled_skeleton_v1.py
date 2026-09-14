#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlled synthetic runner for Context Foundation skeleton v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Tuple


if __package__ in {None, ""}:
    REPO_ROOT = Path(__file__).resolve().parents[4]
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.context_foundation.context_foundation_fixture_v1 import (
    get_context_foundation_fixture_cases_v1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_skeleton_v1 import (
    ContextFoundationSkeletonV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_static_validators_v1 import (
    validate_context_envelope_boundary,
)


def run_controlled_skeleton() -> Tuple[Dict[str, Any], ...]:
    skeleton = ContextFoundationSkeletonV1()
    results = []
    for fixture_case in get_context_foundation_fixture_cases_v1():
        envelope = skeleton.assemble_context(fixture_case.assembly_input)
        snapshot = skeleton.get_context_snapshot(envelope)
        trace = skeleton.create_trace(
            fixture_case.assembly_input,
            (
                "validate_projection_references",
                "preserve_unknown_and_source_owner",
                "assemble_reference_only_envelope_candidate",
                "create_context_trace_candidate",
            ),
        )
        boundary_result = validate_context_envelope_boundary(snapshot)
        results.append(
            {
                "case_id": fixture_case.case_id,
                "context_envelope": asdict(snapshot),
                "trace": asdict(trace),
                "boundary_valid": boundary_result.valid,
                "boundary_issues": boundary_result.issues,
                "forbidden_outputs": fixture_case.forbidden_outputs,
                "synthetic_only": True,
                "skeleton_only": True,
                "runtime_executed": False,
                "state_mutation": False,
                "database_accessed": False,
                "model_called": False,
            }
        )
    return tuple(results)


def main() -> int:
    payload = {
        "runner": "context_foundation_controlled_skeleton_v1",
        "results": run_controlled_skeleton(),
        "skeleton_only": True,
        "runtime_executed": False,
        "state_mutation": False,
        "final_phase_decision_emitted": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
