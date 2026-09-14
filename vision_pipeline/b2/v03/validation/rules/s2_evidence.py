# vision_pipeline/b2/v03/validation/rules/s2_evidence.py
"""
Step 2: Evidence 生命周期自动验收规则
"""

from typing import Dict, Any, List, Tuple


def check_s2_evidence_001(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S2.EVIDENCE.001 — 禁止瞬时证据
    
    规则: 任何 impact != NO_OP 的 trace
    必须至少有 1 条 evidence.state == CONFIRMED
    """
    rule_id = "S2.EVIDENCE.001"
    
    impact_eval = trace.get("impact_eval", {})
    impact = impact_eval.get("impact", "NO_OP")
    
    if impact == "NO_OP":
        return "PASS", "Impact 是 NO_OP，跳过检查", {
            "trace_id": trace_id,
            "impact": impact
        }
    
    # 检查 evidence_state
    evidence_state = trace.get("evidence_state", {})
    if not evidence_state:
        return "FAIL", f"Impact {impact} 但无 evidence_state", {
            "trace_id": trace_id,
            "impact": impact,
            "evidence_state": evidence_state
        }
    
    # 检查是否有 CONFIRMED 证据
    has_confirmed = False
    for factor_key, evidence in evidence_state.items():
        if isinstance(evidence, dict) and evidence.get("state") == "CONFIRMED":
            has_confirmed = True
            break
    
    if not has_confirmed:
        return "FAIL", f"Impact {impact} 但无 CONFIRMED 证据", {
            "trace_id": trace_id,
            "impact": impact,
            "evidence_states": [e.get("state") if isinstance(e, dict) else None 
                               for e in evidence_state.values()]
        }
    
    return "PASS", f"Impact {impact} 有 CONFIRMED 证据", {
        "trace_id": trace_id,
        "impact": impact
    }


def check_s2_evidence_002(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S2.EVIDENCE.002 — 生命周期合法性
    
    规则: evidence.state ∈ {
      OBSERVING,
      CONFIRMED,
      DEGRADED,
      DROPPED
    }
    """
    rule_id = "S2.EVIDENCE.002"
    allowed_states = {"OBSERVING", "CONFIRMED", "DEGRADED", "DROPPED"}
    
    evidence_state = trace.get("evidence_state", {})
    if not evidence_state:
        return "PASS", "无 evidence_state，跳过检查", {
            "trace_id": trace_id
        }
    
    invalid_states = []
    for factor_key, evidence in evidence_state.items():
        if isinstance(evidence, dict):
            state = evidence.get("state")
            if state and state not in allowed_states:
                invalid_states.append({
                    "factor": factor_key,
                    "state": state
                })
    
    if invalid_states:
        return "FAIL", f"发现非法 evidence.state: {invalid_states}", {
            "trace_id": trace_id,
            "invalid_states": invalid_states,
            "allowed": list(allowed_states)
        }
    
    return "PASS", "所有 evidence.state 合法", {
        "trace_id": trace_id
    }


def check_s2_evidence_003(trace: Dict[str, Any], trace_id: int, 
                          prev_trace: Dict[str, Any] = None) -> Tuple[str, str, Dict[str, Any]]:
    """
    S2.EVIDENCE.003 — 生命周期单向性
    
    规则: OBSERVING → CONFIRMED → DEGRADED → DROPPED
    禁止反向跳转
    
    注意: 需要前一帧的 trace 来检查状态变化
    """
    rule_id = "S2.EVIDENCE.003"
    
    if not prev_trace:
        return "PASS", "无前一帧 trace，跳过检查", {
            "trace_id": trace_id
        }
    
    prev_evidence = prev_trace.get("evidence_state", {})
    curr_evidence = trace.get("evidence_state", {})
    
    if not prev_evidence or not curr_evidence:
        return "PASS", "证据状态不完整，跳过检查", {
            "trace_id": trace_id
        }
    
    # 状态转换规则
    valid_transitions = {
        "OBSERVING": {"OBSERVING", "CONFIRMED", "DEGRADED", "DROPPED"},
        "CONFIRMED": {"CONFIRMED", "DEGRADED", "DROPPED"},
        "DEGRADED": {"DEGRADED", "DROPPED", "CONFIRMED"},  # 允许从 DEGRADED 恢复
        "DROPPED": {"DROPPED"}  # DROPPED 不能再变
    }
    
    invalid_transitions = []
    for factor_key in set(prev_evidence.keys()) | set(curr_evidence.keys()):
        prev_state = prev_evidence.get(factor_key, {}).get("state") if isinstance(prev_evidence.get(factor_key), dict) else None
        curr_state = curr_evidence.get(factor_key, {}).get("state") if isinstance(curr_evidence.get(factor_key), dict) else None
        
        if prev_state and curr_state and prev_state != curr_state:
            allowed = valid_transitions.get(prev_state, set())
            if curr_state not in allowed:
                invalid_transitions.append({
                    "factor": factor_key,
                    "from": prev_state,
                    "to": curr_state
                })
    
    if invalid_transitions:
        return "FAIL", f"发现非法状态转换: {invalid_transitions}", {
            "trace_id": trace_id,
            "invalid_transitions": invalid_transitions
        }
    
    return "PASS", "所有状态转换合法", {
        "trace_id": trace_id
    }


def get_all_evidence_rules():
    """获取所有 Evidence 规则检查函数"""
    return [
        check_s2_evidence_001,
        check_s2_evidence_002,
        # check_s2_evidence_003 需要前一帧，在 runner 中特殊处理
    ]
