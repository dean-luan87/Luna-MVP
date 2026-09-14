# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List, Optional

from mid_platform.model_governance.registry.model_registry_service import ModelRegistryService
from mid_platform.model_governance.routing.model_route_decision import ModelRouteDecision
from mid_platform.model_governance.routing.model_route_policy import ModelRoutePolicy
from mid_platform.model_governance.schemas.model_registry_card import ModelRegistryCard


def _candidate_ok_for_scope(
    card: ModelRegistryCard,
    caller_scope: str,
    policy: ModelRoutePolicy,
) -> bool:
    if not card.enabled:
        return False
    if caller_scope == "mainline":
        return card.allowed_in_mainline
    if caller_scope == "shadow":
        return card.allowed_in_shadow_mode
    if caller_scope == "background":
        if policy.background_only_models:
            return card.model_id in policy.background_only_models
        return True
    return False


def _pick_first(
    registry: ModelRegistryService,
    model_ids: List[str],
    caller_scope: str,
    policy: ModelRoutePolicy,
) -> Optional[ModelRegistryCard]:
    for mid in model_ids:
        if not mid:
            continue
        c = registry.get(mid)
        if c and _candidate_ok_for_scope(c, caller_scope, policy):
            return c
    return None


def select_route(
    *,
    task_domain: str,
    caller_scope: str,
    registry: ModelRegistryService,
    policy: ModelRoutePolicy,
) -> ModelRouteDecision:
    """
    按 policy 选主模型；主不可用则尝试域回退、默认回退；
    仍不可用则 rule_chain 或 reject（见 policy.fallback_to_rule_chain）。
    """
    primary_id = policy.task_domain_to_primary.get(task_domain)
    candidates: List[str] = []
    if primary_id:
        candidates.append(primary_id)
    fb = policy.task_domain_to_fallback.get(task_domain)
    if fb:
        candidates.append(fb)
    if policy.default_fallback_model_id:
        candidates.append(policy.default_fallback_model_id)

    picked = _pick_first(registry, candidates, caller_scope, policy)
    if picked:
        is_fb = picked.model_id != primary_id if primary_id else False
        return ModelRouteDecision(
            task_domain=task_domain,
            selected_model_id=picked.model_id,
            selection_reason="primary" if not is_fb else "fallback_model",
            fallback_applied=is_fb,
            fallback_reason="primary_unavailable" if is_fb else None,
            governance_constraints={},
        )

    if policy.fallback_to_rule_chain:
        return ModelRouteDecision(
            task_domain=task_domain,
            selected_model_id=None,
            selection_reason="rule_chain",
            fallback_applied=True,
            fallback_reason="no_model_available_use_rule_chain",
            governance_constraints={"route": "rule_chain"},
        )

    return ModelRouteDecision(
        task_domain=task_domain,
        selected_model_id=None,
        selection_reason="reject",
        fallback_applied=True,
        fallback_reason="no_model_available",
        governance_constraints={"route": "reject"},
    )
