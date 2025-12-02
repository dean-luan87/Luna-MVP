#!/usr/bin/env python3
"""
导航卡死监控模块 v1.3.0
Navigation Stuck Monitor - 检测导航进度卡死
"""

import time
import threading
from typing import Optional, Callable, Dict, Any

# --- Telemetry fallback（防止 1.3.0 没有完整 telemetry 时报错） ---
try:
    from core.telemetry import log_event, build_event, register_observer
except Exception:
    def log_event(evt: dict):
        print("[telemetry-fallback]", evt)

    def build_event(event_type: str, data: dict):
        d = {"ts": time.time(), "type": event_type}
        d.update(data)
        return d

    def register_observer(cb):
        return


class NavStuckMonitor:
    """
    导航卡死监控（NAV_STUCK）：
      - 长时间没有导航进度 → 触发 NAV_STUCK 错误事件
      - 自动监听 telemetry 导航事件
      - 可手动 notify_xxx 通知进度
    """

    def __init__(
        self,
        stuck_threshold_sec: float = 15.0,
        check_interval_sec: float = 2.0,
        min_progress_delta: float = 0.5,
        event_sink: Optional[Callable[[dict], None]] = None,
    ):
        self.stuck_threshold_sec = stuck_threshold_sec
        self.check_interval_sec = check_interval_sec
        self.min_progress_delta = min_progress_delta

        self.event_sink = event_sink or log_event

        # 导航实时状态
        self._lock = threading.Lock()
        self.nav_active = False
        self.current_route_id: Optional[str] = None
        self.last_progress_time: Optional[float] = None
        self.last_progress_value: Optional[float] = None
        self.last_state: Optional[str] = None

        self._running = False
        self._thread: Optional[threading.Thread] = None

    # ====== 手动模式 ======

    def notify_nav_start(self, route_id: Optional[str] = None, state: str = "START"):
        with self._lock:
            self.nav_active = True
            self.current_route_id = route_id or f"route-{int(time.time())}"
            self.last_progress_time = time.time()
            self.last_progress_value = None
            self.last_state = state

    def notify_nav_progress(self, progress_value: float, state: Optional[str] = None):
        now = time.time()
        with self._lock:
            if not self.nav_active:
                self.nav_active = True
                self.last_progress_time = now

            self.last_progress_time = now
            self.last_progress_value = float(progress_value)
            if state:
                self.last_state = state

    def notify_nav_end(self, success: bool = True, reason: str = "COMPLETE"):
        with self._lock:
            self.nav_active = False
            self.last_state = reason

    # ====== 自动模式（Telemetry）======

    def handle_telemetry_event(self, event: Dict[str, Any]):
        domain = event.get("domain", "")

        if not (
            domain.startswith("navigation.path")
            or domain.startswith("navigation.fsm")
        ):
            return

        evt_type = event.get("type")
        data = event.get("data") or event

        # 导航开始
        if evt_type == "nav_start" or data.get("event") == "nav_start":
            self.notify_nav_start(
                route_id=data.get("route_id"),
                state=data.get("state", "START"),
            )
            return

        # 导航结束
        if evt_type == "nav_end" or data.get("event") == "nav_end":
            self.notify_nav_end(
                success=data.get("success", True),
                reason=data.get("reason", "COMPLETE"),
            )
            return

        # 导航进度
        if evt_type == "nav_progress" or "progress_value" in data:
            pv = data.get("progress_value")
            if pv is not None:
                self.notify_nav_progress(
                    float(pv),
                    state=data.get("state"),
                )

    # ====== 卡死检测线程 ======

    def start(self, daemon=True):
        if self._thread and self._thread.is_alive():
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=daemon)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            try:
                self._check_stuck()
            except Exception:
                pass
            time.sleep(self.check_interval_sec)

    def _check_stuck(self):
        now = time.time()
        with self._lock:
            if not self.nav_active:
                return
            if self.last_progress_time is None:
                self.last_progress_time = now
                return

            idle = now - self.last_progress_time
            if idle < self.stuck_threshold_sec:
                return

            route_id = self.current_route_id
            state = self.last_state
            progress = self.last_progress_value

        # 构造 NAV_STUCK 事件
        evt = build_event(
            "error",
            {
                "domain": "navigation.path",
                "code": "NAV_STUCK",
                "msg": "navigation appears stuck (no progress)",
                "severity": 3,
                "route_id": route_id,
                "state": state,
                "last_progress_value": progress,
                "idle_sec": idle,
            },
        )
        self._emit(evt)

    def _emit(self, event: dict):
        # 1) 正常写入 telemetry / 日志
        try:
            self.event_sink(event)
        except Exception:
            pass

        # 2) 如果是 NAV_STUCK，进入自愈 stub 入口（当前版本只记录，不强制重启）
        try:
            if event.get("code") == "NAV_STUCK":
                from selfheal.nav_recovery_stub import handle_nav_stuck
                handle_nav_stuck(event)
        except Exception:
            # 自愈逻辑异常不影响主流程
            pass


_global_nav_monitor: Optional[NavStuckMonitor] = None


def start_global_nav_monitor(
    stuck_threshold_sec: float = 15.0,
    check_interval_sec: float = 2.0,
):
    global _global_nav_monitor
    if _global_nav_monitor:
        return _global_nav_monitor

    nm = NavStuckMonitor(
        stuck_threshold_sec=stuck_threshold_sec,
        check_interval_sec=check_interval_sec,
    )
    _global_nav_monitor = nm
    nm.start()

    # 自动加入 telemetry observer
    try:
        register_observer(nm.handle_telemetry_event)
    except Exception:
        pass

    return nm


if __name__ == "__main__":
    m = start_global_nav_monitor(stuck_threshold_sec=5, check_interval_sec=1)
    m.notify_nav_start(route_id="demo")
    m.notify_nav_progress(10.0)
    print("等待 5 秒触发 NAV_STUCK")
    time.sleep(7)



