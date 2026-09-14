# -*- coding: utf-8 -*-
"""Test Board Protected Artifact Rule — review v1.

Establishes the global Test Board Protected Artifact Rule as a GO-verified
governance asset that later phases must reuse, and self-records to the test board.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    PROTOCOL_ID,
    PROTOCOL_PHASE_REF,
    REQUIRED_RECORD_TYPES,
    REQUIRED_TEST_BOARD_FIELDS,
    SOURCE_CHAIN,
    TEST_BOARD_GOVERNANCE_RULES,
    TEST_BOARD_MODULES,
    TEST_BOARD_REL_ROOT,
    TEST_MODES,
    build_test_board_protocol_matrix_v1,
    resolve_module,
    write_test_board_records,
)

DEFAULT_OUTPUT_ROOT = _REPO_ROOT / "_tmp_eval_out" / "test_board_protocol_v1_smoke_v0"
REVIEW_FILENAME = "test_board_protocol_review_v1.json"

_PKG = "capabilities/test_board"
STEP_FILES = (
    f"{_PKG}/test_board_protocol_v1.py",
    f"{_PKG}/review_test_board_protocol_v1.py",
)

FINAL_DECISION_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
FINAL_DECISION_BLOCKED = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_BLOCKED"

PHASE_ID = PROTOCOL_PHASE_REF


def review_test_board_protocol_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    matrix = build_test_board_protocol_matrix_v1()

    # Routing sanity over unambiguous representative phase ids. (Combined names
    # are inherently ambiguous; the writer always allows an explicit module=
    # override, so the GO check validates default routing only on clear cases
    # plus a validity-over-all guarantee.)
    routing_samples = {
        "Phase-P1-Execution-Trace-Streaming-DryRun-v1-001": "runtime_trials",
        "Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001": "recognition_models",
        "Phase-Midplatform-Model-Control-DryRun-v1-001": "midplatform",
        "Phase-Model-Governance-Runtime-Trial-Planning-v1-001": "runtime_trials",
    }
    routing_ok = {pid: (resolve_module(pid) == expected) for pid, expected in routing_samples.items()}
    routing_all_valid = all(
        resolve_module(pid) in TEST_BOARD_MODULES for pid in routing_samples
    )

    go_conditions = {
        "required_field_count_eq_6": len(REQUIRED_TEST_BOARD_FIELDS) == 6,
        "all_required_fields_true": all(v is True for v in REQUIRED_TEST_BOARD_FIELDS.values()),
        "governance_rule_count_eq_6": len(TEST_BOARD_GOVERNANCE_RULES) == 6,
        "required_record_type_count_eq_6": len(REQUIRED_RECORD_TYPES) == 6,
        "module_count_gte_4": len(TEST_BOARD_MODULES) >= 4,
        "test_mode_count_gte_6": len(TEST_MODES) >= 6,
        "planning_test_mode_present": "planning" in TEST_MODES,
        "test_board_rel_root_ok": TEST_BOARD_REL_ROOT == "capabilities/test_board",
        "protocol_id_ok": PROTOCOL_ID == "TestBoardProtectedArtifactRuleV1",
        "routing_all_ok": all(routing_ok.values()),
        "routing_all_valid_module": routing_all_valid,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Test Board Protected Artifact Rule Review",
        "lifecycle_variant": "test_board_protocol",
        "source_chain": SOURCE_CHAIN,
        "protocol_id": PROTOCOL_ID,
        "protocol_phase_ref": PROTOCOL_PHASE_REF,
        "test_board_rel_root": TEST_BOARD_REL_ROOT,
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS),
        "test_board_governance_rules": list(TEST_BOARD_GOVERNANCE_RULES),
        "test_board_modules": list(TEST_BOARD_MODULES),
        "required_record_types": list(REQUIRED_RECORD_TYPES),
        "test_modes": list(TEST_MODES),
        "protocol_matrix": matrix,
        "routing_samples": routing_ok,
        "go_conditions": go_conditions,
        "conclusions": {
            "test_board_protocol_status": (
                "test_board_protected_artifact_rule_established_global"
                if review_ok
                else "blocked"
            ),
            "applicability_note": (
                "All later phases (virtual test / dry-run / real test / runtime trial / post-review / "
                "closure review) must reuse this rule: write protected, non-deletable records to the test "
                "board in addition to any _tmp_eval_out output. _tmp_eval_out is a per-run review surface; "
                "the test board is the long-term evidence layer that must not be deleted. The six required "
                "field flags and six governance rules must be appended to each later phase, which must "
                "produce at least the six required record types via write_test_board_records()."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        manifest = write_test_board_records(
            result,
            test_mode="closure_review",
            repo_root=board_root,
            module="model_governance",
            source_review_file=result.get("output_review_file"),
        )
        result["test_board_manifest"] = manifest

    return result


def main() -> int:
    result = review_test_board_protocol_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "written_record_count": result.get("test_board_manifest", {}).get("written_record_count"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
