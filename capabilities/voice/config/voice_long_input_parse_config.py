# -*- coding: utf-8 -*-
"""长语音解析路由配置（v1）。默认规则链；YAML 可选加载。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

_CONFIG_DIR = Path(__file__).resolve().parent
_DEFAULT_YAML = _CONFIG_DIR / "voice_long_input_parse_config.yaml"


@dataclass
class VoiceLongInputParseConfig:
    """与 voice_long_input_parse_config.yaml 对齐。"""

    parse_mode: str = "rule_only"  # rule_only | model_preferred_with_rule_fallback
    enable_model_adapter: bool = False
    model_timeout_ms: int = 2000
    fallback_to_rule_on_timeout: bool = True
    fallback_to_rule_on_validation_error: bool = True
    max_task_candidates: int = 3
    allow_non_task_payload: bool = True

    def model_preferred(self) -> bool:
        return self.parse_mode == "model_preferred_with_rule_fallback" and self.enable_model_adapter


def _load_yaml_dict(path: Path) -> Optional[Dict[str, Any]]:
    if not path.is_file():
        return None
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_voice_long_input_parse_config(path: Optional[Path] = None) -> VoiceLongInputParseConfig:
    p = path or _DEFAULT_YAML
    data = _load_yaml_dict(p)
    if not data:
        return VoiceLongInputParseConfig()
    return VoiceLongInputParseConfig(
        parse_mode=str(data.get("parse_mode", "rule_only")),
        enable_model_adapter=bool(data.get("enable_model_adapter", False)),
        model_timeout_ms=int(data.get("model_timeout_ms", 2000)),
        fallback_to_rule_on_timeout=bool(data.get("fallback_to_rule_on_timeout", True)),
        fallback_to_rule_on_validation_error=bool(data.get("fallback_to_rule_on_validation_error", True)),
        max_task_candidates=int(data.get("max_task_candidates", 3)),
        allow_non_task_payload=bool(data.get("allow_non_task_payload", True)),
    )


_DEFAULT_SINGLETON: Optional[VoiceLongInputParseConfig] = None


def get_default_voice_long_input_parse_config() -> VoiceLongInputParseConfig:
    global _DEFAULT_SINGLETON
    if _DEFAULT_SINGLETON is None:
        _DEFAULT_SINGLETON = load_voice_long_input_parse_config()
    return _DEFAULT_SINGLETON
