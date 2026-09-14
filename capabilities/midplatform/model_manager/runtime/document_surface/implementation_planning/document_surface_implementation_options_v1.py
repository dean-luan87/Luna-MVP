# -*- coding: utf-8 -*-
"""Document Surface — implementation options v1."""

from __future__ import annotations

from typing import Any, Dict, List

RUNTIME_ID = "document_surface_detector_v1"
FIRST_REAL_IMPLEMENTATION_CANDIDATE = "option_a_classical_cv_boundary"

IMPLEMENTATION_OPTIONS: List[Dict[str, Any]] = [
    {
        "option_id": "option_a_classical_cv_boundary",
        "label": "Classical CV Document Boundary Detector",
        "description": "基于边缘/轮廓/四边形/透视几何的轻量边界检测（规划描述，不执行）",
        "pros": ["轻量", "可控", "无重量模型依赖", "适合纸张/票据边界", "deterministic baseline"],
        "cons": ["复杂遮挡弱", "低对比弱", "弯折纸张弱"],
        "status": "first_real_implementation_candidate",
        "triggers_ocr": False,
        "triggers_vlm": False,
        "candidate_only": True,
    },
    {
        "option_id": "option_b_lightweight_segmentation",
        "label": "Lightweight Segmentation / Surface Detector",
        "description": "轻量分割模型或可替换 segmentation provider",
        "pros": ["非规则边界更强"],
        "cons": ["依赖模型", "边界治理复杂"],
        "status": "deferred",
        "triggers_ocr": False,
        "triggers_vlm": False,
        "candidate_only": True,
    },
    {
        "option_id": "option_c_layout_document_ai",
        "label": "Layout / Document AI Detector",
        "description": "从文档结构检测迁移，限制为 surface candidate",
        "pros": ["文档区域理解强"],
        "cons": ["易越界 layout semantic / document understanding"],
        "status": "deferred",
        "constraints": ["surface_candidate_only", "no_layout_fact"],
        "triggers_ocr": False,
        "triggers_vlm": False,
        "candidate_only": True,
    },
    {
        "option_id": "option_d_vlm_teacher_assisted",
        "label": "VLM / Teacher Assisted Detection",
        "description": "仅 fallback planning 或 teacher evidence",
        "pros": ["复杂场景辅助证据"],
        "cons": ["不得作为第一真实 runtime", "不得替代 detector"],
        "status": "deferred",
        "constraints": ["not_first_runtime", "teacher_evidence_only", "no_fact_output"],
        "triggers_ocr": False,
        "triggers_vlm": True,
        "candidate_only": True,
    },
]


def evaluate_implementation_options() -> Dict[str, Any]:
    """评估 4 类实现路径，推荐 Option A。"""
    deferred = [o for o in IMPLEMENTATION_OPTIONS if o.get("status") == "deferred"]
    first = next(o for o in IMPLEMENTATION_OPTIONS if o.get("option_id") == FIRST_REAL_IMPLEMENTATION_CANDIDATE)
    return {
        "runtime_id": RUNTIME_ID,
        "options_evaluated_count": len(IMPLEMENTATION_OPTIONS),
        "options": IMPLEMENTATION_OPTIONS,
        "first_real_implementation_candidate": FIRST_REAL_IMPLEMENTATION_CANDIDATE,
        "first_candidate_detail": first,
        "deferred_candidates": [o["option_id"] for o in deferred],
        "vlm_not_first_runtime": all(
            o.get("option_id") != "option_d_vlm_teacher_assisted" or o.get("status") == "deferred"
            for o in IMPLEMENTATION_OPTIONS
        ),
        "no_model_execution": True,
        "candidate_only": True,
        "not_fact": True,
    }
