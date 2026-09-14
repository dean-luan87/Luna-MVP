from abc import ABC, abstractmethod
from typing import Optional


class Evidence:
    def __init__(self, entity_id: str, timestamp: float):
        self.entity_id = entity_id
        self.timestamp = timestamp


class BaseObserver(ABC):
    @abstractmethod
    def poll(self) -> Optional[Evidence]:
        """返回一次 evidence 或 None"""
        raise NotImplementedError
