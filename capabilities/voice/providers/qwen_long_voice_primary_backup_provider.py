# -*- coding: utf-8 -*-
"""
长语音任务拆解 — 接入层主备 Provider（M1）。

语义（写死）：
- **plus → turbo** 仅属**接入层重试**：主 Provider 超时 / 异常 / 无法产出结构化结果（None）时再调备选。
- **不是**规则链 fallback；validator / builder / unsupported 语义仍在 orchestrator 内处理。

主链默认模型与 policy 真值对齐：``qwen-plus`` → ``qwen-turbo``（见 ``VOICE_LONG_VOICE_TASK_PARSE_POLICY_M0``）。
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.voice.interfaces.voice_long_input_model_provider import VoiceLongInputModelProvider
from capabilities.voice.providers.qwen_external_long_input_model_provider import (
    QwenExternalLongInputModelProvider,
    create_qwen_external_long_input_provider_from_env,
    is_qwen_external_llm_configured,
)
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import VoiceLongInputStructuredParseResult

logger = logging.getLogger(__name__)

_CONFIG_PROMPTS = Path(__file__).resolve().parents[1] / "config" / "prompts"
PROMPT_QWEN_PLUS = _CONFIG_PROMPTS / "voice_long_input_parse_v1_1_prompt_qwen_plus.md"
PROMPT_QWEN_TURBO = _CONFIG_PROMPTS / "voice_long_input_parse_v1_1_prompt_qwen_turbo.md"

PRIMARY_MODEL_ID = "qwen-plus"
BACKUP_MODEL_ID = "qwen-turbo"


class QwenLongVoicePrimaryBackupLongInputProvider:
    """
    先主选 ``qwen-plus``，仅在允许的 provider 级失败下再调 ``qwen-turbo``。

    若主选已返回非 None 的结构化结果，**不再**调备选（即使后续 orchestrator 校验失败）。
    """

    def __init__(
        self,
        primary: VoiceLongInputModelProvider,
        backup: VoiceLongInputModelProvider,
        *,
        primary_model_id: str = PRIMARY_MODEL_ID,
        backup_model_id: str = BACKUP_MODEL_ID,
    ) -> None:
        self._primary = primary
        self._backup = backup
        self.primary_model_id = primary_model_id
        self.backup_model_id = backup_model_id
        self.selected_provider_model_id: str = ""
        self.backup_provider_used: bool = False
        self.provider_switch_reason: str = ""
        self.last_api_route: str = ""
        self.last_usage: Dict[str, Any] = {}
        # M3.5.6b：最小观测补证（默认关闭；仅在专项开关下写入）
        self.audit_raw_model_payload_present: Optional[bool] = None
        self.audit_raw_json_present: Optional[bool] = None
        self.audit_raw_json_top_level_keys: Optional[list[str]] = None
        self.audit_model_chain_detection_reason: str = ""
        self.audit_model_chain_detection_failed_reason: str = ""

    def _reset_trace(self) -> None:
        self.selected_provider_model_id = ""
        self.backup_provider_used = False
        self.provider_switch_reason = ""
        self.last_api_route = ""
        self.last_usage = {}
        self.audit_raw_model_payload_present = None
        self.audit_raw_json_present = None
        self.audit_raw_json_top_level_keys = None
        self.audit_model_chain_detection_reason = ""
        self.audit_model_chain_detection_failed_reason = ""

    def _copy_diagnostics_from(self, p: object) -> None:
        self.last_api_route = str(getattr(p, "last_api_route", "") or "")
        u = getattr(p, "last_usage", None)
        self.last_usage = dict(u) if isinstance(u, dict) else {}
        # audit 观测字段（若底层 provider 支持）
        self.audit_raw_model_payload_present = getattr(p, "audit_raw_model_payload_present", None)
        self.audit_raw_json_present = getattr(p, "audit_raw_json_present", None)
        self.audit_raw_json_top_level_keys = getattr(p, "audit_raw_json_top_level_keys", None)
        self.audit_model_chain_detection_reason = str(getattr(p, "audit_model_chain_detection_reason", "") or "")
        self.audit_model_chain_detection_failed_reason = str(getattr(p, "audit_model_chain_detection_failed_reason", "") or "")

    def parse_long_input(
        self,
        text: str,
        *,
        session_hint: str = "",
        request_id: str = "",
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        self._reset_trace()
        self.selected_provider_model_id = self.primary_model_id

        out: Optional[VoiceLongInputStructuredParseResult] = None
        try:
            out = self._primary.parse_long_input(text, session_hint=session_hint, request_id=request_id)
        except Exception as e:
            logger.warning("qwen_primary_backup_primary_exception rid=%s err=%s", request_id or "", e)
            self.provider_switch_reason = f"primary_exception:{type(e).__name__}"
            return self._invoke_backup(text, session_hint=session_hint, request_id=request_id)

        if out is not None:
            self._copy_diagnostics_from(self._primary)
            return out

        self.provider_switch_reason = "primary_returned_none"
        return self._invoke_backup(text, session_hint=session_hint, request_id=request_id)

    def _invoke_backup(
        self,
        text: str,
        *,
        session_hint: str,
        request_id: str,
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        self.backup_provider_used = True
        self.selected_provider_model_id = self.backup_model_id
        logger.info(
            "qwen_primary_backup_switch rid=%s reason=%s -> %s",
            request_id or "",
            self.provider_switch_reason,
            self.backup_model_id,
        )
        try:
            out = self._backup.parse_long_input(text, session_hint=session_hint, request_id=request_id)
        except Exception as e:
            logger.warning("qwen_primary_backup_backup_exception rid=%s err=%s", request_id or "", e)
            self.provider_switch_reason = (self.provider_switch_reason + f";backup_exception:{type(e).__name__}").strip(
                ";"
            )
            return None
        self._copy_diagnostics_from(self._backup)
        if out is None:
            self.provider_switch_reason = (self.provider_switch_reason + ";backup_returned_none").strip(";")
        return out


def create_qwen_long_voice_task_parse_provider_bundle_from_env(
    *,
    timeout_ms: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
) -> Optional[QwenLongVoicePrimaryBackupLongInputProvider]:
    """
    构造主备 Qwen 外部长输入 Provider：主 ``qwen-plus`` + 备 ``qwen-turbo``（专用 prompt 路径）。

    若未配置百炼（``is_qwen_external_llm_configured`` 为假）则返回 None。
    """
    if not is_qwen_external_llm_configured():
        return None
    base = create_qwen_external_long_input_provider_from_env(
        timeout_ms=timeout_ms,
        max_output_tokens=max_output_tokens,
    )
    if base is None:
        return None

    kw: Dict[str, Any] = dict(
        api_key=base.api_key,
        responses_url=base.responses_url,
        chat_base_url=base.chat_base_url,
        timeout_ms=base.timeout_ms,
        max_output_tokens=base.max_output_tokens,
        schema_strict=base.schema_strict,
        prefer_responses_api=base.prefer_responses_api,
        responses_http_timeout_sec=base.responses_http_timeout_sec,
        chat_http_timeout_sec=base.chat_http_timeout_sec,
    )
    primary = QwenExternalLongInputModelProvider(
        **kw,
        model=PRIMARY_MODEL_ID,
        prompt_path=PROMPT_QWEN_PLUS,
    )
    backup = QwenExternalLongInputModelProvider(
        **kw,
        model=BACKUP_MODEL_ID,
        prompt_path=PROMPT_QWEN_TURBO,
    )
    return QwenLongVoicePrimaryBackupLongInputProvider(primary, backup)


def create_qwen_long_voice_single_model_provider_from_env(
    *,
    model_id: str,
    timeout_ms: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
) -> Optional[QwenExternalLongInputModelProvider]:
    """
    单模型长语音解析 Provider（与主备 bundle 共用百炼配置与专用 prompt 路径）。

    ``model_id`` 仅允许 ``qwen-plus`` / ``qwen-turbo``；用于方案 B 前置分档路由（显式开关）。
    """
    if model_id not in (PRIMARY_MODEL_ID, BACKUP_MODEL_ID):
        return None
    if not is_qwen_external_llm_configured():
        return None
    base = create_qwen_external_long_input_provider_from_env(
        timeout_ms=timeout_ms,
        max_output_tokens=max_output_tokens,
    )
    if base is None:
        return None
    kw: Dict[str, Any] = dict(
        api_key=base.api_key,
        responses_url=base.responses_url,
        chat_base_url=base.chat_base_url,
        timeout_ms=base.timeout_ms,
        max_output_tokens=base.max_output_tokens,
        schema_strict=base.schema_strict,
        prefer_responses_api=base.prefer_responses_api,
        responses_http_timeout_sec=base.responses_http_timeout_sec,
        chat_http_timeout_sec=base.chat_http_timeout_sec,
    )
    prompt_path = PROMPT_QWEN_PLUS if model_id == PRIMARY_MODEL_ID else PROMPT_QWEN_TURBO
    return QwenExternalLongInputModelProvider(
        **kw,
        model=model_id,
        prompt_path=prompt_path,
    )
