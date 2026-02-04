# vision_pipeline/b2/v03/b2_audit/rules/s4_impact.py
"""
Step 4: Impact Evaluation 验收规则
"""

from typing import Optional, Dict, Any
from rules.base import AuditRule


class ImpactEnumValidityRule(AuditRule):
    """S4.IMPACT.001 — Impact 枚举封闭性"""
    
    rule_id = "S4.IMPACT.001"
    description = "impact 必须是允许的枚举值"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        allowed_impacts = {
            "NO_OP", "NEED_SLOW_DOWN", "PATH_UNCERTAIN",
            "NEED_DETOUR", "NEED_STOP", "FORCE_ALERT"
        }
        
        for i, t in enumerate(ctx.traces):
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact")
            
            if not impact:
                continue  # 允许缺失（可能是 NO_OP）
            
            if impact not in allowed_impacts:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"Impact 非法值: {impact}",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "actual": impact,
                        "allowed": list(allowed_impacts)
                    }
                }
        return None


class EnvNoDirectImpactRule(AuditRule):
    """S4.IMPACT.002 — ENV 禁止直接影响"""
    
    rule_id = "S4.IMPACT.002"
    description = "ENV 因子不能直接产生 impact"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            derived_from = impact_eval.get("derived_from")
            
            # 检查 main_factor 或 derived_from 是否为 ENV
            if derived_from and derived_from.upper() in ("ENV", "ENVIRONMENT"):
                if impact != "NO_OP":
                    return {
                        "rule_id": self.rule_id,
                        "status": "FAIL",
                        "message": f"ENV 因子产生了非 NO_OP impact: {impact}",
                        "evidence": {
                            "trace_index": i,
                            "frame_id": t.get("time", {}).get("frame_id"),
                            "derived_from": derived_from,
                            "impact": impact
                        }
                    }
        return None


class ForceAlertThresholdRule(AuditRule):
    """S4.IMPACT.003 — FORCE_ALERT 权限约束"""
    
    rule_id = "S4.IMPACT.003"
    description = "FORCE_ALERT 必须满足置信度阈值"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        FORCE_ALERT_THRESHOLD = 0.75
        
        for i, t in enumerate(ctx.traces):
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact")
            
            if impact != "FORCE_ALERT":
                continue
            
            confidence = t.get("confidence", {})
            final_confidence = confidence.get("final")
            
            if final_confidence is None:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": "FORCE_ALERT 但 confidence.final 缺失",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "impact": impact
                    }
                }
            
            if final_confidence < FORCE_ALERT_THRESHOLD:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"FORCE_ALERT 但 confidence.final ({final_confidence}) < 阈值 ({FORCE_ALERT_THRESHOLD})",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "impact": impact,
                        "final_confidence": final_confidence,
                        "threshold": FORCE_ALERT_THRESHOLD
                    }
                }
        return None
