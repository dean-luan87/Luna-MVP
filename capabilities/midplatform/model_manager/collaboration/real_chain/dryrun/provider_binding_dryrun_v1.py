# -*- coding: utf-8 -*-
"""Provider Binding DryRun — slot fill with upgrade support v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.collaboration.real_chain.slot_provider_binding_v1 import (
    bind_slot_providers,
    get_shopfront_chain_slots,
)


def bind_providers_for_dryrun(
    *,
    provider_overrides: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Bind slots to providers; supports ocr_v1 → ocr_v2 upgrade."""
    slots = get_shopfront_chain_slots()
    bound = bind_slot_providers(slots, provider_overrides=provider_overrides)
    return {
        "collaboration_slots": slots,
        "bound_slots": bound,
        "slot_provider_binding": {s["slot_id"]: s["filled_provider_id"] for s in bound},
        "candidate_only": True,
    }


def upgrade_slot_provider(
    *,
    slot_id: str,
    new_provider_id: str,
    original_binding: Dict[str, str],
) -> Dict[str, Any]:
    """Case B: provider upgrade — only binding changes."""
    upgraded = dict(original_binding)
    old_provider = upgraded.get(slot_id)
    upgraded[slot_id] = new_provider_id
    return {
        "slot_id": slot_id,
        "old_provider_id": old_provider,
        "new_provider_id": new_provider_id,
        "slot_provider_binding_before": original_binding,
        "slot_provider_binding_after": upgraded,
        "l1_unchanged": True,
        "l2_unchanged": True,
        "collaboration_plan_unchanged": True,
        "only_binding_changed": True,
        "candidate_only": True,
    }
