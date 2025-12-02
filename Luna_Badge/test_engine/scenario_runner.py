#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心执行器
这是整个 TestEngine 的大脑
"""

import json
import logging
import os
from typing import Dict, Any, Optional

from test_engine.image_fetcher import ImageFetcher
from test_engine.detector import Detector
from test_engine.ocr_reader import OCRReader
from test_engine.evaluator import Evaluator
from test_engine.cluster_engine import ClusterEngine
from test_engine.reporter import Reporter
from test_engine.dataset_manager import DatasetManager

logger = logging.getLogger(__name__)


class ScenarioRunner:
    """核心执行器"""
    
    def __init__(self, vision_engine=None):
        """
        初始化场景运行器
        
        Args:
            vision_engine: 现有的 vision_engine 实例（可选）
        """
        self.fetcher = ImageFetcher()
        self.detector = Detector(vision_engine=vision_engine)
        self.ocr = OCRReader(vision_engine=vision_engine)
        self.evaluator = Evaluator()
        self.cluster_engine = ClusterEngine()
        self.reporter = Reporter()
        self.dataset = DatasetManager()
        
        logger.info("ScenarioRunner 初始化完成")
    
    def run(self, scene_file: str, fetch_images: bool = True, 
            limit: int = 20, run_clustering: bool = True) -> Dict[str, Any]:
        """
        运行场景测试
        
        Args:
            scene_file: 场景配置文件路径（JSON）
            fetch_images: 是否自动搜图（如果为 False，则使用已有图片）
            limit: 每个关键词最多下载/测试多少张图片
            run_clustering: 是否运行错误聚类
        
        Returns:
            {
                "scene_name": "stairs",
                "total_images": 20,
                "results": [...],
                "summary": {...},
                "cluster_info": {...},
                "report": "...",
                "dataset_paths": {"json": "...", "csv": "..."}
            }
        """
        # 1. 加载场景配置
        try:
            with open(scene_file, "r", encoding="utf-8") as f:
                scene = json.load(f)
        except Exception as e:
            logger.error(f"加载场景配置失败: {e}")
            raise
        
        scene_name = scene.get("name", "unknown")
        keyword = scene.get("keyword", "")
        expected_labels = scene.get("expected_labels", [])
        
        logger.info(f"开始运行场景: {scene_name} (关键词: {keyword})")
        
        # 2. 搜图（如果需要）
        if fetch_images:
            logger.info(f"开始搜图: {keyword}")
            images = self.fetcher.fetch(keyword, limit=limit)
            if not images:
                logger.warning(f"未下载到图片，关键词: {keyword}")
                return {
                    "scene_name": scene_name,
                    "total_images": 0,
                    "results": [],
                    "error": "未下载到图片"
                }
        else:
            # 使用已有图片（从 test_engine/data/fetched/ 或 test_images/ 读取）
            import glob
            image_dir = os.path.join("test_engine", "data", "fetched", keyword)
            if not os.path.exists(image_dir):
                image_dir = os.path.join("test_images", keyword)
            
            images = []
            if os.path.exists(image_dir):
                images = glob.glob(os.path.join(image_dir, "*.jpg")) + \
                         glob.glob(os.path.join(image_dir, "*.png")) + \
                         glob.glob(os.path.join(image_dir, "*.webp"))
                images = images[:limit]
        
        logger.info(f"找到 {len(images)} 张图片")
        
        # 3. 批量检测和评估
        all_results = []
        
        for idx, img_path in enumerate(images):
            logger.info(f"处理图片 {idx+1}/{len(images)}: {img_path}")
            
            try:
                # 评估单张图片
                result = self.evaluator.evaluate_image(
                    img_path=img_path,
                    ground_truth=expected_labels,
                    detector=self.detector,
                    ocr_reader=self.ocr
                )
                all_results.append(result)
            except Exception as e:
                logger.error(f"处理图片失败 {img_path}: {e}")
                continue
        
        # 4. 错误聚类（如果需要）
        cluster_info = None
        if run_clustering and all_results:
            error_samples = [
                r for r in all_results 
                if len(r.get("missing", [])) > 0 or len(r.get("extra", [])) > 0
            ]
            if error_samples:
                logger.info(f"开始错误聚类，错误样本数: {len(error_samples)}")
                cluster_info = self.cluster_engine.cluster(error_samples, n_clusters=3)
        
        # 5. 生成报告
        report_text = self.reporter.generate(scene_name, all_results, cluster_info)
        
        # 6. 导出训练数据
        dataset_paths = self.dataset.export_both(all_results, scene_name)
        
        # 7. 保存报告
        report_path = self.reporter.save_report(report_text, scene_name)
        
        # 8. 计算总体统计
        total_images = len(all_results)
        if total_images > 0:
            avg_accuracy = sum(r.get("accuracy", 0.0) for r in all_results) / total_images
            avg_precision = sum(r.get("precision", 0.0) for r in all_results) / total_images
            avg_recall = sum(r.get("recall", 0.0) for r in all_results) / total_images
            avg_f1 = sum(r.get("f1", 0.0) for r in all_results) / total_images
        else:
            avg_accuracy = avg_precision = avg_recall = avg_f1 = 0.0
        
        summary = {
            "total_images": total_images,
            "avg_accuracy": avg_accuracy,
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_f1": avg_f1,
            "total_correct": sum(len(r.get("correct", [])) for r in all_results),
            "total_missing": sum(len(r.get("missing", [])) for r in all_results),
            "total_extra": sum(len(r.get("extra", [])) for r in all_results)
        }
        
        logger.info(f"场景测试完成: {scene_name}")
        logger.info(f"  总图片数: {total_images}")
        logger.info(f"  平均准确率: {avg_accuracy:.2%}")
        
        return {
            "scene_name": scene_name,
            "total_images": total_images,
            "results": all_results,
            "summary": summary,
            "cluster_info": cluster_info,
            "report": report_text,
            "report_path": report_path,
            "dataset_paths": dataset_paths
        }

