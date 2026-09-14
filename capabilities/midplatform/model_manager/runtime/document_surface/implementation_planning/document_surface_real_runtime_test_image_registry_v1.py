# -*- coding: utf-8 -*-
"""Document Surface — test image registry plan v1."""

from __future__ import annotations

from typing import Any, Dict, List

TEST_IMAGE_CATEGORIES: List[Dict[str, Any]] = [
    {"category_id": "single_flat_paper", "description": "单张平放纸张", "real_images_required": False},
    {"category_id": "two_overlapping_papers", "description": "两张叠放纸张", "real_images_required": False},
    {"category_id": "multi_stack_documents", "description": "多文档堆叠", "real_images_required": False},
    {"category_id": "folded_or_curved_paper", "description": "折角或弯曲纸张", "real_images_required": False},
    {"category_id": "receipt_attached_to_package", "description": "票据贴附包装", "real_images_required": False},
    {"category_id": "menu_on_table", "description": "桌面菜单/宣传单", "real_images_required": False},
    {"category_id": "document_on_screen", "description": "屏幕显示文档", "real_images_required": False},
    {"category_id": "low_contrast_paper_on_desk", "description": "低对比度纸张", "real_images_required": False},
    {"category_id": "reflective_glass_with_paper_like_shape", "description": "反光玻璃纸形误检", "real_images_required": False},
    {"category_id": "background_texture_false_positive", "description": "背景纹理假阳性", "real_images_required": False},
]


def build_test_image_registry_plan() -> Dict[str, Any]:
    return {
        "registry_id": "document_surface_test_image_registry_plan_v1",
        "category_count": len(TEST_IMAGE_CATEGORIES),
        "categories": TEST_IMAGE_CATEGORIES,
        "real_image_benchmark_not_started": True,
        "real_images_attached": False,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
    }
