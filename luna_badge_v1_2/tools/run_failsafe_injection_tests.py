#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""P0-3 FailSafe fault injection test runner (deterministic & auditable).

目标：
- 三类故障：Vision 无返回 / Map 超时 / TTS 阻塞
- 产出：
  - failsafe_test_report.md
  - 最小证据包（每个 case 的 canonical event dump + hash 报告）

约束：
- 不修改业务语义 / 不动 DecisionPipeline
- 注入仅发生在 adapter 边界（通过 replay_runner 的 --fault-config）
- 复用 replay_gate 的一致性验证（子进程 5x 快/慢）
"""

from __future__ import annotations

import os
import sys
import json
import subprocess
from typing import Dict, Any, List, Optional, Tuple


PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../luna_badge_v1_2
WORKSPACE_ROOT = os.path.dirname(PKG_ROOT)  # .../Luna-2
RUNNER = os.path.join(PKG_ROOT, "replay", "replay_runner.py")


def _run(cmd: List[str]) -> Tuple[int, str]:
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out, _ = p.communicate()
    return p.returncode, out


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _find_first_safety_mode_step(events: Dict[str, Any]) -> Optional[int]:
    for st in events.get("behavior_states") or []:
        if st.get("state_name") == "safety_mode" and st.get("value") in ("degraded", "emergency"):
            return int(st["step_index"])
    return None


def _has_nav_emit_after(events: Dict[str, Any], step0: int) -> bool:
    for ev in events.get("tts_events") or []:
        if int(ev.get("step_index", -1)) > step0 and ev.get("category") == "NAVIGATION" and ev.get("action") == "EMIT":
            return True
    return False


def main() -> int:
    base_case = os.path.join(PKG_ROOT, "replay", "examples", "case_nav_turn_001.json")
    faults_dir = os.path.join(PKG_ROOT, "replay", "faults")
    evidence_dir = os.path.join(PKG_ROOT, "replay", "evidence", "failsafe")
    os.makedirs(evidence_dir, exist_ok=True)

    cases = [
        ("vision_no_return", os.path.join(faults_dir, "vision_no_return_001.json"), "emergency"),
        ("map_timeout", os.path.join(faults_dir, "map_timeout_001.json"), "degraded"),
        ("tts_block", os.path.join(faults_dir, "tts_block_001.json"), "degraded"),
    ]

    results: List[Dict[str, Any]] = []

    for name, fault_cfg, expect_level in cases:
        dump_path = os.path.join(evidence_dir, f"{name}__events.json")
        # replay_gate 输出文件命名规则：replay_validation_report__<case>__fault_<fault_base>.md
        fault_base = os.path.basename(fault_cfg).replace(".json", "")
        report_path = os.path.join(PKG_ROOT, "replay", f"replay_validation_report__case_nav_turn_001__fault_{fault_base}.md")

        # 1) 生成 canonical events + hash（单次）
        code, out = _run(
            [
                sys.executable,
                RUNNER,
                base_case,
                "--fault-config",
                fault_cfg,
                "--dump-events",
                dump_path,
                "--print-hash-only",
            ]
        )
        if code != 0:
            results.append({"case": name, "pass": False, "error": out.strip()})
            continue

        sha = "unknown"
        for line in out.splitlines()[::-1]:
            if line.startswith("[REPLAY][HASH] sha256="):
                sha = line.split("sha256=", 1)[1].strip()
                break

        # 2) 复用 replay_gate（5x 快/慢）生成审计报告（使用绝对路径，避免 cwd 相关问题）
        code2, out2 = _run(
            [
                sys.executable,
                os.path.join(PKG_ROOT, "tools", "replay_gate.py"),
                "--cases",
                base_case,
                "--runs",
                "5",
                "--fault-config",
                fault_cfg,
            ]
        )
        gate_pass = code2 == 0

        # 3) 解析证据：触发 step、用户可感知事件、TaskChain 停止推进（无 NAV EMIT）
        ev = _load_json(dump_path)
        fs_step = _find_first_safety_mode_step(ev)
        actual_level = None
        for st in ev.get("behavior_states") or []:
            if st.get("state_name") == "safety_mode" and st.get("value") in ("degraded", "emergency"):
                actual_level = st.get("value")
                break
        has_user_evidence = any((e.get("source") == "failsafe") for e in (ev.get("tts_events") or [])) or any(
            (e.get("action") in ("SUPPRESS", "REPLACE", "DROP")) for e in (ev.get("tts_events") or [])
        )
        no_nav_after = True
        if fs_step is not None:
            no_nav_after = not _has_nav_emit_after(ev, fs_step)

        ok = bool(
            gate_pass
            and fs_step is not None
            and actual_level in ("degraded", "emergency")
            and has_user_evidence
            and no_nav_after
            and (actual_level == expect_level)
        )

        results.append(
            {
                "case": name,
                "fault_config": os.path.relpath(fault_cfg, WORKSPACE_ROOT),
                "expected_level": expect_level,
                "actual_level": actual_level,
                "hash": sha,
                "failsafe_step": fs_step,
                "gate_pass": gate_pass,
                "has_user_evidence": has_user_evidence,
                "no_nav_emit_after_failsafe": no_nav_after,
                "pass": ok,
                "events_dump": os.path.relpath(dump_path, WORKSPACE_ROOT),
                "validation_report": os.path.relpath(report_path, WORKSPACE_ROOT),
                "gate_output": out2.strip(),
            }
        )

    # 写报告
    report_file = os.path.join(PKG_ROOT, "failsafe_test_report.md")
    lines: List[str] = []
    lines.append("# failsafe_test_report.md")
    lines.append("")
    lines.append("## Scope")
    lines.append("- Vision 无返回 / Map 超时 / TTS 阻塞 三类故障注入验证（Replay + FaultInjector）")
    lines.append("- 注入仅发生在 adapter 边界（--fault-config）")
    lines.append("- 复用 replay_gate 做 5x 快/慢一致性证明")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    for r in results:
        lines.append(f"### Case: {r['case']}")
        if not r.get("pass"):
            lines.append(f"- **PASS/FAIL**: FAIL")
            lines.append(f"- **fault_config**: `{r.get('fault_config')}`")
            lines.append(f"- **expected_level**: {r.get('expected_level')}")
            lines.append(f"- **actual_level**: {r.get('actual_level')}")
            lines.append(f"- **failsafe_step**: {r.get('failsafe_step')}")
            lines.append(f"- **hash**: `{r.get('hash')}`")
            lines.append(f"- **gate_pass (5x fast/slow)**: {r.get('gate_pass')}")
            lines.append(f"- **user_evidence**: {r.get('has_user_evidence')}")
            lines.append(f"- **taskchain_stop (no NAV EMIT after failsafe)**: {r.get('no_nav_emit_after_failsafe')}")
            lines.append(f"- **events_dump**: `{r.get('events_dump')}`")
            lines.append(f"- **validation_report**: `{r.get('validation_report')}`")
            if r.get("error"):
                lines.append(f"- **error**: {r['error']}")
            lines.append("")
            continue
        lines.append(f"- **PASS/FAIL**: PASS")
        lines.append(f"- **fault_config**: `{r['fault_config']}`")
        lines.append(f"- **failsafe_step**: {r['failsafe_step']}")
        lines.append(f"- **expected_level**: {r['expected_level']}")
        lines.append(f"- **actual_level**: {r.get('actual_level')}")
        lines.append(f"- **hash**: `{r['hash']}`")
        lines.append(f"- **gate_pass (5x fast/slow)**: {r['gate_pass']}")
        lines.append(f"- **user_evidence**: {r['has_user_evidence']}")
        lines.append(f"- **taskchain_stop (no NAV EMIT after failsafe)**: {r['no_nav_emit_after_failsafe']}")
        lines.append(f"- **events_dump**: `{r['events_dump']}`")
        lines.append(f"- **validation_report**: `{r['validation_report']}`")
        lines.append("")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write("\n")

    all_pass = all(bool(r.get("pass")) for r in results) if results else False
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

