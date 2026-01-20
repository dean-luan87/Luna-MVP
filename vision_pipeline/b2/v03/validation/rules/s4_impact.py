# vision_pipeline/b2/v03/validation/rules/s4_impact.py
"""
Step 4: Impact Evaluation 自动验收规则
"""

from typing import Dict, Any, Tuple


def check_s4_impact_001(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S4.IMPACT.001 — Impact 枚举封闭性
    
    规则: impact ∈ {
      NO_OP,
      NEED_SLOW_DOWN,
      PATH_UNCERTAIN,
      NEED_DETOUR,
      NEED_STOP,
      FORCE_ALERT
    }
    """
    rule_id = "S4.IMPACT.001"
    allowed_impacts = {
        "NO_OP", "NEED_SLOW_DOWN", "PATH_UNCERTAIN",
        "NEED_DETOUR", "NEED_STOP", "FORCE_ALERT"
    }
    
    impact_eval = trace.get("impact_eval", {})
    impact = impact_eval.get("impact")
    
    if not impact:
        return "WARN", "impact_eval.impact 缺失", {
            "trace_id": trace_id,
            "field": "impact_eval.impact"
        }
    
    if impact not in allowed_impacts:
        return "FAIL", f"Impact 非法值: {impact}", {
            "trace_id": trace_id,
            "actual": impact,
            "allowed": list(allowed_impacts)
        }
    
    return "PASS", f"Impact 合法: {impact}", {
        "trace_id": trace_id,
        "impact": impact
    }


def check_s4_impact_002(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S4.IMPACT.002 — ENV 禁止直接影响
    
    规则: if main_factor == ENV:
        impact must be NO_OP
    """
    rule_id = "S4.IMPACT.002"
    
    impact_eval = trace.get("impact_eval", {})
    impact = impact_eval.get("impact", "NO_OP")
    derived_from = impact_eval.get("derived_from")
    
    # 检查 main_factor 或 derived_from 是否为 ENV
    if derived_from and derived_from.upper() in ("ENV", "ENVIRONMENT"):
        if impact != "NO_OP":
            return "FAIL", f"ENV 因子产生了非 NO_OP impact: {impact}", {
                "trace_id": trace_id,
                "derived_from": derived_from,
                "impact": impact
            }
    
    return "PASS", "ENV 因子未直接产生 impact", {
        "trace_id": trace_id
    }


def check_s4_impact_003(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    S4.IMPACT.003 — FORCE_ALERT 权限约束
    
    规则: impact == FORCE_ALERT
    →
    evidence.confidence.final >= FORCE_ALERT_THRESHOLD
    """
    rule_id = "S4.IMPACT.003"
    FORCE_ALERT_THRESHOLD = 0.75  # 可配置
    
    impact_eval = trace.get("impact_eval", {})
    impact = impact_eval.get("impact")
    
    if impact != "FORCE_ALERT":
        return "PASS", f"Impact 不是 FORCE_ALERT ({impact})，跳过检查", {
            "trace_id": trace_id
        }
    
    # 检查 confidence
    confidence = trace.get("confidence", {})
    final_confidence = confidence.get("final")
    
    if final_confidence is None:
        return "FAIL", "FORCE_ALERT 但 confidence.final 缺失", {
            "trace_id": trace_id,
            "impact": impact
        }
    
    if final_confidence < FORCE_ALERT_THRESHOLD:
        return "FAIL", f"FORCE_ALERT 但 confidence.final ({final_confidence}) < 阈值 ({FORCE_ALERT_THRESHOLD})", {
            "trace_id": trace_id,
            "impact": impact,
            "final_confidence": final_confidence,
            "threshold": FORCE_ALERT_THRESHOLD
        }
    
    return "PASS", f"FORCE_ALERT 置信度满足要求: {final_confidence}", {
        "trace_id": trace_id,
        "final_confidence": final_confidence
    }


def get_all_impact_rules():
    """获取所有 Impact 规则检查函数"""
    return [
        check_s4_impact_001,
        check_s4_impact_002,
        check_s4_impact_003,
    ]
