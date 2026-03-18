# -*- coding: utf-8 -*-
"""
静态图输入桥 + 候选审计 M0：Visual Candidate Audit。

从 detector / OCR / scene description 与 search_target 做最小审计，
输出 input_source、候选数量/标签、目标映射、candidate_audit_status。
不接入新视觉模型，不重构 detector/OCR 根逻辑。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# 最小 search_target -> 可接受 detector/OCR 标签映射（中英、别名）
# 真实视觉 M0：支持维生素/药瓶→bottle、手机→phone、杯子→cup、纸巾→tissue
_BOTTLE_LIKE = ["bottle", "bottle_like", "药瓶", "药", "维生素", "pill", "medicine", "vessel"]
SEARCH_TARGET_MAPPING: Dict[str, List[str]] = {
    "维生素药瓶": _BOTTLE_LIKE,
    "维生素": _BOTTLE_LIKE,
    "维生素瓶": _BOTTLE_LIKE,
    "药": _BOTTLE_LIKE,
    "药瓶": _BOTTLE_LIKE,
    "手机": ["phone", "cellphone", "cell phone", "mobile phone", "手机", "smartphone"],
    "杯子": ["cup", "mug", "杯子", "水杯", "马克杯", "glass"],
    "纸巾": ["tissue", "tissue pack", "paper", "纸巾", "paper towel"],
    "牙签": ["toothpick", "small box", "transparent box", "牙签", "牙签盒", "box"],
}

CANDIDATE_AUDIT_STATUSES = (
    "no_input",
    "no_visual_candidate",
    "weak_visual_candidate",
    "target_mapped",
    "target_unmapped",
)


@dataclass
class VisualCandidateAuditResult:
    """最小 Visual Candidate Audit 结果（M0）。真实视觉 M0 增加 detector_mode / detector_model_name。"""
    input_source_type: str  # camera / static_image / video_file / unknown
    input_source_path: Optional[str] = None
    detector_candidate_count: int = 0
    detector_candidate_labels: List[str] = field(default_factory=list)  # 最多前 10
    detector_probe_candidate_count: int = 0
    detector_probe_candidate_labels: List[str] = field(default_factory=list)  # probe(弱扫描) 最多前 10
    detector_mode: Optional[str] = None  # real_yolo | demo_fallback
    detector_model_name: Optional[str] = None  # 如 yolo11n
    ocr_candidate_count: int = 0
    ocr_texts: List[str] = field(default_factory=list)  # 最多前 10
    scene_description_present: bool = False
    search_target_label: Optional[str] = None
    mapped_candidate_labels: List[str] = field(default_factory=list)  # 与目标映射上的候选
    candidate_audit_status: str = "no_input"
    candidate_audit_reason: Optional[str] = None


def _norm(s: Optional[str]) -> str:
    return (s or "").strip().lower()


def _labels_from_objects(objects: Any) -> List[str]:
    """从 detector 结果提取标签；支持 YOLO 的 class / label。"""
    out: List[str] = []
    if not objects:
        return out
    for obj in objects[:10]:
        if isinstance(obj, dict):
            lab = obj.get("label") or obj.get("class") or obj.get("class_name") or obj.get("name")
        else:
            lab = getattr(obj, "label", None) or getattr(obj, "class", None) or getattr(obj, "class_name", None)
        if lab and str(lab).strip():
            out.append(str(lab).strip())
    return out


def _texts_from_texts(texts: Any) -> List[str]:
    out: List[str] = []
    if not texts:
        return out
    for t in texts[:10]:
        if isinstance(t, dict):
            x = t.get("text") or t.get("raw_text") or t.get("content")
        else:
            x = getattr(t, "text", None) or getattr(t, "raw_text", None)
        if x and str(x).strip():
            out.append(str(x).strip())
    return out


def _match_target_to_candidates(
    search_target_label: Optional[str],
    detector_labels: List[str],
    ocr_texts: List[str],
) -> Tuple[List[str], bool]:
    """返回 (mapped_candidate_labels, any_match)."""
    if not search_target_label:
        return [], False
    allowed = SEARCH_TARGET_MAPPING.get(search_target_label) or []
    if not allowed:
        allowed = [search_target_label]
    allowed_norm = [_norm(a) for a in allowed]
    mapped: List[str] = []
    for lab in detector_labels:
        if _norm(lab) in allowed_norm or any(_norm(lab) in a or a in _norm(lab) for a in allowed_norm):
            mapped.append(lab)
    for txt in ocr_texts:
        if _norm(txt) in allowed_norm or any(_norm(txt) in a or a in _norm(txt) for a in allowed_norm):
            mapped.append(txt)
    return mapped, len(mapped) > 0


def build_visual_candidate_audit(
    objects: Any,
    probe_objects: Any,
    texts: Any,
    description: Any,
    search_target_label: Optional[str],
    input_source_type: Optional[str],
    input_source_path: Optional[str],
    detector_mode: Optional[str] = None,
    detector_model_name: Optional[str] = None,
) -> VisualCandidateAuditResult:
    """
    从当前帧 detector/OCR/scene 结果与 search target 做最小审计。
    objects/texts 可为 list of dict 或 list of object；空则显式记 0/[]。
    真实视觉 M0：detector_mode/detector_model_name 用于区分真实 YOLO 与 demo_fallback。
    """
    input_source_type = input_source_type or "unknown"
    input_source_path = input_source_path or None
    detector_labels = _labels_from_objects(objects)
    probe_labels = _labels_from_objects(probe_objects)
    ocr_texts = _texts_from_texts(texts)
    detector_count = len(detector_labels)
    probe_count = len(probe_labels)
    ocr_count = len(ocr_texts)
    scene_present = bool(description and str(description).strip())
    search_target_label = (search_target_label or "").strip() or None
    # M0.7：弱候选扫描只用于 search/audit 映射，不污染主 detector_candidate_labels
    mapped, target_matched = _match_target_to_candidates(search_target_label, detector_labels + probe_labels, ocr_texts)

    if input_source_type == "unknown" and not input_source_path:
        status = "no_input"
        reason = "no valid input source or path"
    elif not detector_count and not ocr_count and not scene_present:
        status = "no_visual_candidate"
        reason = "detector/OCR/scene all empty"
    elif target_matched:
        status = "target_mapped"
        reason = f"at least one candidate matched search_target={search_target_label}"
    elif detector_count or ocr_count:
        status = "target_unmapped"
        reason = f"has candidates but no match for search_target={search_target_label or 'none'}"
    else:
        status = "weak_visual_candidate"
        reason = "only scene_description present, no object/OCR candidates"
    return VisualCandidateAuditResult(
        input_source_type=input_source_type,
        input_source_path=input_source_path,
        detector_candidate_count=detector_count,
        detector_candidate_labels=detector_labels,
        detector_probe_candidate_count=probe_count,
        detector_probe_candidate_labels=probe_labels,
        detector_mode=detector_mode,
        detector_model_name=detector_model_name,
        ocr_candidate_count=ocr_count,
        ocr_texts=ocr_texts,
        scene_description_present=scene_present,
        search_target_label=search_target_label,
        mapped_candidate_labels=mapped,
        candidate_audit_status=status,
        candidate_audit_reason=reason,
    )
