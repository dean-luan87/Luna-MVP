"""
C1 Replay Tool 核心引擎

这里只重放"决策逻辑"，不跑系统。
"""

from typing import List, Dict
from .replay_models import C1DecisionRecord, PipelineExecutionRecord


class C1ReplayEngine:
    """
    C1 回放引擎
    
    职责：
    - 重放 C1 决策链
    - 关联 Pipeline 执行记录
    - 生成时间轴
    """
    
    def replay(
        self,
        c1_records: List[C1DecisionRecord],
        pipeline_records: List[PipelineExecutionRecord],
    ) -> List[Dict]:
        """
        重放 C1 决策链
        
        Args:
            c1_records: C1 决策记录列表
            pipeline_records: Pipeline 执行记录列表
        
        Returns:
            时间轴列表
        """
        # 创建 pipeline 记录的时间索引（用于快速查找）
        pipeline_by_time = {
            round(p.timestamp, 2): p for p in pipeline_records
        }

        timeline = []

        for r in c1_records:
            key = round(r.timestamp, 2)
            pipeline = pipeline_by_time.get(key)

            timeline.append({
                "timestamp": r.timestamp,
                "state": r.current_state,
                "decision": {
                    "allow_frame": r.allow_frame,
                    "fps": r.target_fps,
                    "priority": r.priority,
                    "mode": r.observation_mode,
                },
                "reason": r.reason,
                "pipeline": {
                    "navigation": pipeline.navigation_executed if pipeline else False,
                    "modeling": pipeline.modeling_executed if pipeline else False,
                    "latency_ms": pipeline.latency_ms if pipeline else None,
                }
            })

        return timeline
