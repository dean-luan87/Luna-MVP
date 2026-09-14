# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Error Codes v1 — pure helper, no runtime side effects."""

from __future__ import annotations

import re
from typing import Optional, Tuple

from capabilities.midplatform.protocols.protocol_types_v1 import ProtocolErrorClass

ERROR_CODE_PATTERN = re.compile(
    r"^(LUNA-PROTO-L[0-3]-[A-Z0-9-]+)::(CONST|PROC|IFACE|ASSIM|EVID|STATE|AUTH|TTL|TRACE|WB|HEALTH)-(\d{3})$"
)
ERROR_CLASSES: Tuple[str, ...] = (
    "CONST",
    "PROC",
    "IFACE",
    "ASSIM",
    "EVID",
    "STATE",
    "AUTH",
    "TTL",
    "TRACE",
    "WB",
    "HEALTH",
)


def build_error_code(protocol_id: str, error_class: str, number: int) -> str:
    cls = error_class.upper()
    if cls not in ERROR_CLASSES:
        raise ValueError(f"invalid error_class: {error_class}")
    return f"{protocol_id}::{cls}-{number:03d}"


def validate_error_code(error_code: str) -> bool:
    return bool(ERROR_CODE_PATTERN.match(error_code))


def classify_error_class(error_code: str) -> Optional[ProtocolErrorClass]:
    match = ERROR_CODE_PATTERN.match(error_code)
    if not match:
        return None
    return ProtocolErrorClass(match.group(2))


def parse_error_code(error_code: str) -> Optional[Tuple[str, str, int]]:
    match = ERROR_CODE_PATTERN.match(error_code)
    if not match:
        return None
    return match.group(1), match.group(2), int(match.group(3))
