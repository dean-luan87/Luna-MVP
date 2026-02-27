# -*- coding: utf-8 -*-
"""
Phase 2: D1 词典序排名器（Lexicographic Ranker v1）。
输入：一组 candidate 的 suite_report；输出：冠军 + 排名列表 + 淘汰原因 + rank_report.json/md。
L0 硬淘汰 → L1 守法(early_gain↑) → L2 冷静(dwell_p95_delta↓, volatility↓) → L3 不耽误(guarded_ratio_delta↓)。
军工级：Stress Gate 与排序解耦；early_gain 不作为安全门禁；REJECT 均带 reasons。
"""
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from simulation.d1.ranker import _early_gain_for_ranking, _load_scorecard, aggregate_suite

# Phase 1 冻结红线（与 gate.py 一致）
EXIT_LATENCY_P95_LIMIT = 6
HYSTERESIS_EFFICIENCY_MIN = 0.90


class StressGate:
    """军工级 Stress 安全门禁：与排序逻辑解耦；early_gain 不参与门禁。"""

    def __init__(
        self,
        exit_latency_p95_limit: float = EXIT_LATENCY_P95_LIMIT,
        hysteresis_efficiency_min: float = HYSTERESIS_EFFICIENCY_MIN,
    ):
        self.exit_latency_p95_limit = exit_latency_p95_limit
        self.hysteresis_efficiency_min = hysteresis_efficiency_min

    def evaluate(self, stress_scorecard: Dict[str, Any]) -> Dict[str, Any]:
        """
        stress_scorecard 建议包含：
        - guardian_discipline: { status: "PASS"/"FAIL", exit_latency_p95, hysteresis_efficiency, ... }
        - high_risk_frames_count: int
        - early_gain_mean: float（仅用于排序，不参与门禁）
        """
        reasons: List[str] = []
        gd = stress_scorecard.get("guardian_discipline") or {}
        if gd.get("status") != "PASS":
            reasons.append("GUARDIAN_DISCIPLINE_FAIL")
        if stress_scorecard.get("high_risk_frames_count", 0) <= 0:
            reasons.append("NO_HIGH_RISK_FRAMES")
        if reasons:
            return {"status": "REJECTED", "reasons": reasons}
        return {"status": "PASS", "reasons": []}


class D1TournamentJudge:
    """双通道评委：先 Stress Gate，通过后再按 rank_key 排序。"""

    def __init__(self) -> None:
        self.stress_gate = StressGate()

    def evaluate_candidate(
        self,
        stress_scorecard: Dict[str, Any],
        regular_scorecard: Dict[str, Any],
    ) -> Dict[str, Any]:
        gate_result = self.stress_gate.evaluate(stress_scorecard)
        if gate_result["status"] != "PASS":
            return {
                "status": "REJECTED_BY_STRESS",
                "reasons": gate_result["reasons"],
                "rank_key": None,
            }
        rank_key = (
            float(stress_scorecard.get("early_gain_mean", 0) or 0),
            -float(regular_scorecard.get("guarded_tail_ratio_mean", 0) or regular_scorecard.get("guarded_tail_ratio", 0) or 0),
            -float(regular_scorecard.get("volatility_mean", 0) or 0),
        )
        return {
            "status": "PASS",
            "reasons": [],
            "rank_key": rank_key,
        }


def _dwell_p95_delta_mean(scorecards: List[Dict[str, Any]]) -> float:
    vals = []
    for sc in scorecards:
        em = sc.get("event_metrics") or {}
        delta = em.get("delta") or {}
        v = delta.get("dwell_p95_delta")
        if v is not None:
            vals.append(float(v))
    return round(math.fsum(vals) / len(vals), 4) if vals else 0.0


def _aggregate_with_event_metrics(
    suite_report: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """与 ranker.aggregate_suite 一致，并增加 dwell_p95_delta_mean、guarded_tail_ratio_delta（若有）。"""
    agg, scorecards = aggregate_suite(suite_report)
    if not scorecards:
        agg["dwell_p95_delta_mean"] = 0.0
        agg["guarded_tail_ratio_delta_mean"] = 0.0
        return agg, scorecards
    agg["dwell_p95_delta_mean"] = _dwell_p95_delta_mean(scorecards)
    gd_ratios = []
    for sc in scorecards:
        gd = sc.get("guardian_discipline")
        if gd and "guarded_tail_ratio" in gd:
            base = suite_report.get("per_episode") or {}
            # candidate 的 guarded_tail_ratio 已在 audit；baseline 无单独字段，用 0 或从同 episode 的 baseline 取
            gd_ratios.append(float(gd.get("guarded_tail_ratio", 0)))
    if gd_ratios:
        agg["guarded_tail_ratio_mean"] = round(math.fsum(gd_ratios) / len(gd_ratios), 4)
    else:
        agg["guarded_tail_ratio_mean"] = None
    eff_gr = [float((sc.get("efficiency") or {}).get("guarded_ratio_delta", 0) or 0) for sc in scorecards]
    agg["guarded_ratio_delta_mean"] = round(math.fsum(eff_gr) / len(scorecards), 4)
    return agg, scorecards


def _lexicographic_sort_key_v1(agg: Dict[str, Any]) -> Tuple[float, float, float, float, float]:
    """
    L1 最大化 early_gain → L2 最小化 dwell_p95_delta, volatility → L3 最小化 guarded_ratio_delta。
    用于 sort：key 小者排前。
    """
    return (
        -float(agg.get("early_gain_weighted_mean", 0) or 0),
        float(agg.get("dwell_p95_delta_mean", 0) or 0),
        float(agg.get("volatility_mean", 0) or 0),
        float(agg.get("guarded_ratio_delta_mean", 0) or 0),
        0.0,
    )


def _high_risk_frames_count_from_report(suite_report: Dict[str, Any]) -> int:
    """Sum high_risk_seq_count from stress scorecards (early block). 仅基于 replay 行为字段。"""
    per = suite_report.get("per_episode") or {}
    total = 0
    for eid, ep in sorted(per.items()):
        sc_path = ep.get("scorecard_path")
        if not sc_path or not Path(sc_path).is_file():
            continue
        try:
            sc = json.loads(Path(sc_path).read_text(encoding="utf-8"))
        except Exception:
            continue
        early = sc.get("early") or {}
        n = early.get("high_risk_seq_count")
        if isinstance(n, (int, float)):
            total += int(n)
    return total


def _guarded_frames_count_from_report(suite_report: Dict[str, Any]) -> int:
    """Sum GUARDED 帧数：从 per_episode 的 candidate_replay_path 读 replay，数 control_mode==GUARDED。"""
    per = suite_report.get("per_episode") or {}
    total = 0
    for eid, ep in sorted(per.items()):
        replay_path = ep.get("candidate_replay_path")
        if not replay_path or not Path(replay_path).is_file():
            continue
        try:
            for line in Path(replay_path).read_text(encoding="utf-8").strip().splitlines():
                if not line:
                    continue
                rec = json.loads(line)
                mode = (rec.get("decision") or {}).get("control_mode") or ""
                if str(mode).strip().upper() == "GUARDED":
                    total += 1
        except Exception:
            continue
    return total


def _build_stress_scorecard_from_report(stress_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    从 stress suite_report 构建供 StressGate.evaluate 使用的 stress_scorecard。
    含 guardian_discipline（含 status）、high_risk_frames_count、early_gain_mean。
    """
    stress_agg, scorecards = _aggregate_with_event_metrics(stress_report)
    high_risk = _high_risk_frames_count_from_report(stress_report)
    early_gain_mean = float(stress_agg.get("early_gain_weighted_mean", 0) or 0)

    # 从各 episode scorecard 聚合 guardian_discipline，并判定 status
    p95_vals: List[float] = []
    eff_vals: List[float] = []
    for sc in scorecards:
        gd = sc.get("guardian_discipline") or {}
        if isinstance(gd, dict):
            p = gd.get("exit_latency_p95")
            e = gd.get("hysteresis_efficiency")
            if p is not None:
                p95_vals.append(float(p))
            if e is not None:
                eff_vals.append(float(e))
    exit_latency_p95 = max(p95_vals) if p95_vals else None
    hysteresis_efficiency = min(eff_vals) if eff_vals else None
    if exit_latency_p95 is not None and hysteresis_efficiency is not None:
        gd_status = (
            "PASS"
            if exit_latency_p95 <= EXIT_LATENCY_P95_LIMIT and hysteresis_efficiency >= HYSTERESIS_EFFICIENCY_MIN
            else "FAIL"
        )
    else:
        gd_status = "FAIL"  # 缺数据视为不通过
    guardian_discipline: Dict[str, Any] = {
        "status": gd_status,
        "exit_latency_p95": exit_latency_p95,
        "hysteresis_efficiency": hysteresis_efficiency,
    }
    return {
        "guardian_discipline": guardian_discipline,
        "high_risk_frames_count": high_risk,
        "early_gain_mean": early_gain_mean,
        "exit_latency_p95": exit_latency_p95,
        "hysteresis_efficiency": hysteresis_efficiency,
    }


def _lexicographic_sort_key_dual(
    stress_agg: Dict[str, Any],
    regular_agg: Dict[str, Any],
) -> Tuple[float, float, float, float]:
    """L1 stress early_gain↑ L2 regular guarded_ratio_delta↓ L3 regular volatility↓。key 小者排前。"""
    return (
        -float(stress_agg.get("early_gain_weighted_mean", 0) or 0),
        float(regular_agg.get("guarded_ratio_delta_mean", 0) or 0),
        float(regular_agg.get("volatility_mean", 0) or 0),
        0.0,
    )


def rank_candidates_dual_channel(
    run_dir: Path,
    candidate_results: List[Dict[str, Any]],
    rank_by: Optional[str] = None,
) -> Dict[str, Any]:
    """
    双通道词典序：先 Stress Gate（军工级，与排序解耦）→ 通过者按 L1 early_gain↑ → L2 guarded_tail_ratio↓ → L3 volatility↓。
    rank_by="early_gain_only" 时仅按 L1 early_gain 排序（单指标冠军，用于诊断是否排序规则压制变异）。
    candidate_results 需含 stress_suite_report_path、regular_suite_report_path。
    写入 rank_report.json/md；淘汰一律带 reasons（可审计）。
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    ranked: List[Dict[str, Any]] = []
    eliminated: List[Dict[str, Any]] = []
    stress_summary: Dict[str, Any] = {"patch_count": 0, "high_risk_frames_total": 0, "guarded_frames_total": 0, "risk_used_max_sample": None}
    regular_summary: Dict[str, Any] = {"patch_count": 0}
    judge = D1TournamentJudge()

    for cr in candidate_results:
        patch_id = cr.get("patch_id") or ""
        patch_path = cr.get("patch_path") or ""
        stress_path = cr.get("stress_suite_report_path")
        stress_path_resp = cr.get("stress_suite_report_path_responsive")
        regular_path = cr.get("regular_suite_report_path")
        stress_report = json.loads(Path(stress_path).read_text(encoding="utf-8")) if stress_path and Path(stress_path).is_file() else None
        stress_report_resp = json.loads(Path(stress_path_resp).read_text(encoding="utf-8")) if stress_path_resp and Path(stress_path_resp).is_file() else None
        regular_report = json.loads(Path(regular_path).read_text(encoding="utf-8")) if regular_path and Path(regular_path).is_file() else None
        if stress_report is None:
            eliminated.append({"patch_id": patch_id, "reason": "L0: missing_stress_suite_report", "reasons": ["MISSING_STRESS_REPORT"]})
            continue
        if stress_path_resp and stress_report_resp is None:
            eliminated.append({"patch_id": patch_id, "reason": "L0: missing_stress_responsive_suite_report", "reasons": ["MISSING_STRESS_RESPONSIVE_REPORT"]})
            continue
        if regular_report is None:
            eliminated.append({"patch_id": patch_id, "reason": "L0: missing_regular_suite_report", "reasons": ["MISSING_REGULAR_REPORT"]})
            continue
        stress_scorecard = _build_stress_scorecard_from_report(stress_report)
        stress_agg, _ = _aggregate_with_event_metrics(stress_report)
        if stress_report_resp is not None:
            stress_scorecard_resp = _build_stress_scorecard_from_report(stress_report_resp)
            stress_agg_resp, _ = _aggregate_with_event_metrics(stress_report_resp)
            result_resp = judge.evaluate_candidate(stress_scorecard_resp, {"guarded_tail_ratio_mean": None, "guarded_tail_ratio": None, "volatility_mean": None})
            if result_resp["status"] != "PASS":
                eliminated.append({
                    "patch_id": patch_id,
                    "reason": "L0: REJECTED_BY_STRESS_RESPONSIVE",
                    "reasons": result_resp["reasons"],
                })
                continue
            guarded_resp = _guarded_frames_count_from_report(stress_report_resp)
            eligible_resp = _high_risk_frames_count_from_report(stress_report_resp)
            if guarded_resp == 0 or eligible_resp == 0:
                eliminated.append({
                    "patch_id": patch_id,
                    "reason": "L0: REJECTED_BY_STRESS_RESPONSIVE",
                    "reasons": ["RESPONSIVE_REQUIRES_AT_LEAST_ONE_GUARDED_AND_EARLY_GAIN_ELIGIBLE_FRAMES_GT_0"],
                })
                continue
            stress_agg = stress_agg_resp
            stress_scorecard = stress_scorecard_resp
            stress_report = stress_report_resp
        regular_agg, _ = _aggregate_with_event_metrics(regular_report) if regular_report else ({}, [])
        regular_scorecard = {
            "guarded_tail_ratio_mean": regular_agg.get("guarded_tail_ratio_mean"),
            "guarded_tail_ratio": regular_agg.get("guarded_tail_ratio_mean"),
            "volatility_mean": regular_agg.get("volatility_mean"),
        }
        result = judge.evaluate_candidate(stress_scorecard, regular_scorecard)
        if result["status"] != "PASS":
            eliminated.append({
                "patch_id": patch_id,
                "reason": "L0: REJECTED_BY_STRESS",
                "reasons": result["reasons"],
            })
            continue
        high_risk_count = stress_scorecard.get("high_risk_frames_count", 0)
        guarded_count = _guarded_frames_count_from_report(stress_report)
        stress_summary["patch_count"] = stress_summary.get("patch_count", 0) + 1
        stress_summary["high_risk_frames_total"] = stress_summary.get("high_risk_frames_total", 0) + high_risk_count
        stress_summary["guarded_frames_total"] = stress_summary.get("guarded_frames_total", 0) + guarded_count
        rank_key = result["rank_key"]
        if rank_by == "early_gain_only":
            rank_key = (float(stress_agg.get("early_gain_weighted_mean", 0) or 0),)
        ranked.append({
            "patch_id": patch_id,
            "patch_path": patch_path,
            "aggregated": stress_agg,
            "stress_metrics": stress_agg,
            "regular_metrics": regular_agg,
            "stress_high_risk_frames_count": high_risk_count,
            "stress_scorecard": stress_scorecard,
            "_rank_key": rank_key,
            "sort_reason": (
                f"L1 stress_early_gain={stress_agg.get('early_gain_weighted_mean')} "
                f"L2 regular_guarded_tail={regular_agg.get('guarded_tail_ratio_mean')} "
                f"L3 regular_vol={regular_agg.get('volatility_mean')}"
            ) if rank_by != "early_gain_only" else f"early_gain_only={stress_agg.get('early_gain_weighted_mean')}",
        })

    ranked.sort(key=lambda x: x["_rank_key"], reverse=True)
    for e in ranked:
        rk = e["_rank_key"]
        e["rank_key"] = list(rk)  # 持久化供 Determinism 校验（位级一致）
        del e["_rank_key"]
    champion = ranked[0] if ranked else None
    final_rank_reason = (
        "仅按 L1 Stress early_gain↑ 排序（单指标冠军模式）。"
        if rank_by == "early_gain_only"
        else "先过 Stress 安全门禁（high_risk_frames>0 且 gate pass），再按 L1 Stress early_gain↑ → L2 Regular guarded_ratio_delta↓ → L3 Regular volatility↓ 词典序排序。"
    )
    report_data = {
        "champion_id": champion["patch_id"] if champion else None,
        "champion_patch_path": champion["patch_path"] if champion else None,
        "ranked": ranked,
        "eliminated": eliminated,
        "channels": {
            "stress": stress_summary,
            "regular": regular_summary,
        },
        "final_rank_reason": final_rank_reason,
    }
    json_path = run_dir / "rank_report.json"
    json_path.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# D1 Rank Report (Dual Channel)",
        "",
        f"**Champion**: {report_data['champion_id']}",
        "",
        f"**排序说明**: {final_rank_reason}",
        "",
        "## Stress Channel (门禁 + L1 early_gain)",
        "",
        "| Rank | patch_id | stress_early_gain_mean | stress_high_risk_frames |",
        "|------|----------|-------------------------|-------------------------|",
    ]
    for i, r in enumerate(ranked[:20], 1):
        sm = r.get("stress_metrics") or {}
        hr = r.get("stress_high_risk_frames_count", 0)
        md_lines.append(
            f"| {i} | {r.get('patch_id', '')} | {sm.get('early_gain_weighted_mean', '')} | {hr} |"
        )
    md_lines.extend([
        "",
        "## Regular Channel (L2/L3)",
        "",
        "| Rank | patch_id | regular_guarded_ratio_delta_mean | regular_volatility_mean |",
        "|------|----------|-----------------------------------|------------------------|",
    ])
    for i, r in enumerate(ranked[:20], 1):
        rm = r.get("regular_metrics") or {}
        md_lines.append(
            f"| {i} | {r.get('patch_id', '')} | {rm.get('guarded_ratio_delta_mean', '')} | {rm.get('volatility_mean', '')} |"
        )
    md_lines.extend([
        "",
        "## Eliminated (L0)",
        "",
    ])
    for e in eliminated:
        md_lines.append(f"- **{e.get('patch_id', '')}**: {e.get('reason', '')}")
    md_path = run_dir / "rank_report.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    return report_data


def _discover_candidate_results(run_dir: Path) -> List[Dict[str, Any]]:
    """从 run_dir 发现各 candidate 子目录下的 suite_report.json，构造 candidate_results。"""
    out = []
    for sub in sorted(run_dir.iterdir()):
        if not sub.is_dir():
            continue
        report_path = sub / "suite_report.json"
        if not report_path.is_file():
            continue
        patch_id = sub.name
        patch_path = str(sub / "patch.json") if (sub / "patch.json").is_file() else ""
        if not patch_path and (run_dir / "candidates" / f"{patch_id}.json").is_file():
            patch_path = str(run_dir / "candidates" / f"{patch_id}.json")
        out.append({
            "patch_id": patch_id,
            "patch_path": patch_path,
            "suite_report_path": str(report_path),
        })
    return out


def rank_candidates(
    run_dir: Path,
    candidate_results: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    读取每个 candidate 的 suite_report，聚合指标，按 L0~L3 词典序排名。
    若 candidate_results 未传，则从 run_dir 发现 * /suite_report.json 构造列表。
    candidate_results: [{ patch_id, patch_path, suite_report_path }, ...]
    写入 run_dir/rank_report.json 与 run_dir/rank_report.md；返回报告内容 dict。
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    if candidate_results is None:
        candidate_results = _discover_candidate_results(run_dir)
    ranked: List[Dict[str, Any]] = []
    eliminated: List[Dict[str, Any]] = []

    for cr in candidate_results:
        patch_id = cr.get("patch_id") or ""
        patch_path = cr.get("patch_path") or ""
        report_path = cr.get("suite_report_path")
        report = cr.get("suite_report")
        if report is None and report_path and Path(report_path).is_file():
            report = json.loads(Path(report_path).read_text(encoding="utf-8"))
        if report is None:
            eliminated.append({"patch_id": patch_id, "reason": "L0: missing_suite_report"})
            continue
        overall = report.get("overall", False)
        if not overall:
            reasons = report.get("overall_fail_reasons") or []
            eliminated.append({"patch_id": patch_id, "reason": "L0: gate_fail", "details": reasons})
            continue
        agg, scorecards = _aggregate_with_event_metrics(report)
        sort_key = _lexicographic_sort_key_v1(agg)
        ranked.append({
            "patch_id": patch_id,
            "patch_path": patch_path,
            "aggregated": agg,
            "_sort_key": sort_key,
            "sort_reason": (
                f"L1 early_gain={agg.get('early_gain_weighted_mean')} "
                f"L2 dwell_p95_delta={agg.get('dwell_p95_delta_mean')} vol={agg.get('volatility_mean')} "
                f"L3 gr_delta={agg.get('guarded_ratio_delta_mean')}"
            ),
        })

    ranked.sort(key=lambda x: x["_sort_key"])
    for e in ranked:
        del e["_sort_key"]

    champion = ranked[0] if ranked else None
    report_data = {
        "champion_id": champion["patch_id"] if champion else None,
        "champion_patch_path": champion["patch_path"] if champion else None,
        "ranked": ranked,
        "eliminated": eliminated,
    }
    if ranked and all(
        (r.get("aggregated") or {}).get("early_gain_weighted_mean", 0) == 0
        and (r.get("aggregated") or {}).get("volatility_mean", 0) == 0
        for r in ranked
    ):
        report_data["_warnings"] = [
            "all_aggregated_zero: scorecards may be missing or suite produced no variance; check run_dir/<id>/episodes/*/scorecard.json"
        ]

    json_path = run_dir / "rank_report.json"
    json_path.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# D1 Rank Report",
        "",
        f"**Champion**: {report_data['champion_id']}",
        "",
        "## Ranked (L1 early_gain ↑ → L2 dwell_p95_delta/vol ↓ → L3 gr_delta ↓)",
        "",
        "| Rank | patch_id | early_gain_mean | dwell_p95_delta_mean | volatility_mean | guarded_ratio_delta_mean |",
        "|------|----------|-----------------|----------------------|-----------------|---------------------------|",
    ]
    for i, r in enumerate(ranked[:20], 1):
        a = r.get("aggregated") or {}
        md_lines.append(
            f"| {i} | {r.get('patch_id', '')} | "
            f"{a.get('early_gain_weighted_mean', '')} | {a.get('dwell_p95_delta_mean', '')} | "
            f"{a.get('volatility_mean', '')} | {a.get('guarded_ratio_delta_mean', '')} |"
        )
    md_lines.extend([
        "",
        "## Eliminated (L0)",
        "",
    ])
    for e in eliminated:
        md_lines.append(f"- **{e.get('patch_id', '')}**: {e.get('reason', '')}")
    md_path = run_dir / "rank_report.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    return report_data
