"""
Calibration Hint Exporter (v1.4.8 Step 10)

Hint 导出器：用于调试、分析、未来接入人工或学习系统

注意：
- 不用于用户表达
- description 为工程解释，不是表达层文本
"""

import json
from typing import List
from navigation.calibration_hint import CalibrationHint


class CalibrationHintExporter:
    """
    校准提示导出器
    
    功能：
    - JSON 导出
    - 可读文本导出（工程向）
    """
    
    def export_json(self, hints: List[CalibrationHint]) -> str:
        """
        导出为 JSON 格式
        
        Args:
            hints: 校准提示列表
            
        Returns:
            JSON 字符串
        """
        data = {
            "metadata": {
                "hint_count": len(hints),
                "types": list(set(hint.hint_type for hint in hints)),
            },
            "hints": [hint.to_dict() for hint in hints]
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def export_text_timeline(
        self,
        hints: List[CalibrationHint],
        base_ts: float = 0.0
    ) -> str:
        """
        导出为可读文本（工程向）
        
        示例格式：
        [LANDMARK_UNSTABLE]
          authority: MAP_VISION
          landmark: crosswalk_3
          time: 12.3s → 15.8s
          confidence_drop: 0.41
          note: landmark matched/unmatched repeatedly
        
        Args:
            hints: 校准提示列表
            base_ts: 时间基准（用于计算相对时间，默认 0.0）
            
        Returns:
            ASCII 文本
        """
        if not hints:
            return "No calibration hints"
        
        lines = []
        for hint in hints:
            # 计算相对时间
            start_time = hint.time_range[0] - base_ts
            end_time = hint.time_range[1] - base_ts
            
            # 主标题
            lines.append(f"[{hint.hint_type}]")
            
            # authority
            lines.append(f"  authority: {hint.authority}")
            
            # 相关地标
            if hint.related_landmark_ids:
                landmark_str = ", ".join(hint.related_landmark_ids)
                lines.append(f"  landmark: {landmark_str}")
            
            # 时间范围
            lines.append(f"  time: {start_time:.1f}s → {end_time:.1f}s")
            
            # 置信度下降
            lines.append(f"  confidence_drop: {hint.confidence_drop:.2f}")
            
            # 相关地图
            if hint.related_map_ids:
                map_str = ", ".join(hint.related_map_ids)
                lines.append(f"  map: {map_str}")
            
            # 说明
            lines.append(f"  note: {hint.description}")
            
            # 空行分隔
            lines.append("")
        
        return "\n".join(lines)
    
    def export_to_file(
        self,
        filepath: str,
        hints: List[CalibrationHint],
        format: str = "json",
        base_ts: float = 0.0
    ) -> None:
        """
        导出到文件
        
        Args:
            filepath: 文件路径
            hints: 校准提示列表
            format: 格式（"json" 或 "text"）
            base_ts: 时间基准（用于 text 格式，默认 0.0）
        """
        if format == "json":
            content = self.export_json(hints)
        elif format == "text":
            content = self.export_text_timeline(hints, base_ts=base_ts)
        else:
            raise ValueError(f"Unknown format: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)






