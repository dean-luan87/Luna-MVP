# -*- coding: utf-8 -*-
"""
Playback Plane (V1 minimal).

职责（V1 写死）：
- 接收 request_id + audio_bytes + 最小 metadata
- 投递到 Audio Worker 队列（不阻塞）
- 不负责产出 playback_started/finished（真事件必须由 worker 线程产出）
"""

from __future__ import annotations

import os
from typing import Any, Callable, Dict, Optional, Tuple

from capabilities.voice.output.audio_worker_v1 import EmitFn, get_audio_worker_v1


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


class PlaybackPlaneV1:
    def submit(
        self,
        *,
        request_id: str,
        audio_bytes: Optional[bytes],
        metadata: Optional[Dict[str, Any]] = None,
        emit: EmitFn,
    ) -> Tuple[bool, str]:
        worker = get_audio_worker_v1()
        return worker.submit(request_id=request_id, audio_bytes=audio_bytes, metadata=metadata, emit=emit)

    def cancel(self, *, request_id: str, reason: str = "external_cancel") -> Tuple[bool, str]:
        worker = get_audio_worker_v1()
        return worker.cancel(request_id=request_id, reason=reason)


_PLANE_SINGLETON: Optional[PlaybackPlaneV1] = None


def get_playback_plane_v1() -> PlaybackPlaneV1:
    global _PLANE_SINGLETON
    if _PLANE_SINGLETON is None:
        _PLANE_SINGLETON = PlaybackPlaneV1()
    return _PLANE_SINGLETON

