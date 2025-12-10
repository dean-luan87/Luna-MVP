from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Target:
    id: str
    name: str
    lat: float
    lng: float
    extra: dict


class MultiTargetBuffer:
    def __init__(self, max_targets: int = 3) -> None:
        self._max_targets = max_targets
        self._targets: List[Target] = []
        self._current_index: int = -1

    def add_target(self, target: Target) -> bool:
        if len(self._targets) >= self._max_targets:
            return False
        self._targets.append(target)
        return True

    def start(self) -> Optional[Target]:
        if not self._targets:
            return None
        self._current_index = 0
        return self._targets[self._current_index]

    def complete_current(self) -> Optional[Target]:
        if self._current_index == -1:
            return None
        self._current_index += 1
        if self._current_index >= len(self._targets):
            return None
        return self._targets[self._current_index]

    def get_current(self) -> Optional[Target]:
        if 0 <= self._current_index < len(self._targets):
            return self._targets[self._current_index]
        return None

    def get_next(self) -> Optional[Target]:
        idx = self._current_index + 1
        if 0 <= idx < len(self._targets):
            return self._targets[idx]
        return None

    def clear(self) -> None:
        self._targets.clear()
        self._current_index = -1
