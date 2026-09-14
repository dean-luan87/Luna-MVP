# -*- coding: utf-8
"""P1 Luna Decision Validation Layer — dry-run review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Luna-Decision-Validation-Layer-DryRun-v1-001"
DV_REL = "capabilities/midplatform/decision_validation"
GOV_REL = f"{DV_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_decision_validation_layer_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_planning_v1_review_v0/"
        "p1_midplatform_luna_decision_validation_layer_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_planning_v1_review_v0/"
        "p1_midplatform_third_party_teacher_adapter_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DV_REL}/luna_decision_validation_dryrun_adapter_v1.py",
    f"{DV_REL}/luna_decision_validation_processor_v1.py",
    f"{GOV_REL}/luna_decision_validation_dryrun_policy_v1.json",
    f"{GOV_REL}/decision_validation_policy_v1.json",
    f"{TB_REL}/luna_decision_validation_layer_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_decision_validation_layer_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_decision_validation_layer_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter 存在"),
        ("dryrun_fixtures_present", "fixtures 存在"),
        ("dryrun_policy_present", "dryrun policy 存在"),
        ("l1_l2_l25_chain_present", "L1→L2→L2.5 链路存在"),
        ("validation_gates_handoff", "validation 门控 handoff"),
        ("no_plan_override", "validation 不覆盖 plan"),
        ("no_teacher_in_dryrun", "不接 Teacher"),
        ("job_564f1aa93983_fixture", "店招 job fixture"),
        ("case_a_shopfront_validated", "Case A validated"),
        ("case_b_slam_blocked", "Case B SLAM blocked"),
        ("case_c_user_goal_review", "Case C needs_review"),
        ("case_d_blanket_blocked", "Case D blanket blocked"),
        ("case_e_high_risk_review", "Case E 高风险 review"),
        ("l2_feeds_validation_all", "L2 喂入 validation"),
        ("handoff_gated_when_blocked", "blocked 时 handoff 被门控"),
        ("no_tool_execution", "不执行工具"),
        ("no_runner_invocation", "不触发 runner"),
        ("no_fact_write", "不写 fact"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("deterministic_dryrun_only", "仅 deterministic dryrun"),
        ("dryrun_cases_pass", "dryrun cases 通过"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    adapter = _read(f"{DV_REL}/luna_decision_validation_dryrun_adapter_v1.py")
    fixtures = _read(f"{TB_REL}/luna_decision_validation_layer_dryrun_fixtures_v1.py")
    policy = _load_json(_detect_repo_root() / f"{GOV_REL}/luna_decision_validation_dryrun_policy_v1.json")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_decision_validation_layer_dryrun_v1_001.luna_decision_validation_layer_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    a = _case(cases, "case_a_shopfront_ocr_validated")
    b = _case(cases, "case_b_shopfront_slam_blocked")
    c = _case(cases, "case_c_user_goal_needs_review")
    d = _case(cases, "case_d_unknown_blanket_blocked")
    e = _case(cases, "case_e_street_crossing_high_risk_review")
    core = dryrun_result.get("core_validations") or {}
    job = dryrun_result.get("job_564f1aa93983_validation_result") or {}

    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    blocked_cases = [b, d]
    handoff_gated = all(
        (c.get("result") or {}).get("tool_os_handoff_candidate", {}).get("gated_by_validation") is True
        for c in blocked_cases if c.get("passed")
    )

    return {
        "dryrun_adapter_present": "run_decision_validation_dryrun" in adapter,
        "dryrun_fixtures_present": "run_all_dryrun_cases" in fixtures,
        "dryrun_policy_present": bool(policy.get("boundary_flags")),
        "l1_l2_l25_chain_present": "decision_validation_candidate" in adapter and "run_agent_planning_dryrun" in adapter,
        "validation_gates_handoff": "gate_tool_os_handoff_candidate" in adapter,
        "no_plan_override": flags.get("no_plan_override_by_validation") is True,
        "no_teacher_in_dryrun": flags.get("no_teacher_in_dryrun") is True,
        "job_564f1aa93983_fixture": job.get("job_id") == "job_564f1aa93983",
        "case_a_shopfront_validated": a.get("passed") is True,
        "case_b_slam_blocked": b.get("passed") is True,
        "case_c_user_goal_review": c.get("passed") is True,
        "case_d_blanket_blocked": d.get("passed") is True,
        "case_e_high_risk_review": e.get("passed") is True,
        "l2_feeds_validation_all": core.get("l2_feeds_validation") is True,
        "handoff_gated_when_blocked": handoff_gated or b.get("passed") is False,
        "no_tool_execution": flags.get("no_tool_execution_in_dryrun") is True,
        "no_runner_invocation": flags.get("no_runner_invocation_in_dryrun") is True,
        "no_fact_write": flags.get("no_fact_write_in_dryrun") is True,
        "no_existing_runner_mutation": "decision_validation" not in runner,
        "deterministic_dryrun_only": dryrun_result.get("deterministic_dryrun_only") is True,
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
        "upstream_gos_confirmed": upstream_ok,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    generated_files = [rel for rel in REQUIRED_FILES if _read(rel)]
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_decision_validation_layer_dryrun_v1_001.luna_decision_validation_layer_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        pass

    known_limits = [
        "dryrun_only_no_real_tool_execution",
        "no_teacher_adapter_in_this_phase",
        "no_gemini_qwen_gpt_vlm",
        "no_network",
        "no_runner_invocation",
        "no_fact_write",
        "validation_does_not_override_agent_plan",
        "multi_teacher_validation_deferred",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "L2_5_Decision_Validation",
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "dryrun_cases_passed": flags.get("dryrun_cases_pass", False),
        "review_guards_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "job_564f1aa93983_validation_result": dryrun_result.get("job_564f1aa93983_validation_result"),
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_decision_validation_layer_dryrun_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("review_guards_passed"),
        "job_564f1aa93983_validation_result": r.get("job_564f1aa93983_validation_result"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
