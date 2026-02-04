import time
from dataclasses import asdict

from core.system_snapshot import create_snapshot
from observe.trace_writer import TraceWriter
from health.heartbeat import update_heartbeat
from c.controller import decide
from execution.c_veto_adapter import apply_c_veto
from runtime.a3_logger import log_a3

TICK_INTERVAL = 0.1  # 100ms


class MainLoop:
    def __init__(self, trace_path: str, a3_runtime=None, runtime_ctx=None, a3_log: bool = False):
        self.tick_id = 0
        self.trace = TraceWriter(trace_path)
        self.running = True
        self.a3_runtime = a3_runtime
        self.runtime_ctx = runtime_ctx
        self.a3_log = a3_log

    def _env_mode_payload(self):
        if self.runtime_ctx is None:
            return None
        mode = getattr(self.runtime_ctx, "env_mode", None)
        if mode is None:
            return None
        payload = asdict(mode)
        if "safety_level" in payload and hasattr(mode.safety_level, "value"):
            payload["safety_level"] = mode.safety_level.value
        if "control_mode" in payload and hasattr(mode.control_mode, "value"):
            payload["control_mode"] = mode.control_mode.value
        return payload

    def run(self) -> None:
        while self.running:
            tick_start = time.time()
            self.tick_id += 1

            if self.a3_runtime and self.runtime_ctx is not None:
                self.a3_runtime.tick(self.runtime_ctx, now_ms=int(tick_start * 1000))
                if self.a3_log:
                    log_a3(self.a3_runtime.last_mode, self.a3_runtime.last_signals)

            snapshot = create_snapshot()
            snapshot = update_heartbeat(snapshot)
            c_result = decide(snapshot)
            execution_intent = apply_c_veto(c_result)

            self.trace.write(
                {
                    "tick_id": self.tick_id,
                    "timestamp": tick_start,
                    "system_snapshot": snapshot,
                    "env_mode": self._env_mode_payload(),
                    "c_decision": {
                        "decision": c_result.decision.value,
                        "reason": c_result.reason_code,
                        "layer": c_result.layer,
                        "facts": c_result.facts,
                    },
                    "execution_intent": execution_intent,
                }
            )

            elapsed = time.time() - tick_start
            sleep_time = max(0, TICK_INTERVAL - elapsed)
            time.sleep(sleep_time)

    def run_for_seconds(self, run_seconds: float) -> None:
        start = time.time()
        try:
            while time.time() - start < run_seconds:
                self.run_once()
        finally:
            self.stop()

    def run_once(self) -> None:
        tick_start = time.time()
        self.tick_id += 1

        if self.a3_runtime and self.runtime_ctx is not None:
            self.a3_runtime.tick(self.runtime_ctx, now_ms=int(tick_start * 1000))
            if self.a3_log:
                log_a3(self.a3_runtime.last_mode, self.a3_runtime.last_signals)

        snapshot = create_snapshot()
        snapshot = update_heartbeat(snapshot)
        c_result = decide(snapshot)
        execution_intent = apply_c_veto(c_result)

        self.trace.write(
            {
                "tick_id": self.tick_id,
                "timestamp": tick_start,
                "system_snapshot": snapshot,
                "env_mode": self._env_mode_payload(),
                "c_decision": {
                    "decision": c_result.decision.value,
                    "reason": c_result.reason_code,
                    "layer": c_result.layer,
                    "facts": c_result.facts,
                },
                "execution_intent": execution_intent,
            }
        )

        elapsed = time.time() - tick_start
        sleep_time = max(0, TICK_INTERVAL - elapsed)
        time.sleep(sleep_time)

    def stop(self) -> None:
        self.running = False
