#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试报告模块
用于生成场景级别的一次性报告
"""

import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class Reporter:
    """测试报告模块"""
    
    def generate(self, scene_name: str, results: List[Dict[str, Any]], 
                 cluster_info: Dict[str, Any] = None) -> str:
        """
        生成测试报告
        
        Args:
            scene_name: 场景名称
            results: 测试结果列表
            cluster_info: 聚类信息（可选）
        
        Returns:
            报告文本
        """
        if not results:
            return f"=== 测试场景: {scene_name} ===\n\n无测试结果\n"
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append(f"测试场景: {scene_name}")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # 总体统计
        total_images = len(results)
        total_correct = sum(len(r.get("correct", [])) for r in results)
        total_missing = sum(len(r.get("missing", [])) for r in results)
        total_extra = sum(len(r.get("extra", [])) for r in results)
        
        # 计算平均指标
        avg_accuracy = sum(r.get("accuracy", 0.0) for r in results) / total_images if total_images > 0 else 0.0
        avg_precision = sum(r.get("precision", 0.0) for r in results) / total_images if total_images > 0 else 0.0
        avg_recall = sum(r.get("recall", 0.0) for r in results) / total_images if total_images > 0 else 0.0
        avg_f1 = sum(r.get("f1", 0.0) for r in results) / total_images if total_images > 0 else 0.0
        
        report_lines.append("【总体统计】")
        report_lines.append(f"总图片数: {total_images}")
        report_lines.append(f"正确识别数: {total_correct}")
        report_lines.append(f"漏检数: {total_missing}")
        report_lines.append(f"错检数: {total_extra}")
        report_lines.append("")
        
        report_lines.append("【平均指标】")
        report_lines.append(f"准确率 (Accuracy): {avg_accuracy:.2%}")
        report_lines.append(f"精确率 (Precision): {avg_precision:.2%}")
        report_lines.append(f"召回率 (Recall): {avg_recall:.2%}")
        report_lines.append(f"F1 分数: {avg_f1:.2%}")
        report_lines.append("")
        
        # 错误样本统计
        error_samples = [r for r in results if len(r.get("missing", [])) > 0 or len(r.get("extra", [])) > 0]
        if error_samples:
            report_lines.append(f"【错误样本】")
            report_lines.append(f"错误样本数: {len(error_samples)} ({len(error_samples)/total_images:.1%})")
            report_lines.append("")
            
            # 最常见的漏检标签
            missing_tags = {}
            for r in error_samples:
                for tag in r.get("missing", []):
                    missing_tags[tag] = missing_tags.get(tag, 0) + 1
            
            if missing_tags:
                report_lines.append("最常见的漏检标签:")
                sorted_missing = sorted(missing_tags.items(), key=lambda x: x[1], reverse=True)
                for tag, count in sorted_missing[:5]:
                    report_lines.append(f"  - {tag}: {count} 次")
                report_lines.append("")
            
            # 最常见的错检标签
            extra_tags = {}
            for r in error_samples:
                for tag in r.get("extra", []):
                    extra_tags[tag] = extra_tags.get(tag, 0) + 1
            
            if extra_tags:
                report_lines.append("最常见的错检标签:")
                sorted_extra = sorted(extra_tags.items(), key=lambda x: x[1], reverse=True)
                for tag, count in sorted_extra[:5]:
                    report_lines.append(f"  - {tag}: {count} 次")
                report_lines.append("")
        
        # 聚类信息
        if cluster_info and cluster_info.get("clusters"):
            report_lines.append("【错误聚类分析】")
            clusters = cluster_info.get("clusters", [])
            report_lines.append(f"聚类数量: {len(clusters)}")
            for cluster in clusters:
                cluster_id = cluster.get("cluster_id", "?")
                count = cluster.get("count", 0)
                cluster_type = cluster.get("type", "")
                report_lines.append(f"  Cluster {cluster_id}: {count} 个样本" + (f" ({cluster_type})" if cluster_type else ""))
            report_lines.append("")
        
        report_lines.append("=" * 60)
        
        report_text = "\n".join(report_lines)
        return report_text
    
    def save_report(self, report_text: str, scene_name: str, save_dir: str = "test_engine/reports/") -> str:
        """
        保存报告到文件
        
        Args:
            report_text: 报告文本
            scene_name: 场景名称
            save_dir: 保存目录
        
        Returns:
            保存的文件路径
        """
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        filepath = os.path.join(save_dir, f"{scene_name}_report.txt")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report_text)
            logger.info(f"报告保存成功: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"报告保存失败: {e}")
            raise


