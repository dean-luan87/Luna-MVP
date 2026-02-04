# backend/system/watchdog_daemon.py

import threading
import time
from typing import Callable


class WatchdogDaemon:
    """
    简单守护线程：
    - 定期检查一个 "heartbeat" 函数
    - 如果超时/异常，则调用 "on_dead" 回调
    """

    def __init__(self, heartbeat: Callable[[], bool], on_dead: Callable[[], None],
                 interval_sec: float = 5.0, max_fail: int = 3):
        self.heartbeat = heartbeat
        self.on_dead = on_dead
        self.interval_sec = interval_sec
        self.max_fail = max_fail
        self._fail_count = 0
        self._stop_flag = False
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_flag = True

    def _run(self):
        while not self._stop_flag:
            try:
                ok = self.heartbeat()
                if ok:
                    self._fail_count = 0
                else:
                    self._fail_count += 1
            except Exception:
                self._fail_count += 1

            if self._fail_count >= self.max_fail:
                self.on_dead()
                self._fail_count = 0  # 避免不断触发

            time.sleep(self.interval_sec)



