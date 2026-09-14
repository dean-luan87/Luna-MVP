# -*- coding: utf-8 -*-
"""
Phase 3.3-D0: Comparator — 差分检测。
对齐 seq，比较 safety_level / control_mode；回归判定：safety 从更安全到更危险。
"""
import json
import os
from typing import Any, Dict, List, Tuple

# 安全等级序（越右越危险）；用于回归判定
SAFETY_ORDER: Tuple[str, ...] = ("SAFE", "CAUTION", "DANGER")


def _safety_rank(level: str) -> int:
    try:
        return SAFETY_ORDER.index((level or "").strip().upper())
    except ValueError:
        return -1


def _load_replay_records(path: str) -> List[Dict[str, Any]]:
    """path 为 bundle 目录或 replay_output.jsonl 文件路径。"""
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


def compare_decisions(baseline_path: str, candidate_path: str) -> dict:
    """
    对齐 seq，比较 decision.safety_level、decision.control_mode。
    回归：baseline 更安全、candidate 更危险（safety_level 等级升高）。
    返回 regression_count, regression_seqs, mismatch_count, missing_in_candidate, missing_in_baseline。
    """
    baseline_records = _load_replay_records(baseline_path)
    candidate_records = _load_replay_records(candidate_path)
    by_seq_baseline = {r.get("seq"): r for r in baseline_records}
    by_seq_candidate = {r.get("seq"): r for r in candidate_records}
    all_seqs = sorted(set(by_seq_baseline) | set(by_seq_candidate))
    missing_in_candidate = [s for s in all_seqs if s not in by_seq_candidate]
    missing_in_baseline = [s for s in all_seqs if s not in by_seq_baseline]
    regression_seqs: List[int] = []
    mismatch_count = 0
    compared_count = 0
    for seq in all_seqs:
        b = by_seq_baseline.get(seq)
        c = by_seq_candidate.get(seq)
        if b is None or c is None:
            continue
        compared_count += 1
        b_dec = b.get("decision") or {}
        c_dec = c.get("decision") or {}
        b_safety = (b_dec.get("safety_level") or "").strip().upper()
        c_safety = (c_dec.get("safety_level") or "").strip().upper()
        b_mode = (b_dec.get("control_mode") or "").strip()
        c_mode = (c_dec.get("control_mode") or "").strip()
        if b_safety != c_safety or b_mode != c_mode:
            mismatch_count += 1
        if b_safety and c_safety:
            r_b = _safety_rank(b_safety)
            r_c = _safety_rank(c_safety)
            if r_b >= 0 and r_c >= 0 and r_c > r_b:
                regression_seqs.append(seq)
    # D2.3: 帧对齐基线，供 scorecard.reference_alignment
    reference_alignment = {
        "aligned_count": compared_count,
        "missing_ref_frames": missing_in_baseline,
        "missing_cand_frames": missing_in_candidate,
    }
    return {
        "regression_count": len(regression_seqs),
        "regression_seqs": regression_seqs,
        "mismatch_count": mismatch_count,
        "compared_count": compared_count,
        "missing_in_candidate": missing_in_candidate,
        "missing_in_baseline": missing_in_baseline,
        "reference_alignment": reference_alignment,
    }
