# -*- coding: utf-8 -*-
"""
Real Scenario Pack M0（真实场景包 M0）

定位（写死）：
- 不是新平台：复用 Scenario Benchmark Harness 的 case/result/summary 结构与判定
- 只做“已有真实输入”的接入：snapshot_json / trace / image（M0 重点先跑通 snapshot_json）
- 输出必须沿用 ScenarioBenchmarkResult（不另造格式）

说明：
- 当前工程内缺少可直接跑“真实图片→候选→决策链”的自动输入管线；
  因此 M0 默认以 snapshot_json（DecisionMonitorFrame dict）作为真实场景载体。
- 对 image/trace 输入仅做占位加载与 graceful fallback，不做重平台能力扩展。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from tools.scenario_benchmark_harness import (
    ScenarioBenchmarkCase,
    ScenarioBenchmarkResult,
    summarize_results,
)


REAL_DIR = ROOT / "tests" / "real_scenarios"
SNAP_DIR = REAL_DIR / "snapshots"
CTX_DIR = REAL_DIR / "ctx"


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _pick(d: Dict[str, Any], *keys: str) -> Any:
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def _extract_result_from_frame(case: ScenarioBenchmarkCase, frame: Dict[str, Any]) -> ScenarioBenchmarkResult:
    metrics = frame.get("reasoning_tree_metrics") if isinstance(frame.get("reasoning_tree_metrics"), dict) else {}
    overlay = frame.get("reasoning_tree_quality_overlay") if isinstance(frame.get("reasoning_tree_quality_overlay"), dict) else {}
    hint = frame.get("optimization_hint") if isinstance(frame.get("optimization_hint"), dict) else {}
    ofl = frame.get("optimization_feedback_loop") if isinstance(frame.get("optimization_feedback_loop"), dict) else {}

    r = ScenarioBenchmarkResult(
        case_id=case.case_id,
        case_type=case.case_type,
        focus_text=case.focus_text,
        tree_depth=int(metrics.get("tree_depth") or 0),
        branch_count=int(metrics.get("branch_count") or 0),
        dead_branch_count=int(metrics.get("dead_branch_count") or 0),
        resolution_path_length=int(metrics.get("resolution_path_length") or 0),
        effective_feedback_count=int(metrics.get("effective_feedback_count") or 0),
        prune_rate=float(metrics.get("prune_rate") or 0.0),
        active_path_length=int(metrics.get("active_path_length") or 0),
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

    # pass 规则复用（简化内置）
    from tools.scenario_benchmark_harness import _compute_pass  # type: ignore

    passed, why = _compute_pass(case, r)  # noqa: SLF001 (M0: internal reuse)
    r.scenario_passed = passed
    r.scenario_summary = f"{case.case_name} | {why}"
    netr = frame.get("narrative_evidence_tension_review")
    if netr is not None and hasattr(netr, "to_dict"):
        netr = netr.to_dict()
    r.narrative_evidence_tension_review = netr if isinstance(netr, dict) else None
    try:
        from tools.tension_severity_profile_map import map_severity_profile_m14  # type: ignore

        r.severity_profile = map_severity_profile_m14(netr) if isinstance(netr, dict) else None
    except Exception:
        r.severity_profile = None
    return r


def _attach_advisory_sf1_prime(frame: Dict[str, Any], r: ScenarioBenchmarkResult) -> None:
    """M1.6：同帧 SF-1′ 观察；不参与 pass/fail。"""
    try:
        from tools.validate_soft_fail_candidate_clause_m0 import evaluate_clause

        r.advisory_sf1_prime_observation = _augment_sf1_prime_advisory(evaluate_clause(frame))
    except Exception:
        r.advisory_sf1_prime_observation = None


def _severity_audit_summary(results: List[ScenarioBenchmarkResult]) -> Dict[str, Any]:
    """M1.4+：按 overall_severity_profile 归类（仅 passed case；不参与 harness）。"""
    watch_ids: List[str] = []
    review_ids: List[str] = []
    critical_ids: List[str] = []
    none_ids: List[str] = []
    for r in results:
        if not r.scenario_passed:
            continue
        sp = getattr(r, "severity_profile", None)
        if not isinstance(sp, dict):
            continue
        ov = sp.get("overall_severity_profile")
        cid = r.case_id
        if ov == "critical_candidate":
            critical_ids.append(cid)
        elif ov == "review":
            review_ids.append(cid)
        elif ov == "watch":
            watch_ids.append(cid)
        elif ov == "none":
            none_ids.append(cid)
    return {
        "overall_severity_watch_count": len(watch_ids),
        "overall_severity_review_count": len(review_ids),
        "overall_severity_critical_candidate_count": len(critical_ids),
        "overall_severity_none_count": len(none_ids),
        "case_ids_watch": watch_ids[:120],
        "case_ids_review": review_ids[:120],
        "case_ids_critical_candidate": critical_ids[:120],
        "case_ids_none": none_ids[:120],
    }


def _tension_audit_summary(results: List[ScenarioBenchmarkResult]) -> Dict[str, Any]:
    """M1.3+：辅助观察「中高张力但仍通过」；不参与 harness 判定。"""
    hot_levels = ("high", "medium")
    tension_observed_but_not_failed: List[Dict[str, Any]] = []
    keys = (
        "narrative_trace_support_tension",
        "phase_closure_outcome_tension",
        "summary_backfill_tension",
        "local_global_progress_tension",
        "memory_bias_tension",
    )
    for r in results:
        if not r.scenario_passed:
            continue
        net = r.narrative_evidence_tension_review
        if not isinstance(net, dict):
            continue
        hotspots = [f"{k}={net.get(k)}" for k in keys if net.get(k) in hot_levels]
        if not hotspots:
            continue
        tension_observed_but_not_failed.append(
            {
                "case_id": r.case_id,
                "tension_hotspots": hotspots,
                "tension_review_brief": net.get("tension_review_brief"),
                "suggested_backfill_direction_summary": net.get("suggested_backfill_direction_summary"),
            }
        )
    return {
        "tension_observed_but_not_failed_count": len(tension_observed_but_not_failed),
        "tension_observed_but_not_failed": tension_observed_but_not_failed,
    }


def _augment_sf1_prime_advisory(ev: Dict[str, Any]) -> Dict[str, Any]:
    human = bool(ev.get("human_candidate_per_draft"))
    out = dict(ev)
    out["soft_fail_candidate_observed"] = human
    out["soft_fail_candidate_clause_id"] = "SF-1_prime" if human else None
    out["soft_fail_candidate_level"] = "advisory" if human else "none"
    out["soft_fail_candidate_reason_summary"] = (
        "pc∧lg_high;rsr=resume_declared_but_main_not_progressed;tcp_has_global_main_not_terminal_complete"
        if human
        else None
    )
    out["review_gate_recommended"] = human
    out["advisory_only"] = True
    return out


def _advisory_sf1_prime_audit_summary(results: List[ScenarioBenchmarkResult]) -> Dict[str, Any]:
    """M1.6+：SF-1′ 人审高风险候选命中统计（仅 passed case；不参与 harness）。"""
    hits: List[str] = []
    per_pass: List[Dict[str, Any]] = []
    critical_set: set = set()
    for r in results:
        if not r.scenario_passed:
            continue
        sp = getattr(r, "severity_profile", None)
        if (
            isinstance(sp, dict)
            and sp.get("overall_severity_profile") == "critical_candidate"
        ):
            critical_set.add(r.case_id)

    for r in results:
        if not r.scenario_passed:
            continue
        obs = getattr(r, "advisory_sf1_prime_observation", None)
        if not isinstance(obs, dict):
            per_pass.append({"case_id": r.case_id, "advisory_observation": None})
            continue
        oid = r.case_id
        human = bool(obs.get("soft_fail_candidate_observed"))
        if human:
            hits.append(oid)
        is_crit = oid in critical_set
        per_pass.append(
            {
                "case_id": oid,
                "soft_fail_candidate_observed": human,
                "overall_severity_critical": is_crit,
                "sf1_prime_match": obs.get("sf1_prime_match"),
                "sf1_match": obs.get("sf1_match"),
            }
        )

    hit_set = set(hits)
    advisory_only_not_critical = sorted(hit_set - critical_set)
    critical_only_not_advisory = sorted(critical_set - hit_set)
    intersection = sorted(hit_set & critical_set)

    return {
        "advisory_sf1_prime_hit_count": len(hits),
        "case_ids_advisory_sf1_prime": hits,
        "advisory_and_critical_candidate_intersection": intersection,
        "advisory_hit_but_not_critical_candidate": advisory_only_not_critical,
        "critical_candidate_but_not_advisory_sf1_prime": critical_only_not_advisory,
        "per_case_flags": per_pass,
    }


def _load_snapshot_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(d, dict) and isinstance(d.get("frame"), dict):
            return d["frame"]
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def _load_trace_jsonl_last_record(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        for raw in reversed(lines[-200:]):
            try:
                d = json.loads(raw)
                if isinstance(d, dict):
                    return d
            except Exception:
                continue
        return None
    except Exception:
        return None


def _load_ctx_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def default_real_cases() -> List[Tuple[ScenarioBenchmarkCase, Dict[str, Any]]]:
    """
    返回 (case, input_ref) 列表。
    input_ref:
      - {"input_mode": "...", "input_ref": "..."}  # file path
    """
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    CTX_DIR.mkdir(parents=True, exist_ok=True)

    def snap(name: str) -> str:
        return str((SNAP_DIR / name).resolve())

    def ctxref(name: str) -> str:
        return str((CTX_DIR / name).resolve())

    # 6 类最小真实场景（以 snapshot_json 作为“真实场景载体”）
    return [
        (
            ScenarioBenchmarkCase(
                case_id="R1_container_real",
                case_name="真实·容器类（snapshot）",
                case_type="container_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="container",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第一批真实基线：以 ctx_json 驱动 builder，确保定点修复可被评测反映；后续可替换为 image/trace 真实输入。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R1_container_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R2_occlusion_real",
                case_name="真实·遮挡类（ctx）",
                case_type="occlusion_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="occlusion",
                expected_quality_floor="acceptable",
                notes="M0.4：切换到 ctx_json 以反映 hypothesis_layer / 树组织定点修复对逻辑指标的影响。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R2_occlusion_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R3_general_search_real",
                case_name="真实·一般搜索（snapshot）",
                case_type="general_search",
                input_mode="snapshot_json",
                focus_text="keys",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                notes="无明显容器/遮挡信号的搜索。",
            ),
            {"input_mode": "snapshot_json", "input_ref": snap("R3_general_search_real.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R4_feedback_effective_real",
                case_name="真实·反馈有效（ctx）",
                case_type="feedback_effective",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="feedback",
                expected_quality_floor="acceptable",
                notes="M0：将 R4 从 snapshot_json 切到 ctx_json，用当前主逻辑动态重算指标，刷新旧 snapshot 基线的表达偏差。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R4_feedback_effective_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R5_feedback_ineffective_real",
                case_name="真实·反馈无效（snapshot）",
                case_type="feedback_ineffective",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="feedback",
                expected_quality_floor=None,
                expected_issue_type=None,
                notes="反馈存在但推进弱；M0 不强求必命中 feedback_not_effective。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R5_feedback_ineffective_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R6_blocked_or_fallback_real",
                case_name="真实·blocked/fallback（snapshot）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor=None,
                expected_issue_type=None,
                notes="blocked/unresolved 典型；后续补真实 blocked 证据时可标注 expected_issue_type。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R6_blocked_or_fallback_real_ctx.json")},
        ),
        # --- M0.1：第二批真实场景扩充（压力源：更复杂交互与反馈噪声） ---
        (
            ScenarioBenchmarkCase(
                case_id="R7_occlusion_complex_real",
                case_name="真实·复杂遮挡（ctx-like feedback噪声）",
                case_type="occlusion_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="occlusion",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第二批真实场景：复杂遮挡载体 + 明确 user feedback(unknown) 用于制造 feedback_not_effective，从而重新暴露 triage 输入。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R7_occlusion_complex_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R8_multi_candidate_container_real",
                case_name="真实·多候选容器（ctx-like feedback噪声）",
                case_type="container_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="container",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第二批真实场景：多个容器候选竞争 + 明确 user feedback(unknown) 制造 feedback_not_effective。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R8_multi_candidate_container_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R9_feedback_conflict_real",
                case_name="真实·反馈冲突（confirmed_no / occlusion flow）",
                case_type="feedback_effective",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="feedback",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第二批真实场景：在 occlusion flow 下给 confirmed_no，使 confirmation_bridge next_effect 维持 none，从而触发 feedback_not_effective。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R9_feedback_conflict_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R10_partial_memory_vs_novel_real",
                case_name="真实·部分记忆 vs 新观察（一般搜索 + unknown feedback）",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第二批真实场景：无容器/遮挡显式线索 + unknown feedback，制造 feedback_not_effective 以形成新的 triage 压力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R10_partial_memory_vs_novel_real_ctx.json")},
        ),
        # --- M0.2/M1：第三批真实场景扩充（更高噪声/更混乱压力源） ---
        (
            ScenarioBenchmarkCase(
                case_id="R11_occlusion_plus_competition_real",
                case_name="真实·多层遮挡+候选竞争（高运动中断）",
                case_type="occlusion_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="occlusion",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第三批压力：遮挡+竞争叠加并引入高运动不稳定，观察 blocked_without_resolution 在混乱语境下的暴露。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R11_occlusion_plus_competition_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R12_feedback_ambiguous_real",
                case_name="真实·反馈含糊（弱否定+不确定）",
                case_type="feedback_ineffective",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="feedback",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第三批压力：模糊反馈语句与弱线索并存，验证弱反馈场景下的稳定性与可解释性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R12_feedback_ambiguous_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R13_feedback_conflict_loop_real",
                case_name="真实·反馈冲突回环（先否后疑）",
                case_type="feedback_effective",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="feedback",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第三批压力：反馈口径来回切换（否认后又不确定），观察收敛稳定性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R13_feedback_conflict_loop_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R14_task_chain_shift_complex_real",
                case_name="真实·任务链复杂切换（recheck/fallback 压力）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第三批压力：task chain 切换+高运动不稳定，观察 blocked 与收敛路径切换质量。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R14_task_chain_shift_complex_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R15_memory_novel_conflict_real",
                case_name="真实·记忆与新观察冲突（hybrid 压力）",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第三批压力：memory_hint 与 novel_candidate 并存，观察 memory-vs-novel 冲突下路径选择稳定性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R15_memory_novel_conflict_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R16_continuity_break_recovery_real",
                case_name="真实·连续性中断后恢复（break/recovery）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第三批压力：连续性中断后恢复，叠加高运动失稳，验证 continuity/resolution 恢复路径。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R16_continuity_break_recovery_real_ctx.json")},
        ),
        # --- M0.3/M2：第四批真实场景扩充（更高阶交互混乱/目标切换/插入与恢复失败） ---
        (
            ScenarioBenchmarkCase(
                case_id="R17_multi_step_feedback_repair_real",
                case_name="真实·多步反馈修复（多次纠偏）",
                case_type="feedback_effective",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="feedback",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第四批压力：多步反馈逼近语境；为确保在 M0.6 后仍能复现有效 triage，本 case 强制 search_terminal_status=blocked（但避免 runtime frozen/hold_for_floor 阻断）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R17_multi_step_feedback_repair_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R18_user_system_divergence_real",
                case_name="真实·用户/系统持续背离（多轮未对齐）",
                case_type="feedback_ineffective",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="feedback",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第四批压力：用户持续与系统建议背离；强制 terminal=blocked 以保持 triage 可见性（避免触发已修复的 frozen/block 收口路径）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R18_user_system_divergence_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R19_task_insertion_interrupt_real",
                case_name="真实·任务插入中断（插入子任务后恢复）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第四批压力：任务链中途插入子任务并引发恢复失败倾向；强制 terminal=blocked 以生成 blocked_without_resolution 侧压力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R19_task_insertion_interrupt_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R20_target_switch_real",
                case_name="真实·多目标切换（A<->B 干扰）",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第四批压力：多目标切换交错残留，观察路径切换/记忆偏差的代价；强制 terminal=blocked 保证 triage 可生成。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R20_target_switch_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R21_memory_mislead_real",
                case_name="真实·记忆误导 vs 新观察纠偏（hybrid 冲突）",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第四批压力：memory_hint_present + novel_candidate_present 并存，但当前观测拉开矛盾；强制 terminal=blocked 保证 triage 输出可见。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R21_memory_mislead_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R22_continuity_recovery_fail_real",
                case_name="真实·连续性恢复失败后二次收敛（二次失败）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第四批压力：continuity broken + recovery attempt fails 的二次失败倾向；强制 terminal=blocked 以复现收敛失败。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R22_continuity_recovery_fail_real_ctx.json")},
        ),
        # --- M0.4/M3：第五批真实场景扩充（更高阶行为链路/非合规/恢复失败/记忆覆盖） ---
        (
            ScenarioBenchmarkCase(
                case_id="R23_long_chain_recovery_fail_real",
                case_name="真实·长链恢复失败（多次补证后主任务未恢复）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第五批压力：更长的搜索/补证/回退链路；terminal=blocked，且使用非 unknown 确认输入类型以重新制造有效 blocked 类 triage。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R23_long_chain_recovery_fail_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R24_explicit_user_noncompliance_real",
                case_name="真实·用户明确不合规（按相反动作持续背离）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第五批压力：用户侧显式背离（confirmation_input_type 非 unknown）；terminal=blocked 以保持 unresolved。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R24_explicit_user_noncompliance_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R25_task_loss_after_insertion_real",
                case_name="真实·插入任务后主任务遗失（恢复失败倾向）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第五批压力：插入后任务链恢复不稳定；用较长 resolution path 表达插入/回退链，并保持 terminal=blocked。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R25_task_loss_after_insertion_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R26_memory_override_failure_real",
                case_name="真实·记忆覆盖失败（旧记忆未被新证据纠偏）",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第五批压力：memory_hint_present + novel_candidate_present；通过确认输入类型非 unknown 恢复 blocked 类 triage 观测。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R26_memory_override_failure_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R27_multi_object_multi_feedback_real",
                case_name="真实·多对象 + 多反馈复合干扰",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第五批压力：多视觉对象竞争 + 多反馈语境（用 confirmation_input_type 非 unknown + terminal=blocked）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R27_multi_object_multi_feedback_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R28_continuity_second_recovery_real",
                case_name="真实·连续性恢复失败后的二次恢复（仍偏离）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第五批压力：continuity_break_expected + 二次恢复倾向；terminal=blocked 以确保 unresolved blocked 类 issue 可见。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R28_continuity_second_recovery_real_ctx.json")},
        ),
        # --- M0.5/M4：第六批真实场景扩充（更高阶 intent × 执行分裂） ---
        (
            ScenarioBenchmarkCase(
                case_id="R29_goal_drift_real",
                case_name="真实·目标漂移（多轮目标不一致）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第六批压力：目标漂移语境（goal_drift_expected）；通过 object_search_retry_count>=3 触发 repeated_fallback，从而重现 blocked_without_resolution triage 可见性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R29_goal_drift_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R30_success_criteria_shift_real",
                case_name="真实·成功标准切换（确认口径改变）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第六批压力：success_criteria_shift_expected；通过 object_search_retry_count>=3 触发 repeated_fallback，制造 blocked_without_resolution。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R30_success_criteria_shift_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R31_multi_insertion_chain_real",
                case_name="真实·多插入任务串联（主任务维持失败倾向）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第六批压力：multi_insertion_expected；用较长 resolution path + object_search_retry_count>=3 制造执行分裂语境下 repeated_fallback。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R31_multi_insertion_chain_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R32_feedback_action_divergence_real",
                case_name="真实·反馈-动作持续背离（多轮不收敛）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第六批压力：feedback_action_divergence_expected；通过 object_search_retry_count>=3 重现 blocked_without_resolution（再制造新的 triage 观察点）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R32_feedback_action_divergence_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R33_memory_fast_environment_shift_real",
                case_name="真实·记忆误导 + 环境快速变化（仍无法修正）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第六批压力：fast_environment_shift_expected + memory_hint_present + novel_candidate_present；通过 object_search_retry_count>=3 触发 repeated_fallback 重现 triage。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R33_memory_fast_environment_shift_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R34_recovery_under_second_disturbance_real",
                case_name="真实·恢复中二次干扰（再偏离）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第六批压力：second_disturbance_expected；用二次 fallback/rechecking 的 resolution path + object_search_retry_count>=3 重现 blocked_without_resolution。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R34_recovery_under_second_disturbance_real_ctx.json")},
        ),
        # --- M0.6/M5：第七批真实场景扩充（意图-动作-任务三链错位语境） ---
        (
            ScenarioBenchmarkCase(
                case_id="R35_intent_action_task_mismatch_real",
                case_name="真实·意图-动作-任务三链错位",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第七批压力：意图/动作/任务阶段三链错位语境；用 object_search_retry_count<3 绕过 M0.9 repeated fallback 收口，使 triage 可见。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R35_intent_action_task_mismatch_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R36_confirmed_but_not_executed_real",
                case_name="真实·已确认但未执行（确认-动作不一致）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第七批压力：confirmed_but_not_executed_expected；同样保持 retry<3 以绕过 repeated fallback 收口。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R36_confirmed_but_not_executed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R37_executed_but_goal_shifted_real",
                case_name="真实·动作已做但目标漂移（成功标准变了）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第七批压力：executed_but_goal_shifted_expected；通过不同 resolution path + retry<3 制造阶段语义错位。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R37_executed_but_goal_shifted_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R38_subtask_return_semantic_loss_real",
                case_name="真实·子任务返回但主语义丢失",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第七批压力：subtask_return_semantic_loss_expected；保持 retry<3 让潜在 blocked/unresolved 重新可观测。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R38_subtask_return_semantic_loss_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R39_fact_feedback_stage_conflict_real",
                case_name="真实·事实-反馈-阶段冲突（选择优先链失败）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第七批压力：fact_feedback_stage_conflict_expected；retry<3 以避免 M0.9 repeated fallback 收口影响可见性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R39_fact_feedback_stage_conflict_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R40_false_recovery_real",
                case_name="真实·伪恢复（恢复错了）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第七批压力：false_recovery_expected；保持 retry<3 制造 unresolved blocked 语境。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R40_false_recovery_real_ctx.json")},
        ),
        # --- M0.7/M6：第八批真实场景扩充（社会性扰动 / 长链语义漂移 / 多方约束冲突） ---
        (
            ScenarioBenchmarkCase(
                case_id="R41_confirmed_but_long_term_diverged_real",
                case_name="真实·口头确认但长期行为背离",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第八批：短期语言确认 + 后续多步行为持续反向；压力 confirmation / recheck / 长程一致性。ctx 使用 long_term_divergence_expected（不在 M1.0 mismatch 收口白名单内，用于再制造 triage 可见性）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R41_confirmed_but_long_term_diverged_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R42_task_subtask_fact_shift_real",
                case_name="真实·主任务/子任务/环境事实三方漂移",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第八批：主任务仍在、子任务插入改条件、环境事实变化；task_subtask_fact_shift_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R42_task_subtask_fact_shift_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R43_success_condition_overwritten_real",
                case_name="真实·目标未变但成功条件被外部改写",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第八批：非找错目标而是“完成定义”被外部事件改写；success_condition_overwritten_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R43_success_condition_overwritten_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R44_false_multi_recovery_real",
                case_name="真实·多次伪恢复叠加（深层偏航）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第八批：多次看似恢复成功但语义路径持续偏离；false_multi_recovery_expected（与 R40 单点伪恢复区分）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R44_false_multi_recovery_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R45_multi_feedback_source_conflict_real",
                case_name="真实·多反馈源冲突（用户/环境/阶段/记忆）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第八批：多源反馈互相矛盾；confirmation 为 unknown 以保留冲突；multi_feedback_source_conflict_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R45_multi_feedback_source_conflict_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R46_delayed_exposure_mismatch_real",
                case_name="真实·长链分裂后延迟暴露错误",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第八批：记忆/事实/任务链长期分裂，错误晚发；delayed_exposure_mismatch_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R46_delayed_exposure_mismatch_real_ctx.json")},
        ),
        # --- M0.8/M7：第九批真实场景扩充（累积误差 / 多层约束漂移 / 伪一致性 / 慢性错位） ---
        (
            ScenarioBenchmarkCase(
                case_id="R47_gradual_goal_drift_real",
                case_name="真实·长期目标缓慢漂移",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第九批：多步变味非一次切换；gradual_goal_drift_expected（不在 M1.1 收口白名单，用于再制造 triage）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R47_gradual_goal_drift_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R48_local_recovery_global_mismatch_real",
                case_name="真实·局部恢复正确但全局已错位",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第九批：局部正确掩盖全局错误；local_recovery_global_mismatch_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R48_local_recovery_global_mismatch_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R49_multi_constraint_soft_shift_real",
                case_name="真实·多层约束同时轻微变化（叠加偏航）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第九批：环境/意图/成功标准软漂移叠加；multi_constraint_soft_shift_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R49_multi_constraint_soft_shift_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R50_feedback_fact_consistent_but_wrong_real",
                case_name="真实·反馈与事实表面一致但仍错",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第九批：表面一致性欺骗；feedback_fact_consistent_but_wrong_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R50_feedback_fact_consistent_but_wrong_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R51_task_semantic_crack_real",
                case_name="真实·任务链表面稳定但语义裂缝扩大",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第九批：阶段看似正常但当前在做什么已分裂；task_semantic_crack_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R51_task_semantic_crack_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R52_slow_poisoning_real",
                case_name="真实·慢性污染/慢性误导",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="第九批：一连串不离谱输入逐步带歪路径；slow_poisoning_expected。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R52_slow_poisoning_real_ctx.json")},
        ),
        # --- M1.0：第十批真实场景回归（冻结基线压测） ---
        (
            ScenarioBenchmarkCase(
                case_id="R53_main_task_resumed_but_not_progressed_real",
                case_name="真实·主任务恢复但未推进（长链一致性）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.0-A：恢复语义出现但主任务进度未前移，验证 task_chain_progress 与 mainline 收口是否一致。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R53_main_task_resumed_but_not_progressed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R54_inserted_task_exit_ambiguous_real",
                case_name="真实·插入任务退出歧义（长链一致性）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.0-A：inserted 子任务看似结束但 resume target 语义含糊，验证 inserted→main 回切稳定性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R54_inserted_task_exit_ambiguous_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R55_memory_supported_but_observation_conflicted_real",
                case_name="真实·记忆支持但观测冲突（记忆风险）",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.0-C：memory supports_mainline 与 observation 冲突并存，验证 memory_effect 与 backfill 提示边界。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R55_memory_supported_but_observation_conflicted_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R56_dynamic_source_shift_but_mainline_static_real",
                case_name="真实·动态主导源切换但主链叙事静止（调度一致性）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.0-B/D：源格局动态变化，但 mainline state/phase 收口无变化，验证 source×mainline 一致性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R56_dynamic_source_shift_but_mainline_static_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R57_summary_looks_ok_but_requires_backfill_real",
                case_name="真实·summary 看似正常但必须回溯（summary×entry 边界）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.0-E：summary 文本可读但因果敏感，要求 post_processing_summary_entry 触发 trace/event/whitebox backfill。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R57_summary_looks_ok_but_requires_backfill_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R58_local_success_masked_global_failure_real",
                case_name="真实·局部成功掩盖全局失败（任务一致性+状态稳定）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.0-A/D：local success 出现但 global 目标失败，验证 task_position/local_success 与 mainline closure 的一致叙事。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R58_local_success_masked_global_failure_real_ctx.json")},
        ),
        # --- M1.1：第十一批真实场景扩包（冻结基线后的复杂压力源） ---
        (
            ScenarioBenchmarkCase(
                case_id="R59_multi_inserted_recovery_but_main_not_progressed_real",
                case_name="真实·多次插入/恢复后主任务仍未推进",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.1-A：多次 inserted + recovery 叠加后，验证主任务连续推进链是否仍稳定。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R59_multi_inserted_recovery_but_main_not_progressed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R60_recovery_declared_but_resume_chain_fragile_real",
                case_name="真实·宣称恢复但 resume 链路脆弱",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.1-A/E：state/phase 看似恢复，但 closure 语义与主任务推进错位。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R61_memory_bias_accumulated_under_familiar_context_real",
                case_name="真实·熟悉场景下记忆语义偏差累积",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.1-C：观察个性化语义偏差在记忆参与下是否被正确标记为风险/待回溯。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R61_memory_bias_accumulated_under_familiar_context_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R62_source_shift_twice_but_mainline_lagged_real",
                case_name="真实·主导源二次切换但主链叙事滞后",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.1-B：动态源/任务源/记忆源拉扯下，验证 source-summary-mainline 对齐稳定性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R62_source_shift_twice_but_mainline_lagged_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R63_summary_readable_ok_but_backfill_mandatory_real",
                case_name="真实·summary 可读但 backfill 强制",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.1-D：summary 看起来顺，但 post-processing entry 应触发 trace/event/whitebox 回溯。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R63_summary_readable_ok_but_backfill_mandatory_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R64_phase_correct_but_closure_semantics_misaligned_real",
                case_name="真实·phase 正确但 closure 语义错位",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.1-E：多扰动下主链阶段解释可读，但 closure 语义可能与任务推进脱节。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R64_phase_correct_but_closure_semantics_misaligned_real_ctx.json")},
        ),
        # --- M1.2：第十二批真实场景扩包（跨层一致性 / 长链稳态 / 叙事—证据张力） ---
        (
            ScenarioBenchmarkCase(
                case_id="R65_multi_recovery_chain_locally_valid_but_globally_stalled_real",
                case_name="真实·多跳恢复链局部成立但整体主任务未前进",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.2-A：多次恢复/插入后每跳可解释，但全局目标未实质推进；配合主任务停滞语义。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R65_multi_recovery_chain_locally_valid_but_globally_stalled_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R66_task_state_shifted_but_mainline_story_lagged_real",
                case_name="真实·任务/调度已变但主链叙事滞后一拍",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.2-B：task_state/主导源与 mainline 叙事不同步压力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R66_task_state_shifted_but_mainline_story_lagged_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R67_familiar_context_bias_stabilized_without_explicit_conflict_real",
                case_name="真实·熟悉语境下语义偏差稳定化但无明面对抗",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.2-C：惯性+历史模式下的慢性偏差；观察白盒/summary 是否标风险。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R67_familiar_context_bias_stabilized_without_explicit_conflict_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R68_narrative_smooth_but_trace_support_weak_real",
                case_name="真实·叙事顺滑但 trace/event 支撑偏弱",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.2-D：summary/narrative 可读性与证据链张力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R68_narrative_smooth_but_trace_support_weak_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R69_phase_and_closure_aligned_but_outcome_summary_misaligned_real",
                case_name="真实·phase/closure 对齐但 outcome/summary 口径漂移",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.2-E：二层一致 vs 三层 outcome/summary 错位压力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R69_phase_and_closure_aligned_but_outcome_summary_misaligned_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R70_entry_backfill_should_trigger_but_story_looked_complete_real",
                case_name="真实·后处理入口应触发回溯但故事看似已闭环",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.2-D/E：entry backfill 边界 vs 叙事闭环感。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R70_entry_backfill_should_trigger_but_story_looked_complete_real_ctx.json")},
        ),
        # --- M1.3：第十三批真实场景扩包（冻结基线 + tension 审计观察；不升级 hard-fail） ---
        (
            ScenarioBenchmarkCase(
                case_id="R71_locally_consistent_but_globally_slow_main_progress_real",
                case_name="真实·局部一致但全局主任务推进过慢",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.3-A：每段可解释但全局推进不足。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R71_locally_consistent_but_globally_slow_main_progress_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R72_narrative_complete_but_event_support_sparse_real",
                case_name="真实·叙事完整感强但事件层支撑偏稀",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.3-B：压 narrative↔trace 张力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R72_narrative_complete_but_event_support_sparse_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R73_familiar_pattern_bias_stable_without_explicit_failure_real",
                case_name="真实·熟悉模式下偏差稳定化且无显式失败点",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.3-C：个性化语义偏差慢性稳定。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R73_familiar_pattern_bias_stable_without_explicit_failure_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R74_phase_closure_reasonable_but_outcome_claim_too_full_real",
                case_name="真实·phase/closure 合理但 outcome 叙述偏满",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.3-D：三层口径轻微 overclaim。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R74_phase_closure_reasonable_but_outcome_claim_too_full_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R75_entry_story_complete_but_backfill_signal_suppressed_real",
                case_name="真实·入口故事顺但 backfill 信号易被掩盖",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.3-E：顺滑叙事 vs backfill 契约。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R75_entry_story_complete_but_backfill_signal_suppressed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R76_task_resume_ok_locally_but_global_goal_still_drifting_real",
                case_name="真实·局部恢复可接受但全局目标仍在漂移",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.3-A/E：resume 与全局 goal drift。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R76_task_resume_ok_locally_but_global_goal_still_drifting_real_ctx.json")},
        ),
        # --- M1.4：第十四批（severity 画像解读；不接 hard-fail） ---
        (
            ScenarioBenchmarkCase(
                case_id="R77_phase_outcome_overclaim_review_candidate_real",
                case_name="真实·phase/outcome 叙事偏满（review 级）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.4-A：pc 有 review 价值。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R77_phase_outcome_overclaim_review_candidate_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R78_local_progress_repeated_but_global_goal_still_weak_real",
                case_name="真实·局部推进反复但全局主目标仍弱",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.4-B：lg+pc 配对压力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R78_local_progress_repeated_but_global_goal_still_weak_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R79_memory_bias_stable_but_kept_under_watch_real",
                case_name="真实·记忆偏差稳定化但保持观察",
                case_type="general_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="general",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.4-C：mb 背景监控。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R79_memory_bias_stable_but_kept_under_watch_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R80_summary_entry_smooth_but_backfill_still_needed_real",
                case_name="真实·summary/entry 顺滑但仍需 backfill",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.4-D：sb 背景监控。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R80_summary_entry_smooth_but_backfill_still_needed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R81_story_more_complete_than_trace_support_real",
                case_name="真实·故事相对完整于 trace 支撑（nt 对照）",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.4-E：nt 对照样本。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R81_story_more_complete_than_trace_support_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R82_phase_closure_progress_pair_near_critical_candidate_real",
                case_name="真实·phase/closure 与推进链配对近 critical 候选",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.4-B：pc+lg 组合压力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R82_phase_closure_progress_pair_near_critical_candidate_real_ctx.json")},
        ),
        # --- M1.5：第十五批（resume-progress 摘要链验证；critical_candidate 模式观察） ---
        (
            ScenarioBenchmarkCase(
                case_id="R83_resume_declared_main_still_not_progressed_real",
                case_name="真实·恢复已声明但主任务仍未推进",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.5-A：resume-progress 摘要链稳定性。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R83_resume_declared_main_still_not_progressed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R84_recovery_chain_repeated_and_global_goal_not_advanced_real",
                case_name="真实·多轮恢复链但全局目标未前进",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.5-C：局部恢复成立、全局不足。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R84_recovery_chain_repeated_and_global_goal_not_advanced_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R85_phase_closure_progress_pair_reappeared_real",
                case_name="真实·phase/closure 与推进配对再压测",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.5-B/D：pc+lg 复现。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R85_phase_closure_progress_pair_reappeared_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R86_resume_target_present_but_outcome_still_overclaimed_real",
                case_name="真实·resume 目标在但 outcome 仍偏满",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.5-D：复合张力。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R86_resume_target_present_but_outcome_still_overclaimed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R87_complex_but_healthy_resume_and_global_progress_real",
                case_name="真实·复杂但健康（全局推进一致）",
                case_type="container_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="container",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.5-E：健康对照，避免全批 critical。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R87_complex_but_healthy_resume_and_global_progress_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R88_inserted_recovery_resolved_locally_but_main_goal_stagnant_real",
                case_name="真实·插入恢复局部成立但主目标停滞",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.5-C：inserted + 全局停滞。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R88_inserted_recovery_resolved_locally_but_main_goal_stagnant_real_ctx.json")},
        ),
        # --- M1.6：第十六批（advisory/SF-1′ 场景观察；不改 harness） ---
        (
            ScenarioBenchmarkCase(
                case_id="R89_advisory_candidate_resume_fragility_global_stall_real",
                case_name="真实·advisory 正样本 resume 脆弱性+全局停滞",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.6-A：SF-1′ 正样本。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R89_advisory_candidate_resume_fragility_global_stall_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R90_advisory_candidate_near_miss_pc_high_lg_medium_real",
                case_name="真实·advisory 近邻 pc 高 lg 中",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.6-B：近邻排除。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R90_advisory_candidate_near_miss_pc_high_lg_medium_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R91_complex_resume_chain_but_healthy_terminal_real",
                case_name="真实·复杂恢复链但 terminal 健康",
                case_type="container_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="container",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.6-C：健康复杂。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R91_complex_resume_chain_but_healthy_terminal_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R92_critical_like_pattern_but_missing_resume_fragility_real",
                case_name="真实·近 critical 但缺 resume 脆弱性摘要",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.6-D：severity 与 advisory 偏差观察。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R92_critical_like_pattern_but_missing_resume_fragility_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R93_global_stall_repeated_but_closure_still_not_overclaimed_real",
                case_name="真实·全局停滞反复 closure 不升格变体",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.6-E：主模式轻量变体。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R93_global_stall_repeated_but_closure_still_not_overclaimed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R94_phase_closure_shifted_but_advisory_boundary_should_hold_real",
                case_name="真实·phase/outcome 张力无 resume 串边界",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.6-F：advisory 边界应守住。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R94_phase_closure_shifted_but_advisory_boundary_should_hold_real_ctx.json")},
        ),
        # --- M1.7：第十七批（advisory 线在扩包中的持续一致性；不改 harness） ---
        (
            ScenarioBenchmarkCase(
                case_id="R95_advisory_candidate_resume_fragility_repeated_real",
                case_name="真实·advisory 正样本 resume 脆弱性反复",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.7-A：SF-1′ 正样本（与同批 R99 对照）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R95_advisory_candidate_resume_fragility_repeated_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R96_advisory_near_miss_resume_present_but_fragility_insufficient_real",
                case_name="真实·近邻 resume 有但 rsr/tcp 不构成 SF-1′",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.7-B：main+resume 提示，排除 advisory。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R96_advisory_near_miss_resume_present_but_fragility_insufficient_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R97_complex_recovery_chain_but_terminal_aligned_real",
                case_name="真实·复杂恢复链 terminal 最终健康",
                case_type="container_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="container",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.7-C：健康复杂不误伤 advisory。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R97_complex_recovery_chain_but_terminal_aligned_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R98_global_stall_visible_but_closure_not_overclaimed_real",
                case_name="真实·全局停滞可见 lg 中档 advisory 近邻",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.7-D：pc 高 lg 中近邻（对齐 R90 族）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R98_global_stall_visible_but_closure_not_overclaimed_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R99_advisory_candidate_with_entry_summary_alignment_real",
                case_name="真实·advisory 正样本 summary/entry 同向",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.7-E：SF-1′ 正样本，观察三层 wording。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R99_advisory_candidate_with_entry_summary_alignment_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R100_high_tension_review_only_not_advisory_real",
                case_name="真实·高张力仅 review advisory 不命中",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.7-F：无 resume 串，对照边界。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R100_high_tension_review_only_not_advisory_real_ctx.json")},
        ),
        # --- M1.8：第十八批（nt tightening 后的真实扩包协同性验证；不改 harness） ---
        (
            ScenarioBenchmarkCase(
                case_id="R101_long_narrative_sparse_key_anchors_should_raise_nt_real",
                case_name="真实·长叙事关键锚点偏薄 nt 应点亮",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.8-A：nt 正向样本（长叙事+薄锚点）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R101_long_narrative_sparse_key_anchors_should_raise_nt_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R102_long_narrative_with_sufficient_key_support_should_not_raise_nt_real",
                case_name="真实·长叙事但关键锚点充分 nt 不应升格",
                case_type="container_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="container",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.8-B：健康对照（锚点足够）。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R102_long_narrative_with_sufficient_key_support_should_not_raise_nt_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R103_nt_supports_pc_lg_but_not_primary_driver_real",
                case_name="真实·nt 与 pc/lg 同向但非主驱动",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.8-C：nt+pc/lg 协同观察。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R103_nt_supports_pc_lg_but_not_primary_driver_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R104_advisory_strong_but_nt_still_none_should_be_acceptable_real",
                case_name="真实·advisory 强但 nt 非决定项",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.8-D：避免 nt 越权。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R104_advisory_strong_but_nt_still_none_should_be_acceptable_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R105_complex_healthy_narrative_dense_support_real",
                case_name="真实·复杂健康叙事且支撑充分",
                case_type="container_search",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="container",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.8-E：健康复杂样本，nt 应守边界。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R105_complex_healthy_narrative_dense_support_real_ctx.json")},
        ),
        (
            ScenarioBenchmarkCase(
                case_id="R106_entry_summary_smooth_but_key_support_thin_review_only_real",
                case_name="真实·entry/summary 顺滑但关键支撑偏薄",
                case_type="blocked_or_fallback",
                input_mode="ctx_json",
                focus_text="bottle",
                expected_flow_family="blocked",
                expected_quality_floor="acceptable",
                expected_issue_type=None,
                notes="M1.8-F：review-only 对照，验证 nt 不替代 advisory。",
            ),
            {"input_mode": "ctx_json", "input_ref": ctxref("R106_entry_summary_smooth_but_key_support_thin_review_only_real_ctx.json")},
        ),
    ]


def _graceful_missing(case: ScenarioBenchmarkCase, reason: str) -> ScenarioBenchmarkResult:
    r = ScenarioBenchmarkResult(case_id=case.case_id, case_type=case.case_type, focus_text=case.focus_text)
    r.scenario_passed = False
    r.scenario_summary = f"{case.case_name} | missing_input: {reason}"
    return r


def run_real_cases(case_id: Optional[str] = None) -> Tuple[List[ScenarioBenchmarkResult], Dict[str, Any]]:
    cases_with_ref = default_real_cases()
    if case_id:
        cases_with_ref = [x for x in cases_with_ref if x[0].case_id == case_id]
        if not cases_with_ref:
            raise SystemExit(f"case_id not found: {case_id}")

    results: List[ScenarioBenchmarkResult] = []
    real_case_ids: List[str] = []

    for case, ref in cases_with_ref:
        real_case_ids.append(case.case_id)
        mode = ref.get("input_mode")
        p = Path(ref.get("input_ref") or "")
        if mode == "snapshot_json":
            frame = _load_snapshot_json(p)
            if not frame:
                results.append(_graceful_missing(case, f"snapshot_json not found or invalid: {p}"))
                continue
            r0 = _extract_result_from_frame(case, frame)
            _attach_advisory_sf1_prime(frame, r0)
            results.append(r0)
            continue
        if mode == "ctx_json":
            ctx = _load_ctx_json(p)
            if not ctx:
                results.append(_graceful_missing(case, f"ctx_json not found or invalid: {p}"))
                continue
            # build frame via mainline builder (current code)
            try:
                from decision_monitor.builder import DecisionMonitorBuilder

                frame = DecisionMonitorBuilder().build(ctx).to_dict()
                r0 = _extract_result_from_frame(case, frame)
                _attach_advisory_sf1_prime(frame, r0)
                results.append(r0)
            except Exception as e:
                results.append(_graceful_missing(case, f"ctx_json build failed: {e}"))
            continue
        if mode == "trace":
            d = _load_trace_jsonl_last_record(p)
            if not d:
                results.append(_graceful_missing(case, f"trace not found or invalid: {p}"))
                continue
            # trace → frame mapping not implemented in M0 (reserve)
            results.append(_graceful_missing(case, "trace loader reserved (no frame mapping in M0)"))
            continue
        if mode == "image":
            # image → candidate audit pipeline is not wired in this harness (reserve)
            results.append(_graceful_missing(case, "image loader reserved (no auto vision pipeline in M0)"))
            continue
        results.append(_graceful_missing(case, f"unsupported input_mode: {mode}"))

    summary = summarize_results(results)

    # real-pack extra summary
    worst = [r.case_id for r in sorted(results, key=lambda x: (1 if x.quality_grade == "poor" else 0, x.dead_branch_count), reverse=True)[:3]]
    summary.update(
        {
            "real_case_ids": real_case_ids,
            "worst_real_case_ids": worst,
            "real_case_quality_overview": {r.case_id: (r.quality_grade or "unknown") for r in results},
            "tension_audit": _tension_audit_summary(results),
            "severity_audit": _severity_audit_summary(results),
            "advisory_sf1_prime_audit": _advisory_sf1_prime_audit_summary(results),
        }
    )
    return results, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case_id", type=str, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    results, summary = run_real_cases(args.case_id)
    payload = {"summary": summary, "results": [asdict(r) for r in results]}

    if args.out:
        Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote:", args.out)
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

