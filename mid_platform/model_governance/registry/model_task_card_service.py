# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Dict, List, Optional

from mid_platform.model_governance.schemas.model_task_card import ModelTaskCard


class ModelTaskCardService:
    """任务卡注册表（内存）。"""

    def __init__(self) -> None:
        self._by_id: Dict[str, ModelTaskCard] = {}
        self._by_model: Dict[str, List[str]] = {}

    def register(self, card: ModelTaskCard) -> None:
        self._by_id[card.task_card_id] = card
        self._by_model.setdefault(card.model_id, []).append(card.task_card_id)

    def get(self, task_card_id: str) -> Optional[ModelTaskCard]:
        return self._by_id.get(task_card_id)

    def list_for_model(self, model_id: str) -> List[ModelTaskCard]:
        ids = self._by_model.get(model_id, [])
        return [self._by_id[i] for i in ids if i in self._by_id]

    def list_by_task_domain(self, task_domain: str) -> List[ModelTaskCard]:
        return [c for c in self._by_id.values() if c.task_domain == task_domain]
