# -*- coding: utf-8 -*-
"""
长语音模型输出校验（voice_task_parse_v1_1）。

校验失败不得穿透主线；由 orchestrator 触发规则回退。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
    VoiceLongInputStructuredParseResult,
)
from shared.schemas.task_domain_v1 import PRIMARY_DOMAIN_V1

from capabilities.voice.bridge.voice_long_input_model_validation import is_system_mapping_candidate_allowed


@dataclass
class ModelOutputValidationResult:
    ok: bool
    errors: List[str] = field(default_factory=list)
    """若为 False，orchestrator 应整体回退规则链（若配置允许）。"""
    dropped_mapping_ids: List[str] = field(default_factory=list)


def validate_model_structured_output(
    s: VoiceLongInputStructuredParseResult,
    *,
    cfg: VoiceLongInputParseConfig,
) -> ModelOutputValidationResult:
    """
    写死规则：
    1) schema_version 一致
    2) input_mode / global 存在
    3) primary_domain、secondary_domains 均须在 PRIMARY_DOMAIN_V1
    4) task_candidates 数量 ≤ max_task_candidates（且 ≤3 个明确动作）
    5) system_mapping_candidate 须在白名单（非法则整表失败 → 由调用方回退）
    """
    errs: List[str] = []

    if s.schema_version != SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1:
        errs.append("schema_version_mismatch")

    if not (s.input_mode_judgement and s.input_mode_judgement.mode):
        errs.append("missing_input_mode_judgement")
    if not (s.global_judgement and s.global_judgement.primary_domain):
        errs.append("missing_global_judgement")

    gj = s.global_judgement
    if gj.primary_domain and gj.primary_domain not in PRIMARY_DOMAIN_V1:
        errs.append(f"illegal_primary_domain:{gj.primary_domain}")
    for sd in gj.secondary_domains:
        if sd not in PRIMARY_DOMAIN_V1:
            errs.append(f"illegal_secondary_domain:{sd}")

    n = len(s.task_candidates)
    if n > cfg.max_task_candidates:
        errs.append(f"too_many_task_candidates:{n}>{cfg.max_task_candidates}")
    if n > 3:
        errs.append("exceeds_three_actions_v1")

    for tc in s.task_candidates:
        if not is_system_mapping_candidate_allowed(tc.system_mapping_candidate):
            errs.append(f"illegal_system_mapping:{tc.candidate_id}:{tc.system_mapping_candidate}")

    if cfg.allow_non_task_payload is False and s.non_task_payload.exists:
        errs.append("non_task_payload_not_allowed")

    return ModelOutputValidationResult(ok=len(errs) == 0, errors=errs)
