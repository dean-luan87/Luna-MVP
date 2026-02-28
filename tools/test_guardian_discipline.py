#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guardian Discipline Phase 1 完整测试：审计口径 + Gate 红线 + 可选 suite 集成。
不依赖真实 stress_v2，用仓库内 baseline_test*.jsonl / candidate_test.jsonl 验证整条链路。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# 测试文件（项目根目录）
BASELINE_TEST = ROOT / "baseline_test.jsonl"
CANDIDATE_TEST = ROOT / "candidate_test.jsonl"
BASELINE_TEST2 = ROOT / "baseline_test2.jsonl"


def main():
    import argparse
    p = argparse.ArgumentParser(description="Test Guardian Discipline Phase 1: audit + gate")
    p.add_argument("--suite", action="store_true", help="Additionally run run_sim_suite and check guardian_discipline in report")
    args = p.parse_args()

    failed = []
    from tools.audit_exit_latency import run_audit

    # ---------- 1) 审计工具：测试 1（正 latency + efficiency < 1）----------
    if not BASELINE_TEST.is_file() or not CANDIDATE_TEST.is_file():
        print("SKIP: baseline_test.jsonl / candidate_test.jsonl not found (create from docs/GUARDIAN_DISCIPLINE_PHASE1.md)")
    else:
        report1 = run_audit(str(BASELINE_TEST), str(CANDIDATE_TEST), out_path=None)
        s1 = report1["summary"]
        if s1["matched_event_count"] != 2:
            failed.append(f"test1: matched_event_count expected 2, got {s1['matched_event_count']}")
        if s1["exit_latency_p50"] != 1:
            failed.append(f"test1: exit_latency_p50 expected 1, got {s1['exit_latency_p50']}")
        if s1["exit_latency_max"] != 2:
            failed.append(f"test1: exit_latency_max expected 2, got {s1['exit_latency_max']}")
        if abs(s1["hysteresis_efficiency"] - 4 / 7) > 0.01:
            failed.append(f"test1: hysteresis_efficiency expected ~0.5714, got {s1['hysteresis_efficiency']}")
        if s1["baseline_no_entry_count"] != 0:
            failed.append(f"test1: baseline_no_entry_count expected 0, got {s1['baseline_no_entry_count']}")
        if not failed:
            print("OK  audit test1: exit_latency + hysteresis_efficiency 口径正确")

    # ---------- 2) Gate：带 guardian_discipline 的 scorecard 应 FAIL ----------
    from simulation.logic.gate import is_gate_passed

    # 构造一个“其他都通过、仅 guardian 违规”的 scorecard
    bad_gd_scorecard = {
        "regression_count": 0,
        "danger_delta": 0,
        "decision_coverage_delta": 0,
        "lookahead_coverage_delta": 0,
        "volatility_index": 0.1,
        "efficiency": {"guarded_ratio_delta": 0, "lookahead_drop_ratio": 0},
        "perception": {"degradation_rate": 0.0},
        "early_conservative_action_gain": 0,
        "guardian_discipline": {
            "exit_latency_p50": 1,
            "exit_latency_p95": 1,
            "exit_latency_max": 2,
            "hysteresis_efficiency": 0.57,
            "baseline_no_entry_count": 0,
        },
    }
    passed, reasons = is_gate_passed(bad_gd_scorecard)
    if passed:
        failed.append(f"gate: scorecard with efficiency=0.57 should FAIL, got PASS")
    elif not any("GUARDIAN_DISCIPLINE" in r for r in reasons):
        failed.append(f"gate: expected GUARDIAN_DISCIPLINE_VIOLATION in reasons, got {reasons}")
    else:
        print("OK  gate: guardian_discipline efficiency < 0.90 → FAIL + GUARDIAN_DISCIPLINE_VIOLATION")

    # ---------- 3) 审计工具：测试 2（baseline 无事件 → baseline_no_entry）----------
    if BASELINE_TEST2.is_file():
        report2 = run_audit(str(BASELINE_TEST2), str(CANDIDATE_TEST), out_path=None)
        s2 = report2["summary"]
        if s2["matched_event_count"] != 0:
            failed.append(f"test2: matched_event_count expected 0, got {s2['matched_event_count']}")
        if s2["baseline_no_entry_count"] != 2:
            failed.append(f"test2: baseline_no_entry_count expected 2, got {s2['baseline_no_entry_count']}")
        if s2["hysteresis_efficiency"] != 1.0:
            failed.append(f"test2: hysteresis_efficiency expected 1.0 (no matched), got {s2['hysteresis_efficiency']}")
        if not failed:
            print("OK  audit test2: baseline_no_entry 口径正确，无 crash")
    else:
        print("SKIP: baseline_test2.jsonl not found")

    # ---------- 4) 可选：run_sim_suite 集成，检查 report 含 guardian_discipline ----------
    if args.suite:
        patch = ROOT / "patches" / "d1_conservative.json"
        if not patch.is_file():
            failed.append("--suite: patches/d1_conservative.json not found")
        else:
            import subprocess
            out = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "run_sim_suite.py"), "--golden", "--patch", str(patch)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=120,
            )
            if out.returncode != 0:
                failed.append(f"--suite: run_sim_suite exited {out.returncode}: {out.stderr[:500]}")
            else:
                # 找最新 suite_report.json
                suite_dirs = sorted((ROOT / "outputs" / "v1.1" / "sim_suites").glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
                if not suite_dirs:
                    failed.append("--suite: no outputs/v1.1/sim_suites/* found")
                else:
                    report_path = suite_dirs[0] / "suite_report.json"
                    if not report_path.is_file():
                        failed.append(f"--suite: {report_path} not found")
                    else:
                        data = json.loads(report_path.read_text(encoding="utf-8"))
                        per = data.get("per_episode") or {}
                        with_gd = [eid for eid, ep in per.items() if ep.get("guardian_discipline") is not None]
                        if len(with_gd) == 0:
                            failed.append("--suite: no episode has guardian_discipline in suite_report")
                        else:
                            print(f"OK  suite: {len(with_gd)} episodes with guardian_discipline in {report_path}")

    # ---------- 结果 ----------
    if failed:
        for f in failed:
            print("FAIL", f)
        return 1
    print("Guardian Discipline Phase 1 测试全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
