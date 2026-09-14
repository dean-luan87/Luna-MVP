# -*- coding: utf-8 -*-
"""
阿里云百炼（Model Studio）Qwen 外部 API —— 长语音任务拆解 Provider（v1）。

策略（写死）：
1) 优先 OpenAI 兼容 **Responses API**（与百炼文档路径一致）
2) 若 HTTP/解析/结构化失败，回退 OpenAI 兼容 **Chat Completions** + `response_format`（json_schema）
3) 输出统一映射为 `VoiceLongInputStructuredParseResult`，后续 enrich / validator / builder / fallback 不变

治理原则（与产品一致）：
- **执行链与思考链分离**：本 Provider 仅服务「当前轮任务拆解 / 结构化输出 / 进主链」；不在此链路开启千问 **thinking / 深度思考**（显式 `enable_thinking=false` 请求体字段，若服务端识别）。
- **非思考模式**、支持结构化输出的文本模型由调用方选模保证；本类不接 Qwen-Audio、不接多供应商路由。

**默认档位（主链）**：`optimized`（`DEFAULT_QWEN_AB_PROFILE`）— `enable_thinking=false`、默认 `max_output_tokens=1024`、`requests.Session` keep-alive。  
**legacy 档位**：仅用于 A/B 对照、回归基线、故障排查临时对比；**不作为**主链默认。设置 `LUNA_QWEN_AB_PROFILE=legacy`（或 `a`/`baseline`）可切换。

环境变量：
- `LUNA_EXTERNAL_LLM_PROVIDER=qwen`（由 `is_qwen_external_llm_configured` / 工厂读取）
- `DASHSCOPE_API_KEY`：百炼 API Key（与阿里云文档一致）
- `LUNA_QWEN_EXTERNAL_MODEL` 或 `LUNA_EXTERNAL_LLM_MODEL`：模型名（如 `qwen3.5-flash`）
- `LUNA_QWEN_MAX_OUTPUT_TOKENS`：覆盖默认输出上限（默认 1024，结构化 JSON 足够；需更长可显式调大）
- `LUNA_QWEN_AB_PROFILE`（或 `LUNA_QWEN_PROVIDER_PROFILE`）：未设置时等价 **`optimized`（主链默认）**；设为 `legacy` / `a` / `baseline` 则为对照档（不显式关 thinking、默认 max_output=4096、每次请求新建连接）。详见 `docs/architecture/voice/LUNA_VOICE_QWEN_EXTERNAL_PROVIDER_AB_DECISION_M0.md`。

可选：
- `LUNA_QWEN_RESPONSES_URL`：默认中国区 Responses 完整 URL
- `LUNA_QWEN_CHAT_BASE_URL`：默认 `https://dashscope.aliyuncs.com/compatible-mode/v1`（不含末尾 path）
- `LUNA_QWEN_REGION=intl`：切换新加坡兼容 endpoint（Responses + Chat base）
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter

from capabilities.voice.interfaces.voice_long_input_model_provider import VoiceLongInputModelProvider
from capabilities.voice.providers.qwen_long_input_model_provider import dict_to_structured_parse
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import VoiceLongInputStructuredParseResult
from shared.schemas.task_domain_v1 import PRIMARY_DOMAIN_V1

logger = logging.getLogger(__name__)

# 结构化 voice_task_parse JSON 实测输出通常数百 token；下调默认上限有利于缩短解码侧耗时。
_DEFAULT_MAX_OUTPUT_TOKENS = 1024
# A/B 基线（legacy）：与引入 1024 / Session / enable_thinking 之前一致
_LEGACY_DEFAULT_MAX_OUTPUT_TOKENS = 4096

# 主链正式默认：与 A/B 结论一致（见 LUNA_VOICE_QWEN_EXTERNAL_PROVIDER_AB_DECISION_M0.md）
DEFAULT_QWEN_AB_PROFILE = "optimized"


def _read_ab_profile() -> str:
    """
    legacy：不显式传 enable_thinking、默认 max_output=4096、无 Session 复用（仅对照/回归/排障）
    optimized：主链默认（thinking 关、1024、Session）
    """
    p = (
        os.getenv("LUNA_QWEN_AB_PROFILE") or os.getenv("LUNA_QWEN_PROVIDER_PROFILE") or DEFAULT_QWEN_AB_PROFILE
    ).strip().lower()
    if p in ("a", "legacy", "baseline", "old"):
        return "legacy"
    return "optimized"


def qwen_external_ab_profile_label() -> str:
    """供 benchmark / 诊断打印当前档位。"""
    return _read_ab_profile()


def _resolve_max_output_tokens(explicit: Optional[int]) -> int:
    if explicit is not None:
        return max(64, int(explicit))
    raw = (os.getenv("LUNA_QWEN_MAX_OUTPUT_TOKENS") or "").strip()
    if raw:
        return max(64, int(raw))
    return _DEFAULT_MAX_OUTPUT_TOKENS


def _resolve_max_output_tokens_legacy(explicit: Optional[int]) -> int:
    """legacy 基线：默认 4096（与早期 provider 一致）。"""
    if explicit is not None:
        return max(64, int(explicit))
    raw = (os.getenv("LUNA_QWEN_MAX_OUTPUT_TOKENS") or "").strip()
    if raw:
        return max(64, int(raw))
    return _LEGACY_DEFAULT_MAX_OUTPUT_TOKENS


_DEFAULT_PROMPT_PATH = (
    Path(__file__).resolve().parents[1] / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt.md"
)


def _voice_task_parse_v1_1_json_schema() -> Dict[str, Any]:
    """供百炼结构化输出使用的 JSON Schema（strict 默认关，降低兼容摩擦）。"""
    domains = list(PRIMARY_DOMAIN_V1)
    return {
        "type": "object",
        "properties": {
            "schema_version": {"type": "string"},
            "input_mode_judgement": {
                "type": "object",
                "properties": {
                    "mode": {"type": "string"},
                    "has_task_content": {"type": "boolean"},
                    "has_non_task_content": {"type": "boolean"},
                    "should_generate_task_plan": {"type": "boolean"},
                    "should_preserve_non_task_payload": {"type": "boolean"},
                    "confidence": {"type": "number"},
                },
                "required": [
                    "mode",
                    "has_task_content",
                    "has_non_task_content",
                    "should_generate_task_plan",
                    "should_preserve_non_task_payload",
                    "confidence",
                ],
            },
            "global_judgement": {
                "type": "object",
                "properties": {
                    "primary_domain": {"type": "string", "enum": domains},
                    "secondary_domains": {"type": "array", "items": {"type": "string", "enum": domains}},
                    "intent_complexity": {"type": "string"},
                    "can_map_to_system_tasks": {"type": "boolean"},
                    "needs_confirmation": {"type": "boolean"},
                    "needs_clarification": {"type": "boolean"},
                    "should_reject": {"type": "boolean"},
                    "rejection_reason_candidate": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "safety_risk_level": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": [
                    "primary_domain",
                    "secondary_domains",
                    "intent_complexity",
                    "can_map_to_system_tasks",
                    "needs_confirmation",
                    "needs_clarification",
                    "should_reject",
                    "rejection_reason_candidate",
                    "safety_risk_level",
                    "confidence",
                ],
            },
            "task_candidates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "candidate_id": {"type": "string"},
                        "task_domain": {"type": "string"},
                        "task_action": {"type": "string"},
                        "system_mapping_candidate": {"type": "string"},
                        "target": {"type": "object", "additionalProperties": True},
                        "entities": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "entity_type": {"type": "string"},
                                    "entity_value": {"type": "string"},
                                },
                                "required": ["entity_type", "entity_value"],
                            },
                        },
                        "constraints": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "constraint_type": {"type": "string"},
                                    "value": {"type": "string"},
                                },
                                "required": ["constraint_type", "value"],
                            },
                        },
                        "conditional_clauses": {"type": "array", "items": {"type": "string"}},
                        "execution_order": {"type": "integer"},
                        "dependency": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "is_temporary": {"type": "boolean"},
                        "requires_confirmation": {"type": "boolean"},
                        "can_execute_directly_candidate": {"type": "boolean"},
                        "confidence": {"type": "number"},
                    },
                    "required": [
                        "candidate_id",
                        "task_domain",
                        "task_action",
                        "system_mapping_candidate",
                        "target",
                        "entities",
                        "constraints",
                        "conditional_clauses",
                        "execution_order",
                        "dependency",
                        "is_temporary",
                        "requires_confirmation",
                        "can_execute_directly_candidate",
                        "confidence",
                    ],
                },
            },
            "non_task_payload": {
                "type": "object",
                "properties": {
                    "exists": {"type": "boolean"},
                    "segments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "segment_id": {"type": "string"},
                                "segment_type": {"type": "string"},
                                "content": {"type": "string"},
                            },
                            "required": ["segment_id", "segment_type", "content"],
                        },
                    },
                    "handoff_candidate": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": ["exists", "segments", "handoff_candidate", "confidence"],
            },
            "clarification_candidates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "clarification_id": {"type": "string"},
                        "reason": {"type": "string"},
                        "question_candidate": {"type": "string"},
                        "related_task_candidate_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "priority": {"type": "string"},
                    },
                    "required": [
                        "clarification_id",
                        "reason",
                        "question_candidate",
                        "related_task_candidate_id",
                        "priority",
                    ],
                },
            },
            "unsupported_candidates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "string"},
                        "unsupported_type": {"type": "string"},
                        "content": {"type": "string"},
                        "reason_candidate": {"type": "string"},
                        "suggested_fallback": {"type": "string"},
                    },
                    "required": [
                        "item_id",
                        "unsupported_type",
                        "content",
                        "reason_candidate",
                        "suggested_fallback",
                    ],
                },
            },
            "feedback_candidate": {"type": "object", "additionalProperties": True},
            "parser_notes": {
                "type": "object",
                "properties": {
                    "contains_multiple_intents": {"type": "boolean"},
                    "contains_conditional_logic": {"type": "boolean"},
                    "contains_context_reference": {"type": "boolean"},
                    "possible_conflict_with_current_task": {"type": "boolean"},
                    "notes": {"type": "string"},
                },
                "required": [
                    "contains_multiple_intents",
                    "contains_conditional_logic",
                    "contains_context_reference",
                    "possible_conflict_with_current_task",
                    "notes",
                ],
            },
        },
        "required": [
            "schema_version",
            "input_mode_judgement",
            "global_judgement",
            "task_candidates",
            "non_task_payload",
            "clarification_candidates",
            "unsupported_candidates",
            "feedback_candidate",
            "parser_notes",
        ],
    }


def _text_format_json_schema(*, strict: bool = False) -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "name": "voice_task_parse_v1_1",
        "strict": strict,
        "schema": _voice_task_parse_v1_1_json_schema(),
    }


def extract_output_text_from_responses_api_body(body: Dict[str, Any]) -> str:
    """从 OpenAI 兼容 Responses 响应体抽取文本（百炼同形）。"""
    ot = body.get("output_text")
    if isinstance(ot, str) and ot.strip():
        return ot.strip()
    chunks: List[str] = []
    for item in body.get("output") or []:
        if not isinstance(item, dict):
            continue
        if item.get("type") != "message":
            continue
        for part in item.get("content") or []:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "output_text":
                t = part.get("text")
                if isinstance(t, str):
                    chunks.append(t)
            elif part.get("type") == "refusal":
                r = part.get("refusal")
                if isinstance(r, str):
                    chunks.append(r)
    return "".join(chunks).strip()


def _strip_json_fence(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.strip("`").strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t


def _parse_response_json_object(text: str) -> Optional[Dict[str, Any]]:
    raw = _strip_json_fence(text)
    if not raw:
        return None
    try:
        obj = json.loads(raw)
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def _qwen_thinking_off_extra() -> Dict[str, Any]:
    """百炼混合思考模型：请求体显式关闭 thinking（与执行链治理一致）。"""
    return {"enable_thinking": False}


def _default_endpoints_for_region(region: str) -> Tuple[str, str]:
    r = (region or "cn").strip().lower()
    if r in ("intl", "sg", "singapore"):
        return (
            "https://dashscope-intl.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1/responses",
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
    return (
        "https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1/responses",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


class QwenExternalLongInputModelProvider(VoiceLongInputModelProvider):
    """
    百炼 Qwen（OpenAI 兼容）长输入解析。

    API Key 读取顺序：`api_key` 参数 > `DASHSCOPE_API_KEY` > `LUNA_DASHSCOPE_API_KEY`（备用）
    模型读取顺序：构造参数 > `LUNA_QWEN_EXTERNAL_MODEL` > `LUNA_EXTERNAL_LLM_MODEL` > `qwen3.5-flash`
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        responses_url: Optional[str] = None,
        chat_base_url: Optional[str] = None,
        region: Optional[str] = None,
        prompt_path: Optional[Path] = None,
        timeout_ms: int = 120_000,
        max_output_tokens: Optional[int] = None,
        schema_strict: bool = False,
        prefer_responses_api: bool = True,
        responses_http_timeout_sec: Optional[float] = None,
        chat_http_timeout_sec: Optional[float] = None,
    ) -> None:
        self.api_key = (
            (api_key if api_key is not None else os.getenv("DASHSCOPE_API_KEY") or os.getenv("LUNA_DASHSCOPE_API_KEY", ""))
        ).strip()
        self.model = (
            model
            if model is not None
            else (
                os.getenv("LUNA_QWEN_EXTERNAL_MODEL")
                or os.getenv("LUNA_EXTERNAL_LLM_MODEL")
                or "qwen3.5-flash"
            )
        ).strip()
        reg = region if region is not None else os.getenv("LUNA_QWEN_REGION", "cn")
        d_resp, d_chat = _default_endpoints_for_region(reg)
        self.responses_url = (responses_url or os.getenv("LUNA_QWEN_RESPONSES_URL") or d_resp).strip()
        self.chat_base_url = (chat_base_url or os.getenv("LUNA_QWEN_CHAT_BASE_URL") or d_chat).rstrip("/")
        self.prompt_path = prompt_path or _DEFAULT_PROMPT_PATH
        self.timeout_ms = int(timeout_ms)
        self._ab_profile = _read_ab_profile()
        if self._ab_profile == "legacy":
            self.max_output_tokens = _resolve_max_output_tokens_legacy(max_output_tokens)
        else:
            self.max_output_tokens = _resolve_max_output_tokens(max_output_tokens)
        self.schema_strict = bool(schema_strict)
        self.prefer_responses_api = bool(prefer_responses_api)
        # 通道级最小修复：缩短 Responses 单次 HTTP timeout，失败尽快切换 Chat Completions
        # 可用环境变量覆盖（用于 smoke 诊断，避免 120s 抖动污染整轮结果）：
        # - LUNA_QWEN_RESPONSES_HTTP_TIMEOUT_SEC（默认 25）
        # - LUNA_QWEN_CHAT_HTTP_TIMEOUT_SEC（默认 25）
        self.responses_http_timeout_sec = float(
            responses_http_timeout_sec
            if responses_http_timeout_sec is not None
            else os.getenv("LUNA_QWEN_RESPONSES_HTTP_TIMEOUT_SEC", "25")
        )
        self.chat_http_timeout_sec = float(
            chat_http_timeout_sec
            if chat_http_timeout_sec is not None
            else os.getenv("LUNA_QWEN_CHAT_HTTP_TIMEOUT_SEC", "25")
        )
        # 最近一次成功解析出 JSON 对象的通道（供 smoke / 诊断）
        self.last_api_route: str = ""
        # 最近一次成功请求返回的 usage（供 smoke / 诊断），形态保持与返回体一致
        self.last_usage: Dict[str, Any] = {}
        # M3.5.6b：最小观测补证（默认关闭；仅在专项开关下写入，用于定位 model_chain 识别链问题）
        self.audit_raw_model_payload_present: Optional[bool] = None
        self.audit_raw_json_present: Optional[bool] = None
        self.audit_raw_json_top_level_keys: Optional[List[str]] = None
        self.audit_model_chain_detection_reason: str = ""
        self.audit_model_chain_detection_failed_reason: str = ""
        # optimized：同实例多次 parse 复用连接（keep-alive）。legacy：每次请求走 requests.post，便于 A/B 对照
        self._http: Optional[requests.Session]
        if self._ab_profile == "optimized":
            self._http = requests.Session()
            _adapter = HTTPAdapter(pool_connections=4, pool_maxsize=8, max_retries=0)
            self._http.mount("https://", _adapter)
            self._http.mount("http://", _adapter)
            self._http.headers.update(self._headers())
        else:
            self._http = None

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _load_prompt(self) -> str:
        try:
            return self.prompt_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning("qwen_external_prompt_load_failed:%s", e)
            return ""

    def _thinking_merge(self) -> Dict[str, Any]:
        if self._ab_profile == "legacy":
            return {}
        return _qwen_thinking_off_extra()

    def _post_json(self, url: str, payload: Dict[str, Any], *, timeout_sec: float):
        t = max(0.05, float(timeout_sec))
        if self._ab_profile == "legacy":
            return requests.post(url, headers=self._headers(), json=payload, timeout=t)
        assert self._http is not None
        return self._http.post(url, json=payload, timeout=t)

    def _call_responses_api(self, instructions: str, user_input: str, *, timeout_sec: float) -> Optional[Dict[str, Any]]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "instructions": instructions.strip() or "你必须只输出符合 voice_task_parse_v1_1 的 JSON。",
            "input": user_input,
            "max_output_tokens": self.max_output_tokens,
            "text": {"format": _text_format_json_schema(strict=self.schema_strict)},
            **self._thinking_merge(),
        }
        try:
            resp = self._post_json(
                self.responses_url,
                payload,
                timeout_sec=timeout_sec,
            )
        except Exception as e:
            logger.warning("qwen_external_responses_http_error:%s", e)
            return None
        try:
            body = resp.json()
        except Exception:
            logger.warning("qwen_external_responses_non_json status=%s", resp.status_code)
            return None
        if resp.status_code >= 400:
            logger.warning("qwen_external_responses_api_error status=%s body=%s", resp.status_code, body)
            return None
        if isinstance(body.get("error"), dict):
            logger.warning("qwen_external_responses_error_field err=%s", body.get("error"))
            return None
        return body if isinstance(body, dict) else None

    def _call_chat_completions(
        self,
        *,
        messages: List[Dict[str, str]],
        use_json_schema: bool,
        timeout_sec: float,
    ) -> Optional[Dict[str, Any]]:
        url = f"{self.chat_base_url}/chat/completions"
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.0,
            "max_tokens": self.max_output_tokens,
            **self._thinking_merge(),
        }
        if use_json_schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "voice_task_parse_v1_1",
                    "strict": self.schema_strict,
                    "schema": _voice_task_parse_v1_1_json_schema(),
                },
            }
        try:
            resp = self._post_json(
                url,
                payload,
                timeout_sec=timeout_sec,
            )
        except Exception as e:
            logger.warning("qwen_external_chat_http_error:%s", e)
            return None
        try:
            body = resp.json()
        except Exception:
            logger.warning("qwen_external_chat_non_json status=%s", resp.status_code)
            return None
        if resp.status_code >= 400:
            logger.warning("qwen_external_chat_api_error status=%s body=%s", resp.status_code, body)
            return None
        if isinstance(body.get("error"), dict):
            logger.warning("qwen_external_chat_error_field err=%s", body.get("error"))
            return None
        return body if isinstance(body, dict) else None

    def _chat_message_text(self, body: Dict[str, Any]) -> str:
        try:
            return (
                (body.get("choices") or [{}])[0]
                .get("message", {})
                .get("content", "")
            ) or ""
        except Exception:
            return ""

    def _resolve_structured_dict(self, text: str, *, route: str) -> Optional[Dict[str, Any]]:
        obj = _parse_response_json_object(text)
        if obj is None:
            logger.warning("qwen_external_json_parse_failed route=%s", route)
        return obj

    def _remaining_sec(self, deadline_monotonic: float) -> float:
        return max(0.0, deadline_monotonic - time.monotonic())

    def _pick_timeout_sec(self, *, route: str, remaining_sec: float) -> float:
        # 让 provider 总耗时尽量小于 orchestrator 的 model_timeout_ms，避免 120s 卡死污染整轮
        cap = self.responses_http_timeout_sec if route == "responses" else self.chat_http_timeout_sec
        # 预留一点余量给解析/构造对象
        budget = max(0.2, remaining_sec - 0.2)
        return max(0.2, min(float(cap), float(budget)))

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
        if not self.api_key:
            logger.warning("qwen_external_missing_api_key rid=%s", request_id or "")
            return None

        # 每次调用先清空诊断字段，避免上一次残留
        self.last_api_route = ""
        self.last_usage = {}
        self.audit_raw_model_payload_present = None
        self.audit_raw_json_present = None
        self.audit_raw_json_top_level_keys = None
        self.audit_model_chain_detection_reason = ""
        self.audit_model_chain_detection_failed_reason = ""
        audit_on = os.getenv("LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG", "").strip().lower() in ("1", "true", "yes")

        prompt = self._load_prompt()
        instructions = (prompt or "").strip() or "你必须只输出符合 voice_task_parse_v1_1 的 JSON。"
        user_content = f"【长输入】\n{raw}\n\n【上下文 hint】\n{session_hint or ''}\n"

        obj: Optional[Dict[str, Any]] = None
        route = ""
        deadline = time.monotonic() + max(0.2, self.timeout_ms / 1000.0)

        if self.prefer_responses_api:
            rem = self._remaining_sec(deadline)
            if rem <= 0:
                return None
            body = self._call_responses_api(
                instructions,
                user_content,
                timeout_sec=self._pick_timeout_sec(route="responses", remaining_sec=rem),
            )
            if body is not None:
                if audit_on:
                    self.audit_raw_model_payload_present = True
                    self.audit_model_chain_detection_reason = "provider_responses_body_present"
                if isinstance(body.get("usage"), dict):
                    self.last_usage = dict(body.get("usage") or {})
                out_txt = extract_output_text_from_responses_api_body(body)
                obj = self._resolve_structured_dict(out_txt, route="responses")
                if obj is not None:
                    route = "responses"
                    if audit_on:
                        self.audit_raw_json_present = True
                        self.audit_raw_json_top_level_keys = sorted([str(k) for k in obj.keys()])
                else:
                    logger.warning("qwen_external_responses_empty_or_bad_json rid=%s", request_id or "")
                    if audit_on:
                        self.audit_raw_json_present = False
                        self.audit_model_chain_detection_failed_reason = "responses_body_present_but_json_parse_failed_or_empty"
            else:
                if audit_on and self.audit_raw_model_payload_present is None:
                    self.audit_raw_model_payload_present = False
                    self.audit_model_chain_detection_failed_reason = "responses_http_or_json_body_missing"

        if obj is None:
            messages = [
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_content},
            ]
            rem = self._remaining_sec(deadline)
            if rem <= 0:
                return None
            chat_body = self._call_chat_completions(
                messages=messages,
                use_json_schema=True,
                timeout_sec=self._pick_timeout_sec(route="chat", remaining_sec=rem),
            )
            if chat_body is not None:
                if audit_on and (self.audit_raw_model_payload_present is None):
                    self.audit_raw_model_payload_present = True
                    self.audit_model_chain_detection_reason = "provider_chat_body_present"
                if isinstance(chat_body.get("usage"), dict):
                    self.last_usage = dict(chat_body.get("usage") or {})
                txt = self._chat_message_text(chat_body)
                obj = self._resolve_structured_dict(txt, route="chat_completions_json_schema")
                if obj is not None:
                    route = "chat_completions_json_schema"
                    if audit_on:
                        self.audit_raw_json_present = True
                        self.audit_raw_json_top_level_keys = sorted([str(k) for k in obj.keys()])
                else:
                    if audit_on:
                        self.audit_raw_json_present = False
                        if not self.audit_model_chain_detection_failed_reason:
                            self.audit_model_chain_detection_failed_reason = "chat_body_present_but_json_parse_failed_or_empty"
            else:
                if audit_on and self.audit_raw_model_payload_present is None:
                    self.audit_raw_model_payload_present = False
                    if not self.audit_model_chain_detection_failed_reason:
                        self.audit_model_chain_detection_failed_reason = "chat_http_or_json_body_missing"

        if obj is None:
            messages = [
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_content},
            ]
            rem = self._remaining_sec(deadline)
            if rem <= 0:
                return None
            chat_body2 = self._call_chat_completions(
                messages=messages,
                use_json_schema=False,
                timeout_sec=self._pick_timeout_sec(route="chat", remaining_sec=rem),
            )
            if chat_body2 is not None:
                if audit_on and (self.audit_raw_model_payload_present is None):
                    self.audit_raw_model_payload_present = True
                    self.audit_model_chain_detection_reason = "provider_chat_body_present_prompt_only"
                if isinstance(chat_body2.get("usage"), dict):
                    self.last_usage = dict(chat_body2.get("usage") or {})
                txt2 = self._chat_message_text(chat_body2)
                obj = self._resolve_structured_dict(txt2, route="chat_completions_prompt_only")
                if obj is not None:
                    route = "chat_completions_prompt_only"
                    if audit_on:
                        self.audit_raw_json_present = True
                        self.audit_raw_json_top_level_keys = sorted([str(k) for k in obj.keys()])
                else:
                    if audit_on:
                        self.audit_raw_json_present = False
                        if not self.audit_model_chain_detection_failed_reason:
                            self.audit_model_chain_detection_failed_reason = "chat_prompt_only_body_present_but_json_parse_failed_or_empty"
            else:
                if audit_on and self.audit_raw_model_payload_present is None:
                    self.audit_raw_model_payload_present = False
                    if not self.audit_model_chain_detection_failed_reason:
                        self.audit_model_chain_detection_failed_reason = "chat_prompt_only_http_or_json_body_missing"

        if obj is None:
            logger.warning("qwen_external_all_routes_failed rid=%s", request_id or "")
            if audit_on and not self.audit_model_chain_detection_failed_reason:
                self.audit_model_chain_detection_failed_reason = "all_routes_failed_no_structured_json"
            return None

        logger.debug("qwen_external_ok route=%s rid=%s", route, request_id or "")
        try:
            out = dict_to_structured_parse(obj)
            self.last_api_route = route
            return out
        except Exception as e:
            self.last_api_route = ""
            self.last_usage = {}
            logger.warning("qwen_external_structured_parse_build_failed:%s rid=%s", e, request_id or "")
            if audit_on and not self.audit_model_chain_detection_failed_reason:
                self.audit_model_chain_detection_failed_reason = f"dict_to_structured_parse_failed:{type(e).__name__}"
            return None


def is_qwen_external_llm_configured() -> bool:
    prov = (os.getenv("LUNA_EXTERNAL_LLM_PROVIDER") or "").strip().lower()
    key = (os.getenv("DASHSCOPE_API_KEY") or os.getenv("LUNA_DASHSCOPE_API_KEY") or "").strip()
    return prov == "qwen" and bool(key)


def create_qwen_external_long_input_provider_from_env(
    *,
    timeout_ms: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
) -> Optional[QwenExternalLongInputModelProvider]:
    if not is_qwen_external_llm_configured():
        return None
    kwargs: Dict[str, Any] = {}
    if timeout_ms is not None:
        kwargs["timeout_ms"] = timeout_ms
    if max_output_tokens is not None:
        kwargs["max_output_tokens"] = max_output_tokens
    return QwenExternalLongInputModelProvider(**kwargs)
