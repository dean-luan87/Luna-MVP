#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场景描述工具函数
统一调用场景描述接口的逻辑
"""

import base64
import logging
from typing import Optional, Tuple, Dict, Any

import requests

from config.auto_test_config import AutoTestConfig

logger = logging.getLogger(__name__)


def call_scene_description_api(
    image_base64: str,
    extra_payload: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    调用后端 /api/navigation/describe_scene 接口，返回 (描述文本, 原始返回 data)

    Args:
        image_base64: base64 编码的图片字符串
        extra_payload: 额外的请求参数（可选）

    Returns:
        (description, raw_data)
        - description: str 或 None
        - raw_data: dict 或 None
    """
    if not image_base64:
        logger.warning("[SceneDescHelper] 空的 image_base64")
        return None, None

    url = AutoTestConfig.SCENE_DESC_API_BASE_URL.rstrip("/") + AutoTestConfig.SCENE_DESC_API_PATH

    payload: Dict[str, Any] = {"image_base64": image_base64}
    if extra_payload:
        payload.update(extra_payload)

    try:
        resp = requests.post(url, json=payload, timeout=AutoTestConfig.HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error(f"[SceneDescHelper] 调用场景描述接口失败: {e}")
        return None, None

    if not isinstance(data, dict):
        logger.error("[SceneDescHelper] 场景描述返回格式异常（非 dict）")
        return None, None

    if not data.get("success", False):
        logger.warning(f"[SceneDescHelper] 场景描述接口返回失败: {data}")
        return None, data

    raw_data = data.get("data") or {}
    # 尝试多种可能的描述字段名
    description = (
        raw_data.get("description") or 
        raw_data.get("scene_description") or 
        raw_data.get("short_description") or
        raw_data.get("summary") or
        ""
    )
    description = description.strip()

    return (description or None), raw_data


def call_scene_description_engine_direct(
    image_np,
    scene_description_engine,
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    直接调用 scene_description_engine.describe 方法（用于内部调用，避免 HTTP 开销）

    Args:
        image_np: numpy array 图像
        scene_description_engine: SceneDescriptionEngine 实例

    Returns:
        (description, raw_data)
        - description: str 或 None
        - raw_data: dict 或 None
    """
    if scene_description_engine is None:
        logger.warning("[SceneDescHelper] scene_description_engine 未初始化")
        return None, None

    try:
        result = scene_description_engine.describe(image_np)
        if not isinstance(result, dict):
            logger.error("[SceneDescHelper] scene_description_engine.describe 返回格式异常")
            return None, None

        # 尝试多种可能的描述字段名
        description = (
            result.get("summary") or
            result.get("quick_summary") or
            result.get("description") or
            ""
        )

        # 如果没有描述，尝试从其他字段构建
        if not description:
            texts = result.get("texts", [])
            if texts:
                description = " ".join([t.get("text", "") for t in texts[:3]])

        description = description.strip()
        return (description or None), result

    except Exception as e:
        logger.error(f"[SceneDescHelper] 直接调用场景描述引擎失败: {e}")
        return None, None

