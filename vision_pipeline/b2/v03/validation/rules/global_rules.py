# vision_pipeline/b2/v03/validation/rules/global_rules.py
"""
全局 FAIL FAST 规则
"""

from typing import Dict, Any, List, Tuple
import json
import re


def check_g_fail_001(trace: Dict[str, Any], trace_id: int) -> Tuple[str, str, Dict[str, Any]]:
    """
    G.FAIL.001 — 世界语义残留检测
    
    规则: trace / timeline 中禁止出现字段或值：
    WORLD
    SCENE
    WORLD_SHIFT
    SCENE_CHANGE
    """
    rule_id = "G.FAIL.001"
    forbidden_patterns = [
        r"WORLD",
        r"SCENE",
        r"WORLD_SHIFT",
        r"SCENE_CHANGE"
    ]
    
    # 将 trace 转为 JSON 字符串进行检查
    trace_str = json.dumps(trace, ensure_ascii=False)
    
    violations = []
    for pattern in forbidden_patterns:
        matches = re.findall(pattern, trace_str, re.IGNORECASE)
        if matches:
            violations.append({
                "pattern": pattern,
                "matches": matches
            })
    
    if violations:
        return "FAIL", f"发现世界语义残留: {violations}", {
            "trace_id": trace_id,
            "violations": violations
        }
    
    return "PASS", "无世界语义残留", {
        "trace_id": trace_id
    }


def get_all_global_rules():
    """获取所有全局规则检查函数"""
    return [
        check_g_fail_001,
    ]
