# -*- coding: utf-8 -*-
"""Provider Registry Loader — unified registry access v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.lifecycle.model_registry_state_machine_v1 import (
    is_routing_eligible,
)

_REGISTRY_BASE = "capabilities/midplatform/model_manager"


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[3]


def _load_json(rel: str) -> Dict[str, Any]:
    path = _repo_root() / rel
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_provider_registry() -> Dict[str, Any]:
    return _load_json(f"{_REGISTRY_BASE}/registry/provider_registry_v1.json")


def load_capability_registry() -> Dict[str, Any]:
    return _load_json(f"{_REGISTRY_BASE}/registries/capability_registry_v1.json")


def load_model_registry() -> Dict[str, Any]:
    return _load_json(f"{_REGISTRY_BASE}/registries/model_registry_v1.json")


def load_provider_relationships() -> Dict[str, Any]:
    return _load_json(f"{_REGISTRY_BASE}/registry/provider_relationships_v1.json")


def load_model_families() -> Dict[str, Any]:
    return _load_json(f"{_REGISTRY_BASE}/registry/model_families_v1.json")


def get_provider_by_id(model_id: str, registry: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    reg = registry or load_provider_registry()
    return next((p for p in reg.get("providers") or [] if p.get("model_id") == model_id), None)


def get_capability_entry(capability_id: str) -> Optional[Dict[str, Any]]:
    reg = load_capability_registry()
    return next((c for c in reg.get("capabilities") or [] if c.get("capability_id") == capability_id), None)


def get_family_by_id(family_id: str) -> Optional[Dict[str, Any]]:
    reg = load_model_families()
    return next((f for f in reg.get("families") or [] if f.get("family_id") == family_id), None)


def get_provider_relations(model_id: str) -> List[Dict[str, Any]]:
    reg = load_provider_relationships()
    entry = next((r for r in reg.get("relationships") or [] if r.get("provider") == model_id), None)
    return (entry or {}).get("relations") or []


def list_capability_providers(capability_id: str) -> List[Dict[str, Any]]:
    """Capability-first: find all providers for a capability need."""
    cap = get_capability_entry(capability_id)
    provider_reg = load_provider_registry()
    if not cap:
        return []

    results: List[Dict[str, Any]] = []
    for prov in cap.get("providers") or []:
        model_id = prov.get("model_id", "")
        if model_id in ("human_review",):
            continue
        profile = get_provider_by_id(model_id, provider_reg)
        if not profile:
            continue
        if capability_id not in (profile.get("capabilities") or []):
            cap_profile = (profile.get("routing_profile") or {}).get(capability_id)
            if not cap_profile:
                weaknesses = profile.get("weaknesses") or []
                if capability_id in weaknesses:
                    continue
                continue
        results.append({
            **profile,
            "capability_registry_priority": prov.get("priority", 99),
            "capability_registry_status": prov.get("status", "active"),
        })
    return results


def is_provider_routing_eligible(provider: Dict[str, Any]) -> bool:
    state = provider.get("lifecycle_state", "candidate")
    admission = provider.get("admission_status", "")
    if state == "deprecated" or state == "blocked":
        return False
    return is_routing_eligible(state, admission_status=admission)


def filter_routing_eligible(providers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [p for p in providers if is_provider_routing_eligible(p)]
