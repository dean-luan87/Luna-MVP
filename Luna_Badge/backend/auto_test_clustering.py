#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误聚类分析（V6.1）
使用简单的文本特征进行聚类，无需复杂的 embedding
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
    logger.warning(f"sklearn 不可用，错误聚类功能将使用简化版本。原因: {e}")


class ErrorClustering:
    """
    错误样本聚类分析
    """
    
    def __init__(self):
        self.available = SKLEARN_AVAILABLE
    
    def cluster_errors(self, error_samples: List[Dict[str, Any]], n_clusters: int = 3) -> List[Dict[str, Any]]:
        """
        对错误样本进行聚类
        
        Args:
            error_samples: 错误样本列表，每个样本包含 keyword, description 等字段
            n_clusters: 聚类数量
        
        Returns:
            添加了 cluster 标签的样本列表
        """
        if len(error_samples) < n_clusters:
            # 样本太少，直接返回，每个样本 cluster=0
            for sample in error_samples:
                sample["cluster"] = 0
            return error_samples
        
        if not self.available:
            # 如果没有 sklearn，使用简单的关键词分组
            return self._simple_cluster(error_samples)
        
        try:
            # 提取特征：使用描述文本的长度和关键词匹配度作为特征
            features = []
            for sample in error_samples:
                desc = sample.get("description", "")
                keyword = sample.get("keyword", "")
                
                # 简单特征：描述长度、是否包含关键词、描述中的数字数量
                desc_len = len(desc)
                contains_keyword = 1 if keyword.lower() in desc.lower() else 0
                num_count = sum(1 for c in desc if c.isdigit())
                
                features.append([desc_len, contains_keyword, num_count])
            
            if len(features) == 0:
                return error_samples
            
            # KMeans 聚类
            kmeans = KMeans(n_clusters=min(n_clusters, len(features)), random_state=0)
            labels = kmeans.fit_predict(np.array(features))
            
            # 为每个样本添加 cluster 标签
            for i, sample in enumerate(error_samples):
                sample["cluster"] = int(labels[i])
            
            return error_samples
        except Exception as e:
            logger.warning(f"KMeans 聚类失败，使用简化版本: {e}")
            return self._simple_cluster(error_samples)
    
    def _simple_cluster(self, error_samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        简化版聚类：按关键词分组
        """
        keyword_groups = defaultdict(list)
        for i, sample in enumerate(error_samples):
            keyword = sample.get("keyword", "unknown")
            keyword_groups[keyword].append(i)
        
        cluster_id = 0
        for keyword, indices in keyword_groups.items():
            for idx in indices:
                error_samples[idx]["cluster"] = cluster_id
            cluster_id += 1
        
        return error_samples
    
    def get_cluster_summary(self, clustered_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成聚类摘要
        
        Returns:
            {
                "clusters": [
                    {
                        "cluster_id": 0,
                        "count": 5,
                        "keywords": ["医院挂号大厅", "地铁入口"],
                        "sample_descriptions": ["描述1", "描述2"]
                    }
                ]
            }
        """
        clusters = defaultdict(lambda: {
            "cluster_id": 0,
            "count": 0,
            "keywords": set(),
            "sample_descriptions": []
        })
        
        for sample in clustered_samples:
            cluster_id = sample.get("cluster", 0)
            clusters[cluster_id]["cluster_id"] = cluster_id
            clusters[cluster_id]["count"] += 1
            clusters[cluster_id]["keywords"].add(sample.get("keyword", "unknown"))
            desc = sample.get("description", "")
            if desc and len(clusters[cluster_id]["sample_descriptions"]) < 3:
                clusters[cluster_id]["sample_descriptions"].append(desc[:50])  # 截断前50字符
        
        # 转换为列表并格式化
        result = []
        for cluster_id, info in clusters.items():
            result.append({
                "cluster_id": cluster_id,
                "count": info["count"],
                "keywords": list(info["keywords"]),
                "sample_descriptions": info["sample_descriptions"]
            })
        
        return {"clusters": result}

