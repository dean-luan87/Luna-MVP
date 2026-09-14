# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from mid_platform.model_governance.schemas.model_registry_card import ModelRegistryCard


class ModelRegistryService:
    """内存 + 可选 JSON 文件的模型注册表。"""

    def __init__(self, json_path: Optional[Path] = None) -> None:
        self._by_id: Dict[str, ModelRegistryCard] = {}
        self._json_path = json_path
        if json_path and json_path.exists():
            self._load_json(json_path)

    def _load_json(self, path: Path) -> None:
        raw = json.loads(path.read_text(encoding="utf-8"))
        for item in raw.get("models", []):
            card = ModelRegistryCard.from_dict(item)
            self._by_id[card.model_id] = card

    def persist(self, path: Optional[Path] = None) -> None:
        p = path or self._json_path
        if not p:
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = {"models": [c.to_dict() for c in self._by_id.values()]}
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def register(self, card: ModelRegistryCard) -> None:
        self._by_id[card.model_id] = card

    def get(self, model_id: str) -> Optional[ModelRegistryCard]:
        return self._by_id.get(model_id)

    def list_enabled(self) -> List[ModelRegistryCard]:
        return [c for c in self._by_id.values() if c.enabled]

    def filter(
        self,
        *,
        role_type: Optional[str] = None,
        deployment_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[ModelRegistryCard]:
        out: List[ModelRegistryCard] = list(self._by_id.values())
        if role_type is not None:
            out = [c for c in out if c.role_type == role_type]
        if deployment_type is not None:
            out = [c for c in out if c.deployment_type == deployment_type]
        if status is not None:
            out = [c for c in out if c.status == status]
        return out
