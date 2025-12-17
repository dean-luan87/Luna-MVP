#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Replay runner skeleton (v1.4.9 P0-2-A).

P0-2-A 目标：定义并实现 Replay 输入结构，使 Replay 路径不依赖实时输入。

本 runner 的职责：
- 读取 ReplayInput JSON
- 设置 deterministic seed
- 安装逻辑时钟（禁止 wall clock time）
- 逐 step 提供 vision/map/intent 的 SSOT 输入

注意：
- 本文件不修改任何业务逻辑
- 业务系统的“确定性一致性”在 P0-2-B 才会进一步收敛

Run:
    python3 luna_badge_v1_2/replay/replay_runner.py luna_badge_v1_2/replay/examples/case_nav_turn_001.json
"""

from __future__ import annotations

import json
import random
import os
import sys
import hashlib
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

# 支持两种运行方式：
# 1) python3 -m luna_badge_v1_2.replay.replay_runner <file>
# 2) python3 luna_badge_v1_2/replay/replay_runner.py <file>
#
# 直接运行脚本时，相对导入会失败，因此这里做最小兼容处理（不影响业务逻辑）。
if __package__ is None or __package__ == "":
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from luna_badge_v1_2.replay.replay_models import ReplayInput  # type: ignore
    from luna_badge_v1_2.replay.replay_clock import ReplayClock, patch_time  # type: ignore
else:
    from .replay_models import ReplayInput
    from .replay_clock import ReplayClock, patch_time


RUNNER_VERSION = "1.4.9-P0-2-C.1"


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8").strip()
    except Exception:
        return "unknown"


def _canonical_json(obj: Any) -> str:
    # sort_keys=True + separators 固定，确保跨运行/跨机器序列化稳定
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parse_args(argv: List[str]) -> Dict[str, Any]:
    """
    Minimal arg parser (no external deps).

    Supported:
    - <replay_input.json> (positional)
    - --sleep-ms <int>          : wall-clock sleep between steps (does not affect logical clock)
    - --print-hash-only         : only print sha256 line (for validator subprocess parsing)
    - --dump-events <path.json> : dump canonical event stream to file
    - --validate <n>            : run proof mode (spawn subprocess N times for fast+slow)
    - --report <path.md>        : write validation report (proof mode)
    """
    if not argv:
        return {"help": True}

    args: Dict[str, Any] = {
        "input_path": None,
        "sleep_ms": 0,
        "print_hash_only": False,
        "dump_events": None,
        "validate": 0,
        "report": None,
    }

    it = iter(argv)
    for tok in it:
        if tok == "--sleep-ms":
            args["sleep_ms"] = int(next(it))
        elif tok == "--print-hash-only":
            args["print_hash_only"] = True
        elif tok == "--dump-events":
            args["dump_events"] = str(next(it))
        elif tok == "--validate":
            args["validate"] = int(next(it))
        elif tok == "--report":
            args["report"] = str(next(it))
        elif tok.startswith("-"):
            return {"help": True, "error": f"Unknown arg: {tok}"}
        else:
            # first positional is input
            if args["input_path"] is None:
                args["input_path"] = tok
            else:
                return {"help": True, "error": f"Unexpected positional arg: {tok}"}

    if args["input_path"] is None:
        return {"help": True}
    return args


@dataclass
class ReplayEventStream:
    """P0-2-C: hash 的唯一真相（Decision / Behavior / TTS 三段）。"""
    decisions: List[Dict[str, Any]]
    behavior_states: List[Dict[str, Any]]
    tts_events: List[Dict[str, Any]]


def build_event_stream(replay: ReplayInput) -> ReplayEventStream:
    """
    将 replay 输入枚举为“对用户可感知行为面”的标准化事件流。

    注意：
    - 目前 runner 仍是 skeleton，不驱动全业务系统；因此：
      - decisions 以 intent 事件作为序列化载体（start/cancel/confirm 等）
      - behavior_states 以 vision_state（TURNING/STRAIGHT 等行为态）为载体
      - tts_events 预留为空（待后续把业务输出接入 replay 驱动后填充）
    """
    decisions: List[Dict[str, Any]] = []
    behavior_states: List[Dict[str, Any]] = []
    tts_events: List[Dict[str, Any]] = []

    last_vision_state: Optional[str] = None
    for step in range(replay.time.steps):
        vf = replay.vision_at_step(step)
        if vf.vision_state != last_vision_state:
            behavior_states.append(
                {
                    "step_index": step,
                    "vision_state": vf.vision_state,
                }
            )
            last_vision_state = vf.vision_state

        intents = replay.intents_at_step(step)
        for it in intents:
            # 禁止纳入任何非确定性字段（wall clock/uuid/thread id 等）
            decisions.append(
                {
                    "step_index": step,
                    "event_name": it.intent,
                    "task_id": (it.payload or {}).get("task_id"),
                    "params": it.payload or {},
                }
            )

    return ReplayEventStream(
        decisions=decisions,
        behavior_states=behavior_states,
        tts_events=tts_events,
    )


def _run_once(
    input_path: str,
    sleep_ms: int,
    dump_events: Optional[str] = None,
    print_hash_only: bool = False,
) -> Tuple[str, Dict[str, Any]]:
    # NOTE: 这里的 sleep_ms 是 wall-clock 慢跑模拟，不影响逻辑时间与 hash
    from time import sleep as wall_sleep  # bind original before patch_time

    data = load_json(input_path)
    replay = ReplayInput.from_dict(data)
    errors = replay.validate()
    if errors:
        raise RuntimeError("Invalid replay input: " + "; ".join(errors))

    random.seed(replay.seed)

    clock = ReplayClock(
        t0_ms=replay.time.t0,
        delta_ms=replay.time.delta_ms,
        steps=replay.time.steps,
    )

    # 事件流在逻辑时间模式下构建（确保不会误用 wall clock）
    with patch_time(clock):
        event_stream = build_event_stream(replay)

        # 逐 step 枚举（保留原 skeleton 输出能力，但可通过 print_hash_only 关闭）
        if not print_hash_only:
            print(f"[REPLAY] replay_id={replay.replay_id} seed={replay.seed}")
            print(f"[REPLAY] steps={replay.time.steps} delta_ms={replay.time.delta_ms}")
            print("[REPLAY] realtime dependencies blocked: time.time/time.sleep/monotonic/perf_counter")

            for step in range(replay.time.steps):
                clock.step = step
                t_ms = replay.time_ms_at_step(step)
                vf = replay.vision_at_step(step)
                ms = replay.map_at_step(step)
                intents = replay.intents_at_step(step)

                if intents or step == 0 or step == replay.time.steps - 1:
                    print(f"\n[STEP {step:04d}] t_ms={t_ms} vision_state={vf.vision_state}")
                    if ms is not None:
                        # 避免把不稳定 float 作为 hash 输入：这里只展示，不纳入 hash
                        print(f"  map.route_state={ms.route_state} distance_to_turn={ms.distance_to_turn}")
                    if intents:
                        for it in intents:
                            print(f"  intent={it.intent} payload={it.payload}")

                if sleep_ms > 0:
                    wall_sleep(float(sleep_ms) / 1000.0)

    # hash 输入（只包含三段事件流 + 输入时间规格与 replay_id/seed，均为确定性字段）
    hash_input = {
        "replay_id": replay.replay_id,
        "seed": replay.seed,
        "time": {
            "t0_ms": replay.time.t0,
            "delta_ms": replay.time.delta_ms,
            "steps": replay.time.steps,
        },
        "decisions": event_stream.decisions,
        "behavior_states": event_stream.behavior_states,
        "tts_events": event_stream.tts_events,
    }

    canonical = _canonical_json(hash_input)
    digest = _sha256_hex(canonical)

    if dump_events:
        with open(dump_events, "w", encoding="utf-8") as f:
            f.write(canonical)
            f.write("\n")

    if print_hash_only:
        print(f"[REPLAY][HASH] sha256={digest}")
    else:
        print("\n[REPLAY] P0-2-C event stream generated (Decision/Behavior/TTS)")
        print(f"[REPLAY][HASH] sha256={digest}")
        print(f"[REPLAY][META] runner_version={RUNNER_VERSION} git_commit={_git_commit()}")

    meta = {
        "replay_id": replay.replay_id,
        "seed": replay.seed,
        "steps": replay.time.steps,
        "delta_ms": replay.time.delta_ms,
        "runner_version": RUNNER_VERSION,
        "git_commit": _git_commit(),
        "sleep_ms": sleep_ms,
    }
    return digest, meta


def _validate(
    script_path: str,
    input_path: str,
    runs: int,
    report_path: str,
    fast_sleep_ms: int = 0,
    slow_sleep_ms: int = 5,
) -> int:
    def run_subprocess(sleep_ms: int) -> str:
        out = subprocess.check_output(
            [
                sys.executable,
                script_path,
                input_path,
                "--sleep-ms",
                str(sleep_ms),
                "--print-hash-only",
            ],
            stderr=subprocess.STDOUT,
        ).decode("utf-8", errors="replace")
        # parse last hash line
        for line in out.splitlines()[::-1]:
            if line.startswith("[REPLAY][HASH] sha256="):
                return line.split("sha256=", 1)[1].strip()
        raise RuntimeError("Hash line not found in subprocess output:\n" + out)

    fast_hashes: List[str] = []
    slow_hashes: List[str] = []
    for _ in range(runs):
        fast_hashes.append(run_subprocess(fast_sleep_ms))
    for _ in range(runs):
        slow_hashes.append(run_subprocess(slow_sleep_ms))

    all_hashes = fast_hashes + slow_hashes
    ok = len(set(all_hashes)) == 1

    # 写报告（封版证据）
    lines: List[str] = []
    lines.append("# replay_validation_report.md")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- replay_input: `{input_path}`")
    lines.append(f"- runs_fast: {runs} (sleep_ms={fast_sleep_ms})")
    lines.append(f"- runs_slow: {runs} (sleep_ms={slow_sleep_ms})")
    lines.append(f"- runner_version: `{RUNNER_VERSION}`")
    lines.append(f"- git_commit: `{_git_commit()}`")
    lines.append(f"- result: {'PASS' if ok else 'FAIL'}")
    lines.append("")
    lines.append("## Hashes")
    lines.append("")
    lines.append("### fast")
    for i, h in enumerate(fast_hashes, 1):
        lines.append(f"- {i}. `{h}`")
    lines.append("")
    lines.append("### slow")
    for i, h in enumerate(slow_hashes, 1):
        lines.append(f"- {i}. `{h}`")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。")
    lines.append("- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。")
    lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write("\n")

    return 0 if ok else 1


def main() -> int:
    args = _parse_args(sys.argv[1:])
    if args.get("help"):
        if args.get("error"):
            print("[REPLAY][ERROR]", args["error"])
        print("Usage:")
        print("  python3 replay_runner.py <replay_input.json> [--sleep-ms N] [--dump-events out.json]")
        print("  python3 replay_runner.py <replay_input.json> --validate 5 [--report out.md]")
        return 2

    input_path: str = args["input_path"]
    sleep_ms: int = int(args["sleep_ms"])
    dump_events: Optional[str] = args["dump_events"]
    print_hash_only: bool = bool(args["print_hash_only"])
    validate_runs: int = int(args["validate"])
    report_path: Optional[str] = args["report"]

    script_path = os.path.abspath(__file__)

    if validate_runs > 0:
        if report_path is None:
            report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "replay_validation_report.md")
        return _validate(
            script_path=script_path,
            input_path=input_path,
            runs=validate_runs,
            report_path=report_path,
        )

    try:
        _run_once(
            input_path=input_path,
            sleep_ms=sleep_ms,
            dump_events=dump_events,
            print_hash_only=print_hash_only,
        )
        return 0
    except Exception as e:
        print("[REPLAY][FAILED]", str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
