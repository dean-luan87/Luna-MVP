# vision_pipeline/b2/v03/validation/rules/s3_trigger.py
"""
Step 3: Trigger 自动验收规则
"""

from typing import Dict, Any, Tuple


def check_s3_trigger_001(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S3.TRIGGER.001 — Trigger 显式存在
    
    规则: 每一条 trace 必须包含 trigger 字段
    """
    rule_id = "S3.TRIGGER.001"
    
    if "trigger" not in trace:
        return "FAIL", "trace 中无 trigger 字段", {
            "trace_id": trace_id,
            "field": "trigger"
        }
    
    return "PASS", "Trigger 字段存在", {
        "trace_id": trace_id,
        "triggered": trace["trigger"].get("triggered")
    }


def check_s3_trigger_002(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S3.TRIGGER.002 — Gate 控制 Trigger
    
    规则: if gate_eval.mode != ACTIVE:
        trigger.triggered must be false
    """
    rule_id = "S3.TRIGGER.002"
    
    if "gate_eval" not in trace:
        return "WARN", "trace 中无 gate_eval，跳过检查", {
            "trace_id": trace_id
        }
    
    if "trigger" not in trace:
        return "WARN", "trace 中无 trigger，跳过检查", {
            "trace_id": trace_id
        }
    
    gate_mode = trace["gate_eval"].get("mode")
    trigger_triggered = trace["trigger"].get("triggered", False)
    
    if gate_mode != "ACTIVE" and trigger_triggered:
        return "FAIL", f"Gate Mode {gate_mode} 但仍触发 Trigger", {
            "trace_id": trace_id,
            "gate_mode": gate_mode,
            "trigger_triggered": trigger_triggered
        }
    
    return "PASS", f"Gate Mode {gate_mode} 与 Trigger 一致", {
        "trace_id": trace_id,
        "gate_mode": gate_mode,
        "trigger_triggered": trigger_triggered
    }


def get_all_trigger_rules():
    """获取所有 Trigger 规则检查函数"""
    return [
        check_s3_trigger_001,
        check_s3_trigger_002,
    ]
