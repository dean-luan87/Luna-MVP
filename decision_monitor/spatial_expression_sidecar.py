# -*- coding: utf-8 -*-
"""
Spatial Expression Sidecar (M0)

旁路层：把真实视觉候选（bbox）转成二维相对方位表达（human/debug）。
不做深度/距离估计；不反写主决策链；仅用于调试与表达质量验收。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass
class SpatialExpressionCandidate:
    candidate_label: str
    candidate_confidence: Optional[float] = None
    candidate_bbox_center_x_norm: Optional[float] = None
    candidate_bbox_center_y_norm: Optional[float] = None
    candidate_sector: Optional[str] = None  # left/front_left/front/front_right/right
    candidate_relative_bearing_deg: Optional[float] = None  # [-45, +45] deg
    candidate_horizontal_band: Optional[str] = None  # left/mid_left/mid/mid_right/right
    candidate_vertical_band: Optional[str] = None  # back/mid/front (image-top -> back, image-bottom -> front)
    candidate_human_location_text: Optional[str] = None
    candidate_debug_location_text: Optional[str] = None
    candidate_is_focus_target: bool = False
    candidate_source_mode: Optional[str] = None  # main/probe/mapped_target
    # Level 2 口语化行动表达 M0（可选，近场试点）
    candidate_actionable_expression: Optional[str] = None


@dataclass
class SpatialExpressionResult:
    focus_target_label: Optional[str] = None
    focus_target_expression: Optional[str] = None
    focus_target_debug_expression: Optional[str] = None
    candidate_count: int = 0
    candidates: List[SpatialExpressionCandidate] = field(default_factory=list)
    sidecar_reason: Optional[str] = None
    # Level 2 口语化行动表达 M0（近场/桌面试点；仅表达层，不反写底层）
    focus_target_actionable_expression: Optional[str] = None
    focus_target_actionable_debug_reason: Optional[str] = None


def _clamp01(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _xyxy(bbox: Any) -> Optional[Tuple[float, float, float, float]]:
    if bbox is None:
        return None
    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        return float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
    if isinstance(bbox, dict) and all(k in bbox for k in ("x1", "y1", "x2", "y2")):
        return float(bbox["x1"]), float(bbox["y1"]), float(bbox["x2"]), float(bbox["y2"])
    return None


def _bands_from_norm(x: float, y: float) -> Tuple[str, str]:
    # horizontal bands
    if x < 0.2:
        hb = "left"
    elif x < 0.4:
        hb = "mid_left"
    elif x < 0.6:
        hb = "mid"
    elif x < 0.8:
        hb = "mid_right"
    else:
        hb = "right"
    # vertical bands (image-top -> back/far, image-bottom -> front/near)
    if y < 0.33:
        vb = "back"
    elif y < 0.66:
        vb = "mid"
    else:
        vb = "front"
    return hb, vb


def _bearing_and_sector(x: float, bearing_range_deg: float = 45.0) -> Tuple[float, str]:
    # x=0.5 -> 0 deg, linear to [-range, +range]
    bearing = (x - 0.5) * 2.0 * float(bearing_range_deg)
    # sectors: left/front_left/front/front_right/right
    if x < 0.25:
        sector = "left"
    elif x < 0.45:
        sector = "front_left"
    elif x <= 0.55:
        sector = "front"
    elif x <= 0.75:
        sector = "front_right"
    else:
        sector = "right"
    return float(bearing), sector


def _human_location(hb: str, vb: str) -> str:
    hmap = {
        "left": "左侧",
        "mid_left": "中间偏左",
        "mid": "中间",
        "mid_right": "中间偏右",
        "right": "右侧",
    }
    # vb 用“前/后/中部”做粗粒度组合
    if vb == "back":
        suffix = "后方"
    elif vb == "front":
        suffix = "前方"
    else:
        suffix = ""
    base = hmap.get(hb, hb)
    if suffix:
        # “中间”更自然用“中间后侧/前侧”
        if hb == "mid":
            return "中间后侧" if vb == "back" else "中间前侧"
        return base.replace("侧", "") + suffix
    # mid band
    return base


def _debug_location(sector: str, bearing: float, x: float, y: float, hb: str, vb: str) -> str:
    return f"sector={sector}, bearing={bearing:.1f}deg, x={x:.2f}, y={y:.2f}, band={hb}/{vb}"


def build_spatial_expression_sidecar(
    *,
    focus_target_label: Optional[str],
    objects_main: Optional[Sequence[Dict[str, Any]]],
    objects_probe: Optional[Sequence[Dict[str, Any]]],
    mapped_candidate_labels: Optional[Sequence[str]],
    image_width: Optional[int],
    image_height: Optional[int],
    max_candidates: int = 5,
) -> SpatialExpressionResult:
    label = (focus_target_label or "").strip() or None
    w = int(image_width) if isinstance(image_width, (int, float)) and image_width else None
    h = int(image_height) if isinstance(image_height, (int, float)) and image_height else None

    if not w or not h:
        return SpatialExpressionResult(
            focus_target_label=label,
            candidate_count=0,
            candidates=[],
            sidecar_reason="missing_image_dimensions",
        )

    mapped = [str(x) for x in (mapped_candidate_labels or []) if str(x).strip()]
    mapped_set = set(mapped)

    # candidate pool: main then probe (keep order, but tag source_mode)
    pool: List[Tuple[Dict[str, Any], str]] = []
    for o in (objects_main or []):
        if isinstance(o, dict):
            pool.append((o, "main"))
    for o in (objects_probe or []):
        if isinstance(o, dict):
            pool.append((o, "probe"))

    def _cand_key(item: Tuple[Dict[str, Any], str]) -> Tuple[int, float]:
        o, _src = item
        lab = (o.get("label") or o.get("class") or "").strip()
        conf = float(o.get("confidence") or 0.0)
        is_mapped = 1 if (lab in mapped_set) else 0
        return (-is_mapped, -conf)

    # prioritize mapped target candidates, then confidence
    pool_sorted = sorted(pool, key=_cand_key)
    chosen = pool_sorted[: max(1, int(max_candidates))]

    candidates: List[SpatialExpressionCandidate] = []
    focus_expr: Optional[str] = None
    focus_dbg: Optional[str] = None

    for o, src in chosen:
        lab = (o.get("label") or o.get("class") or "").strip() or "unknown"
        bbox = _xyxy(o.get("bbox"))
        if not bbox:
            continue
        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        x_norm = _clamp01(cx / float(w))
        y_norm = _clamp01(cy / float(h))
        hb, vb = _bands_from_norm(x_norm, y_norm)
        bearing, sector = _bearing_and_sector(x_norm)
        human = _human_location(hb, vb)
        debug = _debug_location(sector, bearing, x_norm, y_norm, hb, vb)
        is_focus = bool(lab in mapped_set) if mapped_set else False
        source_mode = "mapped_target" if is_focus else src
        c = SpatialExpressionCandidate(
            candidate_label=lab,
            candidate_confidence=o.get("confidence"),
            candidate_bbox_center_x_norm=x_norm,
            candidate_bbox_center_y_norm=y_norm,
            candidate_sector=sector,
            candidate_relative_bearing_deg=bearing,
            candidate_horizontal_band=hb,
            candidate_vertical_band=vb,
            candidate_human_location_text=human,
            candidate_debug_location_text=debug,
            candidate_is_focus_target=is_focus,
            candidate_source_mode=source_mode,
        )
        candidates.append(c)
        if is_focus and focus_expr is None:
            focus_expr = human
            focus_dbg = debug

    reason = "ok"
    if label and not mapped_set:
        reason = "no_mapped_candidate_labels"
    elif label and mapped_set and focus_expr is None:
        reason = "mapped_labels_not_in_topk"

    return SpatialExpressionResult(
        focus_target_label=label,
        focus_target_expression=focus_expr,
        focus_target_debug_expression=focus_dbg,
        candidate_count=len(candidates),
        candidates=candidates,
        sidecar_reason=reason,
    )


# ---------- Level 2 口语化行动表达 M0（近场/桌面试点） ----------
def _container_display_l2(name: Optional[str]) -> str:
    if not (name or "").strip():
        return "容器"
    c = (name or "").strip().lower()
    return {"cup": "杯子", "bottle": "瓶子", "bowl": "碗"}.get(c, c)


def build_focus_target_actionable_expression(
    sidecar: SpatialExpressionResult,
    search_interaction: Any,
    object_temporal_ledger: Any,
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    基于 sidecar（Level 1）+ search_interaction + object_ledger 生成 Level 2 口语化行动表达。
    返回 (actionable_expression, debug_reason, zone_override, next_step_override)。
    仅近场/桌面场景；不生成厘米/距离；不反写底层主事实。
    """
    loc = (sidecar.focus_target_expression or "").strip() or None
    if not loc:
        return None, None, None, None

    flow_type = _get(search_interaction, "interaction_flow_type")
    action = _get(search_interaction, "interaction_action")
    entry = _get(object_temporal_ledger, "focus_object_entry")
    container_candidate = _get(entry, "current_container_candidate") if entry else None
    container_name = _container_display_l2(container_candidate) if container_candidate else None

    # 取 focus 候选的 band（第一个 is_focus_target 的 candidate）
    focus_cand = None
    for c in getattr(sidecar, "candidates", []) or []:
        if getattr(c, "candidate_is_focus_target", False):
            focus_cand = c
            break
    vb = getattr(focus_cand, "candidate_vertical_band", None) if focus_cand else None
    hb = getattr(focus_cand, "candidate_horizontal_band", None) if focus_cand else None

    actionable: Optional[str] = None
    debug_reason: Optional[str] = None
    next_step_override: Optional[str] = None

    # C. 遮挡流
    if flow_type == "occlusion_clear_flow" or action == "ask_user_to_clear_occlusion":
        actionable = f"在{loc}的位置，可能被挡住了"
        debug_reason = "occlusion_clear_flow;near_field"
        next_step_override = f"{loc}可能被挡住了，先把遮挡移开看看；若仍未发现，再检查容器或口袋"
    # B. 容器候选
    elif container_candidate and (action in ("ask_user_to_open_container", "ask_if_in_container") or flow_type == "container_check_flow"):
        actionable = f"在{loc}那个{container_name}里"
        debug_reason = "container_candidate;near_field"
        next_step_override = f"先看{loc}那个{container_name}里；若未找到，再回到最后可信位置或继续查找"
    # A. 桌面/平面（近场前侧）
    elif vb == "front":
        if hb == "left":
            actionable = "在你左边桌子上"
        elif hb == "right":
            actionable = "在你右边桌子上"
        elif hb == "mid_left":
            actionable = "在桌面中间偏左"
        elif hb == "mid_right":
            actionable = "在桌面中间偏右"
        elif hb == "mid":
            actionable = "在桌面中间"
        else:
            actionable = f"在{loc}的桌面上"
        debug_reason = "desk_front;vertical_band=front"
        if not next_step_override and action in ("report_candidate_location", "continue_search_with_recheck"):
            next_step_override = f"在你前面不远的地方，靠近一点就能看到"
    # D. 近场一般（无容器、非遮挡）
    elif vb in ("mid", "back") or vb is None:
        actionable = f"在{loc}的位置"
        debug_reason = "near_field_general"
        if action in ("report_candidate_location", "ask_last_location") and not next_step_override:
            next_step_override = f"目标大致在{loc}，靠近一点就能看到"
    # E. 回退：不生成 Level 2，返回 None 保留 Level 1
    else:
        actionable = None
        debug_reason = None

    if actionable:
        return actionable, debug_reason or "near_field", actionable, next_step_override
    return None, None, None, None

