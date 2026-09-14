# -*- coding: utf-8 -*-
"""
Qwen 3.5 4B（本地）长输入解析 Provider（v1）。

目标：实现 `VoiceLongInputModelProvider`，把本地 OpenAI-compatible 推理服务的输出
约束为 `VoiceLongInputStructuredParseResult`（voice_task_parse_v1_1）。

边界：
- 只负责调用本地模型 + 产出结构化候选
- 不做系统裁决（不替代 validator / builder）
- 不接执行层、不触碰 V2/Final
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.voice.interfaces.voice_long_input_model_provider import VoiceLongInputModelProvider
from capabilities.voice.providers.local_llm_client import (
    LocalLLMChatCompletionRequest,
    LocalLLMChatMessage,
    LocalLLMClient,
    LocalLLMClientError,
)
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    GlobalJudgementStructuredV1_1,
    InputModeJudgementStructuredV1_1,
    NonTaskPayloadStructuredV1_1,
    NonTaskSegmentStructuredV1_1,
    ParserNotesV1_1,
    SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
    TaskCandidateConstraintV1_1,
    TaskCandidateEntityV1_1,
    TaskCandidateV1_1,
    VoiceInputMetaV1_1,
    VoiceLongInputStructuredParseResult,
)

logger = logging.getLogger(__name__)


_DEFAULT_PROMPT_PATH = (
    Path(__file__).resolve().parents[1] / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt.md"
)


def _as_bool(x: Any, default: bool = False) -> bool:
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        return bool(x)
    if isinstance(x, str):
        v = x.strip().lower()
        if v in ("true", "1", "yes", "y"):
            return True
        if v in ("false", "0", "no", "n"):
            return False
    return default


def _as_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def _as_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def _as_str(x: Any, default: str = "") -> str:
    return x if isinstance(x, str) else default


def _as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []


def _as_dict(x: Any) -> Dict[str, Any]:
    return x if isinstance(x, dict) else {}


def _build_input_mode(d: Dict[str, Any]) -> InputModeJudgementStructuredV1_1:
    return InputModeJudgementStructuredV1_1(
        mode=_as_str(d.get("mode", "")),
        has_task_content=_as_bool(d.get("has_task_content", False)),
        has_non_task_content=_as_bool(d.get("has_non_task_content", False)),
        should_generate_task_plan=_as_bool(d.get("should_generate_task_plan", False)),
        should_preserve_non_task_payload=_as_bool(d.get("should_preserve_non_task_payload", False)),
        confidence=_as_float(d.get("confidence", 0.0)),
    )


def _build_global_judgement(d: Dict[str, Any]) -> GlobalJudgementStructuredV1_1:
    return GlobalJudgementStructuredV1_1(
        primary_domain=_as_str(d.get("primary_domain", "")),
        secondary_domains=[_as_str(x) for x in _as_list(d.get("secondary_domains")) if isinstance(x, str)],
        intent_complexity=_as_str(d.get("intent_complexity", "single_step")) or "single_step",
        can_map_to_system_tasks=_as_bool(d.get("can_map_to_system_tasks", True), default=True),
        needs_confirmation=_as_bool(d.get("needs_confirmation", False)),
        needs_clarification=_as_bool(d.get("needs_clarification", False)),
        should_reject=_as_bool(d.get("should_reject", False)),
        rejection_reason_candidate=d.get("rejection_reason_candidate", None),
        safety_risk_level=_as_str(d.get("safety_risk_level", "low")) or "low",
        confidence=_as_float(d.get("confidence", 0.0)),
    )


def _build_task_candidate(d: Dict[str, Any]) -> TaskCandidateV1_1:
    ent = []
    for e in _as_list(d.get("entities")):
        ed = _as_dict(e)
        ent.append(TaskCandidateEntityV1_1(entity_type=_as_str(ed.get("entity_type")), entity_value=_as_str(ed.get("entity_value"))))

    cons = []
    for c in _as_list(d.get("constraints")):
        cd = _as_dict(c)
        cons.append(TaskCandidateConstraintV1_1(constraint_type=_as_str(cd.get("constraint_type")), value=_as_str(cd.get("value"))))

    return TaskCandidateV1_1(
        candidate_id=_as_str(d.get("candidate_id", "")),
        task_domain=_as_str(d.get("task_domain", "")),
        task_action=_as_str(d.get("task_action", "")),
        system_mapping_candidate=_as_str(d.get("system_mapping_candidate", "")),
        target=_as_dict(d.get("target")),
        entities=ent,
        constraints=cons,
        conditional_clauses=_as_list(d.get("conditional_clauses")),
        execution_order=_as_int(d.get("execution_order", 0)),
        dependency=d.get("dependency", None) if isinstance(d.get("dependency", None), str) else None,
        is_temporary=_as_bool(d.get("is_temporary", False)),
        requires_confirmation=_as_bool(d.get("requires_confirmation", False)),
        can_execute_directly_candidate=_as_bool(d.get("can_execute_directly_candidate", True), default=True),
        confidence=_as_float(d.get("confidence", 0.0)),
    )


def _build_non_task_payload(d: Dict[str, Any]) -> NonTaskPayloadStructuredV1_1:
    segs: List[NonTaskSegmentStructuredV1_1] = []
    for s in _as_list(d.get("segments")):
        sd = _as_dict(s)
        segs.append(
            NonTaskSegmentStructuredV1_1(
                segment_id=_as_str(sd.get("segment_id", "")),
                segment_type=_as_str(sd.get("segment_type", "")),
                content=_as_str(sd.get("content", "")),
            )
        )
    return NonTaskPayloadStructuredV1_1(
        exists=_as_bool(d.get("exists", False)),
        segments=segs,
        handoff_candidate=_as_str(d.get("handoff_candidate", "emotion_engine_future")) or "emotion_engine_future",
        confidence=_as_float(d.get("confidence", 0.0)),
    )


def _build_parser_notes(d: Dict[str, Any]) -> ParserNotesV1_1:
    return ParserNotesV1_1(
        contains_multiple_intents=_as_bool(d.get("contains_multiple_intents", False)),
        contains_conditional_logic=_as_bool(d.get("contains_conditional_logic", False)),
        contains_context_reference=_as_bool(d.get("contains_context_reference", False)),
        possible_conflict_with_current_task=_as_bool(d.get("possible_conflict_with_current_task", False)),
        notes=_as_str(d.get("notes", "")),
    )


def _unwrap_voice_task_parse_root(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    部分云端模型（例如 qwen3.6-plus）会把整份对象包在 schema 名称键下::

        {"voice_task_parse_v1_1": { "input_mode_judgement": ... } }

    而本链路期望顶层即 ``input_mode_judgement`` / ``global_judgement``。
    若顶层缺少 A 组键且存在与 schema 同名的嵌套 dict，则展开一层。
    """
    if not isinstance(obj, dict):
        return obj
    if obj.get("input_mode_judgement") is not None or obj.get("global_judgement") is not None:
        return obj
    inner = obj.get(SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1)
    if isinstance(inner, dict):
        return inner
    return obj


def dict_to_structured_parse(obj: Dict[str, Any]) -> VoiceLongInputStructuredParseResult:
    """
    将模型 JSON（dict）转为 dataclass 结构。
    注意：系统会在 orchestrator 里 enrich B 组并校验；这里不做系统裁决。
    """
    obj = _unwrap_voice_task_parse_root(obj)
    im = _build_input_mode(_as_dict(obj.get("input_mode_judgement")))
    gj = _build_global_judgement(_as_dict(obj.get("global_judgement")))
    tasks = [_build_task_candidate(_as_dict(x)) for x in _as_list(obj.get("task_candidates"))]
    ntp = _build_non_task_payload(_as_dict(obj.get("non_task_payload")))
    pn = _build_parser_notes(_as_dict(obj.get("parser_notes")))

    # 其他块允许空占位（由系统补齐/忽略）
    res = VoiceLongInputStructuredParseResult(
        schema_version=_as_str(obj.get("schema_version", SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1)) or SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
        input_meta=VoiceInputMetaV1_1(),  # 由系统 enrich 覆盖
        input_mode_judgement=im,
        global_judgement=gj,
        task_candidates=tasks,
        non_task_payload=ntp,
        feedback_candidate=_as_dict(obj.get("feedback_candidate")),
        parser_notes=pn,
    )
    return res


class QwenLongInputModelProvider(VoiceLongInputModelProvider):
    """
    真实本地 Provider（OpenAI-compatible）。

    默认从环境变量读取：
    - `LUNA_LOCAL_LLM_BASE_URL`（例如 http://127.0.0.1:8000）
    - `LUNA_LOCAL_LLM_API_KEY`（可空）
    - `LUNA_QWEN_LONG_INPUT_MODEL`（例如 qwen3.5-4b-instruct）
    """

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        prompt_path: Optional[Path] = None,
        timeout_ms: int = 1800,
        max_tokens: int = 1200,
    ) -> None:
        self.base_url = base_url or os.getenv("LUNA_LOCAL_LLM_BASE_URL", "http://127.0.0.1:8000")
        self.api_key = api_key or os.getenv("LUNA_LOCAL_LLM_API_KEY", "")
        self.model = model or os.getenv("LUNA_QWEN_LONG_INPUT_MODEL", "qwen3.5-4b-instruct")
        self.prompt_path = prompt_path or _DEFAULT_PROMPT_PATH
        self.timeout_ms = int(timeout_ms)
        self.max_tokens = int(max_tokens)
        self.client = LocalLLMClient()

    def _load_prompt(self) -> str:
        try:
            return self.prompt_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning("qwen_prompt_load_failed:%s", e)
            return ""

    def parse_long_input(
        self,
        text: str,
        *,
        session_hint: str = "",
        request_id: str = "",
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        raw = (text or "").strip()
        if not raw:
            return None

        prompt = self._load_prompt()
        sys_content = (prompt or "").strip() or "你必须只输出严格 JSON（voice_task_parse_v1_1）。"
        user_content = f"【长输入】\n{raw}\n\n【上下文 hint】\n{session_hint or ''}\n"

        req = LocalLLMChatCompletionRequest(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.model,
            messages=[
                LocalLLMChatMessage(role="system", content=sys_content),
                LocalLLMChatMessage(role="user", content=user_content),
            ],
            temperature=0.0,
            max_tokens=self.max_tokens,
            timeout_ms=self.timeout_ms,
        )

        try:
            obj = self.client.chat_completion_json(req)
        except LocalLLMClientError as e:
            logger.warning("qwen_local_provider_error:%s rid=%s", e, request_id or "")
            return None
        except Exception as e:
            logger.warning("qwen_local_provider_exception:%s rid=%s", e, request_id or "")
            return None

        if not isinstance(obj, dict):
            return None
        try:
            return dict_to_structured_parse(obj)
        except Exception as e:
            logger.warning("qwen_structured_parse_build_failed:%s rid=%s", e, request_id or "")
            return None

