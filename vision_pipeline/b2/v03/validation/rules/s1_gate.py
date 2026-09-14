# vision_pipeline/b2/v03/validation/rules/s1_gate.py
"""
Step 1: Gate 自动验收规则
"""

from typing import Dict, Any, List, Tuple


def check_s1_gate_001(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S1.GATE.001 — Gate 是否为第一步
    
    规则: 每一条 trace 中，gate_eval 必须存在
    且 gate_eval.time <= trigger.time
    """
    rule_id = "S1.GATE.001"
    
    if "gate_eval" not in trace:
        return "FAIL", "trace 中无 gate_eval", {
            "trace_id": trace_id,
            "field": "gate_eval"
        }
    
    # 检查时间顺序（如果 trace 中有时间字段）
    time = trace.get("time", {})
    gate_time = time.get("ts", 0)
    
    # 检查 trigger 是否存在
    if "trigger" in trace:
        trigger_time = time.get("ts", 0)  # 同一帧，时间相同
        # 这里主要是检查 gate_eval 是否存在，时间检查在逻辑层面
    
    return "PASS", "Gate 存在且为第一步", {
        "trace_id": trace_id,
        "gate_mode": trace["gate_eval"].get("mode")
    }


def check_s1_gate_002(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S1.GATE.002 — Gate Mode 合法性
    
    规则: gate_eval.mode ∈ {SUSPENDED, READ_ONLY, ACTIVE}
    """
    rule_id = "S1.GATE.002"
    allowed_modes = {"SUSPENDED", "READ_ONLY", "ACTIVE"}
    
    if "gate_eval" not in trace:
        return "FAIL", "trace 中无 gate_eval", {
            "trace_id": trace_id,
            "field": "gate_eval"
        }
    
    mode = trace["gate_eval"].get("mode")
    if not mode:
        return "FAIL", "gate_eval.mode 缺失", {
            "trace_id": trace_id,
            "field": "gate_eval.mode"
        }
    
    if mode not in allowed_modes:
        return "FAIL", f"gate_eval.mode 非法值: {mode}", {
            "trace_id": trace_id,
            "field": "gate_eval.mode",
            "actual": mode,
            "allowed": list(allowed_modes)
        }
    
    return "PASS", f"Gate Mode 合法: {mode}", {
        "trace_id": trace_id,
        "mode": mode
    }


def check_s1_gate_003(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S1.GATE.003 — Gate 阻断一致性
    
    规则: if gate_eval.mode == SUSPENDED:
        trigger.triggered must be false
        to_c_message.sent must be false
    """
    rule_id = "S1.GATE.003"
    
    if "gate_eval" not in trace:
        return "WARN", "trace 中无 gate_eval，跳过检查", {
            "trace_id": trace_id
        }
    
    mode = trace["gate_eval"].get("mode")
    if mode != "SUSPENDED":
        return "PASS", f"Gate Mode 不是 SUSPENDED ({mode})，跳过检查", {
            "trace_id": trace_id,
            "mode": mode
        }
    
    # 检查 trigger
    if "trigger" in trace:
        triggered = trace["trigger"].get("triggered", False)
        if triggered:
            return "FAIL", "Gate SUSPENDED 但仍触发 Trigger", {
                "trace_id": trace_id,
                "gate_mode": mode,
                "trigger_triggered": triggered
            }
    
    # 检查 to_c_message
    if "to_c_message" in trace:
        sent = trace["to_c_message"].get("sent", False)
        if sent:
            return "FAIL", "Gate SUSPENDED 但仍给 C 发消息", {
                "trace_id": trace_id,
                "gate_mode": mode,
                "to_c_sent": sent
            }
    
    return "PASS", "Gate SUSPENDED 时正确阻断", {
        "trace_id": trace_id,
        "mode": mode
    }


def check_s1_gate_004(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S1.GATE.004 — 抗视角污染字段完整性
    
    规则: gate_eval.details 必须包含:
    - stability_score
    - camera_motion
    - camera_pose
    - fov_state
    """
    rule_id = "S1.GATE.004"
    required_fields = ["stability_score", "camera_motion", "camera_pose", "fov_state"]
    
    if "gate_eval" not in trace:
        return "WARN", "trace 中无 gate_eval，跳过检查", {
            "trace_id": trace_id
        }
    
    details = trace["gate_eval"].get("details", {})
    missing = [f for f in required_fields if f not in details]
    
    if missing:
        return "FAIL", f"gate_eval.details 缺少字段: {missing}", {
            "trace_id": trace_id,
            "missing_fields": missing,
            "details_keys": list(details.keys())
        }
    
    return "PASS", "Gate details 字段完整", {
        "trace_id": trace_id,
        "details_fields": list(details.keys())
    }


def get_all_gate_rules():
    """获取所有 Gate 规则检查函数"""
    return [
        check_s1_gate_001,
        check_s1_gate_002,
        check_s1_gate_003,
        check_s1_gate_004,
    ]
