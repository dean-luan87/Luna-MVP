"""
Evidence Alignment Exporter (v1.4.8 Step 9)

导出器：将 AlignmentIndex 中的数据导出为可调试形式

必须实现：
1. JSON 导出
2. 人类可读时间轴导出
"""

import json
from typing import List
from navigation.evidence_alignment_frame import EvidenceAlignmentFrame


class EvidenceAlignmentExporter:
    """
    证据对齐导出器
    
    功能：
    - JSON 导出
    - 人类可读时间轴导出
    """
    
    def export_json(
        self,
        frames: List[EvidenceAlignmentFrame]
    ) -> str:
        """
        导出为 JSON 格式
        
        Args:
            frames: 证据对齐帧列表
            
        Returns:
            JSON 字符串
        """
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
        frames: List[EvidenceAlignmentFrame]
    ) -> str:
        """
        导出为人类可读时间轴文本
        
        示例格式：
        t=18.0s | MAP_VISION(0.74) | FSM=TAKEN | scene=OUTDOOR
          ├─ local_map: map_042
          ├─ landmark: crosswalk_3 (0.82)
          └─ nodes: turn_12, curb_7
        
        Args:
            frames: 证据对齐帧列表
            
        Returns:
            ASCII 文本
        """
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
                f"{k}({v:.2f})" for k, v in conf_items[:3]  # 只显示前3个
            ])
            
            # 格式化活动主权
            active_str = frame.active_authority
            if frame.candidate_authority:
                active_str += f" -> {frame.candidate_authority}"
            
            # 构建主行
            main_line = (
                f"t={relative_time:.1f}s | "
                f"{active_str} | "
                f"{conf_str} | "
                f"FSM={frame.takeover_state} | "
                f"scene={frame.scene}"
            )
            
            if frame.hint_active:
                main_line += " [HINT]"
            
            lines.append(main_line)
            
            # 构建子行（空间侧信息）
            sub_lines = []
            
            if frame.local_map_id:
                sub_lines.append(f"  ├─ local_map: {frame.local_map_id}")
            
            if frame.landmark_ids:
                landmark_info = []
                for landmark_id in frame.landmark_ids:
                    score = frame.match_scores.get(landmark_id, 0.0)
                    landmark_info.append(f"{landmark_id} ({score:.2f})")
                if landmark_info:
                    sub_lines.append(f"  ├─ landmark: {', '.join(landmark_info)}")
            
            if frame.recent_node_ids:
                nodes_str = ", ".join(frame.recent_node_ids)
                sub_lines.append(f"  └─ nodes: {nodes_str}")
            elif frame.local_map_id or frame.landmark_ids:
                # 如果没有节点但有其他信息，也要添加空的 nodes 行
                sub_lines.append(f"  └─ nodes: (none)")
            
            # 如果没有子信息，不添加子行
            if sub_lines:
                lines.extend(sub_lines)
        
        return "\n".join(lines)
    
    def export_to_file(
        self,
        filepath: str,
        frames: List[EvidenceAlignmentFrame],
        format: str = "json"
    ) -> None:
        """
        导出到文件
        
        Args:
            filepath: 文件路径
            frames: 证据对齐帧列表
            format: 格式（"json" 或 "text"）
        """
        if format == "json":
            content = self.export_json(frames)
        elif format == "text":
            content = self.export_text_timeline(frames)
        else:
            raise ValueError(f"Unknown format: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)






