# -*- coding: utf-8 -*-
"""
Phase 3.3-D0/B1: Scorer — 评分卡。
safety_regression_rate, volatility_index, early_conservative_action_gain, danger_delta, completeness_delta。
"""
import json
import os
from typing import Any, Dict, List, Optional

from simulation.logic.comparator import compare_decisions


def _load_replay_records(path: str) -> List[Dict[str, Any]]:
    if path.endswith(".jsonl"):
        replay_path = path
    else:
        replay_path = os.path.join(path.rstrip("/"), "replay_output.jsonl")
    if not os.path.isfile(replay_path):
        return []
    out: List[Dict[str, Any]] = []
    with open(replay_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _volatility_index(replay_path: str) -> float:
    """control_mode 变更次数 / max(1, record_count)."""
    records = _load_replay_records(replay_path)
    if len(records) <= 1:
        return 0.0
    modes = [(r.get("decision") or {}).get("control_mode") for r in records]
    changes = sum(1 for i in range(1, len(modes)) if modes[i] != modes[i - 1])
    return changes / max(1, len(records))


def _first_guarded_seq(records: List[Dict[str, Any]]) -> Optional[int]:
    """First seq where control_mode == GUARDED; None if never."""
    for r in records:
        mode = (r.get("decision") or {}).get("control_mode") or ""
        if str(mode).strip().upper() == "GUARDED":
            return r.get("seq")
    return None


def _danger_count(records: List[Dict[str, Any]]) -> int:
    """Frames with safety_level == DANGER."""
    return sum(
        1 for r in records
        if ((r.get("decision") or {}).get("safety_level") or "").strip().upper() == "DANGER"
    )


def _early_conservative_action_gain(
    baseline_records: List[Dict[str, Any]],
    candidate_records: List[Dict[str, Any]],
) -> float:
    """
    gain = (baseline_first_guarded_seq - candidate_first_guarded_seq) / total_frames.
    Candidate 更早进入 GUARDED → gain > 0.
    若从未进入 GUARDED，用 total_frames 作为 first_guarded_seq。
    """
    total = max(1, len(baseline_records), len(candidate_records))
    b_first = _first_guarded_seq(baseline_records)
    c_first = _first_guarded_seq(candidate_records)
    if b_first is None:
        b_first = total
    if c_first is None:
        c_first = total
    return (b_first - c_first) / total


def _safe_float(x: Any) -> Optional[float]:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _guarded_ratio(records: List[Dict[str, Any]]) -> float:
    """
    D2.1 冻结：只统计 decision.control_mode 存在的帧，不稀释。
    guarded_ratio = n_guarded / n_valid_frames。
    """
    valid = [r for r in records if "control_mode" in (r.get("decision") or {})]
    if not valid:
        return 0.0
    n_guarded = sum(
        1 for r in valid
        if (r.get("decision") or {}).get("control_mode") and str((r.get("decision") or {}).get("control_mode")).strip().upper() == "GUARDED"
    )
    return n_guarded / len(valid)


def _lookahead_avg_non_guarded(records: List[Dict[str, Any]]) -> Optional[float]:
    """
    D2.1 冻结：lookahead 只在 control_mode != GUARDED 且 pal_lookahead_m != None 的帧统计；
    避免 forced_presence 占位（值为 null）污染效率指标。
    """
    vals = []
    for r in records:
        dec = r.get("decision") or {}
        mode = (dec.get("control_mode") or "").strip().upper()
        if mode == "GUARDED":
            continue
        v = _safe_float(dec.get("pal_lookahead_m"))
        if v is not None:
            vals.append(v)
    if not vals:
        return None
    return sum(vals) / len(vals)


def _is_decision_present(rec: Dict[str, Any]) -> bool:
    """该帧有 decision 对象（含 forced 占位）。"""
    return rec.get("decision") is not None


def _is_decision_valid(rec: Dict[str, Any]) -> bool:
    """D2.2: 该帧存在 decision.safety_level 且 decision.control_mode 非空，且 decision_valid != false。"""
    d = rec.get("decision") or {}
    if d.get("decision_valid") is False:
        return False
    sl = d.get("safety_level")
    cm = d.get("control_mode")
    return sl is not None and cm is not None and str(cm).strip() != ""


def _is_lookahead_valid(rec: Dict[str, Any]) -> bool:
    """D2.2: 该帧存在 decision.pal_lookahead_m 且 > 0（或非 null）。"""
    v = _safe_float((rec.get("decision") or {}).get("pal_lookahead_m"))
    return v is not None and v > 0


def _extract_aligned_frames(
    baseline_records: List[Dict[str, Any]],
    candidate_records: List[Dict[str, Any]],
) -> List[tuple]:
    """D2.2: 按 seq 对齐，返回 [(seq, base_rec, cand_rec), ...]（交集）。"""
    by_b = {r.get("seq"): r for r in baseline_records}
    by_c = {r.get("seq"): r for r in candidate_records}
    common = sorted(set(by_b) & set(by_c))
    return [(seq, by_b[seq], by_c[seq]) for seq in common]


def _is_lookahead_present(rec: Dict[str, Any]) -> bool:
    """该帧 decision 存在 pal_lookahead_m 字段（含 null）。"""
    return "pal_lookahead_m" in (rec.get("decision") or {})


def _coverage_block(
    baseline_records: List[Dict[str, Any]],
    candidate_records: List[Dict[str, Any]],
    total_frames: int,
) -> Dict[str, Any]:
    """
    D2.2 Coverage Gate：防采样逃避。
    Presence-Only：gate 使用的 decision/lookahead_coverage_delta 按 presence（结构）统计，与 runner 对齐后一致则 delta=0。
    有效帧仍用 _is_decision_valid / _is_lookahead_valid 供 decision_valid_ratio 等。
    """
    aligned = _extract_aligned_frames(baseline_records, candidate_records)
    total = max(1, len(aligned) if aligned else total_frames)
    # 有效帧（用于 validity 指标）
    b_dec = sum(1 for _, b, _ in aligned if _is_decision_valid(b))
    c_dec = sum(1 for _, _, c in aligned if _is_decision_valid(c))
    b_la = sum(1 for _, b, _ in aligned if _is_lookahead_valid(b))
    c_la = sum(1 for _, _, c in aligned if _is_lookahead_valid(c))
    # presence（结构）— 用于 gate 的 coverage delta，避免 presence-only 补 null 被误杀
    b_dec_present = sum(1 for _, b, _ in aligned if _is_decision_present(b))
    c_dec_present = sum(1 for _, _, c in aligned if _is_decision_present(c))
    b_la_present = sum(1 for _, b, _ in aligned if _is_lookahead_present(b))
    c_la_present = sum(1 for _, _, c in aligned if _is_lookahead_present(c))
    dr_base = b_dec_present / total
    dr_cand = c_dec_present / total
    lr_base = b_la_present / total
    lr_cand = c_la_present / total
    decision_coverage_delta = round(dr_cand - dr_base, 4)
    lookahead_coverage_delta = round(lr_cand - lr_base, 4)

    # decision_valid_ratio = n_decision_valid / n_decision_present（candidate）
    n_decision_present = sum(1 for r in candidate_records if _is_decision_present(r))
    n_decision_valid = sum(1 for r in candidate_records if _is_decision_valid(r))
    decision_valid_ratio = round(n_decision_valid / max(1, n_decision_present), 4)

    # lookahead_presence_forced_ratio, lookahead_value_valid_ratio（candidate）
    lookahead_present_count = sum(1 for r in candidate_records if _is_lookahead_present(r))
    n_forced_lookahead_presence = sum(1 for r in candidate_records if (r.get("replay_meta") or {}).get("forced_lookahead_presence"))
    n_lookahead_value_valid = sum(1 for r in candidate_records if (r.get("decision") or {}).get("pal_lookahead_m") is not None)
    lookahead_presence_forced_ratio = round(n_forced_lookahead_presence / max(1, lookahead_present_count), 4) if lookahead_present_count else 0.0
    lookahead_value_valid_ratio = round(n_lookahead_value_valid / max(1, lookahead_present_count), 4) if lookahead_present_count else 0.0

    return {
        "total_frames": len(aligned) if aligned else total_frames,
        "decision_valid_frames_baseline": b_dec,
        "decision_valid_frames_candidate": c_dec,
        "lookahead_valid_frames_baseline": b_la,
        "lookahead_valid_frames_candidate": c_la,
        "decision_coverage_ratio_baseline": round(dr_base, 4),
        "decision_coverage_ratio_candidate": round(dr_cand, 4),
        "decision_coverage_delta": decision_coverage_delta,
        "lookahead_coverage_ratio_baseline": round(lr_base, 4),
        "lookahead_coverage_ratio_candidate": round(lr_cand, 4),
        "lookahead_coverage_delta": lookahead_coverage_delta,
        "decision_valid_ratio": decision_valid_ratio,
        "lookahead_presence_forced_ratio": lookahead_presence_forced_ratio,
        "lookahead_value_valid_ratio": lookahead_value_valid_ratio,
    }


def _weighted_early_gain_block(
    baseline_records: List[Dict[str, Any]],
    candidate_records: List[Dict[str, Any]],
    total_frames: int,
) -> Dict[str, Any]:
    """
    D2.2 防低风险刷分：仅在“高风险帧”上算 early gain。
    v1：replay 无 per-frame complexity_delta 时标记 WEIGHTED_EARLY_GAIN_UNAVAILABLE，不进硬门禁。
    """
    high_risk_seqs = set()
    for r in candidate_records:
        complexity_delta = _safe_float(r.get("complexity_delta"))
        if complexity_delta is not None and complexity_delta > 0:
            seq = r.get("seq")
            if seq is not None:
                high_risk_seqs.add(seq)
    if not high_risk_seqs:
        for r in baseline_records:
            complexity_delta = _safe_float(r.get("complexity_delta"))
            if complexity_delta is not None and complexity_delta > 0:
                seq = r.get("seq")
                if seq is not None:
                    high_risk_seqs.add(seq)
    if not high_risk_seqs:
        return {
            "early_gain_weighted": None,
            "weighted_early_gain_available": False,
            "reason": "WEIGHTED_EARLY_GAIN_UNAVAILABLE",
            "high_risk_seq_count": 0,
        }
    n_hr = len(high_risk_seqs)
    total = max(1, total_frames)
    b_first_hr = total
    c_first_hr = total
    for r in sorted(baseline_records, key=lambda x: x.get("seq", 0)):
        if r.get("seq") in high_risk_seqs and (r.get("decision") or {}).get("control_mode") and str((r.get("decision") or {}).get("control_mode")).strip().upper() == "GUARDED":
            b_first_hr = r.get("seq", total)
            break
    for r in sorted(candidate_records, key=lambda x: x.get("seq", 0)):
        if r.get("seq") in high_risk_seqs and (r.get("decision") or {}).get("control_mode") and str((r.get("decision") or {}).get("control_mode")).strip().upper() == "GUARDED":
            c_first_hr = r.get("seq", total)
            break
    early_gain_weighted = round((b_first_hr - c_first_hr) / max(n_hr, 1), 4)
    return {
        "early_gain_weighted": early_gain_weighted,
        "weighted_early_gain_available": True,
        "high_risk_seq_count": n_hr,
        "baseline_first_guarded_in_high_risk": b_first_hr if b_first_hr != total else None,
        "candidate_first_guarded_in_high_risk": c_first_hr if c_first_hr != total else None,
    }


# D2.3: 相对缩短 ≥10% 视为缓解
LOOKAHEAD_SHORTEN_MIN_RATIO = 0.10


def _perception_block(
    baseline_records: List[Dict[str, Any]],
    candidate_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    D2.3 语义守恒：仅在 ref_safety in {CAUTION, DANGER} 的帧上评估；
    cand_safety == SAFE 且无缓解代理 → PERCEPTION_DEGRADATION。
    缓解代理：cand_mode == GUARDED 或 cand_lookahead <= ref_lookahead * (1 - LOOKAHEAD_SHORTEN_MIN_RATIO)。
    """
    aligned = _extract_aligned_frames(baseline_records, candidate_records)
    perception_checked_frames = 0
    degradation_count = 0
    degradation_examples: List[int] = []
    mitigation_by_guarded_count = 0
    mitigation_by_lookahead_count = 0
    max_examples = 10
    for seq, b, c in aligned:
        b_dec = b.get("decision") or {}
        c_dec = c.get("decision") or {}
        ref_safety = (b_dec.get("safety_level") or "").strip().upper()
        cand_safety = (c_dec.get("safety_level") or "").strip().upper()
        ref_mode = (b_dec.get("control_mode") or "").strip().upper()
        cand_mode = (c_dec.get("control_mode") or "").strip().upper()
        ref_lookahead = _safe_float(b_dec.get("pal_lookahead_m"))
        cand_lookahead = _safe_float(c_dec.get("pal_lookahead_m"))
        if ref_safety not in ("CAUTION", "DANGER"):
            continue
        perception_checked_frames += 1
        more_safe = cand_safety == "SAFE" and ref_safety != "SAFE"
        if not more_safe:
            continue
        guarded_ok = cand_mode == "GUARDED"
        ref_la = ref_lookahead if ref_lookahead is not None else 0.0
        cand_la = cand_lookahead if cand_lookahead is not None else 0.0
        shorten_ok = ref_la > 0 and cand_la <= ref_la * (1.0 - LOOKAHEAD_SHORTEN_MIN_RATIO)
        if guarded_ok:
            mitigation_by_guarded_count += 1
        if shorten_ok:
            mitigation_by_lookahead_count += 1
        if guarded_ok or shorten_ok:
            continue
        degradation_count += 1
        if len(degradation_examples) < max_examples:
            degradation_examples.append(seq)
    denom = max(1, perception_checked_frames)
    degradation_rate = round(degradation_count / denom, 6)
    return {
        "perception_checked_frames": perception_checked_frames,
        "degradation_count": degradation_count,
        "degradation_rate": degradation_rate,
        "degradation_examples": degradation_examples,
        "mitigation_by_guarded_count": mitigation_by_guarded_count,
        "mitigation_by_lookahead_count": mitigation_by_lookahead_count,
    }


def _efficiency_block(
    baseline_records: List[Dict[str, Any]],
    candidate_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    D2.1：efficiency 在 scorer 内计算；guarded_ratio 仅有效帧，lookahead 仅非 GUARDED 帧。
    """
    gr_baseline = _guarded_ratio(baseline_records)
    gr_candidate = _guarded_ratio(candidate_records)
    guarded_ratio_delta = round(gr_candidate - gr_baseline, 4)
    la_baseline = _lookahead_avg_non_guarded(baseline_records)
    la_candidate = _lookahead_avg_non_guarded(candidate_records)
    lookahead_avg_baseline = round(la_baseline, 4) if la_baseline is not None else None
    lookahead_avg_candidate = round(la_candidate, 4) if la_candidate is not None else None
    if la_baseline is None or la_baseline <= 0:
        lookahead_drop_ratio = 0.0
    elif la_candidate is None:
        # candidate 无有效 lookahead（如全为 presence 占位 null）时不惩罚，避免结构误杀
        lookahead_drop_ratio = 0.0
    else:
        c_val = la_candidate
        lookahead_drop_ratio = round((la_baseline - c_val) / la_baseline, 4)
    efficiency_penalty = 0.0
    return {
        "guarded_ratio_baseline": round(gr_baseline, 4),
        "guarded_ratio_candidate": round(gr_candidate, 4),
        "guarded_ratio_delta": guarded_ratio_delta,
        "lookahead_avg_baseline": lookahead_avg_baseline,
        "lookahead_avg_candidate": lookahead_avg_candidate,
        "lookahead_drop_ratio": lookahead_drop_ratio,
        "efficiency_penalty": efficiency_penalty,
    }


def score(
    baseline_path: str,
    candidate_path: str,
    explain_baseline_path: Optional[str] = None,
    explain_candidate_path: Optional[str] = None,
) -> dict:
    """
    对比 baseline 与 candidate 的 replay，输出 scorecard。
    B1 新增：early_conservative_action_gain, danger_delta。
    """
    cmp = compare_decisions(baseline_path, candidate_path)
    compared_count = max(1, cmp.get("compared_count", 0))
    regression_count = cmp.get("regression_count", 0)
    safety_regression_rate = regression_count / compared_count
    volatility = _volatility_index(candidate_path)
    baseline_records = _load_replay_records(baseline_path)
    candidate_records = _load_replay_records(candidate_path)
    n_forced_lookahead = sum(1 for r in candidate_records if (r.get("replay_meta") or {}).get("forced_lookahead_presence") or (r.get("replay_meta") or {}).get("forced_lookahead"))
    n_valid_frames = max(1, len(candidate_records))
    lookahead_forced_ratio = round(n_forced_lookahead / n_valid_frames, 4)
    early_gain = _early_conservative_action_gain(baseline_records, candidate_records)
    baseline_danger = _danger_count(baseline_records)
    candidate_danger = _danger_count(candidate_records)
    danger_delta = candidate_danger - baseline_danger
    efficiency = _efficiency_block(baseline_records, candidate_records)
    efficiency["lookahead_forced_ratio"] = lookahead_forced_ratio
    coverage = _coverage_block(baseline_records, candidate_records, compared_count)
    perception = _perception_block(baseline_records, candidate_records)
    early_block = _weighted_early_gain_block(baseline_records, candidate_records, compared_count)
    out = {
        "safety_regression_rate": round(safety_regression_rate, 4),
        "regression_count": regression_count,
        "compared_count": compared_count,
        "volatility_index": round(volatility, 4),
        "early_conservative_action_gain": round(early_gain, 4),
        "danger_delta": danger_delta,
        "explain_completeness_delta": 0.0,
        "efficiency": efficiency,
        "coverage": coverage,
        "perception": perception,
        "reference_alignment": cmp.get("reference_alignment", {}),
        "early": early_block,
        "comparison": cmp,
        "lookahead_forced_ratio": lookahead_forced_ratio,
    }
    out["decision_coverage_delta"] = coverage["decision_coverage_delta"]
    out["lookahead_coverage_delta"] = coverage["lookahead_coverage_delta"]
    out["decision_valid_ratio"] = coverage.get("decision_valid_ratio")
    out["lookahead_presence_forced_ratio"] = coverage.get("lookahead_presence_forced_ratio")
    out["lookahead_value_valid_ratio"] = coverage.get("lookahead_value_valid_ratio")
    return out
