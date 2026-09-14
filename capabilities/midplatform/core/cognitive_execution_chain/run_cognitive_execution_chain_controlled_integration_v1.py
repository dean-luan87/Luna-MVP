"""Controlled runner for Cognitive Execution Chain integration v1.

This runner is intended for user-terminal execution only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (
            candidate / "capabilities/midplatform/core/cognitive_execution_chain"
        ).is_dir():
            return candidate

    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_execution_chain").is_dir():
        return cwd

    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_engine_v1 import (  # noqa: E402
    CognitiveExecutionChainEngineV1,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_fixture_v1 import (  # noqa: E402
    get_cognitive_execution_chain_fixtures_v1,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/cognitive_execution_chain_controlled_integration_v1"


def run_controlled() -> Dict[str, Any]:
    engine = CognitiveExecutionChainEngineV1()
    fixtures = get_cognitive_execution_chain_fixtures_v1()

    results: List[Dict[str, Any]] = []
    for case in fixtures:
        record = engine.run_case(case.directive)
        results.append(
            {
                "case_id": case.case_id,
                "category": case.category,
                "description": case.description,
                "stopped_at": record.stopped_at,
                "runtime_attempted": record.runtime_attempted,
                "handoff_path": list(record.handoff_path),
                "compatibility": [
                    {
                        "hop_id": c.hop_id,
                        "compatibility_status": c.compatibility_status,
                        "allow_handoff": c.allow_handoff,
                        "hard_block": c.hard_block,
                        "reason": c.reason,
                    }
                    for c in record.compatibility
                ],
                "trace": {
                    "root_trace_id": record.end_to_end_trace.root_trace_id,
                    "intent_trace_ref": record.end_to_end_trace.intent_trace_ref,
                    "causal_trace_ref": record.end_to_end_trace.causal_trace_ref,
                    "decision_trace_ref": record.end_to_end_trace.decision_trace_ref,
                    "action_trace_ref": record.end_to_end_trace.action_trace_ref,
                    "execution_trace_ref": record.end_to_end_trace.execution_trace_ref,
                },
                "provenance": {
                    "execution_result_ref": record.provenance.execution_result_ref,
                    "action_candidate_ref": record.provenance.action_candidate_ref,
                    "decision_candidate_ref": record.provenance.decision_candidate_ref,
                    "causal_hypothesis_refs": list(
                        record.provenance.causal_hypothesis_refs
                    ),
                    "intent_candidate_refs": list(
                        record.provenance.intent_candidate_refs
                    ),
                    "source_evidence_or_context_refs": list(
                        record.provenance.source_evidence_or_context_refs
                    ),
                    "reverse_locatable": record.provenance.reverse_locatable,
                },
                "reconsideration_candidates": [
                    {
                        "route_id": r.route_id,
                        "source_owner": r.source_owner,
                        "target_owner": r.target_owner,
                        "reason": r.reason,
                        "related_refs": list(r.related_refs),
                    }
                    for r in record.reconsideration_candidates
                ],
                "diagnostics_candidates": [
                    {
                        "origin_layer": d.origin_layer,
                        "error_namespace": d.error_namespace,
                        "trace_refs": list(d.trace_refs),
                        "failure_category": d.failure_category,
                        "remediation_candidate_refs": list(
                            d.remediation_candidate_refs
                        ),
                    }
                    for d in record.diagnostics_candidates
                ],
                "errors": [
                    {
                        "code": e.code,
                        "message": e.message,
                        "category": e.category,
                        "recoverable": e.recoverable,
                    }
                    for e in record.errors
                ],
                "negative_guards": {
                    "integration_has_no_owner": True,
                    "source_mutation": False,
                    "runtime_side_effect": record.runtime_side_effect,
                    "database_write": False,
                    "device_control": False,
                    "scheduler_execution": False,
                    "task_mutation": False,
                    "field_mutation": False,
                    "memory_mutation": False,
                    "silent_retry": False,
                    "owner_bypass": record.owner_bypass,
                    "runtime_bypass": record.runtime_bypass,
                },
                "metadata": record.metadata,
            }
        )

    passed = sum(1 for item in results if len(item["errors"]) == 0)
    summary = {
        "phase": "Phase-Luna-Cognitive-Execution-Chain-Controlled-Integration-v1-001",
        "scenario_count": len(results),
        "passed_scenario_count": passed,
        "failed_scenario_count": len(results) - passed,
        "candidate_only": True,
        "runtime_executed": False,
        "database_write": False,
        "device_control": False,
        "scheduler_execution": False,
        "task_mutation": False,
        "field_mutation": False,
        "memory_mutation": False,
        "status": "COGNITIVE_EXECUTION_CHAIN_CONTROLLED_INTEGRATION_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": results,
        "trace": {
            "trace_id": "cognitive-execution-chain-controlled-integration-trace-v1",
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "cognitive_execution_chain_result_v1.json"
    cases_path = OUTPUT_DIR / "cognitive_execution_chain_case_results_v1.json"
    trace_path = OUTPUT_DIR / "cognitive_execution_chain_trace_v1.json"

    result_path.write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    cases_path.write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    trace_path.write_text(
        json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "result": str(result_path),
        "cases": str(cases_path),
        "trace": str(trace_path),
    }


def main() -> int:
    payload = run_controlled()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
