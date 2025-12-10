from dataclasses import dataclass
from typing import Callable, Dict
import time
from infra.logging_manager import get_logger

logger = get_logger("recovery")


@dataclass
class ModuleHeartbeat:
    last_ts: float
    timeout_seconds: float


class RecoveryCenter:
    def __init__(
        self,
        get_cpu_load: Callable[[], float],
        safe_mode_enter: Callable[[], None],
        restart_vision: Callable[[], None],
        restart_speech: Callable[[], None],
    ) -> None:
        self._get_cpu_load = get_cpu_load
        self._safe_mode_enter = safe_mode_enter
        self._restart_vision = restart_vision
        self._restart_speech = restart_speech

        self._heartbeats: Dict[str, ModuleHeartbeat] = {}
        self._cpu_overload_triggered: bool = False

    def register_module(self, name: str, timeout_seconds: float) -> None:
        self._heartbeats[name] = ModuleHeartbeat(
            last_ts=time.time(), timeout_seconds=timeout_seconds
        )

    def update_heartbeat(self, name: str) -> None:
        hb = self._heartbeats.get(name)
        if hb:
            hb.last_ts = time.time()

    def _check_heartbeats(self) -> None:
        now = time.time()
        for name, hb in self._heartbeats.items():
            if now - hb.last_ts > hb.timeout_seconds:
                logger.error(f"[RECOVERY] heartbeat timeout for module={name}")
                if "vision" in name:
                    self._restart_vision()
                elif "speech" in name:
                    self._restart_speech()

    def _check_cpu(self) -> None:
        cpu = self._get_cpu_load()
        if cpu > 0.85 and not self._cpu_overload_triggered:
            logger.error(f"[RECOVERY] cpu overload={cpu:.2f}, entering SafeMode.")
            self._cpu_overload_triggered = True
            self._safe_mode_enter()
        elif cpu < 0.7 and self._cpu_overload_triggered:
            logger.info(f"[RECOVERY] cpu back to normal={cpu:.2f}.")
            self._cpu_overload_triggered = False

    def tick(self) -> None:
        self._check_heartbeats()
        self._check_cpu()
