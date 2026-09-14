# -*- coding: utf-8 -*-
"""
Audio Worker (V1 minimal real execution layer).

边界（V1 写死）：
- 单线程
- 单队列（maxsize=1）
- request_id 显式贯穿（不推断）
- 只产出 playback_runtime 真状态事件：started/finished/failed/cancelled
- 不做抢占/恢复/优先级/多设备
"""

from __future__ import annotations

import os
import queue
import threading
import time
from dataclasses import asdict
from typing import Any, Callable, Dict, Optional, Tuple

from capabilities.voice.observations.playback_runtime_observation import PlaybackRuntimeObservation


EmitFn = Callable[[str, Dict[str, Any]], None]  # emit(type, data)


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def _now() -> float:
    return time.time()


class AudioWorkerV1:
    def __init__(self) -> None:
        self._q: queue.Queue[tuple[str, Optional[bytes], Dict[str, Any], EmitFn]] = queue.Queue(maxsize=1)
        self._started = False
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        # V1 cancel：只支持按 request_id 取消“当前正在处理”或“队列中等待”的那一条
        self._current_request_id: Optional[str] = None
        self._current_emit: Optional[EmitFn] = None
        self._current_started: bool = False
        self._queued_request_id: Optional[str] = None
        self._pending_cancel: Dict[str, str] = {}  # request_id -> reason

    def start(self) -> None:
        with self._lock:
            if self._started:
                return
            self._started = True
            t = threading.Thread(target=self._loop, name="audio_worker_v1", daemon=True)
            self._thread = t
            t.start()

    def submit(
        self,
        *,
        request_id: str,
        audio_bytes: Optional[bytes],
        metadata: Optional[Dict[str, Any]] = None,
        emit: EmitFn,
    ) -> Tuple[bool, str]:
        if not request_id:
            return False, "missing_request_id"
        if not self._started:
            self.start()

        item = (request_id, audio_bytes, dict(metadata or {}), emit)
        try:
            self._q.put_nowait(item)
            with self._lock:
                self._queued_request_id = request_id
            return True, "enqueued"
        except queue.Full:
            return False, "queue_full"

    def cancel(self, *, request_id: str, reason: str = "external_cancel") -> Tuple[bool, str]:
        """
        V1 cancel 入口（默认关闭）：
        - 仅支持单队列/单线程语义
        - 必须由执行线程产出 playback_cancelled（不在此线程伪造）
        """
        if not _env_truthy("LUNA_ENABLE_INTERRUPT_CANCEL_V1"):
            return False, "cancel_disabled"
        if not request_id:
            return False, "missing_request_id"

        with self._lock:
            self._pending_cancel[request_id] = reason

            # 1) 若当前正在处理且 request_id 命中：标记 pending，worker 会在 started 后/或结束前落 cancelled
            if self._current_request_id == request_id:
                return True, "cancel_marked_current"

            # 2) 尝试从队列中移除待执行项（如果命中，仍由 worker 线程发出 cancelled：通过“cancel_only item”实现）
            drained: list[tuple[str, Optional[bytes], Dict[str, Any], EmitFn]] = []
            removed_emit: Optional[EmitFn] = None
            removed_md: Optional[Dict[str, Any]] = None
            try:
                while True:
                    drained.append(self._q.get_nowait())
            except queue.Empty:
                pass

            kept: list[tuple[str, Optional[bytes], Dict[str, Any], EmitFn]] = []
            for rid, ab, md, emit in drained:
                if rid == request_id and removed_emit is None:
                    removed_emit = emit
                    removed_md = md
                else:
                    kept.append((rid, ab, md, emit))

            # requeue kept items
            for item in kept:
                try:
                    self._q.put_nowait(item)
                except queue.Full:
                    # 单队列语义下不应发生；发生则丢弃并依赖观测排查
                    break

            if removed_emit is not None:
                self._queued_request_id = None
                # 把取消请求重新投递为“仅取消事件”任务，让 worker 线程产出 playback_cancelled
                try:
                    self._q.put_nowait((request_id, None, dict(removed_md or {}), removed_emit))
                    return True, "cancel_enqueued_pending"
                except queue.Full:
                    return True, "cancel_marked_pending_queue_full"

        return True, "cancel_marked_pending"

    def snapshot_state(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "queued_request_id": self._queued_request_id,
                "current_request_id": self._current_request_id,
                "current_started": bool(self._current_started),
            }

    def _emit(self, emit: EmitFn, obs: PlaybackRuntimeObservation) -> None:
        emit("playback_runtime", asdict(obs))

    def _loop(self) -> None:
        while True:
            request_id, audio_bytes, md, emit = self._q.get()
            try:
                with self._lock:
                    self._current_request_id = request_id
                    self._current_emit = emit
                    self._current_started = False
                    if self._queued_request_id == request_id:
                        self._queued_request_id = None

                # V1: 允许用开关强制取消（用于回归/演练）
                if _env_truthy("LUNA_AUDIO_WORKER_V1_FORCE_CANCEL"):
                    self._emit(
                        emit,
                        PlaybackRuntimeObservation(
                            request_id=request_id,
                            timestamp=_now(),
                            event="playback_cancelled",
                            status="cancelled",
                            reason="forced_cancel_v1",
                            metadata=dict(md),
                        ),
                    )
                    continue

                # cancel pending：在开始处理前先检查（此时不应产出 started）
                cancel_reason = None
                with self._lock:
                    if request_id in self._pending_cancel:
                        cancel_reason = self._pending_cancel.pop(request_id)
                if cancel_reason is not None:
                    self._emit(
                        emit,
                        PlaybackRuntimeObservation(
                            request_id=request_id,
                            timestamp=_now(),
                            event="playback_cancelled",
                            status="cancelled",
                            reason=str(cancel_reason),
                            metadata=dict(md),
                        ),
                    )
                    continue

                if not audio_bytes:
                    self._emit(
                        emit,
                        PlaybackRuntimeObservation(
                            request_id=request_id,
                            timestamp=_now(),
                            event="playback_failed",
                            status="fail",
                            reason="no_audio_bytes",
                            metadata=dict(md),
                        ),
                    )
                    continue

                # 真事件：worker 开始处理才算 playback_started
                self._emit(
                    emit,
                    PlaybackRuntimeObservation(
                        request_id=request_id,
                        timestamp=_now(),
                        event="playback_started",
                        status="ok",
                        reason="audio_worker_started",
                        metadata={**dict(md), "audio_bytes_len": len(audio_bytes)},
                    ),
                )
                with self._lock:
                    self._current_started = True

                # V1：不接真实设备播放，先以“执行层已处理完成”作为最小闭环。
                # 后续接入真实播放设备/队列后，该段改为实际播放调用与阻塞等待。
                # V1 cancel：给一个极小的“执行窗口”，允许外部 cancel 在 started 后生效
                try:
                    play_ms = int(os.getenv("LUNA_AUDIO_WORKER_V1_SIMULATED_PLAY_MS", "0") or "0")
                except Exception:
                    play_ms = 0
                if play_ms > 0:
                    step = 0.01
                    remaining = max(0.0, play_ms / 1000.0)
                    while remaining > 0:
                        time.sleep(min(step, remaining))
                        remaining -= step
                        with self._lock:
                            if request_id in self._pending_cancel:
                                cancel_reason2 = self._pending_cancel.pop(request_id)
                                self._emit(
                                    emit,
                                    PlaybackRuntimeObservation(
                                        request_id=request_id,
                                        timestamp=_now(),
                                        event="playback_cancelled",
                                        status="cancelled",
                                        reason=str(cancel_reason2),
                                        metadata=dict(md),
                                    ),
                                )
                                raise RuntimeError("__cancelled__")

                if _env_truthy("LUNA_AUDIO_WORKER_V1_FORCE_FAIL"):
                    self._emit(
                        emit,
                        PlaybackRuntimeObservation(
                            request_id=request_id,
                            timestamp=_now(),
                            event="playback_failed",
                            status="fail",
                            reason="forced_fail_v1",
                            metadata=dict(md),
                        ),
                    )
                    continue

                self._emit(
                    emit,
                    PlaybackRuntimeObservation(
                        request_id=request_id,
                        timestamp=_now(),
                        event="playback_finished",
                        status="ok",
                        reason="audio_worker_finished",
                        metadata=dict(md),
                    ),
                )
            except RuntimeError as e:
                if str(e) == "__cancelled__":
                    # cancelled 已发出；不要再发 finished/failed
                    pass
                else:
                    raise
            finally:
                with self._lock:
                    self._current_request_id = None
                    self._current_emit = None
                    self._current_started = False
                try:
                    self._q.task_done()
                except Exception:
                    pass


_WORKER_SINGLETON: Optional[AudioWorkerV1] = None


def get_audio_worker_v1() -> AudioWorkerV1:
    global _WORKER_SINGLETON
    if _WORKER_SINGLETON is None:
        _WORKER_SINGLETON = AudioWorkerV1()
        _WORKER_SINGLETON.start()
    return _WORKER_SINGLETON

