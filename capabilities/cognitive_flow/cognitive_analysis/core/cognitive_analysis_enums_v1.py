"""Controlled enum values for the A3 Cognitive Analysis skeleton v1."""

from __future__ import annotations

from enum import Enum


class AdmissionStatusV1(str, Enum):
    ADMITTED = "admitted"
    CONDITIONALLY_ADMITTED = "conditionally_admitted"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class HypothesisTypeV1(str, Enum):
    STATE_INTERPRETATION = "state_interpretation"
    RELATION_INTERPRETATION = "relation_interpretation"
    CHANGE_EXPLANATION = "change_explanation"
    INTENT_CANDIDATE = "intent_candidate"
    RISK_EXPLANATION = "risk_explanation"
    TASK_RELEVANCE = "task_relevance"
    CAUSAL_CANDIDATE = "causal_candidate"
    UNKNOWN = "unknown"


class HypothesisStatusV1(str, Enum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    UNDERDETERMINED = "underdetermined"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class CompetingHypothesisStatusV1(str, Enum):
    UNRESOLVED = "unresolved"
    PARTIALLY_RESOLVED = "partially_resolved"
    PROVISIONALLY_RESOLVED = "provisionally_resolved"
    CONTRADICTED = "contradicted"
    UNKNOWN = "unknown"


class EvidenceRelationV1(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    NEUTRAL = "neutral"
    INSUFFICIENT = "insufficient"
    UNAVAILABLE = "unavailable"
    REVOKED = "revoked"
    UNKNOWN = "unknown"


class InformationGapTypeV1(str, Enum):
    KNOWN_MISSING = "known_missing"
    CONFLICTING_INFORMATION = "conflicting_information"
    STALE_INFORMATION = "stale_information"
    REVOKED_EVIDENCE = "revoked_evidence"
    INSUFFICIENT_RESOLUTION = "insufficient_resolution"
    TEMPORAL_UNKNOWN = "temporal_unknown"
    RELATION_UNKNOWN = "relation_unknown"
    PERMISSION_RESTRICTED = "permission_restricted"
    UNKNOWN = "unknown"


class AnalysisSufficiencyStatusV1(str, Enum):
    SUFFICIENT = "sufficient"
    CONDITIONALLY_SUFFICIENT = "conditionally_sufficient"
    INSUFFICIENT = "insufficient"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class AnalysisResultStatusV1(str, Enum):
    COMPLETE = "complete"
    PROVISIONAL = "provisional"
    INCOMPLETE = "incomplete"
    BLOCKED = "blocked"
    STALE = "stale"
    UNKNOWN = "unknown"


class LifecycleStatusV1(str, Enum):
    ACTIVE = "active"
    STALE = "stale"
    REFRESH_REQUIRED = "refresh_required"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"
    UNKNOWN = "unknown"


class BlockingLevelV1(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
