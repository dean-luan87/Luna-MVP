import time
from typing import Callable, Optional, Any, Dict

from .base import BaseObserver, Evidence


class GenericPresenceObserver(BaseObserver):
    """
    存在型观察器：只关心“是否存在/可见”
    - evaluator(ctx) -> bool
    - True 代表当前可见/存在，返回 Evidence
    """

    def __init__(
        self,
        entity_id: str,
        evaluator: Callable[[Dict[str, Any]], bool],
        ctx: Optional[Dict[str, Any]] = None,
    ):
        self.entity_id = entity_id
        self.evaluator = evaluator
        self.ctx = ctx or {}

    def poll(self) -> Optional[Evidence]:
        if not self.evaluator(self.ctx):
            return None
        return Evidence(entity_id=self.entity_id, timestamp=time.time())


class GenericSignalObserver(BaseObserver):
    """
    信号型观察器：只关心“某个信号是否可读/有效”
    - reader(ctx) -> value | None
    - validator(value) -> bool  (默认：value is not None)
    """

    def __init__(
        self,
        entity_id: str,
        reader: Callable[[Dict[str, Any]], Any],
        validator: Optional[Callable[[Any], bool]] = None,
        ctx: Optional[Dict[str, Any]] = None,
    ):
        self.entity_id = entity_id
        self.reader = reader
        self.validator = validator or (lambda v: v is not None)
        self.ctx = ctx or {}

    def poll(self) -> Optional[Evidence]:
        v = self.reader(self.ctx)
        if not self.validator(v):
            return None
        return Evidence(entity_id=self.entity_id, timestamp=time.time())
