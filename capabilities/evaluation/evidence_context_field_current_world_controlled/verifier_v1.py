"""Verifier for the controlled Evidence -> Field / Current World seam."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.evidence_context_field_current_world_controlled.engine_v1 import EvidenceContextFieldCurrentWorldControlledEngineV1

import json
import sys
from pathlib import Path
from typing import Any, Mapping

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
)

from .fixtures_v1 import (
    EVALUATION_MARKER,
    build_evidence_context_field_current_world_cases_v1,
)


DEFAULT_SUMMARY = Path(
    "_eval_out/evidence_context_field_current_world_controlled_v1/runner_summary_v1.json"
)


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _contains_no_semantic_payload(value: Any) -> bool:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    forbidden = (
        "exit_found",
        "sign_detected",
        "person_count",
        "road_open",
        "object_detected",
        "text_recognized",
    )
    return not any(token in text for token in forbidden)


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: EvidenceContextFieldCurrentWorldControlledEngineV1().run(),
        source="R13 evidence context field current world; canonical fixture + independent engine invocation",
        compare_top_level=("phase", "source_mode"),
    )
    failed = sorted(name for name, passed in proof.items() if not passed)
    return {
        "phase": summary.get("phase"),
        "checks": proof,
        "failed_checks": failed,
        "all_checks_passed": not failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "proof_provenance": {
            "expected_source": "canonical fixture + independent engine invocation",
            "observed_source": "runner summary artifact",
            "recomputed_source": "fresh EvidenceContextFieldCurrentWorldControlledEngineV1().run()",
        },
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    result = verify(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["final_decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
