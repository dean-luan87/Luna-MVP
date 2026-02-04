#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错判自动聚类模块
用于训练数据整理和错误模式分析
"""

import logging
from typing import List, Dict, Any
from collections import defaultdict

logger = logging.getLogger(__name__)

try:
    from sklearn.cluster import KMeans
    import numpy as np
    SKLEARN_AVAILABLE = True
except (ImportError, ValueError, AttributeError) as e:
    SKLEARN_AVAILABLE = False
    logger.warning(f"sklearn 不可用，聚类功能将使用简化版本。原因: {type(e).__name__}")


class ClusterEngine:
    """错判自动聚类模块"""
    
    def __init__(self):
        self.available = SKLEARN_AVAILABLE
    
    def extract_features(self, error_samples: List[Dict[str, Any]]) -> List[List[float]]:
        """
        从错误样本中提取特征
        
        Args:
            error_samples: 错误样本列表，每个样本包含检测结果、OCR 结果等
        
        Returns:
            特征向量列表
        """
        features = []
        
        for sample in error_samples:
            # 特征1: 检测到的标签数量
            detections = sample.get("detections", [])
            num_detections = len(detections)
            
            # 特征2: 漏检数量
            missing = sample.get("missing", [])
            num_missing = len(missing)
            
            # 特征3: 错检数量
            extra = sample.get("extra", [])
            num_extra = len(extra)
            
            # 特征4: OCR 文字数量
            ocr_texts = sample.get("ocr_texts", [])
            num_ocr = len(ocr_texts)
            
            # 特征5: 准确率
            accuracy = sample.get("accuracy", 0.0)
            
            features.append([
                float(num_detections),
                float(num_missing),
                float(num_extra),
                float(num_ocr),
                float(accuracy)
            ])
        
        return features
    
    def cluster(self, error_samples: List[Dict[str, Any]], n_clusters: int = 3) -> Dict[str, Any]:
        """
        对错误样本进行聚类
        
        Args:
            error_samples: 错误样本列表
            n_clusters: 聚类数量
        
        Returns:
            {
                "labels": [0, 1, 0, 2, ...],  # 每个样本的聚类标签
                "centers": [[...], [...], [...]],  # 聚类中心
                "clusters": [  # 按聚类分组的样本
                    {
                        "cluster_id": 0,
                        "count": 5,
                        "samples": [...]
                    }
                ]
            }
        """
        if len(error_samples) < n_clusters:
            # 样本太少，直接返回
            labels = [0] * len(error_samples)
            return {
                "labels": labels,
                "centers": [],
                "clusters": [{"cluster_id": 0, "count": len(error_samples), "samples": error_samples}]
            }
        
        if not self.available:
            # 使用简化版本：按错误类型分组
            return self._simple_cluster(error_samples)
        
        try:
            # 提取特征
            features = self.extract_features(error_samples)
            
            if len(features) == 0:
                return {"labels": [], "centers": [], "clusters": []}
            
            # KMeans 聚类
            kmeans = KMeans(n_clusters=min(n_clusters, len(features)), random_state=0)
            labels = kmeans.fit_predict(np.array(features))
            
            # 按聚类分组
            clusters = defaultdict(list)
            for i, label in enumerate(labels):
                clusters[int(label)].append(error_samples[i])
            
            # 格式化结果
            cluster_list = []
            for cluster_id, samples in clusters.items():
                cluster_list.append({
                    "cluster_id": cluster_id,
                    "count": len(samples),
                    "samples": samples[:5]  # 只保留前5个示例
                })
            
            return {
                "labels": labels.tolist(),
                "centers": kmeans.cluster_centers_.tolist(),
                "clusters": cluster_list
            }
        except Exception as e:
            logger.warning(f"KMeans 聚类失败，使用简化版本: {e}")
            return self._simple_cluster(error_samples)
    
    def _simple_cluster(self, error_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        简化版聚类：按错误类型分组
        """
        clusters = defaultdict(list)
        
        for sample in error_samples:
            # 根据错误类型分组
            missing = sample.get("missing", [])
            extra = sample.get("extra", [])
            
            if len(missing) > 0 and len(extra) == 0:
                cluster_key = "missing_only"
            elif len(extra) > 0 and len(missing) == 0:
                cluster_key = "extra_only"
            else:
                cluster_key = "mixed"
            
            clusters[cluster_key].append(sample)
        
        # 转换为列表
        cluster_list = []
        for idx, (key, samples) in enumerate(clusters.items()):
            cluster_list.append({
                "cluster_id": idx,
                "type": key,
                "count": len(samples),
                "samples": samples[:5]
            })
        
        labels = []
        for sample in error_samples:
            missing = sample.get("missing", [])
            extra = sample.get("extra", [])
            if len(missing) > 0 and len(extra) == 0:
                labels.append(0)
            elif len(extra) > 0 and len(missing) == 0:
                labels.append(1)
            else:
                labels.append(2)
        
        return {
            "labels": labels,
            "centers": [],
            "clusters": cluster_list
        }

