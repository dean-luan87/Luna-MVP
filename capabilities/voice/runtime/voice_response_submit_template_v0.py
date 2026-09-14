# -*- coding: utf-8 -*-
"""
Response Submit Template Interface v0 (minimal).

Engineering boundary (MUST HOLD):

- Execution-kind submit:
  - used for mainline progression (task/action/normal flow)
  - governed by admission layer gates
  - must NOT be bypassed by response templates

- Response-kind submit:
  - used for explanation / clarification / confirmation / refusal templates
  - does NOT imply the original task/action was allowed
  - does NOT change gate results / dispatch / route / proposal

v0 scope: only registers the already-existing continue-request + information gate confirmation template.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional


ResponseTemplateIdV0 = Literal[
    "continue_request_info_confirm_v0",
    "navigation_missing_destination_confirm_v0",
]


@dataclass(frozen=True)
class ResponseSubmitTemplateSpecV0:
    template_id: ResponseTemplateIdV0
    response_type: Literal["confirmation_template"]
    guard_profile: Literal["continue_request_info_confirm", "navigation_missing_destination_confirm"]
    text: str
    source_module: str


def get_response_submit_template_spec_v0(
    template_id: ResponseTemplateIdV0,
    *,
    continue_request_info_confirm_text: str,
    navigation_missing_destination_confirm_text: str,
) -> Optional[ResponseSubmitTemplateSpecV0]:
    if template_id == "continue_request_info_confirm_v0":
        return ResponseSubmitTemplateSpecV0(
            template_id="continue_request_info_confirm_v0",
            response_type="confirmation_template",
            guard_profile="continue_request_info_confirm",
            text=str(continue_request_info_confirm_text or "").strip(),
            source_module="voice_response_submit_template_v0",
        )
    if template_id == "navigation_missing_destination_confirm_v0":
        return ResponseSubmitTemplateSpecV0(
            template_id="navigation_missing_destination_confirm_v0",
            response_type="confirmation_template",
            guard_profile="navigation_missing_destination_confirm",
            text=str(navigation_missing_destination_confirm_text or "").strip(),
            source_module="voice_response_submit_template_v0",
        )
    return None

