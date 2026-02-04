# vision_pipeline/b2/v03/validation/rules/s7_web.py
"""
Step 7: Web 可视化一致性规则
"""

from typing import Dict, Any, Tuple


def check_s7_web_001(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S7.WEB.001 — 前端只读 trace
    
    规则: 所有前端展示字段必须能在 trace 中找到原始字段
    
    注意: 这个检查需要知道前端使用的字段，这里只做基本检查
    """
    rule_id = "S7.WEB.001"
    
    # 前端可能需要的核心字段
    required_for_visualization = [
        "time",
        "gate_eval",
        "trigger",
        "evidence_state",
        "impact_eval",
        "to_c_message"
    ]
    
    missing = [f for f in required_for_visualization if f not in trace]
    
    if missing:
        return "FAIL", f"Trace 缺少前端展示必需字段: {missing}", {
            "trace_id": trace_id,
            "missing_fields": missing
        }
    
    return "PASS", "Trace 包含前端展示必需字段", {
        "trace_id": trace_id
    }


def get_all_web_rules():
    """获取所有 Web 可视化规则检查函数"""
    return [
        check_s7_web_001,
    ]
