# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from mid_platform.model_governance.schemas.model_registry_card import ModelRegistryCard


@dataclass
class GovernancePrecheckResult:
    """治理预检结果（是否允许进入主链等）。"""

    allowed: bool
    reasons: List[str] = field(default_factory=list)


class ModelGovernanceDecisionService:
    """最小治理规则：主链准入、自审禁令、生产角色等（骨架）。"""

    def precheck_mainline(self, card: ModelRegistryCard) -> GovernancePrecheckResult:
        reasons: List[str] = []
        if not card.enabled:
            reasons.append("model_disabled")
        if not card.allowed_in_mainline:
            reasons.append("not_allowed_in_mainline")
        if card.role_type != "production":
            reasons.append("role_conflict_mainline_requires_production")
        if not card.self_judgement_forbidden:
            reasons.append("self_judgement_not_forbidden")
        if card.schema_guard_required is False:
            reasons.append("schema_guard_not_required")
        allowed = len(reasons) == 0
        return GovernancePrecheckResult(allowed=allowed, reasons=reasons)

    def precheck_shadow(self, card: ModelRegistryCard) -> GovernancePrecheckResult:
        reasons: List[str] = []
        if not card.enabled:
            reasons.append("model_disabled")
        if not card.allowed_in_shadow_mode:
            reasons.append("not_allowed_in_shadow_mode")
        allowed = len(reasons) == 0
        return GovernancePrecheckResult(allowed=allowed, reasons=reasons)
