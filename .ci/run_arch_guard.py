#!/usr/bin/env python3
"""
BC Architecture Guard CI 执行器

作用：
- 扫描 trace / 输出
- 命中 Guard → CI FAIL
- 可本地 / GitHub Actions / Cursor 直接跑
"""

import sys
import json
import yaml
import argparse
from pathlib import Path

EXIT_ARCH_VIOLATION = 2
EXIT_OK = 0


def load_guard(path):
    """加载 Guard YAML 文件"""
    if not path.exists():
        print(f"⚠️  Warning: {path} 不存在，跳过 Guard 检查")
        return None
    with open(path, "r") as f:
        return yaml.safe_load(f)


def scan_trace(trace_path):
    """扫描 trace 文件，检测架构违规"""
    violations = []
    
    if not trace_path.exists():
        print(f"⚠️  Warning: {trace_path} 不存在，跳过 trace 扫描")
        return violations
    
    with open(trace_path, "r") as f:
        for idx, line in enumerate(f):
            try:
                record = json.loads(line)
            except Exception:
                continue
            
            gate = record.get("gate_eval", {}) or record.get("gate", {})
            b_output = record.get("to_c_message", {}) or record.get("b_output", {})
            summary = record.get("summary", {})
            impact_eval = record.get("impact_evaluation", {})
            
            # 检查 1: Gate=SUSPENDED but B outputs
            gate_mode = gate.get("mode") or gate.get("gate_mode")
            if gate_mode == "SUSPENDED":
                if b_output.get("sent") or summary.get("impact") != "NO_OP":
                    violations.append((idx + 1, "B_OUTPUT_WHEN_GATE_SUSPENDED", record))
            
            # 检查 2: advisory_only mandatory
            if summary:
                if not summary.get("advisory_only", False):
                    impact = summary.get("impact")
                    if impact and impact != "NO_OP":
                        violations.append((idx + 1, "B_MISSING_ADVISORY_FLAG", record))
            
            # 检查 3: NEED_STOP too close
            if summary:
                impact = summary.get("impact")
                if hasattr(impact, "name"):
                    impact_name = impact.name
                else:
                    impact_name = str(impact)
                
                if impact_name == "NEED_STOP":
                    gate_details = gate.get("details", {})
                    range_m = gate_details.get("range_m") or record.get("range_m", 999)
                    if range_m <= 3.0:
                        violations.append((idx + 1, "B_NEED_STOP_TOO_CLOSE", record))
            
            # 检查 4: ENV triggers behavior
            if summary:
                main_factor = summary.get("main_factor")
                impact = summary.get("impact")
                if hasattr(impact, "name"):
                    impact_name = impact.name
                else:
                    impact_name = str(impact)
                
                if main_factor == "ENV" or main_factor == "env":
                    if impact_name != "NO_OP":
                        violations.append((idx + 1, "ENV_TRIGGER_FORBIDDEN", record))
            
            # 检查 5: 确认性语义（简化检查）
            human_readable = record.get("human_interpretation", {}) or {}
            summary_text = human_readable.get("summary", "") or ""
            if summary_text:
                confirmative_keywords = ["一定", "必然", "确认", "必须", "certain", "must", "confirmed"]
                for keyword in confirmative_keywords:
                    if keyword in summary_text.lower():
                        violations.append((idx + 1, "B_CONFIRMATIVE_SEMANTICS", record))
                        break
    
    return violations


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="BC Architecture Guard CI 执行器")
    parser.add_argument("--trace", type=Path, help="Trace 文件路径（JSONL 格式）")
    parser.add_argument("--guard", type=Path, default=Path(".ci/bc_architecture_guard.yaml"), help="Guard YAML 文件路径")
    
    args = parser.parse_args()
    
    if not args.trace:
        print("⚠️  Warning: 未指定 trace 文件，跳过检查")
        sys.exit(EXIT_OK)
    
    print("=" * 60)
    print("BC Architecture Guard CI 检查")
    print("=" * 60)
    print(f"Trace 文件: {args.trace}")
    print(f"Guard 文件: {args.guard}")
    print()
    
    # 加载 Guard（可选）
    guard = load_guard(args.guard)
    
    # 扫描 trace
    violations = scan_trace(args.trace)
    
    if violations:
        print("❌ ARCHITECTURE VIOLATION DETECTED")
        print()
        for v in violations:
            line_num, violation_type, record = v
            print(f"  Line {line_num}: {violation_type}")
            # 可选：打印更多上下文
            if record:
                gate_mode = record.get("gate_eval", {}).get("mode") or record.get("gate", {}).get("mode")
                impact = record.get("summary", {}).get("impact")
                print(f"    Gate: {gate_mode}, Impact: {impact}")
        print()
        print("=" * 60)
        sys.exit(EXIT_ARCH_VIOLATION)
    
    print("✅ Architecture Guard PASSED")
    print("=" * 60)
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
