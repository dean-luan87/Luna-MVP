# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ModelTaskCard:
    """模型 × 任务 任务卡（最小字段集）。"""

    task_card_id: str
    model_id: str
    task_name: str
    task_code: str
    task_domain: str
    task_goal: str
    task_responsibility: str
    task_boundary: str
    task_non_responsibility: str
    input_sources: List[str]
    input_contract: str
    input_required_fields: List[str]
    input_optional_fields: List[str]
    processing_mode: str
    processing_constraints: List[str]
    processing_forbidden_behaviors: List[str]
    output_contract: str
    output_required_fields: List[str]
    output_optional_fields: List[str]
    output_downstream_consumers: List[str]
    success_criteria: str
    failure_criteria: str
    quality_metrics: List[str]
    fallback_behavior: str

    def __post_init__(self) -> None:
        for name, v in [
            ("task_card_id", self.task_card_id),
            ("model_id", self.model_id),
            ("task_name", self.task_name),
            ("task_code", self.task_code),
            ("task_domain", self.task_domain),
            ("task_goal", self.task_goal),
        ]:
            if not v or not str(v).strip():
                raise ValueError(f"{name} is required")
        if not self.input_required_fields:
            raise ValueError("input_required_fields must be non-empty")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ModelTaskCard:
        return cls(
            task_card_id=str(d["task_card_id"]),
            model_id=str(d["model_id"]),
            task_name=str(d["task_name"]),
            task_code=str(d["task_code"]),
            task_domain=str(d["task_domain"]),
            task_goal=str(d["task_goal"]),
            task_responsibility=str(d.get("task_responsibility", "")),
            task_boundary=str(d.get("task_boundary", "")),
            task_non_responsibility=str(d.get("task_non_responsibility", "")),
            input_sources=list(d.get("input_sources", [])),
            input_contract=str(d["input_contract"]),
            input_required_fields=list(d["input_required_fields"]),
            input_optional_fields=list(d.get("input_optional_fields", [])),
            processing_mode=str(d["processing_mode"]),
            processing_constraints=list(d.get("processing_constraints", [])),
            processing_forbidden_behaviors=list(d.get("processing_forbidden_behaviors", [])),
            output_contract=str(d["output_contract"]),
            output_required_fields=list(d.get("output_required_fields", [])),
            output_optional_fields=list(d.get("output_optional_fields", [])),
            output_downstream_consumers=list(d.get("output_downstream_consumers", [])),
            success_criteria=str(d.get("success_criteria", "")),
            failure_criteria=str(d.get("failure_criteria", "")),
            quality_metrics=list(d.get("quality_metrics", [])),
            fallback_behavior=str(d.get("fallback_behavior", "")),
        )
