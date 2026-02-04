# vision_pipeline/b2/v03/b2_audit/rules/s2_evidence.py
"""
Step 2: Evidence 生命周期验收规则
"""

from typing import Optional, Dict, Any
from rules.base import AuditRule


class NoInstantEvidenceRule(AuditRule):
    """S2.EVIDENCE.001 — 禁止瞬时证据"""
    
    rule_id = "S2.EVIDENCE.001"
    description = "任何 impact != NO_OP 的 trace 必须至少有 1 条 evidence.state == CONFIRMED"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            
            if impact == "NO_OP":
                continue
            
            evidence_state = t.get("evidence_state", {})
            if not evidence_state:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"Impact {impact} 但无 evidence_state",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "impact": impact
                    }
                }
            
            # 检查是否有 CONFIRMED 证据
            has_confirmed = False
            for factor_key, evidence in evidence_state.items():
                if isinstance(evidence, dict) and evidence.get("state") == "CONFIRMED":
                    has_confirmed = True
                    break
            
            if not has_confirmed:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"Impact {impact} 但无 CONFIRMED 证据",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "impact": impact,
                        "evidence_states": [
                            e.get("state") if isinstance(e, dict) else None
                            for e in evidence_state.values()
                        ]
                    }
                }
        return None


class EvidenceStateValidityRule(AuditRule):
    """S2.EVIDENCE.002 — 生命周期合法性"""
    
    rule_id = "S2.EVIDENCE.002"
    description = "evidence.state 必须是 OBSERVING / CONFIRMED / DEGRADED / DROPPED"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        allowed_states = {"OBSERVING", "CONFIRMED", "DEGRADED", "DROPPED"}
        
        for i, t in enumerate(ctx.traces):
            evidence_state = t.get("evidence_state", {})
            if not evidence_state:
                continue
            
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
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"发现非法 evidence.state: {invalid_states}",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "invalid_states": invalid_states,
                        "allowed": list(allowed_states)
                    }
                }
        return None
