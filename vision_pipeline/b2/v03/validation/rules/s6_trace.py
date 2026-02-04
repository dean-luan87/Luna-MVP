# vision_pipeline/b2/v03/validation/rules/s6_trace.py
"""
Step 6: Trace / Timeline 自动验收规则
"""

from typing import Dict, Any, List, Tuple


def check_s6_trace_001(traces: List[Dict[str, Any]], total_frames: int = None) -> Tuple[str, str, Dict[str, Any]]:
    """
    S6.TRACE.001 — Trace 全覆盖
    
    规则: trace_count == total_frame_count
    
    注意: 这个检查需要知道总帧数，可能需要从外部传入
    """
    rule_id = "S6.TRACE.001"
    
    trace_count = len(traces)
    
    if total_frames is not None:
        if trace_count != total_frames:
            return "FAIL", f"Trace 数量 ({trace_count}) != 总帧数 ({total_frames})", {
                "trace_count": trace_count,
                "total_frames": total_frames,
                "missing": total_frames - trace_count
            }
    
    return "PASS", f"Trace 数量: {trace_count}", {
        "trace_count": trace_count
    }


def check_s6_timeline_001(timeline: List[Dict[str, Any]]) -> Tuple[str, str, Dict[str, Any]]:
    """
    S6.TIMELINE.001 — Timeline 去噪
    
    规则: timeline 中禁止出现 impact == NO_OP
    """
    rule_id = "S6.TIMELINE.001"
    
    if not timeline:
        return "PASS", "Timeline 为空，跳过检查", {}
    
    no_op_entries = []
    for i, entry in enumerate(timeline):
        impact = entry.get("impact") or entry.get("impact_eval", {}).get("impact")
        if impact == "NO_OP":
            no_op_entries.append({
                "index": i,
                "entry": entry
            })
    
    if no_op_entries:
        return "FAIL", f"Timeline 中发现 {len(no_op_entries)} 个 NO_OP 条目", {
            "no_op_entries": no_op_entries
        }
    
    return "PASS", f"Timeline 干净，无 NO_OP 条目（共 {len(timeline)} 条）", {
        "timeline_count": len(timeline)
    }


def get_all_trace_rules():
    """获取所有 Trace 规则检查函数"""
    return [
        # check_s6_trace_001 需要所有 traces，在 runner 中特殊处理
        # check_s6_timeline_001 需要 timeline，在 runner 中特殊处理
    ]
