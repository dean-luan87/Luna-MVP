#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云端视觉适配器（OpenAI 等）
"""

import base64
import logging
import json
import requests
from typing import Dict, Any, List, Optional
from config.vision_fusion_config import VisionFusionConfig

logger = logging.getLogger(__name__)


class CloudVisionAdapter:
    """
    云端视觉适配器（OpenAI 等）：
    - 输入：base64 图像 + 可选任务说明
    - 输出：统一结构：
        {
          "raw_description": str,
          "labels": [str, ...],
          "places": [str, ...],
          "objects": [str, ...],
          "confidence": float (0~1)
        }
    """

    def __init__(self):
        self.api_key = VisionFusionConfig.OPENAI_API_KEY
        self.base_url = VisionFusionConfig.OPENAI_BASE_URL
        self.model = VisionFusionConfig.CLOUD_VISION_MODEL

        if not self.api_key:
            logger.warning("⚠️ CloudVisionAdapter: OPENAI_API_KEY 未配置，云端视觉将不可用")

    def is_available(self) -> bool:
        return bool(self.api_key and VisionFusionConfig.ENABLE_CLOUD_VISION)

    def describe_scene(self, image_base64: str, task_hint: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        调用云端模型生成场景描述

        :param image_base64: 不带 'data:image/...' 前缀的纯 base64
        :param task_hint: 可选任务提示（如 '导航安全'）
        """
        if not self.is_available():
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # 只保留纯 base64 内容
            if "," in image_base64:
                image_base64 = image_base64.split(",", 1)[1]

            prompt = (
                "你是盲人辅助系统的视觉解释助手。"
                "请用简洁的中文描述画面中与行走安全、障碍物、道路结构、楼梯、电梯、门、交通设施等相关的信息。"
            )
            if task_hint:
                prompt += f" 当前任务是：{task_hint}。"

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 512,
            }

            url = f"{self.base_url}/chat/completions"
            resp = requests.post(url, headers=headers, data=json.dumps(payload),
                                 timeout=VisionFusionConfig.CLOUD_TIMEOUT_SEC)

            if resp.status_code != 200:
                logger.warning(f"⚠️ CloudVisionAdapter: HTTP {resp.status_code}: {resp.text[:200]}")
                return None

            data = resp.json()
            content = data["choices"][0]["message"]["content"]

            # 这里先简单处理：后续可以引导模型输出 JSON 再解析
            raw_desc = content.strip()

            # 简单关键词抽取（可以后续升级为正则/LLM解析）
            keywords = []
            for kw in ["楼梯", "台阶", "扶梯", "电梯", "斑马线", "红绿灯",
                       "人行道", "马路", "车道", "地铁", "公交站", "施工", "围挡", "坑"]:
                if kw in raw_desc:
                    keywords.append(kw)

            return {
                "raw_description": raw_desc,
                "labels": keywords,
                "places": [],
                "objects": [],
                "confidence": 0.8 if keywords else 0.6
            }
        except Exception as e:
            logger.warning(f"⚠️ CloudVisionAdapter 调用失败: {e}")
            return None

