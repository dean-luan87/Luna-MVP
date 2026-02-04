#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量自动测试执行器
- 按 keyword 扫描本地图片
- 调用 Luna 场景描述
- 自动判定是否匹配
- 输出统计指标 + 错误聚类
"""

import os
import base64
import requests
import logging

from backend.local_image_loader import LocalImageLoader
from backend.auto_test_judger import AutoTestJudger

logger = logging.getLogger(__name__)


class AutoTestRunner:
    """
    批量自动测试执行器
    - 按 keyword 扫描本地图片
    - 调用 Luna 场景描述
    - 自动判定是否匹配
    - 输出统计指标 + 错误聚类
    """

    def __init__(self, base_dir=None):
        # 支持多个目录：优先 downloads/，其次 test_images/
        self.base_dir = base_dir
        self.downloads_dir = "downloads"
        self.test_images_dir = LocalImageLoader.BASE_DIR

    def _list_files(self, keyword):
        """从多个目录查找图片：优先 downloads/，其次 test_images/"""
        files = []
        
        # 1. 优先从 downloads/ 目录查找（V6.1 自动下载的图片）
        downloads_folder = os.path.join(self.downloads_dir, keyword)
        if os.path.exists(downloads_folder):
            files.extend([
                os.path.join(downloads_folder, f)
                for f in os.listdir(downloads_folder)
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ])
        
        # 2. 如果 downloads/ 没有，从 test_images/ 查找（V2-V6 本地图库）
        if not files:
            test_images_folder = os.path.join(self.test_images_dir, keyword)
            if os.path.exists(test_images_folder):
                files.extend([
                    os.path.join(test_images_folder, f)
                    for f in os.listdir(test_images_folder)
                    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
                ])
        
        # 3. 如果指定了 base_dir，也查找
        if not files and self.base_dir:
            custom_folder = os.path.join(self.base_dir, keyword)
            if os.path.exists(custom_folder):
                files.extend([
                    os.path.join(custom_folder, f)
                    for f in os.listdir(custom_folder)
                    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
                ])
        
        return files

    def _describe_image(self, image_bytes):
        img_b64 = base64.b64encode(image_bytes).decode("utf-8")

        try:
            resp = requests.post(
                "http://localhost:9001/api/navigation/describe_scene",
                json={"image_base64": img_b64},
                timeout=10
            )
            data = resp.json()
            if data.get("success") and data.get("data"):
                desc = data.get("data", {}).get("short_description", "") or data.get("data", {}).get("description", "")
            else:
                desc = ""
            return desc, img_b64
        except Exception as e:
            logger.warning(f"描述图片失败: {e}")
            return "", img_b64

    def run_batch(self, keywords, max_per_keyword=None):
        """
        :param keywords: 需要测试的 keyword 列表
        :param max_per_keyword: 每个 keyword 最多测试多少张（None 表示全量）
        :return: 统计结果 dict
        """
        results = []  # 每张图片的结果

        for kw in keywords:
            files = self._list_files(kw)
            if not files:
                continue

            if max_per_keyword is not None:
                files = files[:max_per_keyword]

            for path in files:
                try:
                    with open(path, "rb") as f:
                        img_bytes = f.read()
                except Exception as e:
                    logger.warning(f"读取图片失败 {path}: {e}")
                    continue

                desc, img_b64 = self._describe_image(img_bytes)
                match, hit_word = AutoTestJudger.judge(kw, desc)

                results.append({
                    "keyword": kw,
                    "file": os.path.basename(path),
                    "description": desc,
                    "match": match,
                    "hit": hit_word,
                    "image_base64": img_b64
                })

        # ---- 统计指标 ----
        summary = self._build_summary(results)
        clusters = self._build_error_clusters(results)

        return {
            "summary": summary,
            "error_clusters": clusters,
            "samples": results
        }

    def _build_summary(self, results):
        total = len(results)
        if total == 0:
            return {
                "total": 0,
                "matched": 0,
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "per_keyword": {}
            }

        matched = sum(1 for r in results if r["match"])

        # 这里我们只有"该 keyword 是否被描述到"这一个维度，
        # 精确率 / 召回率本质上和准确率相同，先简化为相同值。
        acc = matched / total if total > 0 else 0.0

        per_keyword = {}
        for r in results:
            kw = r["keyword"]
            if kw not in per_keyword:
                per_keyword[kw] = {"total": 0, "matched": 0}
            per_keyword[kw]["total"] += 1
            if r["match"]:
                per_keyword[kw]["matched"] += 1

        for kw, v in per_keyword.items():
            v["accuracy"] = v["matched"] / v["total"] if v["total"] > 0 else 0.0

        return {
            "total": total,
            "matched": matched,
            "accuracy": acc,
            "precision": acc,
            "recall": acc,
            "f1": acc,
            "per_keyword": per_keyword
        }

    def _build_error_clusters(self, results, max_examples=5):
        """
        简单错误聚类：
        - 按 keyword 聚类
        - 每类取若干示例
        """
        clusters = {}

        for r in results:
            if r["match"]:
                continue
            kw = r["keyword"]
            if kw not in clusters:
                clusters[kw] = {
                    "keyword": kw,
                    "count": 0,
                    "examples": []
                }
            c = clusters[kw]
            c["count"] += 1
            if len(c["examples"]) < max_examples:
                c["examples"].append({
                    "file": r["file"],
                    "description": r["description"]
                })

        return list(clusters.values())

