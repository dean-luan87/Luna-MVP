"""
C1 Replay Tool 日志加载器

支持 JSON Lines 格式（强烈建议统一使用这种格式）。
"""

import json
from typing import List, Tuple
from .replay_models import C1DecisionRecord, PipelineExecutionRecord


def load_c1_logs(path: str) -> Tuple[List[C1DecisionRecord], List[PipelineExecutionRecord]]:
    """
    加载 C1 日志（JSON Lines 格式）
    
    Args:
        path: 日志文件路径
    
    Returns:
        (C1 决策记录列表, Pipeline 执行记录列表)
    """
    c1_records = []
    pipeline_records = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)

                    if obj.get("type") == "c1_decision":
                        c1_records.append(
                            C1DecisionRecord(
                                timestamp=obj["timestamp"],
                                prev_state=obj["prev_state"],
                                current_state=obj["current_state"],
                                motion_score=obj["motion_score"],
                                frame_diff_score=obj["frame_diff_score"],
                                privacy_hit=obj.get("privacy_hit", False),
                                user_override=obj.get("user_override", False),
                                allow_frame=obj["allow_frame"],
                                target_fps=obj["target_fps"],
                                priority=obj["priority"],
                                observation_mode=obj["observation_mode"],
                                reason=obj["reason"],
                            )
                        )

                    elif obj.get("type") == "pipeline_execution":
                        pipeline_records.append(
                            PipelineExecutionRecord(
                                timestamp=obj["timestamp"],
                                navigation_executed=obj.get("navigation_executed", False),
                                modeling_executed=obj.get("modeling_executed", False),
                                latency_ms=obj.get("latency_ms", 0.0),
                            )
                        )
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    # 跳过无效行
                    continue
    except FileNotFoundError:
        print(f"❌ 日志文件不存在: {path}")
    except Exception as e:
        print(f"⚠️  加载日志文件失败: {e}")

    return c1_records, pipeline_records
