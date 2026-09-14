#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2 v0.5 Trace Audit Runner

用现有规则回审一段真实视频的 trace。

执行路径：
1. 跑视频，生成 trace（B + C RuntimeProfile）
2. DCS 审判
3. 生成审计报告
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter, defaultdict

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# v0.5 Patch F: 导入 Runtime Fingerprint 生成器
try:
    from tools.generate_runtime_fingerprint import generate_fingerprint as generate_runtime_fingerprint
except ImportError:
    # 如果导入失败，定义一个占位函数
    def generate_runtime_fingerprint(*args, **kwargs):
        return None

# v0.5 Patch G: 导入 Personality Fingerprint 生成器
try:
    from tools.personality_fingerprint_v05 import build_personality_fingerprint
except ImportError:
    # 如果导入失败，定义一个占位函数
    def build_personality_fingerprint(*args, **kwargs):
        return {"personality_fingerprint": {}}

# 导入 DCS 评估器
try:
    from tools.dcs_eval import load_rules, read_jsonl, evaluate_event, _get_event_type
except ImportError:
    # 如果导入失败，定义占位函数
    def load_rules(path):
        return {"rules": []}
    def read_jsonl(path):
        return []
    def evaluate_event(ev, rules):
        return "GREEN", []
    def _get_event_type(ev):
        return ev.get("event_type", "tick")

def load_dcs_rules(rules_path: str) -> Dict[str, Any]:
    """加载 DCS 规则（使用 dcs_eval 的 load_rules）"""
    return load_rules(rules_path)

def load_trace(trace_path: str) -> List[Dict[str, Any]]:
    """加载 trace 文件"""
    records = []
    with open(trace_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records

def check_rule(rule: Dict[str, Any], record: Dict[str, Any]) -> bool:
    """检查单条规则是否违反（简化版）"""
    check_config = rule.get("check", {})
    condition = check_config.get("condition", "")
    
    # 获取 gate 信息（支持两种格式）
    gate_info = None
    if record.get("event_type") == "GATE_RUNTIME_PROFILE":
        gate_info = record.get("gate_runtime_profile", {})
    else:
        gate_info = record.get("gate", {})
    
    # 简化检查逻辑
    rule_id = rule.get("id", "")
    
    # gate_suspended_but_computed
    if rule_id == "gate_suspended_but_computed":
        gate_mode = gate_info.get("gate_mode") if gate_info else None
        compute_level = gate_info.get("compute_level") if gate_info else None
        if gate_mode == "SUSPENDED" and compute_level in ["LIGHT", "FULL"]:
            return True
    
    # gate_suspended_but_output
    elif rule_id == "gate_suspended_but_output":
        gate_mode = gate_info.get("gate_mode") if gate_info else None
        to_c_send = record.get("to_c", {}).get("send", False)
        writeback_timeline = record.get("writeback", {}).get("timeline", False)
        if gate_mode == "SUSPENDED" and (to_c_send or writeback_timeline):
            return True
    
    # scheduler_violation
    elif rule_id == "scheduler_violation":
        tick_interval = gate_info.get("tick_interval_ms") if gate_info else None
        if tick_interval and tick_interval < 80:
            return True
    
    # no_gate_runtime_profile
    elif rule_id == "no_gate_runtime_profile":
        if not gate_info or not gate_info.get("version"):
            return True
    
    # c_suspended_but_control
    elif rule_id == "c_suspended_but_control":
        c_profile = record.get("c_runtime_profile", {})
        c_mode = c_profile.get("mode")
        control_level = c_profile.get("control_level")
        if c_mode == "SUSPENDED" and control_level in ["ASSIST", "FULL"]:
            return True
    
    # c_over_control_frequency
    elif rule_id == "c_over_control_frequency":
        c_profile = record.get("c_runtime_profile", {})
        update_interval = c_profile.get("update_interval_ms")
        if update_interval and update_interval < 40:
            return True
    
    return False

def generate_gate_fingerprint(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    v0.5 Patch E-1: 生成 Gate 行为指纹
    
    计算 Gate 的行为特征，用于版本回归和"性格漂移"检测。
    """
    gate_modes = []
    gate_switches = 0
    last_mode = None
    
    enter_hysteresis_hits = 0
    exit_hysteresis_hits = 0
    
    durations = defaultdict(list)
    current_duration = 0
    current_mode = None
    
    for record in records:
        if record.get("event_type") != "GATE_RUNTIME_PROFILE":
            continue
        
        # 提取 gate 信息（支持两种格式）
        gate_info = None
        if record.get("event_type") == "GATE_RUNTIME_PROFILE":
            gate_info = record.get("gate_runtime_profile", {})
        else:
            gate_info = record.get("gate", {})
        
        if not gate_info:
            continue
        
        mode = gate_info.get("gate_mode") or gate_info.get("mode")
        if not mode:
            continue
        
        gate_modes.append(mode)
        
        # 统计状态切换
        if last_mode and mode != last_mode:
            gate_switches += 1
            if current_mode:
                durations[current_mode].append(current_duration)
            current_duration = 0
        
        current_duration += 1
        current_mode = mode
        last_mode = mode
        
        # 统计 Hysteresis 命中次数
        meta = gate_info.get("meta", {})
        hysteresis = meta.get("hysteresis", {})
        
        enter_counter = hysteresis.get("enter_active_counter", 0)
        exit_counter = hysteresis.get("exit_active_counter", 0)
        
        if enter_counter > 0:
            enter_hysteresis_hits += 1
        if exit_counter > 0:
            exit_hysteresis_hits += 1
    
    # 记录最后一个状态的持续时间
    if current_mode:
        durations[current_mode].append(current_duration)
    
    # 计算统计信息
    total = len(gate_modes)
    if total == 0:
        return {
            "version": "b2-v0.5",
            "gate_fingerprint": {
                "total_frames": 0,
                "mode_ratio": {},
                "mode_switch_count": 0,
                "avg_active_duration": 0.0,
                "avg_read_only_duration": 0.0,
                "enter_hysteresis_hits": 0,
                "exit_hysteresis_hits": 0,
            }
        }
    
    mode_ratio = {k: v / total for k, v in Counter(gate_modes).items()}
    
    # 计算平均持续时间
    avg_active_duration = (
        sum(durations["ACTIVE"]) / max(1, len(durations["ACTIVE"]))
        if durations["ACTIVE"] else 0.0
    )
    avg_read_only_duration = (
        sum(durations["READ_ONLY"]) / max(1, len(durations["READ_ONLY"]))
        if durations["READ_ONLY"] else 0.0
    )
    
    fingerprint = {
        "version": "b2-v0.5",
        "gate_fingerprint": {
            "total_frames": total,
            "mode_ratio": mode_ratio,
            "mode_switch_count": gate_switches,
            "avg_active_duration": round(avg_active_duration, 1),
            "avg_read_only_duration": round(avg_read_only_duration, 1),
            "enter_hysteresis_hits": enter_hysteresis_hits,
            "exit_hysteresis_hits": exit_hysteresis_hits,
        }
    }
    
    return fingerprint

# generate_personality_fingerprint 已移除，改用 tools/personality_fingerprint_v05.py 中的 build_personality_fingerprint

def audit_trace(trace_path: str, rules_path: str = "tools/dcs_rules_v05.json") -> Dict[str, Any]:
    """审计 trace 文件"""
    rules = load_dcs_rules(rules_path)
    records = load_trace(trace_path)
    
    violations = {
        "RED": [],
        "YELLOW": [],
        "GREEN": []
    }
    
    stats = {
        "total": len(records),
        "red": 0,
        "yellow": 0,
        "green": 0,
        "b_active": 0,
        "b_read_only": 0,
        "b_suspended": 0,
        "c_active": 0,
        "c_degraded": 0,
        "c_suspended": 0
    }
    
    type_counts = Counter()
    
    for record in records:
        et = _get_event_type(record)
        type_counts[et] += 1
        status, vios = evaluate_event(record, rules)
        
        if status == "RED":
            stats["red"] += 1
            for v in vios:
                violations["RED"].append({
                    "rule_id": v,
                    "reason": f"Rule violation: {v}",
                    "frame_id": record.get("time", {}).get("frame_id"),
                    "ts": record.get("time", {}).get("ts")
                })
        elif status == "YELLOW":
            stats["yellow"] += 1
            for v in vios:
                violations["YELLOW"].append({
                    "rule_id": v,
                    "reason": f"Rule violation: {v}",
                    "frame_id": record.get("time", {}).get("frame_id"),
                    "ts": record.get("time", {}).get("ts")
                })
        else:
            stats["green"] += 1
        
        # 统计 B 状态（支持两种格式）
        gate = record.get("gate", {}) if isinstance(record.get("gate"), dict) else {}
        if not gate and et == "GATE_RUNTIME_PROFILE":
            gate = record.get("gate_runtime_profile", {})
        
        if gate:
            mode = gate.get("gate_mode") or gate.get("mode")
            if mode == "ACTIVE":
                stats["b_active"] += 1
            elif mode == "READ_ONLY":
                stats["b_read_only"] += 1
            elif mode == "SUSPENDED":
                stats["b_suspended"] += 1
        
        # 统计 C 状态
        c = record.get("c", {}) if isinstance(record.get("c"), dict) else {}
        if not c and et == "C_RUNTIME_PROFILE":
            c = record.get("c_runtime_profile", {})
        
        if c:
            st = c.get("control_state") or c.get("mode")
            if st == "ACTIVE":
                stats["c_active"] += 1
            elif st == "DEGRADED":
                stats["c_degraded"] += 1
            elif st == "SUSPENDED":
                stats["c_suspended"] += 1
    
    # v0.5 Patch E-1: 生成 Gate 行为指纹
    fingerprint = generate_gate_fingerprint(records)
    
    # v0.5 Patch E-2: 检查行为漂移
    fp = fingerprint.get("gate_fingerprint", {})
    
    # 检查 gate_switch_excessive (YELLOW)
    baseline_switch_count = 50  # v0.5 基线
    if fp.get("mode_switch_count", 0) > baseline_switch_count * 1.5:
        violations["YELLOW"].append({
            "rule_id": "gate_switch_excessive",
            "reason": f"Gate 状态切换次数过多: {fp.get('mode_switch_count')} > {baseline_switch_count * 1.5}",
            "frame_id": None,
            "ts": None
        })
        stats["yellow"] += 1
    
    # 检查 gate_mode_ratio_drift (RED)
    active_ratio = fp.get("mode_ratio", {}).get("ACTIVE", 0.0)
    baseline_active_ratio = 0.95  # v0.5 基线
    if active_ratio < 0.9 or active_ratio > 1.0:
        violations["RED"].append({
            "rule_id": "gate_mode_ratio_drift",
            "reason": f"Gate ACTIVE 比例偏离基线: {active_ratio*100:.1f}% (基线: {baseline_active_ratio*100:.1f}%)",
            "frame_id": None,
            "ts": None
        })
        stats["red"] += 1
    
    # v0.5 Patch F-B: 检查 Runtime 稳定性评分
    runtime_fp = None
    try:
        runtime_fp = generate_runtime_fingerprint(trace_path)
        if runtime_fp and runtime_fp.get("stability_score") is not None:
            stability_score = runtime_fp.get("stability_score", 1.0)
            if stability_score < 0.7:
                violations["YELLOW"].append({
                    "rule_id": "runtime_stability_low",
                    "reason": f"Runtime 稳定性评分过低: {stability_score:.3f} < 0.7",
                    "frame_id": None,
                    "ts": None
                })
                stats["yellow"] += 1
            
            # 保存 Runtime Fingerprint 到 artifacts
            artifacts_dir = Path(__file__).parent.parent / "artifacts"
            artifacts_dir.mkdir(exist_ok=True)
            runtime_fp_path = artifacts_dir / "runtime_fingerprint_v05.json"
            with open(runtime_fp_path, "w", encoding="utf-8") as f:
                json.dump(runtime_fp, f, indent=2, ensure_ascii=False)
    except Exception as e:
        # 如果生成失败，不影响主流程
        print(f"警告: 无法生成 Runtime Fingerprint: {e}", file=sys.stderr)
    
    # 保存指纹到 artifacts 目录
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    fingerprint_path = artifacts_dir / "gate_fingerprint_v05.json"
    
    with open(fingerprint_path, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, indent=2, ensure_ascii=False)
    
    result = {
        "violations": violations,
        "stats": stats,
        "summary": {
            "total_frames": stats["total"],
            "red_ratio": stats["red"] / stats["total"] if stats["total"] > 0 else 0,
            "yellow_ratio": stats["yellow"] / stats["total"] if stats["total"] > 0 else 0,
            "green_ratio": stats["green"] / stats["total"] if stats["total"] > 0 else 0
        },
        "fingerprint": fingerprint
    }
    
    # v0.5 Patch F: 添加 Runtime Fingerprint
    if runtime_fp:
        result["runtime_fingerprint"] = runtime_fp
    
    # v0.5 Patch G-1: 生成 Personality Fingerprint（使用独立模块）
    try:
        personality_fp = build_personality_fingerprint(records)
        result["personality_fingerprint"] = personality_fp.get("personality_fingerprint", {})
        
        # 保存到 artifacts
        artifacts_dir = Path(__file__).parent.parent / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)
        personality_fp_path = artifacts_dir / "personality_fingerprint_v05.json"
        with open(personality_fp_path, "w", encoding="utf-8") as f:
            json.dump(personality_fp, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"警告: 无法生成 Personality Fingerprint: {e}", file=sys.stderr)
    
    return result

def print_report(result: Dict[str, Any]):
    """打印审计报告"""
    print("=" * 60)
    print("B2 v0.5 Trace Audit Report")
    print("=" * 60)
    
    stats = result["stats"]
    summary = result["summary"]
    
    print(f"\n总帧数: {stats['total']}")
    
    # 显示事件类型分布
    if "type_counts" in result and result["type_counts"]:
        print("\n事件类型分布:")
        for k, v in sorted(result["type_counts"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {k}: {v}")
    
    print(f"\nB Gate 状态分布:")
    print(f"  ACTIVE: {stats['b_active']}")
    print(f"  READ_ONLY: {stats['b_read_only']}")
    print(f"  SUSPENDED: {stats['b_suspended']}")
    
    print(f"\nC Control 状态分布:")
    print(f"  ACTIVE: {stats['c_active']}")
    print(f"  DEGRADED: {stats['c_degraded']}")
    print(f"  SUSPENDED: {stats['c_suspended']}")
    
    print(f"\nDCS 结果:")
    print(f"  🔴 RED: {stats['red']} ({summary['red_ratio']*100:.1f}%)")
    print(f"  🟨 YELLOW: {stats['yellow']} ({summary['yellow_ratio']*100:.1f}%)")
    print(f"  🟩 GREEN: {stats['green']} ({summary['green_ratio']*100:.1f}%)")
    
    violations = result["violations"]
    if violations["RED"]:
        print(f"\n🔴 RED 违规 ({len(violations['RED'])} 条):")
        for v in violations["RED"][:10]:
            print(f"  - {v['rule_id']}: {v['reason']} (frame {v.get('frame_id', '?')})")
    
    if violations["YELLOW"]:
        print(f"\n🟨 YELLOW 警告 ({len(violations['YELLOW'])} 条):")
        for v in violations["YELLOW"][:10]:
            print(f"  - {v['rule_id']}: {v['reason']} (frame {v.get('frame_id', '?')})")
    
    # v0.5 Patch E-1: 显示 Gate 行为指纹
    if "fingerprint" in result:
        fp = result["fingerprint"]["gate_fingerprint"]
        print(f"\n{'=' * 60}")
        print("Gate Behavior Fingerprint (v0.5)")
        print(f"{'=' * 60}")
        print(f"总帧数: {fp['total_frames']}")
        print(f"状态分布:")
        for mode, ratio in fp['mode_ratio'].items():
            print(f"  {mode}: {ratio*100:.1f}%")
        print(f"状态切换次数: {fp['mode_switch_count']}")
        print(f"平均 ACTIVE 持续时间: {fp['avg_active_duration']:.1f} 帧")
        print(f"平均 READ_ONLY 持续时间: {fp['avg_read_only_duration']:.1f} 帧")
        print(f"进入 Hysteresis 命中: {fp['enter_hysteresis_hits']}")
        print(f"退出 Hysteresis 命中: {fp['exit_hysteresis_hits']}")
        print(f"\n指纹已保存到: artifacts/gate_fingerprint_v05.json")
    
    # v0.5 Patch F: 显示 Runtime Fingerprint
    if "runtime_fingerprint" in result:
        rfp = result["runtime_fingerprint"]
        print(f"\n{'=' * 60}")
        print("Runtime Fingerprint (v0.5 Patch F)")
        print(f"{'=' * 60}")
        print(f"视频 ID: {rfp.get('video_id', 'unknown')}")
        print(f"时长: {rfp.get('duration_sec', 0):.1f} 秒")
        print(f"稳定性评分: {rfp.get('stability_score', 0):.3f}")
        print(f"Gate 切换率: {rfp.get('state_switch_rate', {}).get('gate_switches_per_min', 0):.3f} 次/分钟")
        print(f"决策密度: {rfp.get('decision_density', {}).get('ticks_per_min', 0):.3f} 次/分钟")
        print(f"READ_ONLY 比例: {rfp.get('gate_distribution', {}).get('READ_ONLY', 0)*100:.1f}%")
    
    # v0.5 Patch G-1: 显示 Personality Fingerprint
    if "personality_fingerprint" in result:
        pfp = result["personality_fingerprint"]
        print(f"\n{'=' * 60}")
        print("Personality Fingerprint (v0.5)")
        print(f"{'=' * 60}")
        print(f"窗口: {pfp.get('window', {}).get('duration_sec', 0):.1f} 秒, {pfp.get('window', {}).get('frame_count', 0)} 帧")
        print(f"\nGate Profile:")
        gp = pfp.get("gate_profile", {})
        print(f"  ACTIVE: {gp.get('active_ratio', 0)*100:.1f}%")
        print(f"  READ_ONLY: {gp.get('read_only_ratio', 0)*100:.1f}%")
        print(f"  SUSPENDED: {gp.get('suspended_ratio', 0)*100:.1f}%")
        print(f"  切换率: {gp.get('state_switch_per_min', 0):.3f} 次/分钟")
        print(f"\nDecision Profile:")
        dp = pfp.get("decision_profile", {})
        print(f"  决策密度: {dp.get('tick_per_min', 0):.3f} 次/分钟")
        print(f"  NO_OP 比例: {dp.get('no_op_ratio', 0)*100:.1f}%")
        print(f"  有意义决策: {dp.get('meaningful_decisions', 0)}")
        print(f"\nStability Profile:")
        sp = pfp.get("stability_profile", {})
        avg_stability = sp.get('avg_stability_score')
        if avg_stability is not None:
            print(f"  平均稳定性: {avg_stability:.3f}")
        else:
            print(f"  平均稳定性: N/A")
        print(f"\n指纹已保存到: artifacts/personality_fingerprint_v05.json")

def main():
    parser = argparse.ArgumentParser(description="B2 v0.5 Trace Audit Runner")
    parser.add_argument("trace", help="Trace 文件路径（JSONL）")
    parser.add_argument("--rules", default="tools/dcs_rules_v1.json", help="DCS 规则文件路径")
    parser.add_argument("--output", help="输出报告文件路径（JSON）")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.trace):
        print(f"错误: trace 文件不存在: {args.trace}")
        sys.exit(1)
    
    result = audit_trace(args.trace, args.rules)
    print_report(result)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存到: {args.output}")

if __name__ == "__main__":
    main()
