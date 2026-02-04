#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视觉融合引擎：融合本地 YOLO+OCR 和云端视觉结果
"""

import logging
from typing import Dict, Any, Optional
from config.vision_fusion_config import VisionFusionConfig

logger = logging.getLogger(__name__)


class SceneFusionEngine:
    """
    视觉融合引擎：
    - 把本地 YOLO+OCR 和 云端视觉结果融合
    - 只输出与"当前任务"相关的信息（导航 / 安全）
    """

    def __init__(self, local_adapter, cloud_adapter=None):
        self.local_adapter = local_adapter
        self.cloud_adapter = cloud_adapter

    def _local_quality(self, local_result: Dict[str, Any]) -> float:
        """简单评估本地识别质量，用于决定是否启用云端补强"""
        objs = local_result.get("objects", []) or []
        valid_objs = [o for o in objs if o.get("confidence", 0.0) >= VisionFusionConfig.MIN_LOCAL_CONFIDENCE]
        score = min(1.0, len(valid_objs) / max(1, VisionFusionConfig.MIN_LOCAL_OBJECTS))
        return score

    def fuse(
            self,
            image_np,
            image_base64: Optional[str] = None,
            task_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        返回统一的场景理解结果：
        {
          "description": str,
          "tags": [str, ...],
          "local": {...},
          "cloud": {... or None},
          "fusion_meta": {...}
        }
        """
        # 1. 本地分析
        local_result = self.local_adapter.analyze_image(image_np) if self.local_adapter else {
            "objects": [], "texts": [], "raw": None
        }

        local_quality = self._local_quality(local_result)
        use_cloud = (
            VisionFusionConfig.ENABLE_FUSION and
            self.cloud_adapter is not None and
            self.cloud_adapter.is_available() and
            (local_quality < 0.85 or not local_result.get("objects")) and
            image_base64 is not None
        )

        cloud_result = None
        if use_cloud:
            cloud_result = self.cloud_adapter.describe_scene(image_base64, task_hint=task_hint)

        # 2. 构造 tags
        tags = set()
        objects = local_result.get("objects", [])
        texts = local_result.get("texts", [])

        for o in objects:
            label = (o.get("label") or "").lower()
            if not label:
                continue
            # 这一步可以做映射 / 规范化
            tags.add(label)

        # 文本中提取常见地点词
        join_text = " ".join(texts)
        for kw in ["出口", "电梯", "扶梯", "地铁", "公交", "医院", "挂号", "服务台",
                   "厕所", "卫生间", "门诊", "商场", "超市", "停车场"]:
            if kw in join_text:
                tags.add(kw)

        cloud_desc = ""
        if cloud_result and cloud_result.get("raw_description"):
            cloud_desc = cloud_result["raw_description"]
            for kw in cloud_result.get("labels", []):
                tags.add(kw)

        # 3. 生成最终描述（优先云端 + 本地补充）
        parts = []

        # 云端主描述
        if cloud_desc:
            parts.append(cloud_desc)

        # 本地重要补充（如果云端没提到）
        # 只补充与导航 / 安全直接相关的关键词
        safe_keywords = [
            "stairs", "stair", "台阶", "楼梯",
            "escalator", "扶梯",
            "elevator", "电梯",
            "zebra", "斑马线",
            "traffic light", "红绿灯",
            "construction", "施工", "围挡", "路障",
            "pit", "坑", "井盖",
            "bus", "公交", "站台",
            "subway", "metro", "地铁"
        ]

        if objects:
            important_objs = []
            for o in objects:
                label = (o.get("label") or "").lower()
                if any(k in label for k in safe_keywords):
                    important_objs.append(o)

            if important_objs:
                desc_local_bits = []
                for o in important_objs:
                    desc_local_bits.append(o.get("label", ""))
                if desc_local_bits:
                    parts.append("本地检测到与安全相关的物体：" + "、".join(desc_local_bits))

        # 文本信息补充
        if texts:
            # 只取前几条关键文字
            preview = " / ".join(texts[:3])
            parts.append(f"画面中出现的文字提示包含：{preview}")

        # 如果啥也没有，就至少说一句"不太清楚"
        if not parts:
            parts.append("画面内容较难识别，没有发现明显的道路或障碍信息。")

        final_desc = "；".join(parts)

        fusion_meta = {
            "local_quality": local_quality,
            "cloud_used": bool(cloud_result),
        }

        return {
            "description": final_desc,
            "tags": list(tags),
            "local": local_result,
            "cloud": cloud_result,
            "fusion_meta": fusion_meta
        }


