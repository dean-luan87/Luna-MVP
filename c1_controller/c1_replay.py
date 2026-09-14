"""
C1 行为回放工具（Offline Replay）

用日志重放 C1 决策，看"如果当时这样走，会不会更好"。

这是后面时间连续性 / 世界预测 / 看视频的必经之路。
"""

import json
import time
from typing import List, Dict, Any, Optional
from .c1_logger import C1LogRecord
from .c1_controller import C1Controller
from .c1_types import C1Input, C1Decision


class C1Replay:
    """
    C1 行为回放工具
    
    职责：
    - 从日志文件加载 C1 决策历史
    - 重放 C1 决策过程
    - 分析决策模式
    - 支持"如果当时这样走"的假设分析
    """
    
    def __init__(self, log_file: Optional[str] = None):
        """
        初始化 C1 回放工具
        
        Args:
            log_file: 日志文件路径（可选）
        """
        self.log_file = log_file
        self.records: List[C1LogRecord] = []
    
    def load_logs(self, log_file: Optional[str] = None) -> List[C1LogRecord]:
        """
        从日志文件加载 C1 日志记录
        
        Args:
            log_file: 日志文件路径（如果为 None，使用 self.log_file）
        
        Returns:
            日志记录列表
        """
        file_path = log_file or self.log_file
        if not file_path:
            return []
        
        records = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    record = C1LogRecord(**data)
                    records.append(record)
        except FileNotFoundError:
            print(f"⚠️  日志文件不存在: {file_path}")
        except Exception as e:
            print(f"⚠️  加载日志文件失败: {e}")
        
        self.records = records
        return records
    
    def replay(self, start_idx: int = 0, end_idx: Optional[int] = None) -> List[C1Decision]:
        """
        重放 C1 决策过程
        
        Args:
            start_idx: 开始索引
            end_idx: 结束索引（如果为 None，则到末尾）
        
        Returns:
            重放的决策列表
        """
        if not self.records:
            return []
        
        end_idx = end_idx or len(self.records)
        records_to_replay = self.records[start_idx:end_idx]
        
        c1 = C1Controller()
        decisions = []
        
        for record in records_to_replay:
            # 重建 C1Input
            c1_input = C1Input(
                timestamp=record.timestamp,
                motion_score=record.motion_score,
                frame_diff_score=record.frame_diff_score,
                next_scene_hint=record.next_scene_hint,
                risk_hint=record.risk_hint,
                privacy_zone=record.privacy_zone,
                user_camera_override=False,  # 日志中没有记录，使用默认值
            )
            
            # 重放决策
            decision = c1.decide(c1_input)
            decisions.append(decision)
        
        return decisions
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """
        分析决策模式
        
        Returns:
            分析结果字典
        """
        if not self.records:
            return {}
        
        analysis = {
            "total_records": len(self.records),
            "state_transitions": {},
            "suspended_events": [],
            "priority_distribution": {},
            "fps_distribution": {},
        }
        
        prev_state = None
        for record in self.records:
            # 状态转换统计
            if prev_state != record.current_state:
                transition_key = f"{prev_state or 'unknown'} -> {record.current_state}"
                analysis["state_transitions"][transition_key] = \
                    analysis["state_transitions"].get(transition_key, 0) + 1
                prev_state = record.current_state
            
            # 暂停事件
            if not record.allow_frame:
                analysis["suspended_events"].append({
                    "timestamp": record.timestamp,
                    "reason": record.reason,
                    "state": record.current_state,
                })
            
            # 优先级分布
            analysis["priority_distribution"][record.priority] = \
                analysis["priority_distribution"].get(record.priority, 0) + 1
            
            # FPS 分布
            analysis["fps_distribution"][record.target_fps] = \
                analysis["fps_distribution"].get(record.target_fps, 0) + 1
        
        return analysis
    
    def what_if(
        self,
        record_idx: int,
        modified_input: Optional[C1Input] = None,
    ) -> C1Decision:
        """
        假设分析："如果当时这样走，会不会更好"
        
        Args:
            record_idx: 日志记录索引
            modified_input: 修改后的输入（如果为 None，使用原始输入）
        
        Returns:
            假设情况下的决策
        """
        if record_idx >= len(self.records):
            raise IndexError(f"记录索引超出范围: {record_idx} >= {len(self.records)}")
        
        record = self.records[record_idx]
        
        # 使用修改后的输入或原始输入
        if modified_input is None:
            c1_input = C1Input(
                timestamp=record.timestamp,
                motion_score=record.motion_score,
                frame_diff_score=record.frame_diff_score,
                next_scene_hint=record.next_scene_hint,
                risk_hint=record.risk_hint,
                privacy_zone=record.privacy_zone,
                user_camera_override=False,
            )
        else:
            c1_input = modified_input
        
        # 重放决策
        c1 = C1Controller()
        decision = c1.decide(c1_input)
        
        return decision


