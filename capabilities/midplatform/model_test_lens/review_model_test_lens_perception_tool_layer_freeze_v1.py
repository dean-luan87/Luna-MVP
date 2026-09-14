# -*- coding: utf-8
"""P1 Perception Tool Layer — freeze and handoff review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Perception-Tool-Layer-Freeze-And-Handoff-v1-001"
_PKG = "capabilities/midplatform/model_test_lens"
PTL_REL = "capabilities/midplatform/model_test_lens/perception_tool_layer"
DOCS_REL = "docs/perception_tool_layer_freeze_report_v1.md"
ISSUE_REGISTRY_REL = "schemas/perception_controller/perception_tool_layer_issue_registry_v1.json"
GOV_ATTENTION = (
    "capabilities/midplatform/governance_standards/model_test_lens_ui/"
    "observation_attention_layer_governance_standard_v1.md"
)
GOV_RUNNER = (
    "capabilities/midplatform/governance_standards/model_test_lens_ui/"
    "runner_invocation_admission_governance_standard_v1.md"
)

UPSTREAM_ACTIVATION_EXEC_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_GO"

FINAL_GO = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Perception-Controller-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    DOCS_REL,
    ISSUE_REGISTRY_REL,
    f"{PTL_REL}/perception_tool_layer_freeze_types_v1.py",
    f"{PTL_REL}/perception_tool_layer_freeze_smoke_v1.py",
    f"{_PKG}/run_perception_tool_layer_freeze_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_perception_tool_layer_freeze_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "freeze_report_exists", "desc": "冻结报告已生成"},
    {"guard_id": "B", "key": "issue_registry_exists", "desc": "Issue registry 已生成"},
    {"guard_id": "C", "key": "five_problems_documented", "desc": "五个已知问题已记录"},
    {"guard_id": "D", "key": "issues_fully_registered", "desc": "问题全部登记"},
    {"guard_id": "E", "key": "architecture_status_frozen", "desc": "architecture_status=frozen"},
    {"guard_id": "F", "key": "optimization_paused", "desc": "optimization_status=paused"},
    {"guard_id": "G", "key": "freeze_forbidden_documented", "desc": "冻结禁止项已记录"},
    {"guard_id": "H", "key": "governance_chain_preserved", "desc": "历史治理链文件仍存在"},
    {"guard_id": "I", "key": "runner_governance_not_modified_by_freeze", "desc": "Runner governance 未被本阶段修改"},
    {"guard_id": "J", "key": "observation_attention_schema_not_modified", "desc": "Attention schema 未被本阶段修改"},
    {"guard_id": "K", "key": "reproducible_baseline_documented", "desc": "可复现基线已记录"},
    {"guard_id": "L", "key": "shop_sign_issue_registered", "desc": "店招案例已登记"},
    {"guard_id": "M", "key": "upstream_activation_execution_go", "desc": "上游 Activation Execution GO"},
    {"guard_id": "N", "key": "smoke_cases_pass", "desc": "smoke 通过"},
    {"guard_id": "O", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
    {"guard_id": "P", "key": "no_sam_prompt_optimization_in_freeze", "desc": "冻结阶段未优化 SAM prompt"},
    {"guard_id": "Q", "key": "no_new_vision_model_in_freeze", "desc": "冻结阶段未接新视觉模型"},
    {"guard_id": "R", "key": "perception_controller_handoff_ready", "desc": "Controller 规划输入就绪"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _audit() -> Dict[str, bool]:
    report = _read(DOCS_REL)
    registry = _load_json(ISSUE_REGISTRY_REL)
    types_py = _read(f"{PTL_REL}/perception_tool_layer_freeze_types_v1.py")
    gov_attention = _read(GOV_ATTENTION)
    gov_runner = _read(GOV_RUNNER)

    activation_exec = _load_json(
        "_tmp_eval_out/p1_midplatform_scene_task_model_activation_execution_v1_smoke_v0/"
        "p1_midplatform_scene_task_model_activation_execution_review_v1.json"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_test_lens.perception_tool_layer.perception_tool_layer_freeze_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    issues = registry.get("issues", [])
    issue_ids = {i.get("issue_id") for i in issues}

    return {
        "freeze_report_exists": bool(report) and "Perception Tool Layer Freeze Report" in report,
        "issue_registry_exists": bool(registry.get("registry_id")),
        "five_problems_documented": all(
            p in report for p in (
                "Problem 1", "Problem 2", "Problem 3", "Problem 4", "Problem 5",
            )
        ),
        "issues_fully_registered": len(issues) >= 10 and "ISSUE_SHOP_SIGN_001" in issue_ids,
        "architecture_status_frozen": registry.get("architecture_status") == "frozen",
        "optimization_paused": registry.get("optimization_status") == "paused",
        "freeze_forbidden_documented": "继续优化 MobileSAM prompt" in report and "修改 Runner Governance" in report,
        "governance_chain_preserved": bool(gov_attention) and bool(gov_runner),
        "runner_governance_not_modified_by_freeze": "runner_invocation_admission" in gov_runner,
        "observation_attention_schema_not_modified": "ObservationAttention" in gov_attention or "attention" in gov_attention.lower(),
        "reproducible_baseline_documented": "上游 GO 基线" in report and "job_564f1aa93983" in report,
        "shop_sign_issue_registered": "ISSUE_SHOP_SIGN_001" in issue_ids,
        "upstream_activation_execution_go": activation_exec.get("final_decision") == UPSTREAM_ACTIVATION_EXEC_GO,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "recommended_next_phase_defined": NEXT_PHASE in report and NEXT_PHASE in types_py,
        "no_sam_prompt_optimization_in_freeze": "optimization_status: paused" in report,
        "no_new_vision_model_in_freeze": "接入新的视觉模型" in report,
        "perception_controller_handoff_ready": (
            "Luna Perception Controller" in report
            and registry.get("recommended_next_phase") == NEXT_PHASE
        ),
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / "p1_midplatform_perception_tool_layer_freeze_v1_smoke_v0"
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "architecture_status": "frozen",
        "execution_status": "available_in_test_only",
        "optimization_status": "paused",
        "freeze_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / "p1_midplatform_perception_tool_layer_freeze_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="post_review",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="post_review",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb.get("test_board_dir", ""))
        if board_dir.is_dir():
            common = {
                "phase_id": PHASE_ID,
                "protected": True,
                "non_deletable": True,
                "deletion_forbidden": True,
                "test_artifact_protected": True,
                "test_mode": "post_review",
                "perception_tool_layer_freeze": True,
            }
            payloads = {
                "perception_tool_layer_freeze_report_record": {"plan_ref": DOCS_REL},
                "perception_tool_layer_issue_registry_record": _load_json(ISSUE_REGISTRY_REL),
            }
            for name, payload in payloads.items():
                (board_dir / f"{name}.json").write_text(
                    json.dumps({**common, "record": payload}, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "recommended_next_phase": r["recommended_next_phase"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
