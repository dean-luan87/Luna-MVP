# -*- coding: utf-8 -*-
"""
Scenario Benchmark & Evaluation Harness M0（场景基准包 + 评测支架）

定位（写死）：
- 统一评测支架，不是零散 smoke/临时脚本集合
- 每个场景统一产出：structure tree / quality overlay / issue / optimization hint / feedback loop
- M0：少量标准场景 + 统一结果结构 + 单场景/场景组最小运行方式 + summary
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _i(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


QUALITY_ORDER = {"poor": 0, "acceptable": 1, "good": 2}


@dataclass
class ScenarioBenchmarkCase:
    case_id: str
    case_name: str
    case_type: str
    input_mode: str  # image / trace / synthetic / snapshot
    focus_text: Optional[str] = None
    expected_flow_family: Optional[str] = None
    expected_quality_floor: Optional[str] = None  # good/acceptable/poor
    expected_issue_type: Optional[str] = None
    notes: Optional[str] = None
    # M0: minimal ctx for DecisionMonitorBuilder
    ctx: Optional[Dict[str, Any]] = None


@dataclass
class ScenarioBenchmarkResult:
    case_id: str
    case_type: str
    focus_text: Optional[str]

    tree_depth: int = 0
    branch_count: int = 0
    dead_branch_count: int = 0
    resolution_path_length: int = 0
    effective_feedback_count: int = 0
    prune_rate: float = 0.0
    active_path_length: int = 0
    blocked: bool = False
    resolved: bool = False

    quality_grade: Optional[str] = None
    quality_summary: Optional[str] = None

    issue_type: Optional[str] = None
    issue_reason: Optional[str] = None

    optimization_hint_type: Optional[str] = None
    optimization_hint_module: Optional[str] = None
    optimization_validation_result: Optional[str] = None

    scenario_passed: bool = False
    scenario_summary: Optional[str] = None
    # Real Scenario Pack：随 frame 附带的只读审计（不参与 pass/fail）
    narrative_evidence_tension_review: Optional[Dict[str, Any]] = None
    # M1.4+：severity 画像（文档化映射，不参与 pass/fail）
    severity_profile: Optional[Dict[str, Any]] = None
    # M1.6+：SF-1′ advisory 观察（文档化，不参与 pass/fail；见 ADVISORY_REVIEW_GATE_DRAFT_M0）
    advisory_sf1_prime_observation: Optional[Dict[str, Any]] = None


def default_cases() -> List[ScenarioBenchmarkCase]:
    """
    M0 最小 6 类标准场景（写死少量）：
    - container_search / occlusion_search / general_search
    - feedback_effective / feedback_ineffective / blocked_or_fallback
    """
    base = {"frame_seq": 1, "current_ts": 0.0}
    return [
        ScenarioBenchmarkCase(
            case_id="S1_container_search",
            case_name="容器类：容器候选 + 打开反馈",
            case_type="container_search",
            input_mode="synthetic",
            focus_text="bottle",
            expected_quality_floor="acceptable",
            expected_issue_type=None,
            notes="目标验证 container flow/hypothesis 分支可跑通并产出树+质量。",
            ctx={
                **base,
                "trace_anchor_id": "bench_S1",
                "focus_object_label": "bottle",
                "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 40, 80]}, {"label": "cup", "bbox": [0, 0, 60, 60]}],
                "confirmation_input_raw_text": "我打开了",
                "confirmation_input_type": "opened_container",
            },
        ),
        ScenarioBenchmarkCase(
            case_id="S2_occlusion_search",
            case_name="遮挡类：遮挡清理反馈",
            case_type="occlusion_search",
            input_mode="synthetic",
            focus_text="bottle",
            expected_quality_floor="acceptable",
            notes="验证 occlusion 相关节点与反馈标记。",
            ctx={
                **base,
                "trace_anchor_id": "bench_S2",
                "focus_object_label": "bottle",
                "visual_audit_objects_main": [{"label": "bottle", "bbox": [12, 12, 30, 60]}],
                "confirmation_input_raw_text": "我移开了挡的",
                "confirmation_input_type": "occlusion_cleared",
            },
        ),
        ScenarioBenchmarkCase(
            case_id="S3_general_search",
            case_name="一般搜索类：无明显容器/遮挡信号",
            case_type="general_search",
            input_mode="synthetic",
            focus_text="keys",
            expected_quality_floor="acceptable",
            notes="验证 general 路径仍能统一产出主线字段。",
            ctx={
                **base,
                "trace_anchor_id": "bench_S3",
                "focus_object_label": "keys",
                "visual_audit_objects_main": [{"label": "table", "bbox": [0, 0, 100, 100]}],
            },
        ),
        ScenarioBenchmarkCase(
            case_id="S4_feedback_effective",
            case_name="反馈有效类：target_found 推动收敛",
            case_type="feedback_effective",
            input_mode="synthetic",
            focus_text="bottle",
            expected_quality_floor="acceptable",
            notes="期待 effective_feedback_count > 0。",
            ctx={
                **base,
                "trace_anchor_id": "bench_S4",
                "focus_object_label": "bottle",
                "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 50, 80]}],
                "confirmation_input_raw_text": "找到了",
                "confirmation_input_type": "target_found",
            },
        ),
        ScenarioBenchmarkCase(
            case_id="S5_feedback_ineffective",
            case_name="反馈无效类：有反馈但推进弱（占位）",
            case_type="feedback_ineffective",
            input_mode="synthetic",
            focus_text="bottle",
            expected_quality_floor="acceptable",
            expected_issue_type=None,
            notes="M0 规则下不保证命中 feedback_not_effective；重点验证字段齐全可比较。",
            ctx={
                **base,
                "trace_anchor_id": "bench_S5",
                "focus_object_label": "bottle",
                "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 50, 80]}],
                "confirmation_input_raw_text": "不知道",
                "confirmation_input_type": "unknown",
            },
        ),
        ScenarioBenchmarkCase(
            case_id="S6_blocked_or_fallback",
            case_name="blocked/fallback 类：recheck blocked",
            case_type="blocked_or_fallback",
            input_mode="synthetic",
            focus_text="bottle",
            expected_quality_floor="poor",
            expected_issue_type="blocked_without_resolution",
            notes="通过 ctx 触发 minimum_mode_active 使 recheck 被阻断，期待 blocked issue 与 poor/acceptable 边界。",
            ctx={
                **base,
                "trace_anchor_id": "bench_S6",
                "focus_object_label": "bottle",
                "minimum_mode_active": True,
                "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 50, 80]}],
                "confirmation_input_raw_text": "我看过了没有",
                "confirmation_input_type": "checked_and_not_found",
            },
        ),
    ]


def _grade_meets_floor(grade: Optional[str], floor: Optional[str]) -> bool:
    if not floor:
        return True
    if grade not in QUALITY_ORDER or floor not in QUALITY_ORDER:
        return False
    return QUALITY_ORDER.get(grade, 0) >= QUALITY_ORDER.get(floor, 0)


def _compute_pass(case: ScenarioBenchmarkCase, r: ScenarioBenchmarkResult) -> Tuple[bool, str]:
    if case.expected_quality_floor:
        ok = _grade_meets_floor(r.quality_grade, case.expected_quality_floor)
        return ok, f"quality_floor={case.expected_quality_floor} grade={r.quality_grade}"
    if case.expected_issue_type:
        ok = (r.issue_type == case.expected_issue_type)
        return ok, f"expected_issue={case.expected_issue_type} got={r.issue_type}"
    # default M0: not poor and not blocked-unresolved
    if (r.quality_grade == "poor") or (r.blocked and not r.resolved):
        return False, "default_rule: poor_or_blocked_unresolved"
    return True, "default_rule: acceptable"


def evaluate_case(case: ScenarioBenchmarkCase) -> ScenarioBenchmarkResult:
    from decision_monitor.builder import DecisionMonitorBuilder

    ctx = case.ctx or {}
    b = DecisionMonitorBuilder()
    frame = b.build(ctx)
    d = frame.to_dict()

    metrics = d.get("reasoning_tree_metrics") if isinstance(d.get("reasoning_tree_metrics"), dict) else {}
    overlay = d.get("reasoning_tree_quality_overlay") if isinstance(d.get("reasoning_tree_quality_overlay"), dict) else {}
    hint = d.get("optimization_hint") if isinstance(d.get("optimization_hint"), dict) else {}
    ofl = d.get("optimization_feedback_loop") if isinstance(d.get("optimization_feedback_loop"), dict) else {}

    r = ScenarioBenchmarkResult(
        case_id=case.case_id,
        case_type=case.case_type,
        focus_text=case.focus_text,
        tree_depth=_i(metrics.get("tree_depth"), 0),
        branch_count=_i(metrics.get("branch_count"), 0),
        dead_branch_count=_i(metrics.get("dead_branch_count"), 0),
        resolution_path_length=_i(metrics.get("resolution_path_length"), 0),
        effective_feedback_count=_i(metrics.get("effective_feedback_count"), 0),
        prune_rate=_f(metrics.get("prune_rate"), 0.0),
        active_path_length=_i(metrics.get("active_path_length"), 0),
        blocked=bool(metrics.get("blocked") is True),
        resolved=bool(metrics.get("resolved") is True),
        quality_grade=_s(overlay.get("quality_grade")),
        quality_summary=_s(overlay.get("quality_summary")),
        issue_type=_s(metrics.get("possible_tree_issue_type")),
        issue_reason=_s(metrics.get("possible_tree_issue_reason")),
        optimization_hint_type=_s(hint.get("optimization_hint_type")),
        optimization_hint_module=_s(hint.get("suggested_optimization_module")),
        optimization_validation_result=_s(ofl.get("validation_result")),
    )
    passed, why = _compute_pass(case, r)
    r.scenario_passed = passed
    r.scenario_summary = f"{case.case_name} | {why}"
    netr = d.get("narrative_evidence_tension_review")
    if netr is not None and hasattr(netr, "to_dict"):
        netr = netr.to_dict()
    r.narrative_evidence_tension_review = netr if isinstance(netr, dict) else None
    try:
        from tools.tension_severity_profile_map import map_severity_profile_m14  # type: ignore

        r.severity_profile = map_severity_profile_m14(netr) if isinstance(netr, dict) else None
    except Exception:
        r.severity_profile = None
    return r


def summarize_results(results: List[ScenarioBenchmarkResult]) -> Dict[str, Any]:
    total = len(results)
    passed = sum(1 for r in results if r.scenario_passed)
    q_dist: Dict[str, int] = {}
    issue_dist: Dict[str, int] = {}
    for r in results:
        q = r.quality_grade or "unknown"
        q_dist[q] = q_dist.get(q, 0) + 1
        it = r.issue_type or "none"
        issue_dist[it] = issue_dist.get(it, 0) + 1

    # top problem cases: poor first, then dead_branch_count, then blocked
    def key(r: ScenarioBenchmarkResult) -> Tuple[int, int, int]:
        poor = 1 if r.quality_grade == "poor" else 0
        blk = 1 if (r.blocked and not r.resolved) else 0
        return (poor, r.dead_branch_count, blk)

    top_problem = sorted(results, key=key, reverse=True)[:3]
    top_problem_case_ids = [r.case_id for r in top_problem]

    # top priority optimization modules (count suggested modules among poor/acceptable)
    mod_count: Dict[str, int] = {}
    for r in results:
        m = r.optimization_hint_module
        if not m:
            continue
        mod_count[m] = mod_count.get(m, 0) + 1
    top_modules = [k for k, _ in sorted(mod_count.items(), key=lambda kv: kv[1], reverse=True)[:5]]

    return {
        "total_cases": total,
        "passed_cases": passed,
        "quality_grade_distribution": q_dist,
        "issue_type_distribution": issue_dist,
        "top_problem_case_ids": top_problem_case_ids,
        "top_priority_optimization_modules": top_modules,
    }


def run_cases(cases: List[ScenarioBenchmarkCase]) -> Tuple[List[ScenarioBenchmarkResult], Dict[str, Any]]:
    results = [evaluate_case(c) for c in cases]
    summary = summarize_results(results)
    return results, summary


def _to_jsonable_results(results: List[ScenarioBenchmarkResult]) -> List[Dict[str, Any]]:
    return [asdict(r) for r in results]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case_id", type=str, default=None, help="run single case_id")
    ap.add_argument("--out", type=str, default=None, help="write results JSON to path")
    args = ap.parse_args()

    cases = default_cases()
    if args.case_id:
        cases = [c for c in cases if c.case_id == args.case_id]
        if not cases:
            raise SystemExit(f"case_id not found: {args.case_id}")

    results, summary = run_cases(cases)
    payload = {"summary": summary, "results": _to_jsonable_results(results)}

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("wrote:", args.out)
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

