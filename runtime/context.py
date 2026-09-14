from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from a3.types import EnvironmentMode


@dataclass
class RuntimeContext:
    env_mode: Optional[EnvironmentMode] = None
    engagement: Optional[Dict[str, Any]] = None
    # D) ENGAGED 失败诊断：在「最终决定不说」处归因用
    rhythm_state: Optional[str] = None
    eligibility: Optional[Dict[str, Any]] = None
    view_confidence: Optional[float] = None
    frame_quality: Optional[str] = None

    # Reasoning Timeline View M0 (reserve-only): summary fields
    timeline_key_transition_count: Optional[int] = None
    timeline_key_transition_summary: Optional[str] = None

    # Memory vs Novel Information Channel M0 (reserve-only)
    dominant_reasoning_channel: Optional[str] = None
    dominant_decision_channel: Optional[str] = None
    novel_memory_candidate_label: Optional[str] = None
    novel_memory_candidate_ready: Optional[bool] = None

    # Environment & Task Context Reserve M0（前提条件摘要；由 DecisionMonitor 帧写回时填充）
    environment_scene_type: Optional[str] = None
    environment_visibility_state: Optional[str] = None
    task_chain_stage: Optional[str] = None
    task_chain_current_action: Optional[str] = None
    task_mode: Optional[str] = None
    task_resume_target: Optional[str] = None
    context_premise_summary: Optional[str] = None

    # Decision Contamination Guard Reserve M0（由 DecisionMonitor 帧写回时填充；仅占位摘要）
    contamination_observation_summary: Optional[str] = None
    contamination_entry_risk_hint: Optional[str] = None
    contamination_mitigation_reserved: Optional[str] = None

    # Post-Processing Intelligence Reserve M0（由 DecisionMonitor 帧写回时填充；仅占位摘要）
    post_processing_summary: Optional[str] = None
    post_processing_routing_hint: Optional[str] = None
    memory_write_reserved: Optional[bool] = None
    library_link_reserved: Optional[bool] = None

    # Scheduled Source State M0（由 DecisionMonitor 帧写回时填充；仅占位摘要）
    scheduled_dominant_source: Optional[str] = None
    scheduled_source_conflict_summary: Optional[str] = None
    scheduled_priority_override_summary: Optional[str] = None

    # Run Summary Reference M0.2（由 DecisionMonitor 帧写回时填充；总结入口摘要，非黑匣子原件）
    run_summary_brief: Optional[str] = None
    run_summary_issue_hint: Optional[str] = None

    # Memory Invocation Explanation M0.3（占位：与 DecisionMonitor frame 对齐时可写回）
    memory_invocation_reason_summary: Optional[str] = None
    memory_invocation_effect_summary: Optional[str] = None

    # Mainline State / Phase M0.4（占位）
    mainline_state: Optional[str] = None
    mainline_phase: Optional[str] = None

    # Summary × Post-Processing Boundary M0.5（占位：与 DecisionMonitor 帧对齐时可写回）
    post_processing_entry_id: Optional[str] = None
    post_processing_requires_trace_backfill: Optional[bool] = None

    # Mainline Narrative Alignment M0.6（占位：统一口径可读摘要）
    mainline_narrative_readable: Optional[str] = None
