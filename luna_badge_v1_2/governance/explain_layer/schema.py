from dataclasses import dataclass
from typing import List


SCHEMA_VERSION = "explain.v1"


@dataclass(frozen=True)
class ExplainOutput:
    explanation_tags: List[str]
    episodes: List[str]
    confidence: str
    schema_version: str = SCHEMA_VERSION
