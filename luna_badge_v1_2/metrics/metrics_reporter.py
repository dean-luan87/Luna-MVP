"""
Metrics Reporter

指标报告生成器。

v1.5: 简单的报告生成，用于验收和审计。
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict


class MetricsReporter:
    """
    指标报告生成器
    
    职责：
    - 解析日志文件
    - 生成简单的统计报告
    - v1.5: 不做复杂可视化，只做可读的文本报告
    """
    
    def __init__(self, trace_path: str, metrics_path: str, error_path: str):
        """
        初始化报告生成器
        
        Args:
            trace_path: 执行跟踪日志路径
            metrics_path: 性能指标日志路径
            error_path: 错误日志路径
        """
        self.trace_path = Path(trace_path)
        self.metrics_path = Path(metrics_path)
        self.error_path = Path(error_path)
    
    def _load_jsonl(self, path: Path) -> List[Dict[str, Any]]:
        """
        加载 JSONL 文件
        
        Args:
            path: 文件路径
            
        Returns:
            记录列表
        """
        if not path.exists():
            return []
        
        records = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return records
    
    def generate_report(self) -> Dict[str, Any]:
        """
        生成指标报告
        
        Returns:
            报告字典
        """
        trace_records = self._load_jsonl(self.trace_path)
        metrics_records = self._load_jsonl(self.metrics_path)
        error_records = self._load_jsonl(self.error_path)
        
        # 统计事件类型
        event_counts = defaultdict(int)
        for record in trace_records:
            event = record.get("event", "unknown")
            event_counts[event] += 1
        
        # 统计错误类型和严重程度
        error_counts = defaultdict(int)
        severity_counts = defaultdict(int)
        for record in error_records:
            error_type = record.get("error_type", "unknown")
            severity = record.get("severity", "unknown")
            error_counts[error_type] += 1
            severity_counts[severity] += 1
        
        # 统计指标（简单统计）
        metric_stats = defaultdict(list)
        for record in metrics_records:
            metric_name = record.get("metric", "unknown")
            value = record.get("value", 0)
            metric_stats[metric_name].append(value)
        
        # 计算分位数（简单版）
        metric_percentiles = {}
        for metric_name, values in metric_stats.items():
            if values:
                sorted_values = sorted(values)
                p50_idx = int(len(sorted_values) * 0.5)
                p95_idx = int(len(sorted_values) * 0.95)
                metric_percentiles[metric_name] = {
                    "p50": sorted_values[p50_idx] if p50_idx < len(sorted_values) else sorted_values[-1],
                    "p95": sorted_values[p95_idx] if p95_idx < len(sorted_values) else sorted_values[-1],
                    "count": len(values)
                }
        
        return {
            "trace": {
                "total_records": len(trace_records),
                "event_counts": dict(event_counts)
            },
            "errors": {
                "total_records": len(error_records),
                "error_type_counts": dict(error_counts),
                "severity_counts": dict(severity_counts)
            },
            "metrics": {
                "total_records": len(metrics_records),
                "metric_percentiles": metric_percentiles
            }
        }
    
    def print_report(self):
        """打印报告到控制台"""
        report = self.generate_report()
        
        print("=" * 60)
        print("Runtime Metrics Report")
        print("=" * 60)
        
        print(f"\n执行跟踪 (Trace):")
        print(f"  总记录数: {report['trace']['total_records']}")
        print(f"  事件分布:")
        for event, count in report['trace']['event_counts'].items():
            print(f"    {event}: {count}")
        
        print(f"\n错误日志 (Errors):")
        print(f"  总记录数: {report['errors']['total_records']}")
        print(f"  错误类型分布:")
        for error_type, count in report['errors']['error_type_counts'].items():
            print(f"    {error_type}: {count}")
        print(f"  严重程度分布:")
        for severity, count in report['errors']['severity_counts'].items():
            print(f"    {severity}: {count}")
        
        print(f"\n性能指标 (Metrics):")
        print(f"  总记录数: {report['metrics']['total_records']}")
        print(f"  指标分位数:")
        for metric_name, stats in report['metrics']['metric_percentiles'].items():
            print(f"    {metric_name}:")
            print(f"      P50: {stats['p50']:.2f}")
            print(f"      P95: {stats['p95']:.2f}")
            print(f"      样本数: {stats['count']}")




