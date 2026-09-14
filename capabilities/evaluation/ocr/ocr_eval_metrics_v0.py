# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-001 — OCR evaluation metrics v0 (CER / Chinese recall / garbled score).

Evaluation-only utilities. No runtime integration.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Tuple


_WS_RE = re.compile(r"\s+")


def normalize_ocr_text_for_eval_v0(text: str) -> str:
    # Keep newlines as separators but normalize whitespace within lines
    lines = [(t or "").strip() for t in (text or "").splitlines()]
    lines = [_WS_RE.sub(" ", ln) for ln in lines if ln]
    return "\n".join(lines).strip()


def levenshtein_distance_v0(a: str, b: str) -> int:
    a = a or ""
    b = b or ""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    # DP with O(min(n,m)) memory
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return int(prev[-1])


def compute_cer_v0(pred: str, truth: str) -> Dict[str, Any]:
    p = normalize_ocr_text_for_eval_v0(pred)
    t = normalize_ocr_text_for_eval_v0(truth)
    dist = levenshtein_distance_v0(p, t)
    denom = max(1, len(t))
    cer = float(dist) / float(denom)
    return {
        "pred_len": len(p),
        "truth_len": len(t),
        "edit_distance": int(dist),
        "cer": float(cer),
    }


def _is_chinese_char(ch: str) -> bool:
    if not ch:
        return False
    cp = ord(ch)
    # CJK Unified Ideographs + common extension A
    return (0x4E00 <= cp <= 0x9FFF) or (0x3400 <= cp <= 0x4DBF)


def compute_chinese_char_recall_v0(pred: str, truth: str) -> Dict[str, Any]:
    p = normalize_ocr_text_for_eval_v0(pred)
    t = normalize_ocr_text_for_eval_v0(truth)
    truth_chars = [c for c in t if _is_chinese_char(c)]
    if not truth_chars:
        return {"truth_chinese_count": 0, "hit_chinese_count": 0, "chinese_char_recall": None}
    pred_set = set([c for c in p if _is_chinese_char(c)])
    hit = sum(1 for c in truth_chars if c in pred_set)
    recall = float(hit) / float(len(truth_chars))
    return {"truth_chinese_count": len(truth_chars), "hit_chinese_count": hit, "chinese_char_recall": recall}


def compute_garbled_score_v0(text: str) -> Dict[str, Any]:
    """
    Heuristic garbled score:
    - counts unusual/unknown glyphs outside common ranges
    - penalizes excessive non-alnum/punct ratio
    Returns score in [0,1] (higher = more garbled).
    """
    s = (text or "").strip()
    if not s:
        return {"garbled_score": 0.0, "garbled_ratio": 0.0, "total_chars": 0}
    total = len(s)
    garbled = 0
    for ch in s:
        cp = ord(ch)
        ok = False
        if ch.isascii():
            ok = True
        elif _is_chinese_char(ch):
            ok = True
        elif 0x3000 <= cp <= 0x303F:  # CJK punctuation
            ok = True
        elif 0xFF00 <= cp <= 0xFFEF:  # Fullwidth forms
            ok = True
        if not ok:
            garbled += 1
    ratio = float(garbled) / float(max(1, total))
    # soft clamp
    score = max(0.0, min(1.0, ratio))
    return {"garbled_score": score, "garbled_ratio": ratio, "total_chars": total}


def classify_ocr_eval_result_v0(*, cer: float, garbled_score: float, raw_text_empty: bool) -> str:
    if raw_text_empty:
        return "fail"
    if cer <= 0.15 and garbled_score <= 0.10:
        return "pass"
    if cer <= 0.35 and garbled_score <= 0.20:
        return "weak_pass"
    if cer > 0.50 or garbled_score >= 0.35:
        return "fail"
    return "review_pending"

