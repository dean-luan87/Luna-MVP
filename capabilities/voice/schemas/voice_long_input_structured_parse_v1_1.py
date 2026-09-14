# -*- coding: utf-8 -*-
"""
长语音模型输出总 Schema v1.1（voice_task_parse_v1_1）。

模型/规则层输出的是**候选理解结构**，不是执行结果。
顶层块固定，不再扩展；与 LUNA_VOICE_LONG_INPUT_STRUCTURED_PARSE_SCHEMA_V1_1.md 一致。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1 = "voice_task_parse_v1_1"


# —— 2. input_meta ——


@dataclass
class VoiceInputMetaV1_1:
    input_type: str = "voice_long_text"
    source_language: str = "zh"
    raw_text: str = ""
    normalized_text: str = ""
    is_continuation: bool = False
    context_resume_hint: str = ""
    parse_timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_type": self.input_type,
            "source_language": self.source_language,
            "raw_text": self.raw_text,
            "normalized_text": self.normalized_text,
            "is_continuation": self.is_continuation,
            "context_resume_hint": self.context_resume_hint,
            "parse_timestamp": self.parse_timestamp,
        }


# —— 3. input_mode_judgement ——


@dataclass
class InputModeJudgementStructuredV1_1:
    mode: str = ""
    has_task_content: bool = False
    has_non_task_content: bool = False
    should_generate_task_plan: bool = False
    should_preserve_non_task_payload: bool = False
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "has_task_content": self.has_task_content,
            "has_non_task_content": self.has_non_task_content,
            "should_generate_task_plan": self.should_generate_task_plan,
            "should_preserve_non_task_payload": self.should_preserve_non_task_payload,
            "confidence": self.confidence,
        }


# —— 4. global_judgement ——


@dataclass
class GlobalJudgementStructuredV1_1:
    primary_domain: str = ""
    secondary_domains: List[str] = field(default_factory=list)
    intent_complexity: str = "single_step"
    can_map_to_system_tasks: bool = True
    needs_confirmation: bool = False
    needs_clarification: bool = False
    should_reject: bool = False
    rejection_reason_candidate: Optional[str] = None
    safety_risk_level: str = "low"
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_domain": self.primary_domain,
            "secondary_domains": list(self.secondary_domains),
            "intent_complexity": self.intent_complexity,
            "can_map_to_system_tasks": self.can_map_to_system_tasks,
            "needs_confirmation": self.needs_confirmation,
            "needs_clarification": self.needs_clarification,
            "should_reject": self.should_reject,
            "rejection_reason_candidate": self.rejection_reason_candidate,
            "safety_risk_level": self.safety_risk_level,
            "confidence": self.confidence,
        }


# —— 5. task_candidates ——


@dataclass
class TaskCandidateEntityV1_1:
    entity_type: str = ""
    entity_value: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"entity_type": self.entity_type, "entity_value": self.entity_value}


@dataclass
class TaskCandidateConstraintV1_1:
    constraint_type: str = ""
    value: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"constraint_type": self.constraint_type, "value": self.value}


@dataclass
class TaskCandidateV1_1:
    candidate_id: str = ""
    task_domain: str = ""
    task_action: str = ""
    system_mapping_candidate: str = ""
    target: Dict[str, Any] = field(default_factory=dict)
    entities: List[TaskCandidateEntityV1_1] = field(default_factory=list)
    constraints: List[TaskCandidateConstraintV1_1] = field(default_factory=list)
    conditional_clauses: List[Any] = field(default_factory=list)
    execution_order: int = 0
    dependency: Optional[str] = None
    is_temporary: bool = False
    requires_confirmation: bool = False
    can_execute_directly_candidate: bool = True
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "task_domain": self.task_domain,
            "task_action": self.task_action,
            "system_mapping_candidate": self.system_mapping_candidate,
            "target": dict(self.target),
            "entities": [e.to_dict() for e in self.entities],
            "constraints": [c.to_dict() for c in self.constraints],
            "conditional_clauses": list(self.conditional_clauses),
            "execution_order": self.execution_order,
            "dependency": self.dependency,
            "is_temporary": self.is_temporary,
            "requires_confirmation": self.requires_confirmation,
            "can_execute_directly_candidate": self.can_execute_directly_candidate,
            "confidence": self.confidence,
        }


# —— 6. non_task_payload ——


@dataclass
class NonTaskSegmentStructuredV1_1:
    segment_id: str = ""
    segment_type: str = ""
    content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "segment_id": self.segment_id,
            "segment_type": self.segment_type,
            "content": self.content,
        }


@dataclass
class NonTaskPayloadStructuredV1_1:
    exists: bool = False
    segments: List[NonTaskSegmentStructuredV1_1] = field(default_factory=list)
    handoff_candidate: str = "emotion_engine_future"
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exists": self.exists,
            "segments": [s.to_dict() for s in self.segments],
            "handoff_candidate": self.handoff_candidate,
            "confidence": self.confidence,
        }


# —— 7. knowledge_collaboration ——


@dataclass
class MatchedHistoryTaskV1_1:
    task_id: str = ""
    task_type: str = ""
    match_reason: str = ""
    similarity: float = 0.0
    last_used_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "match_reason": self.match_reason,
            "similarity": self.similarity,
            "last_used_at": self.last_used_at,
        }


@dataclass
class MatchedMemoryEntityV1_1:
    entity_type: str = ""
    entity_name: str = ""
    match_reason: str = ""
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "entity_name": self.entity_name,
            "match_reason": self.match_reason,
            "confidence": self.confidence,
        }


@dataclass
class AutoFilledFieldV1_1:
    field_name: str = ""
    filled_value: str = ""
    source: str = ""
    requires_confirmation: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_name": self.field_name,
            "filled_value": self.filled_value,
            "source": self.source,
            "requires_confirmation": self.requires_confirmation,
        }


@dataclass
class KnowledgeCollaborationV1_1:
    history_used: bool = False
    history_confirmation_recommended: bool = False
    matched_history_tasks: List[MatchedHistoryTaskV1_1] = field(default_factory=list)
    matched_memory_entities: List[MatchedMemoryEntityV1_1] = field(default_factory=list)
    auto_filled_fields: List[AutoFilledFieldV1_1] = field(default_factory=list)
    reused_experience_candidates: List[Any] = field(default_factory=list)
    history_conflict_flags: List[Any] = field(default_factory=list)
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "history_used": self.history_used,
            "history_confirmation_recommended": self.history_confirmation_recommended,
            "matched_history_tasks": [x.to_dict() for x in self.matched_history_tasks],
            "matched_memory_entities": [x.to_dict() for x in self.matched_memory_entities],
            "auto_filled_fields": [x.to_dict() for x in self.auto_filled_fields],
            "reused_experience_candidates": list(self.reused_experience_candidates),
            "history_conflict_flags": list(self.history_conflict_flags),
            "confidence": self.confidence,
        }


# —— 8. task_optimization ——


@dataclass
class OptimizationCandidateV1_1:
    optimization_type: str = ""
    from_order: List[str] = field(default_factory=list)
    to_order: List[str] = field(default_factory=list)
    reason: str = ""
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.optimization_type,
            "from_order": list(self.from_order),
            "to_order": list(self.to_order),
            "reason": self.reason,
            "confidence": self.confidence,
        }


@dataclass
class TaskOptimizationV1_1:
    optimization_applied: bool = False
    optimization_candidates: List[OptimizationCandidateV1_1] = field(default_factory=list)
    recommended_reordering: List[str] = field(default_factory=list)
    requires_user_confirmation: bool = False
    optimization_reasoning_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "optimization_applied": self.optimization_applied,
            "optimization_candidates": [o.to_dict() for o in self.optimization_candidates],
            "recommended_reordering": list(self.recommended_reordering),
            "requires_user_confirmation": self.requires_user_confirmation,
            "optimization_reasoning_summary": self.optimization_reasoning_summary,
        }


# —— 9–10. clarification / unsupported ——


@dataclass
class ClarificationCandidateV1_1:
    clarification_id: str = ""
    reason: str = ""
    question_candidate: str = ""
    related_task_candidate_id: Optional[str] = None
    priority: str = "medium"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "clarification_id": self.clarification_id,
            "reason": self.reason,
            "question_candidate": self.question_candidate,
            "related_task_candidate_id": self.related_task_candidate_id,
            "priority": self.priority,
        }


@dataclass
class UnsupportedCandidateV1_1:
    item_id: str = ""
    unsupported_type: str = ""
    content: str = ""
    reason_candidate: str = ""
    suggested_fallback: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "unsupported_type": self.unsupported_type,
            "content": self.content,
            "reason_candidate": self.reason_candidate,
            "suggested_fallback": self.suggested_fallback,
        }


# —— 12. parser_notes ——


@dataclass
class ParserNotesV1_1:
    contains_multiple_intents: bool = False
    contains_conditional_logic: bool = False
    contains_context_reference: bool = False
    possible_conflict_with_current_task: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contains_multiple_intents": self.contains_multiple_intents,
            "contains_conditional_logic": self.contains_conditional_logic,
            "contains_context_reference": self.contains_context_reference,
            "possible_conflict_with_current_task": self.possible_conflict_with_current_task,
            "notes": self.notes,
        }


# —— 11. feedback_candidate（复用 VoiceLongVoiceFeedbackResult 的 dict 形态）——


@dataclass
class VoiceLongInputStructuredParseResult:
    """
    长语音/长文本结构化理解总结果（v1.1）。

    与 `VoiceLongInputParseResult` 并存：前者为管线内对象，本对象为**可图书馆/白盒/模型**交换的总视图。
    """

    schema_version: str = SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1
    input_meta: VoiceInputMetaV1_1 = field(default_factory=VoiceInputMetaV1_1)
    input_mode_judgement: InputModeJudgementStructuredV1_1 = field(default_factory=InputModeJudgementStructuredV1_1)
    global_judgement: GlobalJudgementStructuredV1_1 = field(default_factory=GlobalJudgementStructuredV1_1)
    task_candidates: List[TaskCandidateV1_1] = field(default_factory=list)
    non_task_payload: NonTaskPayloadStructuredV1_1 = field(default_factory=NonTaskPayloadStructuredV1_1)
    knowledge_collaboration: KnowledgeCollaborationV1_1 = field(default_factory=KnowledgeCollaborationV1_1)
    task_optimization: TaskOptimizationV1_1 = field(default_factory=TaskOptimizationV1_1)
    clarification_candidates: List[ClarificationCandidateV1_1] = field(default_factory=list)
    unsupported_candidates: List[UnsupportedCandidateV1_1] = field(default_factory=list)
    feedback_candidate: Dict[str, Any] = field(default_factory=dict)
    parser_notes: ParserNotesV1_1 = field(default_factory=ParserNotesV1_1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "input_meta": self.input_meta.to_dict(),
            "input_mode_judgement": self.input_mode_judgement.to_dict(),
            "global_judgement": self.global_judgement.to_dict(),
            "task_candidates": [t.to_dict() for t in self.task_candidates],
            "non_task_payload": self.non_task_payload.to_dict(),
            "knowledge_collaboration": self.knowledge_collaboration.to_dict(),
            "task_optimization": self.task_optimization.to_dict(),
            "clarification_candidates": [c.to_dict() for c in self.clarification_candidates],
            "unsupported_candidates": [u.to_dict() for u in self.unsupported_candidates],
            "feedback_candidate": dict(self.feedback_candidate),
            "parser_notes": self.parser_notes.to_dict(),
        }
