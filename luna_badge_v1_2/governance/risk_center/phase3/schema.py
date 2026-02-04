from dataclasses import dataclass
from enum import Enum


SCHEMA_VERSION = "risk.phase3.v1"


class RiskAcceleration(str, Enum):
    INCREASING = "INCREASING"
    STABLE = "STABLE"
    DECREASING = "DECREASING"
    UNKNOWN = "UNKNOWN"


class RiskCurvature(str, Enum):
    TOWARD_RISK = "TOWARD_RISK"
    STABLE = "STABLE"
    AWAY_FROM_RISK = "AWAY_FROM_RISK"
    UNKNOWN = "UNKNOWN"


class RiskIrreversibility(str, Enum):
    REVERSIBLE = "REVERSIBLE"
    LIKELY_IRREVERSIBLE = "LIKELY_IRREVERSIBLE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class RiskPhase3Output:
    acceleration: RiskAcceleration
    curvature: RiskCurvature
    irreversibility: RiskIrreversibility
    schema_version: str = SCHEMA_VERSION
