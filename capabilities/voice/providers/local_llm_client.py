# -*- coding: utf-8 -*-
"""
本地 LLM 推理客户端（OpenAI-compatible）。

用途：为长语音解析 provider（如 Qwen 3.5 4B）提供最小可复用的本地推理调用封装。
边界：只负责 HTTP 调用与返回抽取；不做系统裁决、不接执行层。
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)


class LocalLLMClientError(RuntimeError):
    pass


@dataclass
class LocalLLMChatMessage:
    role: str
    content: str

    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role, "content": self.content}


@dataclass
class LocalLLMChatCompletionRequest:
    base_url: str
    api_key: str
    model: str
    messages: List[LocalLLMChatMessage]
    temperature: float = 0.0
    max_tokens: int = 1200
    timeout_ms: int = 2000

    def endpoint(self) -> str:
        b = (self.base_url or "").rstrip("/")
        return f"{b}/v1/chat/completions"

    def headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if (self.api_key or "").strip():
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def payload(self) -> Dict[str, Any]:
        p: Dict[str, Any] = {
            "model": self.model,
            "messages": [m.to_dict() for m in self.messages],
            "temperature": float(self.temperature),
            "max_tokens": int(self.max_tokens),
        }
        return p


class LocalLLMClient:
    """
    OpenAI-compatible client（chat.completions 形态）。

    约定：上层 prompt 要求模型“只输出 JSON”，本层提供：
    - `chat_completion_text`：返回模型 message.content 文本
    - `chat_completion_json`：尝试 json.loads；失败抛错给上层处理（通常触发回退规则链）
    """

    def chat_completion_text(self, req: LocalLLMChatCompletionRequest) -> str:
        url = req.endpoint()
        try:
            resp = requests.post(
                url,
                headers=req.headers(),
                json=req.payload(),
                timeout=max(0.05, req.timeout_ms / 1000.0),
            )
        except requests.exceptions.Timeout as e:
            raise LocalLLMClientError("timeout") from e
        except requests.exceptions.RequestException as e:
            raise LocalLLMClientError(f"request_error:{e}") from e

        if resp.status_code >= 400:
            raise LocalLLMClientError(f"http_status:{resp.status_code}:{resp.text[:200]}")

        try:
            data = resp.json()
        except Exception as e:
            raise LocalLLMClientError("invalid_json_response") from e

        try:
            return (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            ) or ""
        except Exception as e:
            raise LocalLLMClientError("unexpected_response_shape") from e

    def chat_completion_json(self, req: LocalLLMChatCompletionRequest) -> Dict[str, Any]:
        text = self.chat_completion_text(req).strip()
        if not text:
            raise LocalLLMClientError("empty_model_output")

        # 兼容偶发 ```json 围栏；prompt 仍要求严格输出 JSON。
        if text.startswith("```"):
            text = text.strip("`").strip()
            if text.lower().startswith("json"):
                text = text[4:].strip()

        try:
            obj = json.loads(text)
        except Exception as e:
            raise LocalLLMClientError("model_output_not_json") from e

        if not isinstance(obj, dict):
            raise LocalLLMClientError("model_output_json_not_object")
        return obj

