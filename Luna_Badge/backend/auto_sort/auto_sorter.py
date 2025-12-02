#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动识别 + 分类引擎
从目录扫描图片 → 调用场景描述 → 按8大类别分类 → 复制到 auto_sorted/
"""

import os
import shutil
import logging
from typing import Dict, List, Any, Tuple
from PIL import Image
import io
import base64
import numpy as np
import cv2

logger = logging.getLogger(__name__)

# 8 大固定类别
CATEGORIES = [
    "人行道",
    "斑马线",
    "台阶",
    "地铁入口",
    "公交站牌",
    "电梯",
    "扶梯",
    "路口",
    "障碍物",
]

# 每个类别对应的一组关键词（在场景描述中命中就算匹配）
CATEGORY_RULES = {
    "人行道": ["人行道", "人行区域", "行人通道", "sidewalk", "步道", "盲道旁的人行道"],
    "斑马线": ["斑马线", "人行横道", "过马路", "zebra crossing"],
    "台阶": ["台阶", "阶梯", "楼梯", "台阶上", "台阶附近"],
    "地铁入口": ["地铁入口", "地铁站入口", "subway entrance", "metro entrance", "地铁出入口"],
    "公交站牌": ["公交站", "公交站牌", "bus stop", "公交车站"],
    "电梯": ["电梯门", "电梯口", "厢式电梯", "升降电梯", "elevator"],
    "扶梯": ["扶梯", "自动扶梯", "电动扶梯", "escalator"],
    "路口": ["路口", "十字路口", "交叉路口", "拐弯处", "intersection"],
    "障碍物": ["障碍", "路障", "施工围挡", "施工区域", "井盖", "坑洞", "堆放物", "障碍物"],
}


class AutoSortResult:
    """存储一次自动分类的统计结果"""

    def __init__(self):
        self.total = 0
        self.per_category = {c: 0 for c in CATEGORIES}
        self.unknown = 0
        self.errors: List[Dict[str, Any]] = []

    def to_dict(self):
        return {
            "total": self.total,
            "per_category": self.per_category,
            "unknown": self.unknown,
            "errors": self.errors,
        }


def _load_image_bytes(path: str) -> bytes:
    """加载图片为 bytes"""
    with open(path, "rb") as f:
        return f.read()


def _load_image_np(path: str) -> np.ndarray:
    """加载图片为 numpy array (OpenCV格式)"""
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"无法读取图片: {path}")
    return img


def _ensure_dir(path: str):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)


def _classify_by_description(desc: str) -> Tuple[str, str]:
    """
    根据描述文本匹配类别

    返回:
        (category, hit_word)
        category 为 "未知" 表示没有匹配到
    """
    if not desc:
        return "未知", ""

    desc_lower = desc.lower()

    for cat, words in CATEGORY_RULES.items():
        for w in words:
            if w.lower() in desc_lower:
                return cat, w
    return "未知", ""


class AutoSorter:
    """
    自动识别 + 分类引擎

    说明：
    - 不删除原图，只做复制
    - 默认输入目录为 test_images
    - 默认输出目录为 auto_sorted
    """

    def __init__(self, scene_description_engine=None):
        """
        scene_description_engine: 如果传入，则直接用；否则延迟导入 SceneDescriptionEngine 创建一个本地实例
        """
        self._engine = scene_description_engine
        self._inited_local_engine = False

    def _ensure_engine(self):
        """确保有可用的场景描述引擎"""
        if self._engine is not None:
            return

        if not self._inited_local_engine:
            try:
                # 尝试从 web_test_server 获取全局引擎
                from web_test_server import scene_description_engine
                if scene_description_engine is not None:
                    self._engine = scene_description_engine
                    logger.info("✅ AutoSorter 使用全局 SceneDescriptionEngine")
                    return
            except Exception:
                pass

            try:
                # 如果全局引擎不可用，尝试创建本地实例
                from backend.vision.scene_description_engine import SceneDescriptionEngine
                # 创建最小化实例（不依赖所有模块）
                self._engine = SceneDescriptionEngine()
                logger.info("✅ AutoSorter 本地 SceneDescriptionEngine 初始化成功")
            except Exception as e:
                logger.exception("❌ AutoSorter 初始化本地 SceneDescriptionEngine 失败: %s", e)
            finally:
                self._inited_local_engine = True

    def describe_image(self, img_path: str) -> str:
        """
        使用 SceneDescriptionEngine 输出一段场景描述文本
        """
        self._ensure_engine()
        if self._engine is None:
            logger.warning("⚠️ AutoSorter 没有可用的 SceneDescriptionEngine")
            return ""

        try:
            # 加载图片为 numpy array
            img_np = _load_image_np(img_path)
            
            # 调用 describe 方法
            result = self._engine.describe(img_np, nav_state=None)
            
            # 提取描述文本
            if isinstance(result, dict):
                # 优先使用 summary，其次 quick_summary，最后 description
                desc = result.get("summary") or result.get("quick_summary") or result.get("description") or ""
                return desc.strip()
            
            return str(result).strip()
        except Exception as e:
            logger.exception("❌ AutoSorter 描述图片失败: %s", img_path)
            return ""

    def scan_and_classify(
        self,
        input_dir: str = "test_images",
        output_dir: str = "auto_sorted",
    ) -> Dict[str, Any]:
        """
        核心入口：
        - 扫描 input_dir 下所有图片（递归）
        - 描述 → 分类 → 复制到 auto_sorted/类别名/
        - 返回统计结果
        """
        result = AutoSortResult()

        if not os.path.isdir(input_dir):
            logger.warning("AutoSorter: 输入目录不存在: %s", input_dir)
            return result.to_dict()

        _ensure_dir(output_dir)

        # 收集所有图片文件
        image_files = []
        for root, _, files in os.walk(input_dir):
            for name in files:
                if name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    image_files.append(os.path.join(root, name))

        logger.info(f"📂 AutoSorter: 找到 {len(image_files)} 张图片，开始分类...")

        for src_path in image_files:
            result.total += 1

            try:
                desc = self.describe_image(src_path)
                category, hit_word = _classify_by_description(desc)

                if category == "未知":
                    result.unknown += 1
                    dest_dir = os.path.join(output_dir, "未知")
                else:
                    result.per_category[category] = result.per_category.get(category, 0) + 1
                    dest_dir = os.path.join(output_dir, category)

                _ensure_dir(dest_dir)
                
                # 生成目标文件名（保持原文件名，如果重名则加序号）
                base_name = os.path.basename(src_path)
                dest_path = os.path.join(dest_dir, base_name)
                
                # 如果文件已存在，添加序号
                counter = 1
                while os.path.exists(dest_path):
                    name, ext = os.path.splitext(base_name)
                    dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
                    counter += 1

                # 不删除原图，只复制
                shutil.copy2(src_path, dest_path)

                logger.info(
                    "📂 AutoSorter: %s → %s  (类别: %s, 命中: %s, 描述: %s)",
                    os.path.basename(src_path),
                    category,
                    category,
                    hit_word,
                    (desc[:60] + "...") if len(desc) > 60 else desc,
                )

            except Exception as e:
                logger.exception("❌ AutoSorter 处理图片失败: %s", src_path)
                result.errors.append(
                    {
                        "path": src_path,
                        "error": str(e),
                    }
                )

        logger.info(f"✅ AutoSorter: 分类完成，总计 {result.total} 张，未知 {result.unknown} 张")
        return result.to_dict()


