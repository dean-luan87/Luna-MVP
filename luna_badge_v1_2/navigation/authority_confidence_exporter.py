"""
Authority Confidence Exporter (v1.4.8 Step 8)

导出/回放功能（最小版）

v1.4.8 只支持 2 种能力：
1. JSON 导出
2. ASCII 时间轴打印（调试用）
"""

import json
from typing import List, Optional
from navigation.authority_confidence_timeline import AuthorityConfidenceFrame
from navigation.authority_confidence_store import AuthorityConfidenceStore


class AuthorityConfidenceExporter:
    """
    主权置信度导出器
    
    功能：
    - JSON 导出
    - ASCII 时间轴打印（调试用）
    """
    
    def __init__(self, store: AuthorityConfidenceStore):
        """
        初始化导出器
        
        Args:
            store: 存储对象
        """
        self.store = store
    
    def export_json(
        self,
        start_ts: Optional[float] = None,
        end_ts: Optional[float] = None
    ) -> str:
        """
        导出为 JSON 格式
        
        Args:
            start_ts: 开始时间戳（可选）
            end_ts: 结束时间戳（可选）
            
        Returns:
            JSON 字符串
        """
        frames = self.store.get_frames(start_ts=start_ts, end_ts=end_ts)
        
        data = {
            "metadata": {
                "frame_count": len(frames),
                "start_ts": frames[0].ts if frames else None,
                "end_ts": frames[-1].ts if frames else None,
            },
            "frames": [frame.to_dict() for frame in frames]
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def export_text_timeline(
        self,
        start_ts: Optional[float] = None,
        end_ts: Optional[float] = None
    ) -> str:
        """
        导出为 ASCII 时间轴文本（调试用）
        
        示例输出：
        t=12.0s | VISUAL(0.81) MAP(0.62) GPS(0.22) | FSM=LOCKING
        t=12.5s | VISUAL(0.79) MAP(0.65) GPS(0.24) | FSM=LOCKING
        t=13.0s | MAP_VISION(0.71) VISUAL(0.68)    | FSM=TAKEN
        
        Args:
            start_ts: 开始时间戳（可选）
            end_ts: 结束时间戳（可选）
            
        Returns:
            ASCII 文本
        """
        frames = self.store.get_frames(start_ts=start_ts, end_ts=end_ts)
        
        if not frames:
            return "Timeline is empty"
        
        # 计算时间基准（使用第一帧的时间戳）
        base_ts = frames[0].ts
        
        lines = []
        for frame in frames:
            # 计算相对时间
            relative_time = frame.ts - base_ts
            
            # 格式化置信度（按分数排序）
            conf_items = sorted(
                frame.confidence.items(),
                key=lambda x: x[1],
                reverse=True
            )
            conf_str = " ".join([
                f"{k}({v:.2f})" for k, v in conf_items
            ])
            
            # 格式化活动主权
            active_str = frame.active_authority
            if frame.candidate_authority:
                active_str += f" -> {frame.candidate_authority}"
            
            # 构建行
            line = (
                f"t={relative_time:.1f}s | "
                f"{active_str} | "
                f"{conf_str} | "
                f"FSM={frame.takeover_state}"
            )
            
            if frame.hint_active:
                line += " [HINT]"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def export_to_file(
        self,
        filepath: str,
        format: str = "json",
        start_ts: Optional[float] = None,
        end_ts: Optional[float] = None
    ) -> None:
        """
        导出到文件
        
        Args:
            filepath: 文件路径
            format: 格式（"json" 或 "text"）
            start_ts: 开始时间戳（可选）
            end_ts: 结束时间戳（可选）
        """
        if format == "json":
            content = self.export_json(start_ts=start_ts, end_ts=end_ts)
        elif format == "text":
            content = self.export_text_timeline(start_ts=start_ts, end_ts=end_ts)
        else:
            raise ValueError(f"Unknown format: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)






