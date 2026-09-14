#!/usr/bin/env python3
"""
生成 Viewer Artifact（CI 使用）

每次 CI 运行后，自动生成包含 trace 的 Viewer HTML
"""

import json
import os
import shutil
import sys
from pathlib import Path

def generate_viewer_artifact(trace_path: str, output_dir: str = "artifacts"):
    """
    生成 Viewer Artifact
    
    :param trace_path: trace JSONL 文件路径
    :param output_dir: 输出目录
    """
    trace_path = Path(trace_path)
    output_dir = Path(output_dir)
    
    if not trace_path.exists():
        print(f"❌ Trace file not found: {trace_path}")
        return False
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制 trace 文件
    trace_output = output_dir / "trace.jsonl"
    shutil.copy2(trace_path, trace_output)
    print(f"✅ Copied trace: {trace_output}")
    
    # 复制 Viewer HTML
    viewer_source = Path(__file__).parent / "trace_viewer_min.html"
    viewer_output = output_dir / "trace_viewer.html"
    if viewer_source.exists():
        shutil.copy2(viewer_source, viewer_output)
        print(f"✅ Copied viewer: {viewer_output}")
    else:
        print(f"⚠️ Viewer source not found: {viewer_source}")
    
    # 生成 DCS 报告
    dcs_report = generate_dcs_report(trace_path)
    dcs_output = output_dir / "dcs_report.json"
    with open(dcs_output, "w", encoding="utf-8") as f:
        json.dump(dcs_report, f, ensure_ascii=False, indent=2)
    print(f"✅ Generated DCS report: {dcs_output}")
    
    # CI 判死规则：RED > 0 → FAIL
    if dcs_report.get("red_count", 0) > 0:
        print(f"\n🔴 CI FAIL: DCS RED count = {dcs_report['red_count']}")
        print("   Viewer generated for post-mortem analysis")
        return False
    
    print(f"\n✅ CI PASS: DCS RED count = 0")
    return True

def generate_dcs_report(trace_path: Path) -> dict:
    """生成 DCS 报告"""
    dcs_count = {"GREEN": 0, "YELLOW": 0, "RED": 0, "N/A": 0}
    violations = []
    
    with open(trace_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                dcs = rec.get("dcs", {})
                grade = dcs.get("grade", "N/A")
                
                if grade in dcs_count:
                    dcs_count[grade] += 1
                else:
                    dcs_count["N/A"] += 1
                
                if grade == "RED":
                    violations.append({
                        "line": line_num,
                        "frame_id": rec.get("time", {}).get("frame_id"),
                        "t_video_s": rec.get("time", {}).get("t_video_s"),
                        "violations": dcs.get("violations", [])
                    })
            except Exception as e:
                print(f"⚠️ Parse error at line {line_num}: {e}")
    
    return {
        "total": sum(dcs_count.values()),
        "green_count": dcs_count["GREEN"],
        "yellow_count": dcs_count["YELLOW"],
        "red_count": dcs_count["RED"],
        "na_count": dcs_count["N/A"],
        "violations": violations[:20]  # 最多显示 20 条
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_viewer_artifact.py <trace.jsonl> [output_dir]")
        sys.exit(1)
    
    trace_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "artifacts"
    
    success = generate_viewer_artifact(trace_path, output_dir)
    sys.exit(0 if success else 1)
