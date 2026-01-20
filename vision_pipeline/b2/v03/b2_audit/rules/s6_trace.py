# vision_pipeline/b2/v03/b2_audit/rules/s6_trace.py
"""
Step 6: Trace / Timeline 验收规则
"""

from typing import Optional, Dict, Any
from rules.base import AuditRule


class TimelineNoNoOpRule(AuditRule):
    """S6.TIMELINE.001 — Timeline 去噪"""
    
    rule_id = "S6.TIMELINE.001"
    description = "timeline 中禁止出现 impact == NO_OP"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        if not ctx.timeline:
            return None  # 无 timeline，跳过检查
        
        no_op_entries = []
        for i, entry in enumerate(ctx.timeline):
            impact = entry.get("impact") or entry.get("impact_eval", {}).get("impact")
            if impact == "NO_OP":
                no_op_entries.append({
                    "index": i,
                    "entry": entry
                })
        
        if no_op_entries:
            return {
                "rule_id": self.rule_id,
                "status": "FAIL",
                "message": f"Timeline 中发现 {len(no_op_entries)} 个 NO_OP 条目",
                "evidence": {
                    "no_op_entries": no_op_entries[:5]  # 只显示前 5 个
                }
            }
        return None
