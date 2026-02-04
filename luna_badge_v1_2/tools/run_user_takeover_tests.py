#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""P0-5: User takeover verification (v1.4.9).

目标：
验证在取消、降级、不确定场景下，用户始终拥有最终控制权：
- 接管后不再出现 NAVIGATION EMIT
- task_mode 收敛至 idle/ended
- 无“纠正用户”的反向决策（接管后不再出现系统对抗性输出）

约束：
- 不修改业务语义，不动 DecisionPipeline
- 复用 replay_runner / replay_gate / fault-config
"""

from __future__ import annotations

import json
import os
import sys
import subprocess
from typing import Any, Dict, List, Optional, Tuple


PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../luna_badge_v1_2
WORKSPACE_ROOT = os.path.dirname(PKG_ROOT)
RUNNER = os.path.join(PKG_ROOT, "replay", "replay_runner.py")
GATE = os.path.join(PKG_ROOT, "tools", "replay_gate.py")


def _run(cmd: List[str]) -> Tuple[int, str]:
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out, _ = p.communicate()
    return p.returncode, out


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _last_task_mode(events: Dict[str, Any]) -> Optional[str]:
    last = None
    for st in events.get("behavior_states") or []:
        if st.get("state_name") == "task_mode":
            last = st.get("value")
    return last


def _takeover_step(events: Dict[str, Any], takeover_event_names: List[str]) -> Optional[int]:
    # 优先从 decisions 查找明确的接管事件
    for d in events.get("decisions") or []:
        if d.get("event_name") in takeover_event_names:
            return int(d.get("step_index"))
    # fallback：以 task_mode 进入 ended/idle 作为接管点
    for st in events.get("behavior_states") or []:
        if st.get("state_name") == "task_mode" and st.get("value") in ("ended", "idle"):
            return int(st.get("step_index"))
    return None


def _nav_emit_after(events: Dict[str, Any], step0: int) -> List[Dict[str, Any]]:
    bad: List[Dict[str, Any]] = []
    for ev in events.get("tts_events") or []:
        if int(ev.get("step_index", -1)) > step0 and ev.get("category") == "NAVIGATION" and ev.get("action") == "EMIT":
            bad.append(ev)
    return bad


def _has_contradicting_decisions(events: Dict[str, Any], takeover_step: int) -> bool:
    # 接管后不应出现 start_task/恢复导航等“对抗性推进”
    for d in events.get("decisions") or []:
        if int(d.get("step_index", -1)) > takeover_step and d.get("event_name") in ("start_task", "resume_task"):
            return True
    return False


def main() -> int:
    evidence_dir = os.path.join(PKG_ROOT, "replay", "evidence", "user_takeover")
    os.makedirs(evidence_dir, exist_ok=True)

    # 5 scenarios
    scenarios = [
        {
            "id": "cancel_task",
            "replay": os.path.join(PKG_ROOT, "replay", "examples", "p0_5_user_cancel_001.json"),
            "fault_config": None,
            "takeover_events": ["confirm_cancel", "user_exit", "user_override", "system_silence_timeout", "failsafe_triggered"],
        },
        {
            "id": "failsafe_then_exit",
            "replay": os.path.join(PKG_ROOT, "replay", "examples", "p0_5_failsafe_then_exit_001.json"),
            "fault_config": os.path.join(PKG_ROOT, "replay", "faults", "vision_no_return_001.json"),
            "takeover_events": ["failsafe_triggered", "user_exit"],
        },
        {
            "id": "uncertainty_user_choice",
            "replay": os.path.join(PKG_ROOT, "replay", "examples", "p0_5_uncertainty_user_choice_001.json"),
            "fault_config": None,
            "takeover_events": ["user_choice", "user_exit", "user_override"],
        },
        {
            "id": "reverse_instruction",
            "replay": os.path.join(PKG_ROOT, "replay", "examples", "p0_5_reverse_instruction_001.json"),
            "fault_config": None,
            "takeover_events": ["user_override"],
        },
        {
            "id": "silence_exit",
            "replay": os.path.join(PKG_ROOT, "replay", "examples", "p0_5_silence_exit_001.json"),
            "fault_config": None,
            "takeover_events": ["system_silence_timeout"],
        },
    ]

    results: List[Dict[str, Any]] = []

    for s in scenarios:
        sid = s["id"]
        replay_path = s["replay"]
        fault_cfg = s.get("fault_config")

        events_dump = os.path.join(evidence_dir, f"{sid}__events.json")

        # 1) 单次生成 events dump（证据）
        cmd = [sys.executable, RUNNER, replay_path, "--dump-events", events_dump, "--print-hash-only"]
        if fault_cfg:
            cmd.extend(["--fault-config", fault_cfg])
        code, out = _run(cmd)
        if code != 0:
            results.append({"scenario": sid, "pass": False, "error": out.strip()})
            continue

        sha = "unknown"
        for line in out.splitlines()[::-1]:
            if line.startswith("[REPLAY][HASH] sha256="):
                sha = line.split("sha256=", 1)[1].strip()
                break

        # 2) 复用 gate（5x 快/慢）做回归门禁
        gate_cmd = [
            sys.executable,
            GATE,
            "--cases",
            replay_path,
            "--runs",
            "5",
        ]
        if fault_cfg:
            gate_cmd.extend(["--fault-config", fault_cfg])
        gate_code, gate_out = _run(gate_cmd)
        gate_pass = gate_code == 0

        # 3) 规则判定
        ev = _load_json(events_dump)
        takeover_step = _takeover_step(ev, s["takeover_events"])
        last_mode = _last_task_mode(ev)

        nav_after: List[Dict[str, Any]] = []
        contradict = False
        ok_mode = last_mode in ("idle", "ended")

        if takeover_step is not None:
            nav_after = _nav_emit_after(ev, takeover_step)
            contradict = _has_contradicting_decisions(ev, takeover_step)

        ok = bool(
            gate_pass
            and takeover_step is not None
            and ok_mode
            and (not nav_after)
            and (not contradict)
        )

        results.append(
            {
                "scenario": sid,
                "replay": os.path.relpath(replay_path, WORKSPACE_ROOT),
                "fault_config": os.path.relpath(fault_cfg, WORKSPACE_ROOT) if fault_cfg else "",
                "hash": sha,
                "takeover_step": takeover_step,
                "final_task_mode": last_mode,
                "gate_pass": gate_pass,
                "nav_emit_after_takeover_count": len(nav_after),
                "contradicting_decisions_after_takeover": contradict,
                "events_dump": os.path.relpath(events_dump, WORKSPACE_ROOT),
                "pass": ok,
            }
        )

    # 写报告
    report_path = os.path.join(PKG_ROOT, "user_takeover_test_report.md")
    lines: List[str] = []
    lines.append("# user_takeover_test_report.md")
    lines.append("")
    lines.append("## Scope")
    lines.append("- P0-5 用户可接管验证（v1.4.9）")
    lines.append("- 复用 replay_runner / replay_gate / fault-config")
    lines.append("")
    lines.append("## Pass criteria (hard)")
    lines.append("- takeover 后不再出现 `NAVIGATION EMIT`")
    lines.append("- task_mode 收敛至 `idle/ended`")
    lines.append("- takeover 后无对抗性推进（例如再次 start_task/resume_task）")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    for r in results:
        lines.append(f"### Scenario: {r['scenario']}")
        if not r.get("pass"):
            lines.append("- **PASS/FAIL**: FAIL")
            if r.get("error"):
                lines.append(f"- **error**: {r['error']}")
            else:
                lines.append(f"- **gate_pass**: {r.get('gate_pass')}")
                lines.append(f"- **takeover_step**: {r.get('takeover_step')}")
                lines.append(f"- **final_task_mode**: {r.get('final_task_mode')}")
                lines.append(f"- **nav_emit_after_takeover_count**: {r.get('nav_emit_after_takeover_count')}")
                lines.append(f"- **contradicting_decisions_after_takeover**: {r.get('contradicting_decisions_after_takeover')}")
                lines.append(f"- **events_dump**: `{r.get('events_dump')}`")
            lines.append("")
            continue
        lines.append("- **PASS/FAIL**: PASS")
        lines.append(f"- **replay**: `{r['replay']}`")
        if r.get("fault_config"):
            lines.append(f"- **fault_config**: `{r['fault_config']}`")
        lines.append(f"- **hash**: `{r['hash']}`")
        lines.append(f"- **takeover_step**: {r['takeover_step']}")
        lines.append(f"- **final_task_mode**: {r['final_task_mode']}")
        lines.append(f"- **gate_pass (5x fast/slow)**: {r['gate_pass']}")
        lines.append(f"- **events_dump**: `{r['events_dump']}`")
        lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write("\n")

    all_pass = all(bool(r.get("pass")) for r in results)
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

