# vision_pipeline/b2/v03/b2_audit/rules/bc_boundary_rules.py
"""
B/C Boundary Rules for DCS
Maps the 7 boundary assumptions to DCS scoring rules
"""

from typing import Optional, Dict, Any
from rules.base import AuditRule
import re


class R1FrequencyAlignmentRule(AuditRule):
    """R1: Frequency Mismatch Is Intentional"""
    
    rule_id = "R1.FREQUENCY"
    description = "B and C must operate at different frequencies with shared reference"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        # Check B code for real-time actions
        # Check C code for future prediction
        # This is a code-level check, so we check trace for violations
        
        violations = []
        for i, t in enumerate(ctx.traces):
            # Check if B is attempting real-time actions
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            
            # B should not have immediate/real-time semantics
            to_c_message = t.get("to_c_message", {})
            if to_c_message.get("sent"):
                payload = to_c_message.get("payload", {})
                urgency = payload.get("urgency", "").upper()
                if urgency in ("IMMEDIATE", "REAL_TIME", "URGENT"):
                    violations.append({
                        "trace_index": i,
                        "violation": "B attempting real-time action",
                        "evidence": urgency
                    })
        
        if violations:
            return {
                "rule_id": self.rule_id,
                "status": "FAIL",
                "message": f"B attempting real-time actions: {len(violations)} violations",
                "evidence": {
                    "violations": violations[:5]  # First 5
                }
            }
        return None


class R2NoSelfWakeupRule(AuditRule):
    """R2: B Is System-Awakened, Not Self-Driven"""
    
    rule_id = "R2.SELF_WAKEUP"
    description = "B must not contain self-trigger or auto-wake logic"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        # This is primarily a code-level check
        # For trace-level, we check if B is making decisions about when to run
        
        # Check for B making "should I run" decisions
        for i, t in enumerate(ctx.traces):
            gate_eval = t.get("gate_eval", {})
            mode = gate_eval.get("mode", "")
            reason = gate_eval.get("reason", "").lower()
            
            # B should not decide to wake itself
            if "self" in reason and ("wake" in reason or "trigger" in reason):
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": "B contains self-wakeup logic",
                    "evidence": {
                        "trace_index": i,
                        "gate_reason": reason
                    }
                }
        
        return None


class R3NoRiskConfirmationRule(AuditRule):
    """R3: B Never Confirms Risk, Only Signals It"""
    
    rule_id = "R3.RISK_CONFIRMATION"
    description = "B must not use confirmed/verified/must language"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        forbidden_words = ["confirmed", "verified", "must", "enforce", "guaranteed"]
        
        violations = []
        for i, t in enumerate(ctx.traces):
            # Check to_c_message
            to_c_message = t.get("to_c_message", {})
            if to_c_message.get("sent"):
                payload = to_c_message.get("payload", {})
                payload_str = str(payload).lower()
                
                for word in forbidden_words:
                    if word in payload_str:
                        violations.append({
                            "trace_index": i,
                            "forbidden_word": word,
                            "context": payload_str[:100]
                        })
            
            # Check human_explanation
            human_explain = t.get("human_interpretation", {})
            explain_str = str(human_explain).lower()
            
            for word in forbidden_words:
                if word in explain_str:
                    violations.append({
                        "trace_index": i,
                        "forbidden_word": word,
                        "context": "human_explanation"
                    })
        
        if violations:
            return {
                "rule_id": self.rule_id,
                "status": "FAIL",
                "message": f"B using forbidden confirmation language: {len(violations)} violations",
                "evidence": {
                    "violations": violations[:5]
                }
            }
        return None


class R4ConservativeCAcceptableRule(AuditRule):
    """R4: Conservative C Is Acceptable in Early Phases"""
    
    rule_id = "R4.CONSERVATIVE_C"
    description = "C may be overly conservative - this is acceptable"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        # This is a LOW penalty rule - we don't want to penalize conservative C
        # Actually, we should NOT fail on this - it's acceptable
        # So we return None (PASS)
        return None


class R5SilenceNoExplanationRule(AuditRule):
    """R5: Silence Requires No Immediate Explanation"""
    
    rule_id = "R5.SILENCE"
    description = "NO_OP must not force user explanation"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        violations = []
        for i, t in enumerate(ctx.traces):
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            
            if impact == "NO_OP":
                # Check if NO_OP is forcing explanation
                to_c_message = t.get("to_c_message", {})
                if to_c_message.get("sent"):
                    violations.append({
                        "trace_index": i,
                        "violation": "NO_OP sending message to C"
                    })
                
                # Check if timeline is written (should not be)
                writeback = t.get("writeback", {})
                if writeback.get("timeline_written"):
                    violations.append({
                        "trace_index": i,
                        "violation": "NO_OP written to timeline"
                    })
        
        if violations:
            return {
                "rule_id": self.rule_id,
                "status": "FAIL",
                "message": f"NO_OP forcing explanation: {len(violations)} violations",
                "evidence": {
                    "violations": violations[:5]
                }
            }
        return None


class R6SystemTimeOnlyRule(AuditRule):
    """R6: System Time Is the Only Time"""
    
    rule_id = "R6.TIME"
    description = "All B-C communication must use system time only"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        forbidden_time_sources = ["camera_time", "perception_time", "external_timestamp", "video_timestamp"]
        
        violations = []
        for i, t in enumerate(ctx.traces):
            time_info = t.get("time", {})
            to_c_message = t.get("to_c_message", {})
            
            if to_c_message.get("sent"):
                header = to_c_message.get("payload", {}).get("header", {})
                
                # Check if system_ts exists
                if "system_ts" not in header and "ts" not in header:
                    violations.append({
                        "trace_index": i,
                        "violation": "Missing system_ts in B→C message"
                    })
                
                # Check for forbidden time sources
                for forbidden in forbidden_time_sources:
                    if forbidden in str(header).lower():
                        violations.append({
                            "trace_index": i,
                            "violation": f"Using forbidden time source: {forbidden}"
                        })
        
        if violations:
            return {
                "rule_id": self.rule_id,
                "status": "FAIL",
                "message": f"Time authority violation: {len(violations)} violations",
                "evidence": {
                    "violations": violations[:5]
                }
            }
        return None


class R7EvolutionDirectionRule(AuditRule):
    """R7: B and C Evolve Orthogonally"""
    
    rule_id = "R7.EVOLUTION"
    description = "B and C must not substitute capabilities or escalate authority"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        # This is primarily a code-level check
        # For trace-level, we check for capability substitution patterns
        
        violations = []
        for i, t in enumerate(ctx.traces):
            # Check if B is doing real-time precision (C's job)
            impact_eval = t.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            
            # B should not have immediate execution semantics
            if impact in ("NEED_STOP", "FORCE_ALERT"):
                to_c_message = t.get("to_c_message", {})
                if to_c_message.get("sent"):
                    payload = to_c_message.get("payload", {})
                    # Check if B is trying to execute (C's job)
                    if "execute" in str(payload).lower() or "immediate" in str(payload).lower():
                        violations.append({
                            "trace_index": i,
                            "violation": "B attempting execution (C's capability)"
                        })
        
        if violations:
            return {
                "rule_id": self.rule_id,
                "status": "WARN",  # Warning, not fail, as this is evolutionary
                "message": f"Potential capability substitution: {len(violations)} cases",
                "evidence": {
                    "violations": violations[:5]
                }
            }
        return None


def get_all_boundary_rules():
    """获取所有 B/C 边界规则"""
    return [
        R1FrequencyAlignmentRule(),
        R2NoSelfWakeupRule(),
        R3NoRiskConfirmationRule(),
        R4ConservativeCAcceptableRule(),
        R5SilenceNoExplanationRule(),
        R6SystemTimeOnlyRule(),
        R7EvolutionDirectionRule(),
    ]
