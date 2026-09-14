# -*- coding: utf-8
"""Teacher provider stubs — planning only, no network."""

from capabilities.midplatform.teacher_adapter.providers.gemini_adapter_v1 import (
    PROVIDER_ID as GEMINI_PROVIDER_ID,
    invoke_gemini_teacher_stub,
)
from capabilities.midplatform.teacher_adapter.providers.gpt_vision_adapter_v1 import (
    PROVIDER_ID as GPT_PROVIDER_ID,
    invoke_gpt_vision_teacher_stub,
)
from capabilities.midplatform.teacher_adapter.providers.internvl_adapter_v1 import (
    PROVIDER_ID as INTERNVL_PROVIDER_ID,
    invoke_internvl_teacher_stub,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl_adapter_v1 import (
    PROVIDER_ID as QWEN_PROVIDER_ID,
    invoke_qwen_vl_teacher_stub,
)

PROVIDER_REGISTRY = {
    GEMINI_PROVIDER_ID: invoke_gemini_teacher_stub,
    QWEN_PROVIDER_ID: invoke_qwen_vl_teacher_stub,
    GPT_PROVIDER_ID: invoke_gpt_vision_teacher_stub,
    INTERNVL_PROVIDER_ID: invoke_internvl_teacher_stub,
}

__all__ = ["PROVIDER_REGISTRY"]
