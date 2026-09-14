# vision_pipeline/b2/v03/b2_audit/rules/s1_gate.py
"""
Step 1: Gate 验收规则
"""

from typing import Optional, Dict, Any
from rules.base import AuditRule


class GateMustExistRule(AuditRule):
    """S1.GATE.001 — Gate 是否为第一步"""
    
    rule_id = "S1.GATE.001"
    description = "每一条 trace 必须先经过 gate_eval"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            if "gate_eval" not in t:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": "gate_eval 缺失",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "human_time": t.get("time", {}).get("human_time")
                    }
                }
        return None


class GateModeValidityRule(AuditRule):
    """S1.GATE.002 — Gate Mode 合法性"""
    
    rule_id = "S1.GATE.002"
    description = "gate_eval.mode 必须是 SUSPENDED / READ_ONLY / ACTIVE"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        allowed_modes = {"SUSPENDED", "READ_ONLY", "ACTIVE"}
        
        for i, t in enumerate(ctx.traces):
            gate = t.get("gate_eval", {})
            if not gate:
                continue  # 由 GateMustExistRule 检查
            
            mode = gate.get("mode")
            if not mode:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": "gate_eval.mode 缺失",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id")
                    }
                }
            
            if mode not in allowed_modes:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"gate_eval.mode 非法值: {mode}",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "actual": mode,
                        "allowed": list(allowed_modes)
                    }
                }
        return None


class GateBlockConsistencyRule(AuditRule):
    """S1.GATE.003 — Gate 阻断一致性"""
    
    rule_id = "S1.GATE.003"
    description = "Gate=SUSPENDED 时禁止触发和通信"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            gate = t.get("gate_eval", {})
            if gate.get("mode") == "SUSPENDED":
                # 检查 trigger
                if t.get("trigger", {}).get("triggered"):
                    return {
                        "rule_id": self.rule_id,
                        "status": "FAIL",
                        "message": "Gate 挂起但仍触发 trigger",
                        "evidence": {
                            "trace_index": i,
                            "frame_id": t.get("time", {}).get("frame_id"),
                            "gate_mode": "SUSPENDED",
                            "trigger_triggered": True
                        }
                    }
                
                # 检查 to_c_message
                if t.get("to_c_message", {}).get("sent"):
                    return {
                        "rule_id": self.rule_id,
                        "status": "FAIL",
                        "message": "Gate 挂起但仍发送给 C",
                        "evidence": {
                            "trace_index": i,
                            "frame_id": t.get("time", {}).get("frame_id"),
                            "gate_mode": "SUSPENDED",
                            "to_c_sent": True
                        }
                    }
        return None


class GateDetailsCompletenessRule(AuditRule):
    """S1.GATE.004 — 抗视角污染字段完整性"""
    
    rule_id = "S1.GATE.004"
    description = "gate_eval.details 必须包含稳定性相关字段"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        required_fields = ["stability_score"]
        
        for i, t in enumerate(ctx.traces):
            gate = t.get("gate_eval", {})
            if not gate:
                continue
            
            details = gate.get("details", {})
            missing = [f for f in required_fields if f not in details]
            
            if missing:
                return {
                    "rule_id": self.rule_id,
                    "status": "WARN",
                    "message": f"gate_eval.details 缺少字段: {missing}",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "missing_fields": missing
                    }
                }
        return None
