# -*- coding: utf-8 -*-
"""
D1 Lexicographic 排名 + 冲突集提取。
只读 scorecard / suite_report；只在 Gate PASS 的候选内排序。
排序键：early_gain_weighted(↑) → volatility_index(↓) → guarded_ratio_delta(↓) → lookahead_drop_ratio(↓)。
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 与 gate 一致，用于冲突集“接近门槛”判定
VOLATILITY_MAX = 0.2
MAX_GUARDED_RATIO_DELTA = 0.30
MAX_LOOKAHEAD_DROP_RATIO = 0.15
NEAR_THRESHOLD_RATIO = 0.8  # ≥ 80% 门槛视为“接近”
CONFLICT_TOP_K = 5  # 每候选最多取 K 条冲突样本


def _safe_float(x: Any) -> Optional[float]:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _early_gain_for_ranking(sc: Dict[str, Any]) -> float:
    """D1 排名用 early gain：优先 early_gain_weighted，不可用时用 early_conservative_action_gain。"""
    early = sc.get("early") or {}
    if early.get("weighted_early_gain_available") and early.get("early_gain_weighted") is not None:
        return float(early["early_gain_weighted"])
    return float(sc.get("early_conservative_action_gain", 0) or 0)


def _load_scorecard(path: str) -> Optional[Dict[str, Any]]:
    p = Path(path)
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def aggregate_suite(
    suite_report: Dict[str, Any],
    scorecard_paths: Optional[Dict[str, str]] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    从 suite_report 聚合指标。若未传 scorecard_paths，从 per_episode[].scorecard_path 读取。
    返回 (aggregated, per_episode_scorecards)。
    aggregated: early_gain_weighted_mean, volatility_mean, guarded_ratio_delta_mean, lookahead_drop_mean,
                by_bucket 等；以及 min/max。
    """
    per = suite_report.get("per_episode") or {}
    if scorecard_paths:
        paths = scorecard_paths
    else:
        paths = {eid: (ep.get("scorecard_path") or "") for eid, ep in per.items() if ep.get("scorecard_path")}
    scorecards: List[Dict[str, Any]] = []
    for eid in sorted(paths.keys()):
        path = paths.get(eid)
        if not path:
            continue
        sc = _load_scorecard(path)
        if sc is None:
            continue
        sc["_episode_id"] = eid
        sc["_tags"] = suite_report.get("per_episode", {}).get(eid, {}).get("tags") or []
        scorecards.append(sc)
    if not scorecards:
        return {
            "early_gain_weighted_mean": 0.0,
            "volatility_mean": 0.0,
            "guarded_ratio_delta_mean": 0.0,
            "lookahead_drop_mean": 0.0,
            "early_gain_min": 0.0,
            "early_gain_max": 0.0,
            "volatility_min": 0.0,
            "volatility_max": 0.0,
            "by_bucket": {},
        }, []
    n = len(scorecards)
    early_gains = [_early_gain_for_ranking(sc) for sc in scorecards]
    vol = [float(sc.get("volatility_index", 0) or 0) for sc in scorecards]
    eff_gr = [float((sc.get("efficiency") or {}).get("guarded_ratio_delta", 0) or 0) for sc in scorecards]
    eff_la = [float((sc.get("efficiency") or {}).get("lookahead_drop_ratio", 0) or 0) for sc in scorecards]
    by_bucket: Dict[str, List[float]] = {}
    for sc in scorecards:
        for t in sc.get("_tags") or []:
            by_bucket.setdefault(t, []).append(_early_gain_for_ranking(sc))
    aggregated = {
        "early_gain_weighted_mean": round(sum(early_gains) / n, 4),
        "volatility_mean": round(sum(vol) / n, 4),
        "guarded_ratio_delta_mean": round(sum(eff_gr) / n, 4),
        "lookahead_drop_mean": round(sum(eff_la) / n, 4),
        "early_gain_min": round(min(early_gains), 4),
        "early_gain_max": round(max(early_gains), 4),
        "volatility_min": round(min(vol), 4),
        "volatility_max": round(max(vol), 4),
        "by_bucket": {t: round(sum(v) / len(v), 4) for t, v in by_bucket.items()},
        "episode_count": n,
    }
    return aggregated, scorecards


def lexicographic_key(agg: Dict[str, Any]) -> Tuple[float, float, float, float]:
    """(primary:-early, secondary:vol, tertiary:guarded_delta, tie:lookahead_drop) 用于 sort。"""
    return (
        -float(agg.get("early_gain_weighted_mean", 0) or 0),
        float(agg.get("volatility_mean", 0) or 0),
        float(agg.get("guarded_ratio_delta_mean", 0) or 0),
        float(agg.get("lookahead_drop_mean", 0) or 0),
    )


def extract_conflicts(
    candidate_id: str,
    patch_path: str,
    suite_report: Dict[str, Any],
    aggregated: Dict[str, Any],
    scorecards: List[Dict[str, Any]],
    top_k: int = CONFLICT_TOP_K,
) -> List[Dict[str, Any]]:
    """
    冲突集：Case A/B/C/D，每类取高价值样本，共最多 top_k 条。
    返回 [{ episode_id, scorecard_path, gate_result_path, reasons, tags }, ...]
    """
    per = suite_report.get("per_episode") or {}
    conflicts: List[Tuple[float, Dict[str, Any]]] = []  # (priority, record)
    vol_thresh = VOLATILITY_MAX * NEAR_THRESHOLD_RATIO
    gr_thresh = MAX_GUARDED_RATIO_DELTA * NEAR_THRESHOLD_RATIO

    for sc in scorecards:
        eid = sc.get("_episode_id", "")
        tags = sc.get("_tags") or []
        ep = per.get(eid) or {}
        scorecard_path = ep.get("scorecard_path") or ""
        gate_result_path = ep.get("gate_result_path") or ""
        early = _early_gain_for_ranking(sc)
        vol = float(sc.get("volatility_index", 0) or 0)
        gr = float((sc.get("efficiency") or {}).get("guarded_ratio_delta", 0) or 0)
        reasons: List[str] = []

        # Case A: early 提升但 guarded_ratio_delta 接近门槛
        if early > 0 and gr >= gr_thresh:
            reasons.append("CASE_A: early_gain_up_guarded_near_threshold")
        # Case B: early 提升但 volatility 接近门槛
        if early > 0 and vol >= vol_thresh:
            reasons.append("CASE_B: early_gain_up_volatility_near_threshold")
        if not reasons:
            continue
        priority = early + (gr / max(gr_thresh, 1e-6)) + (vol / max(vol_thresh, 1e-6))
        conflicts.append((priority, {
            "candidate_id": candidate_id,
            "patch_path": patch_path,
            "episode_id": eid,
            "scorecard_path": scorecard_path,
            "gate_result_path": gate_result_path,
            "reasons": reasons,
            "tags": tags,
            "early_gain": early,
            "volatility_index": vol,
            "guarded_ratio_delta": gr,
        }))
    # Case C: 某 bucket 表现明显差（桶间差异大）
    by_bucket = aggregated.get("by_bucket") or {}
    if len(by_bucket) >= 2:
        vals = list(by_bucket.values())
        if max(vals) - min(vals) > 0.05:
            worst_bucket = min(by_bucket, key=by_bucket.get)
            for sc in scorecards:
                if worst_bucket in (sc.get("_tags") or []):
                    ep = per.get(sc.get("_episode_id") or "") or {}
                    conflicts.append((1.0, {
                        "candidate_id": candidate_id,
                        "patch_path": patch_path,
                        "episode_id": sc.get("_episode_id"),
                        "scorecard_path": ep.get("scorecard_path"),
                        "gate_result_path": ep.get("gate_result_path"),
                        "reasons": ["CASE_C: bucket_variance_worst_bucket"],
                        "tags": sc.get("_tags") or [],
                        "early_gain": _early_gain_for_ranking(sc),
                        "volatility_index": float(sc.get("volatility_index") or 0),
                        "guarded_ratio_delta": float((sc.get("efficiency") or {}).get("guarded_ratio_delta") or 0),
                    }))
                    break  # 每候选只加一条 CASE_C 代表
    conflicts.sort(key=lambda x: -x[0])
    out = [x[1] for x in conflicts[:top_k]]
    return out


def run_ranker(
    candidate_results: List[Dict[str, Any]],
    out_dir: str,
    conflict_top_k: int = CONFLICT_TOP_K,
) -> Tuple[str, str, str]:
    """
    candidate_results: [{ patch_id, patch_path, suite_report_path, suite_report? }, ...]
    若已有 suite_report 对象可传入，否则从 suite_report_path 读取。
    写出 leaderboard.json, results.jsonl, conflict_set.jsonl；返回三路径。
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ranked: List[Dict[str, Any]] = []
    all_results: List[Dict[str, Any]] = []
    conflict_rows: List[Dict[str, Any]] = []

    for cr in candidate_results:
        patch_id = cr.get("patch_id") or ""
        patch_path = cr.get("patch_path") or ""
        report = cr.get("suite_report")
        if report is None:
            path = cr.get("suite_report_path")
            if path and Path(path).is_file():
                report = json.loads(Path(path).read_text(encoding="utf-8"))
        if report is None:
            all_results.append({"patch_id": patch_id, "patch_path": patch_path, "gate_passed": False, "error": "missing_suite_report"})
            continue
        overall = report.get("overall", False)
        if not overall:
            all_results.append({
                "patch_id": patch_id,
                "patch_path": patch_path,
                "gate_passed": False,
                "overall_fail_reasons": report.get("overall_fail_reasons", []),
            })
            continue
        agg, scorecards = aggregate_suite(report)
        key = lexicographic_key(agg)
        missing = report.get("missing_buckets") or []
        entry = {
            "patch_id": patch_id,
            "patch_path": patch_path,
            "gate_passed": True,
            "aggregated": agg,
            "missing_buckets": missing,
            "_sort_key": key,
        }
        ranked.append(entry)
        all_results.append({
            "patch_id": patch_id,
            "patch_path": patch_path,
            "gate_passed": True,
            "aggregated": agg,
            "missing_buckets": missing,
        })
        conflicts = extract_conflicts(patch_id, patch_path, report, agg, scorecards, top_k=conflict_top_k)
        for c in conflicts:
            conflict_rows.append(c)
        # Case D: overall 强但 missing_buckets 存在（覆盖不足）
        missing = report.get("missing_buckets") or []
        if missing:
            conflict_rows.append({
                "candidate_id": patch_id,
                "patch_path": patch_path,
                "episode_id": None,
                "scorecard_path": None,
                "gate_result_path": None,
                "reasons": ["CASE_D: missing_buckets_coverage_gap"],
                "tags": [],
                "missing_buckets": missing,
            })

    ranked.sort(key=lambda x: x["_sort_key"])
    for e in ranked:
        del e["_sort_key"]

    leaderboard = {
        "ordered": [{"patch_id": e["patch_id"], "patch_path": e["patch_path"], "aggregated": e["aggregated"], "missing_buckets": e["missing_buckets"]} for e in ranked],
        "champion": ranked[0] if ranked else None,
    }
    out = Path(out_dir)
    lb_path = out / "leaderboard.json"
    lb_path.write_text(json.dumps(leaderboard, ensure_ascii=False, indent=2), encoding="utf-8")
    res_path = out / "results.jsonl"
    with open(res_path, "w", encoding="utf-8") as f:
        for r in all_results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    cf_path = out / "conflict_set.jsonl"
    with open(cf_path, "w", encoding="utf-8") as f:
        for c in conflict_rows:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return str(lb_path), str(res_path), str(cf_path)
