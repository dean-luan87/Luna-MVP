#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旁路诊断：对比 qwen-plus 与 qwen3.6-plus（或其它模型 ID）在长语音结构化输出上的**原始 JSON** 差异。

用法（需已配置百炼）：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...
  python3 tools/diagnose_qwen_contract_diff.py
  python3 tools/diagnose_qwen_contract_diff.py --models qwen-plus,qwen3.6-plus

不改主链；仅打印键、关键字段与 validator 结果。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROMPT_PLUS = ROOT / "capabilities" / "voice" / "config" / "prompts" / "voice_long_input_parse_v1_1_prompt_qwen_plus.md"
DEFAULT_TEXT = "导航回家。"


def _summarize_obj(obj: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not obj:
        return {"_error": "no_json_object"}
    keys = sorted(obj.keys())
    im = obj.get("input_mode_judgement")
    gj = obj.get("global_judgement")
    out: Dict[str, Any] = {
        "top_level_keys": keys,
        "has_input_mode_judgement": isinstance(im, dict),
        "has_global_judgement": isinstance(gj, dict),
    }
    if isinstance(im, dict):
        out["input_mode.mode"] = im.get("mode")
        out["input_mode.keys"] = sorted(im.keys())
    else:
        out["input_mode_judgement_type"] = type(im).__name__
    if isinstance(gj, dict):
        out["global.primary_domain"] = gj.get("primary_domain")
        out["global.keys"] = sorted(gj.keys())
    else:
        out["global_judgement_type"] = type(gj).__name__
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--models",
        default="qwen-plus,qwen3.6-plus",
        help="逗号分隔的模型名",
    )
    ap.add_argument("--text", default=DEFAULT_TEXT, help="单条测试长输入")
    args = ap.parse_args()

    from capabilities.voice.bridge.voice_long_input_model_output_validator import validate_model_structured_output
    from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig
    from capabilities.voice.providers import qwen_external_long_input_model_provider as ext_mod
    from capabilities.voice.providers.qwen_external_long_input_model_provider import (
        create_qwen_external_long_input_provider_from_env,
        is_qwen_external_llm_configured,
    )
    from capabilities.voice.providers.qwen_long_input_model_provider import dict_to_structured_parse

    if not is_qwen_external_llm_configured():
        print("请设置 LUNA_EXTERNAL_LLM_PROVIDER=qwen 且 DASHSCOPE_API_KEY。", file=sys.stderr)
        sys.exit(2)

    base = create_qwen_external_long_input_provider_from_env(timeout_ms=120_000)
    if base is None:
        print("无法构造 Provider。", file=sys.stderr)
        sys.exit(2)

    cfg = VoiceLongInputParseConfig(
        parse_mode="model_preferred_with_rule_fallback",
        enable_model_adapter=True,
        model_timeout_ms=120_000,
        fallback_to_rule_on_timeout=True,
        fallback_to_rule_on_validation_error=True,
        max_task_candidates=3,
        allow_non_task_payload=True,
    )

    models: List[str] = [m.strip() for m in args.models.split(",") if m.strip()]
    text = args.text.strip()

    print("诊断文本:", repr(text[:200]))
    print("prompt:", PROMPT_PLUS)
    print()

    for model in models:
        captured: Dict[str, Any] = {}

        def _wrap_dict_to_structured(obj: Dict[str, Any]):
            captured["raw_json"] = obj
            return dict_to_structured_parse(obj)

        # 替换 external 模块内对 dict_to_structured_parse 的引用（该模块用 from-import）
        ext_mod.dict_to_structured_parse = _wrap_dict_to_structured

        from capabilities.voice.providers.qwen_external_long_input_model_provider import QwenExternalLongInputModelProvider

        p = QwenExternalLongInputModelProvider(
            api_key=base.api_key,
            model=model,
            responses_url=base.responses_url,
            chat_base_url=base.chat_base_url,
            prompt_path=PROMPT_PLUS,
            timeout_ms=base.timeout_ms,
            max_output_tokens=base.max_output_tokens,
            schema_strict=base.schema_strict,
            prefer_responses_api=base.prefer_responses_api,
            responses_http_timeout_sec=base.responses_http_timeout_sec,
            chat_http_timeout_sec=base.chat_http_timeout_sec,
        )

        structured = p.parse_long_input(text, request_id=f"diag_{model}")

        raw = captured.get("raw_json")
        summ = _summarize_obj(raw if isinstance(raw, dict) else None)

        vr = None
        if structured is not None:
            vr = validate_model_structured_output(structured, cfg=cfg)

        print(f"========== model={model} | api_route={getattr(p, 'last_api_route', '')} ==========")
        print("摘要:", json.dumps(summ, ensure_ascii=False, indent=2))
        if vr is not None:
            print("validate_model_structured_output:", "ok" if vr.ok else vr.errors)
        else:
            print("validate_model_structured_output: (structured is None)")
        if isinstance(raw, dict):
            # 只打印前 4000 字符，避免刷屏
            blob = json.dumps(raw, ensure_ascii=False, indent=2)
            if len(blob) > 4000:
                print("原始 JSON（截断）:\n", blob[:4000], "\n... [truncated]", sep="")
            else:
                print("原始 JSON:\n", blob, sep="")
        print()


if __name__ == "__main__":
    main()
