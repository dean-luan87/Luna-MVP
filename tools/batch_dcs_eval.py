#!/usr/bin/env python3
"""
批量 DCS 评估脚本

用于对比 v0.3 → v0.4.3 的危险消退曲线
"""

import sys
import json
from pathlib import Path
from typing import Dict, List
import subprocess

def run_dcs_eval(trace_path: str) -> Dict:
    """运行 DCS 评估并返回报告"""
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    # 运行 dcs_eval.py
    result = subprocess.run(
        [sys.executable, "tools/dcs_eval.py", trace_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ DCS 评估失败: {trace_path}")
        print(result.stderr)
        return None
    
    # 读取生成的报告
    report_path = artifacts_dir / "dcs_report.json"
    if not report_path.exists():
        print(f"⚠️ 报告文件不存在: {report_path}")
        return None
    
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    
    return report

def main():
    """批量评估多个 trace 文件"""
    if len(sys.argv) < 2:
        print("用法: python3 tools/batch_dcs_eval.py <trace1> [trace2] [trace3] ...")
        print("示例: python3 tools/batch_dcs_eval.py artifacts/trace_v03.jsonl artifacts/trace_v041.jsonl artifacts/trace_v043.jsonl")
        sys.exit(1)
    
    trace_files = sys.argv[1:]
    results = {}
    
    print("=" * 70)
    print("批量 DCS 评估")
    print("=" * 70)
    print()
    
    for trace_path in trace_files:
        trace_name = Path(trace_path).stem
        print(f"评估: {trace_name}...")
        
        report = run_dcs_eval(trace_path)
        if report:
            results[trace_name] = report
            print(f"  ✅ RED: {report.get('red_count', 0)}")
            print(f"  ⚠️  YELLOW: {report.get('yellow_count', 0)}")
            print(f"  ✅ GREEN: {report.get('green_count', 0)}")
        else:
            print(f"  ❌ 评估失败")
        print()
    
    # 生成对比报告
    comparison_path = Path("artifacts/dcs_comparison.json")
    with open(comparison_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("=" * 70)
    print(f"对比报告已保存: {comparison_path}")
    print("=" * 70)
    
    # 打印对比摘要
    print("\n📊 对比摘要:")
    print("-" * 70)
    print(f"{'版本':<20} | {'RED':<6} | {'YELLOW':<8} | {'GREEN':<8}")
    print("-" * 70)
    for name, report in sorted(results.items()):
        red = report.get('red_count', 0)
        yellow = report.get('yellow_count', 0)
        green = report.get('green_count', 0)
        print(f"{name:<20} | {red:<6} | {yellow:<8} | {green:<8}")
    print("-" * 70)

if __name__ == "__main__":
    main()
