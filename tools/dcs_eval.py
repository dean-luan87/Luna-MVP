#!/usr/bin/env python3
"""
DCS 评估器

读取 trace.jsonl -> 输出 dcs_report.json，同时把 grade 写回事件用于 Viewer 展示
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, Any, List, Optional, Tuple

# 加载规则
RULES_FILE = Path(__file__).parent / "dcs_rules_v1.json"

DEFAULT_EVENT_TYPE = "tick"

def _get_event_type(ev: Dict[str, Any]) -> str:
    """
    v0.5: event_type in {"tick","GATE_RUNTIME_PROFILE","C_RUNTIME_PROFILE"}
    v0.4: may not have event_type -> treat as tick
    """
    return ev.get("event_type") or ev.get("type") or DEFAULT_EVENT_TYPE

def _rule_applies(rule: Dict[str, Any], event_type: str) -> bool:
    applies_to = rule.get("applies_to")
    if not applies_to:
        # Backward compatible: if not specified, assume tick-only to prevent runtime false RED
        return event_type == DEFAULT_EVENT_TYPE
    return event_type in applies_to

def safe_get(obj: Dict, path: str, default=None):
    """安全获取嵌套字段"""
    try:
        keys = path.split(".")
        val = obj
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
            if val is None:
                return default
        return val
    except:
        return default

def check_authority_violation(event: Dict) -> bool:
    """B 在 2m 内输出 NEED_STOP/NEED_DETOUR/INTERRUPT"""
    range_m = safe_get(event, "range_m") or safe_get(event, "gate.details.range_m")
    if range_m is None:
        return False
    if float(range_m) >= 2.0:
        return False
    
    impact = safe_get(event, "impact.impact") or safe_get(event, "impact")
    decision_level = safe_get(event, "impact.level") or safe_get(event, "decision.level")
    
    if impact in ["NEED_STOP", "NEED_DETOUR"]:
        return True
    if decision_level == "INTERRUPT":
        return True
    return False

def check_env_overreach(event: Dict) -> bool:
    """ENV 触发 CONDITION_CHANGE 或 INTERRUPT"""
    main_factor = safe_get(event, "factors.main_factor") or safe_get(event, "main_factor")
    if main_factor != "ENV":
        return False
    
    decision_level = safe_get(event, "impact.level") or safe_get(event, "decision.level")
    if decision_level in ["CONDITION_CHANGE", "INTERRUPT"]:
        return True
    return False

def check_no_op_timeline(event: Dict) -> bool:
    """impact=NO_OP 仍写入 timeline/decision"""
    impact = safe_get(event, "impact.impact") or safe_get(event, "impact")
    if impact != "NO_OP":
        return False
    
    writeback = safe_get(event, "writeback", {})
    if writeback.get("timeline") or writeback.get("decision"):
        return True
    return False

def check_missing_advisory(event: Dict) -> bool:
    """缺少 advisory_only=true（若字段存在则必须为 true）"""
    impact = safe_get(event, "impact", {})
    if isinstance(impact, dict):
        if "advisory_only" in impact and impact.get("advisory_only") is not True:
            return True
    return False

def check_missing_core_fields(event: Dict) -> bool:
    """
    缺少 engine_version/time/frame_id/impact 任一字段
    
    v0.5: Runtime Profile 事件不需要 impact 字段，跳过此检查
    """
    event_type = event.get("event_type", "tick")
    if event_type in ["GATE_RUNTIME_PROFILE", "C_RUNTIME_PROFILE"]:
        # Runtime Profile 不需要 impact 字段
        if not safe_get(event, "time"):
            return True
        if not safe_get(event, "time.frame_id") and not safe_get(event, "frame_id"):
            return True
        return False
    
    # Decision 事件需要所有字段
    if not safe_get(event, "engine_version") and not safe_get(event, "version"):
        return True
    if not safe_get(event, "time"):
        return True
    if not safe_get(event, "time.frame_id") and not safe_get(event, "frame_id"):
        return True
    if not safe_get(event, "impact"):
        return True
    return False

def check_over_prediction_language(event: Dict) -> bool:
    """human_interpretation 或 reasons 包含确认性词"""
    keywords = ["一定", "必然", "确认", "已发生", "confirmed", "certain", "inevitable"]
    
    human_interpretation = safe_get(event, "human_interpretation") or safe_get(event, "trace_explain.human_interpretation", "")
    reason = safe_get(event, "reason") or safe_get(event, "gate.reason", "")
    
    text = (str(human_interpretation) + " " + str(reason)).lower()
    for kw in keywords:
        if kw.lower() in text:
            return True
    return False

def check_gate_suspended_but_output(event: Dict) -> bool:
    """Gate=SUSPENDED 仍出现 decision/timeline/to_c_message"""
    gate_mode = safe_get(event, "gate.mode") or safe_get(event, "gate_eval.mode")
    if gate_mode != "SUSPENDED":
        return False
    
    writeback = safe_get(event, "writeback", {})
    to_c = safe_get(event, "to_c", {})
    
    if writeback.get("timeline") or writeback.get("decision"):
        return True
    if to_c.get("send"):
        return True
    return False

def check_missing_view_state_but_active(event: Dict) -> bool:
    """
    Gate 进入 ACTIVE 但 trace 中缺少 view_state，违反视角前提假设
    
    规则：如果 gate.mode == "ACTIVE"，则必须存在有效的 view_state
    检查：
    1. view_state 字段存在
    2. view_state.stability_score 存在（或至少 view_state 不是空字典）
    """
    gate_mode = safe_get(event, "gate.mode") or safe_get(event, "gate_eval.mode")
    if gate_mode != "ACTIVE":
        return False
    
    # 检查 view_state 是否存在
    view_state = safe_get(event, "view_state")
    if view_state is None:
        return True  # 缺少 view_state
    
    # 如果 view_state 是空字典或缺少关键字段，也视为违规
    if isinstance(view_state, dict):
        # 检查是否有稳定性相关字段（至少应该有一个）
        if not view_state or "stability_score" not in view_state:
            # 如果 view_state 存在但为空，或者缺少 stability_score，视为违规
            # 但允许其他字段存在（如 camera_motion, camera_pose 等）
            # 这里我们检查：如果 view_state 是空字典，或者只有非关键字段，则违规
            if not view_state or (len(view_state) == 0):
                return True
    
    return False

# ============================================================
# v0.5 DCS Rules – Gate Runtime Scheduling
# ============================================================

def check_gate_suspended_but_b_executed(event: Dict) -> bool:
    """
    R1: Gate=SUSPENDED 但 B 仍执行了任意感知/判断/输出逻辑
    """
    gate_mode = safe_get(event, "gate.mode") or safe_get(event, "gate_eval.mode") or safe_get(event, "gate_mode")
    if gate_mode != "SUSPENDED":
        return False
    
    # 检查是否有 B 的输出
    impact = safe_get(event, "impact") or safe_get(event, "impact.impact")
    summary = safe_get(event, "summary")
    to_c_send = safe_get(event, "to_c.send") or safe_get(event, "to_c_message.sent")
    
    if impact or summary or to_c_send:
        return True
    
    return False

def check_compute_none_but_output_exists(event: Dict) -> bool:
    """
    R2: runtime_profile.compute_level == NONE 但存在任何 B summary/impact/trace 输出
    """
    runtime_profile = safe_get(event, "runtime_profile") or safe_get(event, "gate.runtime_profile")
    if not isinstance(runtime_profile, dict):
        return False
    
    compute_level = runtime_profile.get("compute_level")
    if compute_level != "NONE":
        return False
    
    # 检查是否有输出
    impact = safe_get(event, "impact") or safe_get(event, "impact.impact")
    summary = safe_get(event, "summary")
    
    if impact or summary:
        return True
    
    return False

def check_future_probe_enabled_in_v05(event: Dict) -> bool:
    """
    R4: runtime_profile.allow_future_probe == true（v0.5 明确禁止）
    """
    runtime_profile = safe_get(event, "runtime_profile") or safe_get(event, "gate.runtime_profile")
    if not isinstance(runtime_profile, dict):
        return False
    
    allow_future_probe = runtime_profile.get("allow_future_probe")
    if allow_future_probe is True:
        return True
    
    return False

def check_gate_profile_missing(event: Dict) -> bool:
    """
    R5: B trace/runtime 中缺失 gate_runtime_profile
    
    v0.5: Runtime Profile 事件本身包含 gate_runtime_profile，不需要额外检查
    """
    event_type = event.get("event_type", "tick")
    if event_type == "GATE_RUNTIME_PROFILE":
        # GATE_RUNTIME_PROFILE 事件本身包含 gate_runtime_profile 字段
        if not safe_get(event, "gate_runtime_profile"):
            return True
        return False
    
    # Decision 事件需要检查 gate.runtime_profile
    runtime_profile = safe_get(event, "runtime_profile") or safe_get(event, "gate.runtime_profile")
    if runtime_profile is None:
        return True
    
    return False

def check_read_only_but_heavy_compute(event: Dict) -> bool:
    """
    Y1: gate_mode == READ_ONLY 但 runtime_profile.compute_level == FULL
    """
    gate_mode = safe_get(event, "gate.mode") or safe_get(event, "gate_eval.mode") or safe_get(event, "gate_mode")
    if gate_mode != "READ_ONLY":
        return False
    
    runtime_profile = safe_get(event, "runtime_profile") or safe_get(event, "gate.runtime_profile")
    if not isinstance(runtime_profile, dict):
        return False
    
    compute_level = runtime_profile.get("compute_level")
    if compute_level == "FULL":
        return True
    
    return False

def check_gate_blocked_reason_missing(event: Dict) -> bool:
    """
    Y3: gate_mode != ACTIVE 但 blocked_by == null
    
    v0.5: 支持 GATE_RUNTIME_PROFILE 事件格式
    """
    event_type = event.get("event_type", "tick")
    
    # 从不同格式提取 gate_mode
    if event_type == "GATE_RUNTIME_PROFILE":
        gate_runtime_profile = safe_get(event, "gate_runtime_profile", {})
        gate_mode = gate_runtime_profile.get("gate_mode") or gate_runtime_profile.get("mode")
        blocked_by = gate_runtime_profile.get("blocked_by")
    else:
        gate_mode = safe_get(event, "gate.mode") or safe_get(event, "gate.gate_mode") or safe_get(event, "gate_eval.mode") or safe_get(event, "gate_mode")
        blocked_by = safe_get(event, "gate.blocked_by") or safe_get(event, "gate_eval.blocked_by")
    
    if gate_mode == "ACTIVE":
        return False
    
    if blocked_by is None:
        return True
    
    return False

def load_rules(path: str) -> Dict[str, Any]:
    """加载 DCS 规则"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_jsonl(path: str) -> List[Dict[str, Any]]:
    """读取 JSONL 文件"""
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out

def evaluate_event(ev: Dict[str, Any], rules: Dict[str, Any]) -> Tuple[str, List[str]]:
    """
    评估单个事件，返回 (status, violations)
    
    v0.5: 按 event_type 分流，规则按 applies_to 作用域生效
    """
    violations: List[str] = []
    event_type = _get_event_type(ev)
    
    for rule in rules.get("rules", []):
        if not rule.get("enabled", True):
            continue
        if not _rule_applies(rule, event_type):
            continue
        rid = rule["id"]
        
        # 新增规则：no_gate_runtime_profile
        if rid == "no_gate_runtime_profile":
            # Only for GATE_RUNTIME_PROFILE
            gate_info = ev.get("gate_runtime_profile") or ev.get("gate")
            if gate_info is None:
                violations.append(rid)
            continue
        
        # 新增规则：no_c_runtime_profile
        if rid == "no_c_runtime_profile":
            # Only for C_RUNTIME_PROFILE
            c_info = ev.get("c_runtime_profile") or ev.get("c")
            if c_info is None:
                violations.append(rid)
            continue
        
        # 原有的规则检查逻辑（保持兼容）
        # 注意：这些规则现在只会在 applies_to 匹配时执行
        
        # 对于 tick 事件的规则检查
        if rid == "authority_violation" and check_authority_violation(ev):
            violations.append(rid)
        elif rid == "env_overreach" and check_env_overreach(ev):
            violations.append(rid)
        elif rid == "no_op_timeline" and check_no_op_timeline(ev):
            violations.append(rid)
        elif rid == "over_prediction_language" and check_over_prediction_language(ev):
            violations.append(rid)
        elif rid == "gate_suspended_but_output" and check_gate_suspended_but_output(ev):
            violations.append(rid)
        elif rid == "missing_view_state_but_active" and check_missing_view_state_but_active(ev):
            violations.append(rid)
        elif rid == "gate_suspended_but_b_executed" and check_gate_suspended_but_b_executed(ev):
            violations.append(rid)
        elif rid == "compute_none_but_output_exists" and check_compute_none_but_output_exists(ev):
            violations.append(rid)
        elif rid == "future_probe_enabled_in_v05" and check_future_probe_enabled_in_v05(ev):
            violations.append(rid)
        elif rid == "read_only_but_heavy_compute" and check_read_only_but_heavy_compute(ev):
            violations.append(rid)
        elif rid == "gate_blocked_reason_missing" and check_gate_blocked_reason_missing(ev):
            violations.append(rid)
        elif rid == "gate_profile_missing" and check_gate_profile_missing(ev):
            violations.append(rid)
        elif rid == "missing_advisory" and check_missing_advisory(ev):
            violations.append(rid)
        elif rid == "missing_core_fields" and check_missing_core_fields(ev):
            violations.append(rid)
        # 其他规则可以继续添加...
    
    # v0.5 Patch B: 对 tick 的 NO_OP 直接 SKIP
    if event_type == "tick":
        impact = safe_get(ev, "impact.impact") or safe_get(ev, "impact") or safe_get(ev, "impact_evaluation.impact")
        if isinstance(impact, str) and impact == "NO_OP":
            return "GREEN", []
    
    # 确定 status
    def _is_red(v: str, rules: Dict) -> bool:
        for r in rules.get("rules", []):
            if r.get("id") == v:
                return r.get("severity") == "RED" or r.get("level") == "RED"
        return False
    
    def _is_yellow(v: str, rules: Dict) -> bool:
        for r in rules.get("rules", []):
            if r.get("id") == v:
                return r.get("severity") == "YELLOW" or r.get("level") == "YELLOW"
        return False
    
    if any(_is_red(v, rules) for v in violations):
        return "RED", violations
    if any(_is_yellow(v, rules) for v in violations):
        return "YELLOW", violations
    return "GREEN", violations

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/dcs_eval.py <trace.jsonl> [rules.json]")
        sys.exit(1)
    
    trace_path = sys.argv[1]
    rules_path = sys.argv[2] if len(sys.argv) >= 3 else str(RULES_FILE)
    rules = load_rules(rules_path)
    events = read_jsonl(trace_path)
    
    counts = Counter()
    vio_counts = Counter()
    enriched_path = "artifacts/trace_enriched.jsonl"
    Path(enriched_path).parent.mkdir(parents=True, exist_ok=True)
    red_samples = []
    
    with open(enriched_path, "w", encoding="utf-8") as out:
        for ev in events:
            et = _get_event_type(ev)
            status, vios = evaluate_event(ev, rules)
            counts[status] += 1
            for v in vios:
                vio_counts[v] += 1
            
            ev2 = dict(ev)
            ev2["event_type"] = et
            ev2["dcs"] = {"status": status, "violations": vios}
            out.write(json.dumps(ev2, ensure_ascii=False) + "\n")
            
            if status == "RED" and len(red_samples) < 10:
                red_samples.append(ev2)
    
    # 输出报告
    print("=" * 60)
    print("DCS Evaluation Report")
    print("=" * 60)
    print(f"\nTotal events: {len(events)}")
    print(f"\nStatus distribution:")
    for status in ["RED", "YELLOW", "GREEN"]:
        count = counts.get(status, 0)
        pct = (count / len(events) * 100) if events else 0
        icon = "🔴" if status == "RED" else ("🟨" if status == "YELLOW" else "🟩")
        print(f"  {icon} {status}: {count} ({pct:.1f}%)")
    
    if vio_counts:
        print(f"\nTop violations:")
        for v, c in vio_counts.most_common(10):
            print(f"  - {v}: {c}")
    
    if red_samples:
        print(f"\nRED sample events (first 3):")
        for i, ev in enumerate(red_samples[:3], 1):
            print(f"  {i}. {ev.get('event_type', 'unknown')} - {ev.get('dcs', {}).get('violations', [])}")
    
    print(f"\nEnriched trace saved to: {enriched_path}")

if __name__ == "__main__":
    main()
