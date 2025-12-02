#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场景描述服务：基于 SceneDescriptionEngine 的结果，拼接可读中文描述
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SceneDescribeService:
    def __init__(self, scene_engine):
        """
        scene_engine: SceneDescriptionEngine 实例
        """
        self.scene_engine = scene_engine

    def describe_scene_from_image(self, image_np) -> Dict[str, Any]:
        """
        高层入口：
        1) 调用 SceneDescriptionEngine.analyze_scene
        2) 基于结构化结果生成多层描述
        返回结构示例：
        {
          "scene_tags": [...],
          "scene_type": "hospital_hall",
          "short_description": "你现在大概在医院挂号大厅附近。",
          "details": [
             "前方有一个服务台，周围有多人排队。",
             "附近检测到一些标识牌，例如：挂号、收费、候诊区。",
             ...
          ],
          "elements": {... 原始结构化信息 ...}
        }
        """
        raw = self.scene_engine.analyze_scene(image_np)
        tags = raw.get("scene_tags") or []

        scene_type = self._infer_scene_type(tags)
        short_desc = self._build_short_desc(scene_type, raw)
        detail_lines = self._build_detail_lines(scene_type, raw)

        return {
            "scene_tags": tags,
            "scene_type": scene_type,
            "short_description": short_desc,
            "details": detail_lines,
            "elements": raw,
        }

    # ======= 内部逻辑 =======

    def _infer_scene_type(self, tags: List[str]) -> str:
        """把 tags 粗略归类为一个 scene_type，方便前端显示"""

        # 优先级顺序：医院 > 地铁 > 商场 > 洗手间 > 走廊 > 大厅 > 室外 > 室内 > unknown
        if "hospital" in tags:
            return "hospital_area"
        if "metro" in tags:
            return "metro_area"
        if "mall" in tags:
            return "mall_area"
        if "restroom" in tags:
            return "restroom_area"
        if "corridor" in tags:
            return "corridor"
        if "hall" in tags:
            return "hall"
        if "outdoor" in tags and "indoor" not in tags:
            return "outdoor"
        if "indoor" in tags and "outdoor" not in tags:
            return "indoor"

        return "unknown"

    def _build_short_desc(self, scene_type: str, raw: Dict[str, Any]) -> str:
        """一句话概述，尽量贴近期望的生活场景"""

        base = raw.get("quick_summary") or ""

        if scene_type == "hospital_area":
            if base:
                return base.replace("医院环境附近", "医院相关区域，可能是挂号大厅、候诊区或走廊")
            return "你现在大概率在医院相关区域，可能是挂号大厅、候诊区或走廊。"
        if scene_type == "metro_area":
            return "你现在大概率在地铁站附近，可能是站厅或站台区域。"
        if scene_type == "mall_area":
            return "你现在大概在商场或超市附近，周围可能有货架和收银台。"
        if scene_type == "restroom_area":
            return "附近应该有洗手间或卫生间入口。"
        if scene_type == "corridor":
            return "你现在大概在一条走廊或通道里。"
        if scene_type == "hall":
            return "你现在可能位于大厅或比较开阔的室内空间。"
        if scene_type == "outdoor":
            return "你现在大概率在户外，比如人行道、广场或路边环境。"
        if scene_type == "indoor":
            return "你现在更像是在室内环境里。"

        return base or "我已经识别了当前画面，可以帮你描述更具体的环境情况。"

    def _build_detail_lines(self, scene_type: str, raw: Dict[str, Any]) -> List[str]:
        """生成若干行更细的描述，方便播报或展示"""

        lines: List[str] = []

        # 1) 危险 & 台阶
        hazards = raw.get("hazards") or []
        step = raw.get("step")
        crowd = raw.get("crowd")

        if hazards:
            lines.append(f"画面中检测到 {len(hazards)} 处可能的危险区域，我会提醒你注意安全。")

        if step:
            direction = step.get("direction") or ""
            distance = step.get("distance")
            if distance is not None:
                lines.append(f"前方大约 {distance:.1f} 米处有台阶（{direction or '未知方向'}），请注意脚下。")
            else:
                lines.append("前方存在台阶或高度落差，请注意脚下。")

        if crowd and isinstance(crowd, dict):
            level = crowd.get("level") or crowd.get("density_level") or ""
            desc = crowd.get("description") or ""
            if level or desc:
                lines.append(f"人群密度检测：{desc or level}。")

        # 2) 标识牌 & 文字
        texts_join = self._collect_some_texts(raw)
        if texts_join:
            lines.append(f"我能看到一些文字或标识，例如：{texts_join}。")

        # 3) 医院 / 商场 / 地铁 / 洗手间特化一点
        if scene_type == "hospital_area":
            lines.append("如果你是来就医的，可以留意挂号窗口、取号机或咨询台的位置。")
        elif scene_type == "metro_area":
            lines.append("如果你在找地铁方向，我可以根据站内指示牌帮你判断进站口或站台方向。")
        elif scene_type == "mall_area":
            lines.append("周围可能有收银台、货架或门店招牌，如果你需要找某家店，我可以帮你一起找。")
        elif scene_type == "restroom_area":
            lines.append("如果你在找洗手间，可以顺着写有“卫生间 / WC / Restroom”的方向前进。")

        # 4) 默认兜底
        if not lines:
            lines.append("目前画面信息有限，如果你告诉我你想找什么，我可以结合视觉一起帮你判断。")

        return lines

    def _collect_some_texts(self, raw: Dict[str, Any], max_items: int = 3) -> str:
        """从 OCR + 标识牌里取几条有代表性的文字，避免太长"""
        candidates: List[str] = []

        for t in raw.get("texts") or []:
            if not isinstance(t, dict):
                continue
            txt = t.get("text") or t.get("content")
            if not txt:
                continue
            txt = str(txt).strip()
            if 1 <= len(txt) <= 12:  # 太长就不念了
                candidates.append(txt)
            if len(candidates) >= max_items:
                break

        if len(candidates) < max_items:
            for sb in raw.get("signboards") or []:
                if not isinstance(sb, dict):
                    continue
                label = sb.get("label") or sb.get("text")
                if not label:
                    continue
                label = str(label).strip()
                if 1 <= len(label) <= 12 and label not in candidates:
                    candidates.append(label)
                if len(candidates) >= max_items:
                    break

        return "、".join(candidates)


