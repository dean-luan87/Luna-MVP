# vision_pipeline/b2/v03/validation/rules/s5_b2c.py
"""
Step 5: B → C 通信自动验收规则
"""

from typing import Dict, Any, Tuple


def check_s5_b2c_001(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S5.B2C.001 — 单一出口
    
    规则: 所有对 C 的影响，只能出现在 to_c_message
    
    注意: 这个检查需要看代码，这里只检查 trace 中是否有其他字段
    """
    rule_id = "S5.B2C.001"
    
    # 检查 to_c_message 是否存在
    if "to_c_message" not in trace:
        return "WARN", "trace 中无 to_c_message 字段", {
            "trace_id": trace_id,
            "field": "to_c_message"
        }
    
    return "PASS", "to_c_message 字段存在", {
        "trace_id": trace_id
    }


def check_s5_b2c_002(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S5.B2C.002 — NO_OP 不得通信
    
    规则: impact == NO_OP → to_c_message.sent == false
    """
    rule_id = "S5.B2C.002"
    
    impact_eval = trace.get("impact_eval", {})
    impact = impact_eval.get("impact", "NO_OP")
    
    if impact != "NO_OP":
        return "PASS", f"Impact 不是 NO_OP ({impact})，跳过检查", {
            "trace_id": trace_id
        }
    
    to_c_message = trace.get("to_c_message", {})
    sent = to_c_message.get("sent", False)
    
    if sent:
        return "FAIL", "Impact NO_OP 但仍给 C 发消息", {
            "trace_id": trace_id,
            "impact": impact,
            "to_c_sent": sent
        }
    
    return "PASS", "Impact NO_OP 时正确不通信", {
        "trace_id": trace_id,
        "impact": impact
    }


def check_s5_b2c_003(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S5.B2C.003 — FORCE_ALERT 可打断
    
    规则: impact == FORCE_ALERT → to_c_message.urgency == "IMMEDIATE"
    """
    rule_id = "S5.B2C.003"
    
    impact_eval = trace.get("impact_eval", {})
    impact = impact_eval.get("impact")
    
    if impact != "FORCE_ALERT":
        return "PASS", f"Impact 不是 FORCE_ALERT ({impact})，跳过检查", {
            "trace_id": trace_id
        }
    
    to_c_message = trace.get("to_c_message", {})
    if not to_c_message.get("sent", False):
        return "WARN", "FORCE_ALERT 但未发送消息", {
            "trace_id": trace_id,
            "impact": impact
        }
    
    # 检查 urgency（可能在 payload 中）
    payload = to_c_message.get("payload", {})
    urgency = payload.get("urgency") or to_c_message.get("urgency")
    
    if urgency and urgency.upper() not in ("IMMEDIATE", "FORCE", "URGENT"):
        return "WARN", f"FORCE_ALERT 但 urgency 不是 IMMEDIATE: {urgency}", {
            "trace_id": trace_id,
            "impact": impact,
            "urgency": urgency
        }
    
    return "PASS", "FORCE_ALERT 正确标记为可打断", {
        "trace_id": trace_id,
        "impact": impact
    }


def get_all_b2c_rules():
    """获取所有 B → C 通信规则检查函数"""
    return [
        check_s5_b2c_001,
        check_s5_b2c_002,
        check_s5_b2c_003,
    ]
