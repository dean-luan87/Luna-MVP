# -*- coding: utf-8 -*-
"""Qwen-VL Teacher provider package v1."""

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_adapter_v1 import (
    QwenVLTeacherAdapter,
    request_teacher_assistance,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    PROVIDER_ID,
    PROVIDER_LABEL,
    TEACHER_ROLE,
)

__all__ = [
    "PROVIDER_ID",
    "PROVIDER_LABEL",
    "TEACHER_ROLE",
    "QwenVLTeacherAdapter",
    "request_teacher_assistance",
]
