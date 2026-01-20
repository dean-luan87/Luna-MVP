# vision_pipeline/b2/v03/b2_audit/rules/s3_trigger.py
"""
Step 3: Trigger 验收规则
"""

from typing import Optional, Dict, Any
from rules.base import AuditRule


class TriggerMustExistRule(AuditRule):
    """S3.TRIGGER.001 — Trigger 显式存在"""
    
    rule_id = "S3.TRIGGER.001"
    description = "每一条 trace 必须包含 trigger 字段"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            if "trigger" not in t:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": "trace 中无 trigger 字段",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id")
                    }
                }
        return None


class GateControlsTriggerRule(AuditRule):
    """S3.TRIGGER.002 — Gate 控制 Trigger"""
    
    rule_id = "S3.TRIGGER.002"
    description = "Gate != ACTIVE 时，trigger.triggered 必须为 false"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            gate = t.get("gate_eval", {})
            trigger = t.get("trigger", {})
            
            if not gate or not trigger:
                continue
            
            gate_mode = gate.get("mode")
            trigger_triggered = trigger.get("triggered", False)
            
            if gate_mode != "ACTIVE" and trigger_triggered:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"Gate Mode {gate_mode} 但仍触发 Trigger",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "gate_mode": gate_mode,
                        "trigger_triggered": trigger_triggered
                    }
                }
        return None
