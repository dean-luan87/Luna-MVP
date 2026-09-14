# -*- coding: utf-8 -*-
"""百炼 OpenAI 兼容 Responses 响应体抽取（无网络）。"""

from __future__ import annotations

from capabilities.voice.providers.qwen_external_long_input_model_provider import extract_output_text_from_responses_api_body


def test_extract_prefers_top_level_output_text() -> None:
    body = {"output_text": '{"a": 1}', "output": []}
    assert extract_output_text_from_responses_api_body(body) == '{"a": 1}'


def test_extract_from_message_content() -> None:
    body = {
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": '{"schema_version":"voice_task_parse_v1_1"}'}],
            }
        ]
    }
    assert extract_output_text_from_responses_api_body(body) == '{"schema_version":"voice_task_parse_v1_1"}'
