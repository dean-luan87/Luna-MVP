from dataclasses import dataclass
from typing import Dict


SCHEMA_VERSION = "evaluation.v1"


@dataclass(frozen=True)
class EvaluationMetrics:
    schema_version: str
    window: str
    metrics: Dict[str, float]
    sample_size: int
    generated_at: float
