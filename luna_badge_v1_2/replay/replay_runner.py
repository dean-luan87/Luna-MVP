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
import tempfile
import difflib
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

# P0-4: performance baseline must use wall-clock perf_counter.
# replay_clock.patch_time() will patch time.perf_counter; we capture the original here.
import time as _wall_time
_WALL_PERF_COUNTER = _wall_time.perf_counter

# 支持两种运行方式：
# 1) python3 -m luna_badge_v1_2.replay.replay_runner <file>
# 2) python3 luna_badge_v1_2/replay/replay_runner.py <file>
#
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pkg_root = os.path.join(repo_root, "luna_badge_v1_2")
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
if pkg_root not in sys.path:
    # 兼容代码库中大量以 `task_engine.* / core.*` 为根的绝对导入
    sys.path.insert(0, pkg_root)

if __package__ is None or __package__ == "":
    from luna_badge_v1_2.replay.replay_models import ReplayInput  # type: ignore
    from luna_badge_v1_2.replay.replay_clock import ReplayClock, patch_time  # type: ignore
else:
    from .replay_models import ReplayInput
    from .replay_clock import ReplayClock, patch_time


RUNNER_VERSION = "1.4.9-P0-5.1"


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
    - --fault-config <path.json>: P0-3 test-only adapter fault injection config
    - --perf-json <path.json>   : P0-4 perf baseline output (not included in hash)
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
        "fault_config": None,
        "perf_json": None,
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
        elif tok == "--fault-config":
            args["fault_config"] = str(next(it))
        elif tok == "--perf-json":
            args["perf_json"] = str(next(it))
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


def build_event_stream(
    replay: ReplayInput,
    clock: ReplayClock,
    *,
    fault_config_path: Optional[str] = None,
    perf: Optional[Dict[str, Any]] = None,
) -> ReplayEventStream:
    """
    将 replay 输入枚举为“对用户可感知行为面”的标准化事件流。

    注意：
    - 目前 runner 仍是 skeleton，不驱动全业务系统；因此：
      - decisions 以 intent 事件作为序列化载体（start/cancel/confirm 等）
      - behavior_states 至少覆盖：vision_mode / task_mode / safety_mode
      - tts_events 至少覆盖：表达系统最终决策事件流（C5）与最小 TTS 路由决策流（节流/入队）
    """
    decisions: List[Dict[str, Any]] = []
    behavior_states: List[Dict[str, Any]] = []
    tts_events: List[Dict[str, Any]] = []

    # perf collector (P0-4 only; never used for hashing)
    if perf is not None:
        perf.setdefault("step_wall_us", [])
        perf.setdefault("tts_enqueue_wall_us", [])

    # P0-3: fault injection (test-only, adapter boundary)
    from replay.fault_injector import load_fault_config, FaultConfig
    fault_cfg: FaultConfig = FaultConfig()
    if fault_config_path:
        fault_cfg = load_fault_config(fault_config_path)

    # ---------------------------
    # Behavior states (3 modes)
    # ---------------------------
    def vision_mode_from_state(vs: str) -> str:
        v = (vs or "").upper()
        if v in ("TURNING",):
            return "turning"
        if v in ("STRAIGHT", "STABLE", "LOCKED"):
            return "straight"
        return "unknown"

    task_mode: str = "active" if replay.initial_state.has_active_task else "idle"
    safety_mode: str = "normal"
    failsafe_triggered_at: Optional[int] = None

    def _maybe_record_task_safety(step: int) -> None:
        nonlocal last_task_mode, last_safety_mode, task_mode, safety_mode
        if task_mode != last_task_mode:
            record_state(step, "task_mode", task_mode)
            last_task_mode = task_mode
        if safety_mode != last_safety_mode:
            record_state(step, "safety_mode", safety_mode)
            last_safety_mode = safety_mode

    def trigger_failsafe(step: int, *, level: str, reason: str) -> None:
        nonlocal safety_mode, task_mode, failsafe_triggered_at
        if failsafe_triggered_at is not None:
            return
        failsafe_triggered_at = step
        safety_mode = level  # degraded | emergency
        # TaskChain 不再推进：进入 ended（行为态），并停止后续导航输出
        task_mode = "ended"
        # 触发点必须被记录为“行为态变化”（即使触发发生在本 step 的后半段）
        _maybe_record_task_safety(step)
        decisions.append(
            {
                "step_index": step,
                "event_name": "failsafe_triggered",
                "task_id": None,
                "params": {"level": level, "reason": reason},
            }
        )
        # 用户可感知行为证据：发出一条“进入降级/应急”的安全播报事件（不 hash 原始文本）
        tts_events.append(
            {
                "step_index": step,
                "source": "failsafe",
                "action": "EMIT",
                "category": "SAFETY",
                "priority_band": "P0_SAFETY",
                "message_id": f"failsafe.enter_{level}",
                "reason": reason,
            }
        )
    last_vision_mode: Optional[str] = None
    last_task_mode: Optional[str] = None
    last_safety_mode: Optional[str] = None

    def record_state(step: int, name: str, value: str) -> None:
        behavior_states.append(
            {
                "step_index": step,
                "state_name": name,
                "value": value,
            }
        )

    # 记录初始态（step=0）
    clock.step = 0
    vf0 = replay.vision_at_step(0)
    last_vision_mode = vision_mode_from_state(vf0.vision_state)
    last_task_mode = task_mode
    last_safety_mode = safety_mode
    record_state(0, "vision_mode", last_vision_mode)
    record_state(0, "task_mode", last_task_mode)
    record_state(0, "safety_mode", last_safety_mode)

    # cancel_confirm 的“ended->idle”用 next_step 触发，避免同 step 双变更
    pending_task_mode_at_step: Dict[int, str] = {}

    # ---------------------------
    # TTS events capture (C5 + minimal TTS router)
    # ---------------------------
    # C5: expression decision stream (EMIT/DROP/REPLACE/SUPPRESS)
    from expression.scheduler.c5_scheduler import C5Scheduler
    from expression.scheduler.c5_types import VisionRhythmContext, ExpressionCandidate

    current_step = 0

    def c5_observer(ev: Dict[str, Any]) -> None:
        # 映射到 tts_events 口径（不 hash 原始文本）
        # priority_band：critical/high 归为 P0_SAFETY，其余视为 P1_NAV
        urgency = str(ev.get("urgency") or "normal")
        is_critical = bool(ev.get("is_critical"))
        band = "P0_SAFETY" if (is_critical or urgency == "high") else "P1_NAV"
        tts_events.append(
            {
                "step_index": current_step,
                "source": "c5",
                "action": ev.get("action"),
                "category": "NAVIGATION" if band == "P1_NAV" else "SAFETY",
                "priority_band": band,
                "message_id": f"expr:{ev.get('contract_id')}",
                "contract_id": ev.get("contract_id"),
                "reason": ev.get("reason"),
                "delay_ms": int(ev.get("delay_ms") or 0),
            }
        )

    c5 = C5Scheduler(event_observer=c5_observer)
    c5.reset()

    # Minimal TTS routing decisions (TimeWindowGate throttle -> enqueue or suppress)
    # 注意：这里不要求真实音频，仅捕获“是否入队/被节流”这一行为面。
    from task_engine.tts.tts_manager import TtsManager
    from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
    from task_engine.tts.router_facade import TTSRouterFacade
    from task_engine.tts.tts_policy import TTSCategory
    from task_engine.tts.priority_bands import PriorityBand

    tts_mgr = TtsManager()
    nav_router = NavigationVoiceRouter(tts_manager_instance=tts_mgr)
    # Replay 起点时间可能为 0。为了复现“首次播报允许”的现实语义，
    # 将 last_* 初始化到“窗口之前”，避免 t0=0 导致首次被误抑制。
    nav_router.gate.reset()
    nav_router.gate.last_navigation_time = clock.now_s() - nav_router.gate.navigation_window
    nav_router.gate.last_safety_time = clock.now_s() - nav_router.gate.safety_window
    facade = TTSRouterFacade(nav_router=nav_router, queue_manager=tts_mgr)

    def record_tts_from_queue_delta(
        *,
        step: int,
        category: str,
        band: str,
        message_id: str,
        before_main: int,
        after_main: int,
        before_safety: int,
        after_safety: int,
        source: str,
    ) -> None:
        emitted = (after_main > before_main) or (after_safety > before_safety)
        tts_events.append(
            {
                "step_index": step,
                "source": source,
                "action": "EMIT" if emitted else "SUPPRESS",
                "category": category,
                "priority_band": band,
                "message_id": message_id,
            }
        )

    # Adapter boundary wrappers (fault injection happens ONLY here)
    def vision_adapter(step: int) -> Optional[Any]:
        if fault_cfg.match(step, "vision_no_return"):
            return None
        if fault_cfg.match(step, "vision_timeout"):
            raise TimeoutError("vision_timeout")
        return replay.vision_at_step(step)

    def map_adapter(step: int) -> Optional[Any]:
        if fault_cfg.match(step, "map_timeout"):
            raise TimeoutError("map_timeout")
        return map_snapshots_by_step.get(step)

    def tts_adapter_emit(step: int, *, category: Any, meta: Dict[str, Any]) -> None:
        if fault_cfg.match(step, "tts_block"):
            raise TimeoutError("tts_block")
        if fault_cfg.match(step, "tts_exception"):
            raise RuntimeError("tts_exception")
        facade.emit(text="NAV_UPDATE", category=category, meta=meta)

    # 仅在 snapshot step 触发“输入变化”相关的表达/播报，避免伪造大量事件。
    map_snapshots_by_step = {s.step: s for s in replay.map_snapshots}
    last_map_snapshot_step: Optional[int] = max(map_snapshots_by_step.keys()) if map_snapshots_by_step else None
    vision_snapshot_steps = {f.step for f in replay.vision_frames}

    for step in range(replay.time.steps):
        step_t0 = _WALL_PERF_COUNTER()
        clock.step = step
        current_step = step

        # delayed task_mode transitions
        if step in pending_task_mode_at_step:
            task_mode = pending_task_mode_at_step[step]

        # Vision adapter boundary
        try:
            vf = vision_adapter(step)
        except Exception as e:
            trigger_failsafe(step, level="emergency", reason=f"vision_error:{type(e).__name__}")
            vf = None
        if vf is None:
            trigger_failsafe(step, level="emergency", reason="vision_no_return")
            # 视觉缺失后，行为态转 unknown
            vm = "unknown"
        else:
            vm = vision_mode_from_state(vf.vision_state)
        if vm != last_vision_mode:
            record_state(step, "vision_mode", vm)
            last_vision_mode = vm

        # FailSafe 触发后：TaskChain 不再推进（停止后续导航输出与调度）
        if failsafe_triggered_at is not None and step > failsafe_triggered_at:
            # 仍允许记录外部输入（decisions），但不再产生导航输出
            intents = replay.intents_at_step(step)
            for it in intents:
                decisions.append(
                    {
                        "step_index": step,
                        "event_name": it.intent,
                        "task_id": (it.payload or {}).get("task_id"),
                        "params": it.payload or {},
                    }
                )
            continue

        intents = replay.intents_at_step(step)
        replace_probe = False
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

            # task_mode derived from intents (一期实现语义：confirm-cancel 两步)
            if it.intent == "start_task":
                task_mode = "active"
                # 触发一次“同 duplicate_key 更新”，用于覆盖 C5 的 REPLACE 行为（不引入新信息）
                # 仅在直行/稳定场景下触发，避免与 TURNING flush 语义耦合。
                if vm == "straight":
                    replace_probe = True
            elif it.intent == "cancel_task":
                # 进入确认式取消等待态
                task_mode = "cancel_confirm"
            elif it.intent == "confirm_cancel":
                if bool((it.payload or {}).get("confirm")):
                    task_mode = "ended"
                    # 下一步回到 idle（隐式状态）
                    if step + 1 < replay.time.steps:
                        pending_task_mode_at_step[step + 1] = "idle"
            # P0-5: 用户接管/退出（一期必须服从用户）
            elif it.intent in ("user_exit", "user_override"):
                task_mode = "ended"
                if step + 1 < replay.time.steps:
                    pending_task_mode_at_step[step + 1] = "idle"
            # P0-5: 系统不确定性提示 + 用户选择（仅用于审计回放，不改变业务语义）
            elif it.intent == "system_uncertainty_prompt":
                tts_events.append(
                    {
                        "step_index": step,
                        "source": "system",
                        "action": "EMIT",
                        "category": "SYSTEM",
                        "priority_band": "P2_TASK",
                        "message_id": str((it.payload or {}).get("message_id") or "system.uncertainty_prompt"),
                    }
                )
            elif it.intent == "user_choice":
                choice = str((it.payload or {}).get("choice") or "").lower()
                if choice in ("exit", "cancel", "stop"):
                    task_mode = "ended"
                    if step + 1 < replay.time.steps:
                        pending_task_mode_at_step[step + 1] = "idle"
                elif choice in ("continue", "go", "yes"):
                    task_mode = "active"
            # P0-5: 反向指令（用户不按系统建议）
            elif it.intent == "system_suggest_nav":
                tts_events.append(
                    {
                        "step_index": step,
                        "source": "system",
                        "action": "EMIT",
                        "category": "NAVIGATION",
                        "priority_band": "P1_NAV",
                        "message_id": str((it.payload or {}).get("message_id") or "nav.suggest"),
                    }
                )
            # P0-5: 用户沉默后的静默退出（无 TTS）
            elif it.intent == "system_silence_timeout":
                task_mode = "ended"
                if step + 1 < replay.time.steps:
                    pending_task_mode_at_step[step + 1] = "idle"

        # intents 处理完后，再记录 task/safety 的行为态变化，确保 step_index 对齐用户体验
        _maybe_record_task_safety(step)

        # P0-5 hard rule: 用户接管/任务结束后，不再产生任何 NAVIGATION EMIT
        # 说明：replay_runner 是“行为审计抽取器”，这里仅停止后续输出事件生成，不改业务逻辑。
        if task_mode in ("idle", "ended"):
            if perf is not None:
                perf["step_wall_us"].append(int((_WALL_PERF_COUNTER() - step_t0) * 1_000_000))
            continue

        # -------- C5 decision stream driven by replay snapshots --------
        # 将 replay 的 vision_state 映射到 C5 的 vision_state 词表
        c5_vs = "TURNING" if vm == "turning" else "STABLE"
        ctx = VisionRhythmContext(
            vision_state=c5_vs,  # type: ignore[arg-type]
            speed_mps=0.8,       # 固定值：ReplayInput 未提供速度，避免引入浮点随机源
            last_vision_ts=float(step),  # step-based，避免 wall clock
        )

        # Map adapter boundary
        try:
            ms = map_adapter(step)
        except Exception as e:
            trigger_failsafe(step, level="degraded", reason=f"map_error:{type(e).__name__}")
            ms = None
        if ms is not None:
            dist_m = int(round(ms.distance_to_turn))
            expr = ExpressionCandidate(
                contract_id="nav.distance_to_turn",
                urgency="low",
                is_critical=False,
                duplicate_key="nav.distance_to_turn",
            )
            # 触发一次 schedule（replace/turning drop/emit 都可在 observer 中体现）
            c5.schedule(expr, ctx, emit_callback=lambda _e, _d: None)

        # C5 REPLACE 覆盖：start_task step 下再次 schedule 相同 duplicate_key
        if replace_probe:
            c5.schedule(
                ExpressionCandidate(
                    contract_id="nav.distance_to_turn",
                    urgency="low",
                    is_critical=False,
                    duplicate_key="nav.distance_to_turn",
                ),
                ctx,
                emit_callback=lambda _e, _d: None,
            )

        # TURNING 行为态变化时：触发一次非关键表达，用于验证 TURNING 白名单兜底的稳定 DROP
        # （来源于 replay 的 vision snapshot，不引入新信息）
        if vm == "turning" and step in vision_snapshot_steps:
            c5.schedule(
                ExpressionCandidate(
                    contract_id="nav.turning_suppress_probe",
                    urgency="normal",
                    is_critical=False,
                    duplicate_key="nav.turning_suppress_probe",
                ),
                ctx,
                emit_callback=lambda _e, _d: None,
            )

        # 仅在最后一个 map snapshot step 处理队列，保证能覆盖 REPLACE 语义：
        # step0 入队 → step10 replace → step10 出队 emit
        if last_map_snapshot_step is not None and step == last_map_snapshot_step:
            c5.process_queue(ctx, emit_callback=lambda _e, _d: None)

        # -------- Minimal TTS routing decisions (throttle vs enqueue) --------
        # 仅在 “straight 且有 map snapshot” 时尝试一次导航播报。
        if ms is not None and vm == "straight":
            dist_m = int(round(ms.distance_to_turn))
            message_id = f"tts:nav.distance_to_turn:{dist_m}"
            before_main = len(tts_mgr.get_queue())
            before_safety = len(tts_mgr.get_safety_queue())

            # 走 RouterFacade，确保 category/band 语义与一期一致
            try:
                tts_t0 = _WALL_PERF_COUNTER()
                tts_adapter_emit(
                    step,
                    category=TTSCategory.NAVIGATION,
                    meta={
                        "template_id": "nav.distance_to_turn",
                        "distance_m": dist_m,
                        "step_index": step,
                    },
                )
                if perf is not None:
                    perf["tts_enqueue_wall_us"].append(int((_WALL_PERF_COUNTER() - tts_t0) * 1_000_000))
            except Exception as e:
                # TTS adapter boundary failure → degraded（可感知行为：SUPPRESS）
                trigger_failsafe(step, level="degraded", reason=f"tts_error:{type(e).__name__}")
                tts_events.append(
                    {
                        "step_index": step,
                        "source": "tts_router",
                        "action": "SUPPRESS",
                        "category": "NAVIGATION",
                        "priority_band": PriorityBand.from_priority(75).name,
                        "message_id": message_id,
                        "reason": f"tts_error:{type(e).__name__}",
                    }
                )
                continue

            after_main = len(tts_mgr.get_queue())
            after_safety = len(tts_mgr.get_safety_queue())
            record_tts_from_queue_delta(
                step=step,
                category="NAVIGATION",
                band=PriorityBand.from_priority(75).name,
                message_id=message_id,
                before_main=before_main,
                after_main=after_main,
                before_safety=before_safety,
                after_safety=after_safety,
                source="tts_router",
            )
        if perf is not None:
            perf["step_wall_us"].append(int((_WALL_PERF_COUNTER() - step_t0) * 1_000_000))

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
    fault_config: Optional[str] = None,
    perf_json: Optional[str] = None,
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
        perf: Optional[Dict[str, Any]] = {} if perf_json else None
        t0_wall = _WALL_PERF_COUNTER()
        event_stream = build_event_stream(replay, clock, fault_config_path=fault_config, perf=perf)
        t1_wall = _WALL_PERF_COUNTER()

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

    if perf_json:
        # 输出 perf 数据（不参与 hash）
        perf_out = {
            "runner_version": RUNNER_VERSION,
            "git_commit": _git_commit(),
            "replay_id": replay.replay_id,
            "steps": replay.time.steps,
            "delta_ms": replay.time.delta_ms,
            "fault_config": fault_config or "",
            "wall_total_ms": int((t1_wall - t0_wall) * 1000.0),
            "step_wall_us": (perf or {}).get("step_wall_us", []),
            "tts_enqueue_wall_us": (perf or {}).get("tts_enqueue_wall_us", []),
        }
        with open(perf_json, "w", encoding="utf-8") as f:
            f.write(json.dumps(perf_out, ensure_ascii=False, sort_keys=True, indent=2))
            f.write("\n")

    # hash 输入（只包含三段事件流 + 输入时间规格与 replay_id/seed，均为确定性字段）
    hash_input = {
        "replay_id": replay.replay_id,
        "seed": replay.seed,
        "time": {
            "t0_ms": replay.time.t0,
            "delta_ms": replay.time.delta_ms,
            "steps": replay.time.steps,
        },
        "fault_config": fault_config or "",
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
        "fault_config": fault_config or "",
    }
    return digest, meta


def _validate(
    script_path: str,
    input_path: str,
    runs: int,
    report_path: str,
    fast_sleep_ms: int = 0,
    slow_sleep_ms: int = 5,
    fault_config: Optional[str] = None,
) -> int:
    def run_subprocess(sleep_ms: int, dump_events_path: str) -> str:
        out = subprocess.check_output(
            [
                sys.executable,
                script_path,
                input_path,
                "--sleep-ms",
                str(sleep_ms),
                "--dump-events",
                dump_events_path,
                "--print-hash-only",
                *(["--fault-config", fault_config] if fault_config else []),
            ],
            stderr=subprocess.STDOUT,
        ).decode("utf-8", errors="replace")
        for line in out.splitlines()[::-1]:
            if line.startswith("[REPLAY][HASH] sha256="):
                return line.split("sha256=", 1)[1].strip()
        raise RuntimeError("Hash line not found in subprocess output:\n" + out)

    fast_hashes: List[str] = []
    slow_hashes: List[str] = []
    first_diff: Optional[str] = None

    with tempfile.TemporaryDirectory(prefix="replay_gate_") as td:
        fast_events: List[str] = []
        slow_events: List[str] = []

        for i in range(runs):
            p = os.path.join(td, f"fast_{i+1}.json")
            fast_hashes.append(run_subprocess(fast_sleep_ms, p))
            fast_events.append(open(p, "r", encoding="utf-8").read())

        for i in range(runs):
            p = os.path.join(td, f"slow_{i+1}.json")
            slow_hashes.append(run_subprocess(slow_sleep_ms, p))
            slow_events.append(open(p, "r", encoding="utf-8").read())

        # 若 hash 不一致，给出首差异定位（基于 canonical JSON 内容）
        baseline = fast_events[0] if fast_events else ""
        all_events = fast_events + slow_events
        for idx, evs in enumerate(all_events, 1):
            if evs != baseline:
                # pretty diff
                try:
                    a = json.dumps(json.loads(baseline), ensure_ascii=False, sort_keys=True, indent=2).splitlines()
                    b = json.dumps(json.loads(evs), ensure_ascii=False, sort_keys=True, indent=2).splitlines()
                    diff_lines = list(
                        difflib.unified_diff(
                            a, b, fromfile="baseline", tofile=f"run_{idx}", lineterm=""
                        )
                    )
                    first_diff = "\n".join(diff_lines[:200])
                except Exception:
                    first_diff = "diff_unavailable"
                break

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
    if fault_config:
        lines.append(f"- fault_config: `{fault_config}`")
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
    if not ok and first_diff:
        lines.append("")
        lines.append("## First diff (truncated)")
        lines.append("")
        lines.append("```")
        lines.append(first_diff)
        lines.append("```")
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
    fault_config: Optional[str] = args["fault_config"]
    perf_json: Optional[str] = args["perf_json"]

    script_path = os.path.abspath(__file__)

    if validate_runs > 0:
        if report_path is None:
            report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "replay_validation_report.md")
        return _validate(
            script_path=script_path,
            input_path=input_path,
            runs=validate_runs,
            report_path=report_path,
            fault_config=fault_config,
        )

    try:
        _run_once(
            input_path=input_path,
            sleep_ms=sleep_ms,
            dump_events=dump_events,
            print_hash_only=print_hash_only,
            fault_config=fault_config,
            perf_json=perf_json,
        )
        return 0
    except Exception as e:
        print("[REPLAY][FAILED]", str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
