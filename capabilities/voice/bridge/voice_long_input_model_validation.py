# -*- coding: utf-8 -*-
"""
长语音模型输出校验（系统治理层，v1）。

非法 system_mapping_candidate 不得穿透到执行链；模型建议可被覆盖。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
    TaskCandidateV1_1,
    VoiceLongInputStructuredParseResult,
)

# 与 internal_task_instructions_v1 前缀对齐的粗粒度白名单
_ALLOWED_MAPPING_PREFIXES: Tuple[str, ...] = (
    "navigation.",
    "observation.",
    "task.",
    "device.",
    "confirmation.",
    "casual_observation.",
    "feedback.",
)


@dataclass
class ModelValidationReport:
    ok: bool = True
    dropped_candidates: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def is_system_mapping_candidate_allowed(system_mapping_candidate: str) -> bool:
    s = (system_mapping_candidate or "").strip()
    if not s:
        return False
    return any(s.startswith(p) for p in _ALLOWED_MAPPING_PREFIXES)


def filter_task_candidates_by_mapping(
    candidates: List[TaskCandidateV1_1],
) -> Tuple[List[TaskCandidateV1_1], ModelValidationReport]:
    """丢弃非法 mapping 的候选，记录 whitebox 可追溯项。"""
    kept: List[TaskCandidateV1_1] = []
    rep = ModelValidationReport()
    for c in candidates:
        if is_system_mapping_candidate_allowed(c.system_mapping_candidate):
            kept.append(c)
        else:
            rep.dropped_candidates.append(c.candidate_id or c.system_mapping_candidate)
    if rep.dropped_candidates:
        rep.errors.append("illegal_system_mapping_candidate")
        rep.ok = False
    return kept, rep


def validate_structured_parse_minimal(s: VoiceLongInputStructuredParseResult) -> Tuple[bool, str]:
    """关键字段缺失则整体视为不可用，触发规则降级。"""
    if s.schema_version != SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1:
        return False, "schema_version_mismatch"
    if not (s.input_mode_judgement and s.input_mode_judgement.mode):
        return False, "missing_input_mode_judgement"
    if not (s.global_judgement and s.global_judgement.primary_domain):
        return False, "missing_global_judgement"
    return True, ""


def sanitize_structured_parse_mappings(s: VoiceLongInputStructuredParseResult) -> VoiceLongInputStructuredParseResult:
    """原地过滤 task_candidates 非法 mapping（仅丢弃，不改写），并在 parser_notes 留痕。

    须在 `validate_model_structured_output` 之前调用（见 `voice_long_input_parse_orchestrator`）；
    否则非法 `system_mapping_candidate` 会先触发整表校验失败并整条回退规则链。
    """
    kept, rep = filter_task_candidates_by_mapping(list(s.task_candidates))
    s.task_candidates = kept
    if rep.errors:
        note = s.parser_notes.notes or ""
        extra = f";mapping_validation:{','.join(rep.dropped_candidates)}"
        s.parser_notes.notes = (note + extra).strip(";")
    return s
