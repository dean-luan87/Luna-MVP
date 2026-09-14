# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


def _req_str(name: str, v: str) -> str:
    if v is None or (isinstance(v, str) and not v.strip()):
        raise ValueError(f"{name} is required")
    return str(v).strip()


@dataclass
class ModelRegistryCard:
    """中台模型注册卡（最小字段集）。"""

    model_id: str
    display_name: str
    provider: str
    version: str
    deployment_type: str
    runtime_location: str
    role_type: str
    capability_domains: List[str]
    supported_tasks: List[str]
    input_contract_id: str
    input_contract_version: str
    output_contract_id: str
    output_contract_version: str
    allowed_in_mainline: bool
    allowed_in_shadow_mode: bool
    allowed_for_user_facing: bool
    fallback_target_model_id: Optional[str]
    fallback_to_rule_chain: bool
    latency_tier: str
    cost_tier: str
    schema_guard_required: bool
    self_judgement_forbidden: bool
    auto_promotion_forbidden: bool
    enabled: bool
    status: str
    priority: int
    owner_module: str

    def __post_init__(self) -> None:
        self.model_id = _req_str("model_id", self.model_id)
        self.display_name = _req_str("display_name", self.display_name)
        self.provider = _req_str("provider", self.provider)
        self.version = _req_str("version", self.version)
        self.deployment_type = _req_str("deployment_type", self.deployment_type)
        self.runtime_location = _req_str("runtime_location", self.runtime_location)
        self.role_type = _req_str("role_type", self.role_type)
        self.input_contract_id = _req_str("input_contract_id", self.input_contract_id)
        self.input_contract_version = _req_str("input_contract_version", self.input_contract_version)
        self.output_contract_id = _req_str("output_contract_id", self.output_contract_id)
        self.output_contract_version = _req_str("output_contract_version", self.output_contract_version)
        self.latency_tier = _req_str("latency_tier", self.latency_tier)
        self.cost_tier = _req_str("cost_tier", self.cost_tier)
        self.status = _req_str("status", self.status)
        self.owner_module = _req_str("owner_module", self.owner_module)
        if not isinstance(self.capability_domains, list) or not self.capability_domains:
            raise ValueError("capability_domains must be a non-empty list")
        if not isinstance(self.supported_tasks, list) or not self.supported_tasks:
            raise ValueError("supported_tasks must be a non-empty list")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelRegistryCard:
        return cls(
            model_id=str(d["model_id"]),
            display_name=str(d["display_name"]),
            provider=str(d["provider"]),
            version=str(d["version"]),
            deployment_type=str(d["deployment_type"]),
            runtime_location=str(d["runtime_location"]),
            role_type=str(d["role_type"]),
            capability_domains=list(d["capability_domains"]),
            supported_tasks=list(d["supported_tasks"]),
            input_contract_id=str(d["input_contract_id"]),
            input_contract_version=str(d["input_contract_version"]),
            output_contract_id=str(d["output_contract_id"]),
            output_contract_version=str(d["output_contract_version"]),
            allowed_in_mainline=bool(d["allowed_in_mainline"]),
            allowed_in_shadow_mode=bool(d["allowed_in_shadow_mode"]),
            allowed_for_user_facing=bool(d["allowed_for_user_facing"]),
            fallback_target_model_id=(
                None if d.get("fallback_target_model_id") in (None, "") else str(d["fallback_target_model_id"])
            ),
            fallback_to_rule_chain=bool(d["fallback_to_rule_chain"]),
            latency_tier=str(d["latency_tier"]),
            cost_tier=str(d["cost_tier"]),
            schema_guard_required=bool(d["schema_guard_required"]),
            self_judgement_forbidden=bool(d["self_judgement_forbidden"]),
            auto_promotion_forbidden=bool(d["auto_promotion_forbidden"]),
            enabled=bool(d["enabled"]),
            status=str(d["status"]),
            priority=int(d["priority"]),
            owner_module=str(d["owner_module"]),
        )
