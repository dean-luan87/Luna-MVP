from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Sequence, Tuple


OCR_MANAGER_MODULE_STATUSES_V1: Tuple[str, ...] = (
    "invalid_input",
    "request_rejected",
    "engine_unavailable",
    "no_text_detected",
    "raw_evidence_ready",
    "layout_ambiguous",
    "reading_order_ambiguous",
    "enhancement_candidate_ready",
    "correction_candidate_ready",
    "crossmodal_conflict",
    "structured_evidence_ready",
    "degraded",
    "unavailable",
)


@dataclass(frozen=True)
class OCRManagerRequestV1:
    request_id: str
    capability: str = "luna.ocr_manager"
    request_type: str = "task_ocr_request"
    source_ref: str = ""
    source_kind: str = "synthetic_fixture"
    frame_ref: str = ""
    image_candidate: Mapping[str, Any] = field(default_factory=dict)
    visual_region_candidates: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    poster_region_candidates: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    task_ocr_request: Mapping[str, Any] = field(default_factory=dict)
    human_correction_input: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    synthetic_integration_fixture: Mapping[str, Any] = field(default_factory=dict)
    crossmodal_context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OCRManagerInputCandidateV1:
    request_id: str
    source_ref: str
    frame_ref: str
    request_type: str
    source_kind: str
    image_candidate: Mapping[str, Any]
    region_candidates: Sequence[Mapping[str, Any]]
    task_ocr_request: Mapping[str, Any]
    human_correction_input: Sequence[Mapping[str, Any]]
    synthetic_integration_fixture: Mapping[str, Any]
    crossmodal_context: Mapping[str, Any]
    input_valid: bool
    rejection_reasons: Sequence[str]


@dataclass(frozen=True)
class OCRRegionCandidateV1:
    region_id: str
    region_type: str
    parent_region_id: str | None
    attribution_target: str
    confidence: float
    unresolved: bool = False


@dataclass(frozen=True)
class OCRRawEvidenceV1:
    evidence_id: str
    raw_text: str
    normalized_text_candidate: str
    region_ref: str
    line_ref: str
    engine_ref: str
    confidence: float
    language_candidate: str
    bounding_geometry: Mapping[str, Any]
    source_frame_ref: str
    captured_at: str
    evidence_status: str


@dataclass(frozen=True)
class OCRTextBlockV1:
    block_id: str
    text: str
    line_refs: Sequence[str]
    region_ref: str
    confidence: float


@dataclass(frozen=True)
class OCRReadingOrderCandidateV1:
    order_id: str
    order_type: str
    ordered_refs: Sequence[str]
    ambiguous: bool
    unresolved_order: bool


@dataclass(frozen=True)
class OCRLayoutCandidateV1:
    layout_id: str
    block_grouping: Sequence[Mapping[str, Any]]
    paragraph_candidates: Sequence[Mapping[str, Any]]
    table_candidates: Sequence[Mapping[str, Any]]
    label_value_candidates: Sequence[Mapping[str, Any]]
    title_body_candidates: Sequence[Mapping[str, Any]]
    spatial_relation_candidates: Sequence[Mapping[str, Any]]


@dataclass(frozen=True)
class OCREnhancementCandidateV1:
    enhancement_id: str
    enhancement_type: str
    original_text_ref: str
    candidate_text: str
    confidence: float
    enhancement_is_evidence_candidate: bool = True
    interpretation_authority: bool = False
    fact_promotion_allowed: bool = False


@dataclass(frozen=True)
class OCRCorrectionCandidateV1:
    correction_id: str
    correction_target: str
    correction_type: str
    original_ocr_ref: str
    corrected_text_candidate: str
    user_correction_source: str
    reviewer_candidate: str
    correction_confidence: float
    correction_trace: Mapping[str, Any]
    training_signal_candidate: Mapping[str, Any]


@dataclass(frozen=True)
class OCRCrossModalConsistencyCandidateV1:
    consistency_id: str
    status: str
    compared_with: str
    detail: str


@dataclass(frozen=True)
class OCRStructuredEvidenceEnvelopeV1:
    request_id: str
    evidence_envelope_id: str
    source_refs: Sequence[str]
    engine_refs: Sequence[str]
    raw_evidence: Sequence[Mapping[str, Any]]
    layout_candidates: Sequence[Mapping[str, Any]]
    reading_order_candidates: Sequence[Mapping[str, Any]]
    region_attribution_candidates: Sequence[Mapping[str, Any]]
    enhancement_candidates: Sequence[Mapping[str, Any]]
    correction_candidates: Sequence[Mapping[str, Any]]
    crossmodal_consistency_candidates: Sequence[Mapping[str, Any]]
    ambiguity_flags: Sequence[str]
    conflict_flags: Sequence[str]
    provenance_refs: Sequence[str]
    trace_ref: str
    replay_key: str
    candidate_only: bool = True
    not_fact: bool = True


@dataclass(frozen=True)
class OCRManagerDiagnosticsV1:
    module_status: str
    request_status: str
    engine_candidate_status: str
    region_status: str
    layout_status: str
    reading_order_status: str
    enhancement_status: str
    correction_status: str
    crossmodal_status: str
    unresolved_items: Sequence[str]
    rejection_reasons: Sequence[str]
    warnings: Sequence[str]
    boundary_flags: Mapping[str, bool]


@dataclass(frozen=True)
class OCRManagerResultV1:
    module_status: str
    input_candidate: Mapping[str, Any]
    governance: Mapping[str, Any]
    engine_capability_candidate: Mapping[str, Any]
    raw_evidence: Sequence[Mapping[str, Any]]
    text_blocks: Sequence[Mapping[str, Any]]
    region_attribution_candidates: Sequence[Mapping[str, Any]]
    layout_candidates: Sequence[Mapping[str, Any]]
    reading_order_candidates: Sequence[Mapping[str, Any]]
    enhancement_candidates: Sequence[Mapping[str, Any]]
    correction_candidates: Sequence[Mapping[str, Any]]
    crossmodal_consistency_candidates: Sequence[Mapping[str, Any]]
    evidence_envelope: Mapping[str, Any]
    diagnostics: Mapping[str, Any]
    trace_ref: str
    replay_key: str
