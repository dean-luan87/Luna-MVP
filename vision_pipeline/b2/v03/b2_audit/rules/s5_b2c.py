# vision_pipeline/b2/v03/b2_audit/rules/s5_b2c.py
"""
Step 5: B → C 通信验收规则
"""

from typing import Optional, Dict, Any
from rules.base import AuditRule


class NoOpNoCommunicationRule(AuditRule):
    """S5.B2C.002 — NO_OP 不得通信"""
    
    rule_id = "S5.B2C.002"
    description = "impact == NO_OP → to_c_message.sent == false"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            
            if impact != "NO_OP":
                continue
            
            to_c_message = t.get("to_c_message", {})
            sent = to_c_message.get("sent", False)
            
            if sent:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": "Impact NO_OP 但仍给 C 发消息",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "impact": impact,
                        "to_c_sent": sent
                    }
                }
        return None


class ForceAlertCanInterruptRule(AuditRule):
    """S5.B2C.003 — FORCE_ALERT 可打断"""
    
    rule_id = "S5.B2C.003"
    description = "FORCE_ALERT 必须标记为可打断"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact")
            
            if impact != "FORCE_ALERT":
                continue
            
            to_c_message = t.get("to_c_message", {})
            if not to_c_message.get("sent", False):
                continue  # 未发送，跳过检查
            
            # 检查 urgency（可能在 payload 中）
            payload = to_c_message.get("payload", {})
            urgency = payload.get("urgency") or to_c_message.get("urgency")
            
            if urgency and urgency.upper() not in ("IMMEDIATE", "FORCE", "URGENT"):
                return {
                    "rule_id": self.rule_id,
                    "status": "WARN",
                    "message": f"FORCE_ALERT 但 urgency 不是 IMMEDIATE: {urgency}",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "impact": impact,
                        "urgency": urgency
                    }
                }
        return None
