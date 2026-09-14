"""PCN resource reference and degradation candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceBudgetReference:
    budget_ref: str
    budget_label: str
    source_owner: str


@dataclass(frozen=True)
class ActivationBudgetCandidate:
    candidate_id: str
    resource_ref: ResourceBudgetReference
    scope_label: str
    fixed_max_nodes: bool = False
    fixed_max_links: bool = False
    fixed_depth: bool = False
    fixed_retention_days: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class DegradationCandidate:
    candidate_id: str
    resource_ref: ResourceBudgetReference
    degradation_mode: str
    shrink_active_projection: bool = True
    source_deleted: bool = False
    candidate_only: bool = True
