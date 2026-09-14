# vision_pipeline/b2/v03/b2_audit/rules/g_failfast.py
"""
全局 FAIL FAST 规则
"""

import json
from typing import Optional, Dict, Any
from rules.base import AuditRule


FORBIDDEN_KEYS = [
    "WORLD",
    "SCENE",
    "WORLD_SHIFT",
    "SCENE_CHANGE"
]


class WorldSemanticLeakRule(AuditRule):
    """G.FAIL.001 — 世界语义残留检测"""
    
    rule_id = "G.FAIL.001"
    description = "禁止世界/场景语义残留"
    
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(ctx.traces):
            # 将 trace 转为 JSON 字符串进行检查
            try:
                trace_str = json.dumps(t, ensure_ascii=False)
            except:
                trace_str = str(t)
            
            violations = []
            for key in FORBIDDEN_KEYS:
                if key in trace_str:
                    violations.append(key)
            
            if violations:
                return {
                    "rule_id": self.rule_id,
                    "status": "FAIL",
                    "message": f"发现禁止语义: {violations}",
                    "evidence": {
                        "trace_index": i,
                        "frame_id": t.get("time", {}).get("frame_id"),
                        "violations": violations
                    }
                }
        return None
