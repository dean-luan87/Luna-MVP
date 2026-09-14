# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-012-Improve-B — OCR Layout / Symbol / Reading Order Governance v0.

This module adds a governance layer around OCR raw candidates WITHOUT semantic interpretation
and WITHOUT MidPlatform/SceneDelta/WorldContext integration.

v0 design constraints (intentionally lightweight):
- No new ML models
- No pixel-level CV required
- Operates primarily on OCR candidate bboxes + confidences + text strings

The goal is to output structured evidence so downstream systems do not need to rely on a
single flat `raw_text_joined`.
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple


NoiseCharSet = frozenset({"0", "O", "o", "I", "l", "1", "J", "C", "y", "Y"})


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _bbox_area(bb: Sequence[float]) -> float:
    x1, y1, x2, y2 = [float(v) for v in bb]
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def _bbox_center(bb: Sequence[float]) -> Tuple[float, float]:
    x1, y1, x2, y2 = [float(v) for v in bb]
    return ((x1 + x2) * 0.5, (y1 + y2) * 0.5)


def _bbox_union(a: Sequence[float], b: Sequence[float]) -> List[float]:
    ax1, ay1, ax2, ay2 = [float(v) for v in a]
    bx1, by1, bx2, by2 = [float(v) for v in b]
    return [min(ax1, bx1), min(ay1, by1), max(ax2, bx2), max(ay2, by2)]


def _bbox_iou(a: Sequence[float], b: Sequence[float]) -> float:
    ax1, ay1, ax2, ay2 = [float(v) for v in a]
    bx1, by1, bx2, by2 = [float(v) for v in b]
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0.0:
        return 0.0
    ua = _bbox_area(a) + _bbox_area(b) - inter
    return float(inter / ua) if ua > 0 else 0.0


def _text_norm(s: str) -> str:
    return " ".join((s or "").strip().split())


def _is_short_noise_text(s: str) -> bool:
    t = _text_norm(s)
    if not t:
        return False
    if len(t) > 2:
        return False
    # High-risk short tokens: single char or two chars composed of noise set
    return all(ch in NoiseCharSet for ch in t)


def _is_stylized_glyph_candidate(text: str, conf: Optional[float], bbox: Sequence[float]) -> bool:
    """
    v0 heuristic: treat single-digit or single-letter low-confidence boxes as glyph candidates.
    This is NOT semantic; it's a 'requires confirmation' bucket.
    """
    t = _text_norm(text)
    if len(t) != 1:
        return False
    if not (t.isdigit() or t.isalpha()):
        return False
    c = float(conf) if conf is not None else 0.0
    # Lower confidence -> more likely stylized / ambiguous glyph
    if c >= 0.90:
        return False
    # Square-ish boxes are common for badges/line numbers/icons
    x1, y1, x2, y2 = [float(v) for v in bbox]
    w, h = max(1.0, x2 - x1), max(1.0, y2 - y1)
    ar = w / h
    return 0.6 <= ar <= 1.7


def classify_ocr_region_type_v0(cand: Dict[str, Any]) -> str:
    """
    Region types:
    - text_region
    - visual_symbol (likely non-text symbol noise)
    - visual_glyph (ambiguous stylized glyph)
    - decorative_graphic (very low-signal short candidates)
    - unknown
    """
    text = str(cand.get("text") or cand.get("normalized_text") or "")
    conf = cand.get("confidence")
    bbox = cand.get("bbox")
    if not isinstance(bbox, list) or len(bbox) != 4:
        return "unknown"

    t = _text_norm(text)
    c = float(conf) if conf is not None else None

    if _is_short_noise_text(t):
        return "visual_symbol"
    if _is_stylized_glyph_candidate(t, c, bbox):
        return "visual_glyph"
    if not t and (c is None or c < 0.3):
        return "decorative_graphic"
    return "text_region" if t else "unknown"


@dataclass(frozen=True)
class ReadingOrderCandidateV0:
    reading_order_id: str
    scope: str  # global | layout_group
    order_type: str
    confidence: float
    ordered_candidate_ids: List[str]
    should_join_globally: bool
    reason: str


def _estimate_reading_order_for_candidates(
    candidate_rows: List[Dict[str, Any]],
    *,
    scope: str,
) -> ReadingOrderCandidateV0:
    """
    v0 heuristic:
    - Sort by y-center (top->bottom) then x-center (left->right)
    - If bbox clusters suggest multi-column, lower confidence and do not join globally.
    """
    ids: List[str] = []
    pts: List[Tuple[float, float]] = []
    for r in candidate_rows:
        bb = r.get("bbox")
        if not isinstance(bb, list) or len(bb) != 4:
            continue
        cid = str(r.get("candidate_id") or r.get("text_id") or "")
        if not cid:
            continue
        ids.append(cid)
        pts.append(_bbox_center(bb))

    # Detect multi-column: large spread in x with comparable spread in y.
    xs = [p[0] for p in pts] or [0.0]
    ys = [p[1] for p in pts] or [0.0]
    xspan = max(xs) - min(xs)
    yspan = max(ys) - min(ys)
    multi_col = bool(xspan > 1.2 * max(1.0, yspan) and len(pts) >= 8)

    # Ordering
    items = []
    for r in candidate_rows:
        bb = r.get("bbox")
        if not isinstance(bb, list) or len(bb) != 4:
            continue
        cid = str(r.get("candidate_id") or r.get("text_id") or "")
        if not cid:
            continue
        x, y = _bbox_center(bb)
        items.append((y, x, cid))
    ordered = [cid for _, __, cid in sorted(items)]

    if multi_col:
        return ReadingOrderCandidateV0(
            reading_order_id=f"ro_{uuid.uuid4().hex[:10]}",
            scope=scope,
            order_type="multi_column",
            confidence=0.35,
            ordered_candidate_ids=ordered,
            should_join_globally=False,
            reason="xspan_suggests_multi_column;join_requires_layout_groups",
        )
    return ReadingOrderCandidateV0(
        reading_order_id=f"ro_{uuid.uuid4().hex[:10]}",
        scope=scope,
        order_type="left_to_right_top_to_bottom",
        confidence=0.70,
        ordered_candidate_ids=ordered,
        should_join_globally=True,
        reason="heuristic_y_then_x",
    )


class _UnionFind:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.r[ra] < self.r[rb]:
            self.p[ra] = rb
        elif self.r[ra] > self.r[rb]:
            self.p[rb] = ra
        else:
            self.p[rb] = ra
            self.r[ra] += 1


def group_text_candidates_by_layout_v0(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    v0 grouping: connected components by bbox proximity/overlap.
    This avoids cross-panel concatenation in many common signage layouts.
    """
    cand = [r for r in rows if isinstance(r.get("bbox"), list) and len(r.get("bbox")) == 4]
    if not cand:
        return []

    bbs = [c["bbox"] for c in cand]
    # scale threshold from median bbox height
    hs = [max(1.0, float(bb[3]) - float(bb[1])) for bb in bbs]
    hs_sorted = sorted(hs)
    med_h = hs_sorted[len(hs_sorted) // 2] if hs_sorted else 20.0
    dist_thr = 2.5 * med_h

    uf = _UnionFind(len(cand))
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            a, b = bbs[i], bbs[j]
            if _bbox_iou(a, b) >= 0.01:
                uf.union(i, j)
                continue
            ax, ay = _bbox_center(a)
            bx, by = _bbox_center(b)
            d = math.hypot(ax - bx, ay - by)
            if d <= dist_thr:
                uf.union(i, j)

    groups: Dict[int, List[Dict[str, Any]]] = {}
    for i, row in enumerate(cand):
        groups.setdefault(uf.find(i), []).append(row)

    out: List[Dict[str, Any]] = []
    for g_rows in groups.values():
        gbb: Optional[List[float]] = None
        for r in g_rows:
            bb = r.get("bbox")
            if not isinstance(bb, list) or len(bb) != 4:
                continue
            gbb = bb if gbb is None else _bbox_union(gbb, bb)
        out.append({"bbox": gbb, "rows": g_rows})

    # sort groups top-to-bottom then left-to-right
    def _gk(g: Dict[str, Any]) -> Tuple[float, float]:
        bb = g.get("bbox") or [0, 0, 0, 0]
        x, y = _bbox_center(bb)
        return (y, x)

    return sorted(out, key=_gk)


def build_ocr_layout_governance_evidence_v0(
    *,
    image_id: str,
    provider: str,
    raw_ocr_payload: Dict[str, Any],
    source_image_path: str,
) -> Dict[str, Any]:
    """
    Build OcrLayoutGovernanceEvidenceV0 from RapidOCR payload.
    """
    raw_candidates = raw_ocr_payload.get("raw_text_candidates")
    if not isinstance(raw_candidates, list):
        raw_candidates = []

    # Enrich candidate ids and classification
    enriched: List[Dict[str, Any]] = []
    for i, c in enumerate(raw_candidates):
        if not isinstance(c, dict):
            continue
        bb = c.get("bbox")
        if not isinstance(bb, list) or len(bb) != 4:
            continue
        cid = str(c.get("text_id") or f"txt_{i+1:03d}")
        text = str(c.get("normalized_text") or c.get("text") or "")
        conf = c.get("confidence")
        region_type = classify_ocr_region_type_v0({"text": text, "confidence": conf, "bbox": bb})
        enriched.append(
            {
                "candidate_id": cid,
                "text_id": cid,
                "text": str(c.get("text") or ""),
                "normalized_text": _text_norm(text),
                "bbox": [float(x) for x in bb],
                "confidence": float(conf) if conf is not None else None,
                "region_type": region_type,
            }
        )

    # Derive symbol/glyph candidates and suppression set
    visual_symbol_candidates: List[Dict[str, Any]] = []
    visual_glyph_candidates: List[Dict[str, Any]] = []
    decorative_graphic_candidates: List[Dict[str, Any]] = []

    suppress_from_joined: set[str] = set()
    for c in enriched:
        rt = c.get("region_type")
        if rt == "visual_symbol":
            sid = f"sym_{uuid.uuid4().hex[:10]}"
            visual_symbol_candidates.append(
                {
                    "symbol_id": sid,
                    "symbol_type": "icon_or_shape_noise_v0",
                    "bbox": c.get("bbox"),
                    "should_enter_raw_text": False,
                    "overlapping_ocr_candidates": [c["candidate_id"]],
                    "filter_effect": "suppress_from_joined",
                    "notes": "derived_from_short_high_risk_token",
                }
            )
            suppress_from_joined.add(c["candidate_id"])
        elif rt == "visual_glyph":
            gid = f"gly_{uuid.uuid4().hex[:10]}"
            visual_glyph_candidates.append(
                {
                    "glyph_id": gid,
                    "glyph_type": "stylized_digit_or_letter_v0",
                    "visual_hint": c.get("normalized_text"),
                    "bbox": c.get("bbox"),
                    "confidence": 0.0,
                    "source": "ocr_low_confidence_single_char",
                    "ocr_confirmed": False,
                    "requires_confirmation": True,
                    "should_enter_raw_text": False,
                    "linked_ocr_candidate_id": c["candidate_id"],
                }
            )
            suppress_from_joined.add(c["candidate_id"])
        elif rt == "decorative_graphic":
            decorative_graphic_candidates.append(
                {
                    "decor_id": f"dec_{uuid.uuid4().hex[:10]}",
                    "bbox": c.get("bbox"),
                    "notes": "low_signal_candidate",
                }
            )

    # Grouping & reading order per group
    text_rows = [c for c in enriched if c.get("region_type") == "text_region"]
    grouped = group_text_candidates_by_layout_v0(text_rows)

    layout_groups: List[Dict[str, Any]] = []
    reading_orders: List[Dict[str, Any]] = []
    raw_text_joined_by_group: List[Dict[str, Any]] = []

    for gi, g in enumerate(grouped):
        g_rows = g.get("rows") or []
        gbb = g.get("bbox")
        group_id = f"grp_{gi+1:03d}_{uuid.uuid4().hex[:8]}"

        ro = _estimate_reading_order_for_candidates(g_rows, scope="layout_group")
        reading_orders.append(ro.__dict__)

        # Join in estimated order; exclude suppressed/glyph/symbol
        id_to_text = {str(r.get("candidate_id")): str(r.get("normalized_text") or "") for r in g_rows}
        ordered_ids = [cid for cid in ro.ordered_candidate_ids if cid in id_to_text]
        joined_lines = [id_to_text[cid] for cid in ordered_ids if id_to_text.get(cid)]
        joined = "\n".join(joined_lines)

        layout_groups.append(
            {
                "group_id": group_id,
                "group_type": "unknown_panel_v0",
                "bbox": gbb,
                "text_candidate_ids": ordered_ids,
                "visual_symbol_ids": [],
                "visual_glyph_ids": [],
                "reading_order_id": ro.reading_order_id,
                "group_raw_text_joined": joined,
                "group_confidence": _clip01(float(ro.confidence)),
            }
        )
        raw_text_joined_by_group.append(
            {
                "group_id": group_id,
                "reading_order_id": ro.reading_order_id,
                "joined_text": joined,
                "ordered_candidate_ids": ordered_ids,
                "join_reliable": bool(ro.should_join_globally and ro.confidence >= 0.6),
            }
        )

    # Global reading order candidate (over groups)
    ro_global = _estimate_reading_order_for_candidates(text_rows, scope="global")
    reading_orders.append(ro_global.__dict__)

    # Global joined is debug only when order uncertain
    global_join = "\n\n".join([x.get("joined_text") or "" for x in raw_text_joined_by_group if (x.get("joined_text") or "").strip()])

    uncertainty = {
        "reading_order_uncertain": bool(ro_global.confidence < 0.6 or not ro_global.should_join_globally),
        "layout_grouping_uncertain": bool(len(layout_groups) <= 1 and len(text_rows) >= 12),
        "glyph_confirmation_required": bool(visual_glyph_candidates),
    }

    evidence = {
        "image_id": image_id,
        "source_image_path": source_image_path,
        "provider": provider,
        "layout_governance_version": "v0",
        "text_regions": [{"bbox": g.get("bbox"), "group_id": lg.get("group_id")} for g, lg in zip(grouped, layout_groups)],
        "visual_symbol_candidates": visual_symbol_candidates,
        "visual_glyph_candidates": visual_glyph_candidates,
        "decorative_graphic_candidates": decorative_graphic_candidates,
        "layout_groups": layout_groups,
        "reading_order_candidates": reading_orders,
        "raw_text_candidates": enriched,
        "symbol_noise_filter_report": {
            "suppressed_candidate_ids": sorted(list(suppress_from_joined)),
            "suppressed_reason": "visual_symbol_or_visual_glyph_v0",
        },
        "raw_text_joined_by_group": raw_text_joined_by_group,
        "raw_text_joined_global": global_join,
        "raw_text_joined_global_is_debug_only": True,
        "uncertainty": uncertainty,
        "hard_audit": {
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "downstream_invocation_count": 0,
        },
    }
    return evidence

