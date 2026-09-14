from __future__ import annotations

import hashlib
from typing import Iterable

from .a_route_product_loop_integration_core_types_v1 import ProductLoopInputV1
from .a_route_real_user_input_adapter_types_v1 import (
    ADAPTER_OWNER,
    MAX_INPUT_LENGTH,
    SUPPORTED_REAL_INGRESS_KINDS,
    RealUserInputAdapterResultV1,
    RealUserInputRecordV1,
)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def normalize_user_text(value: str) -> str:
    """Perform structural normalization only; never infer meaning."""

    if not isinstance(value, str):
        raise ValueError("INPUT_NOT_TEXT")
    return " ".join(value.split())


def _rejected_record(
    value: object,
    ingress_kind: str,
    session_ref: str,
    cycle_ref: str,
    sensitivity: str,
    correction_ref: str,
    rejection_code: str,
    duplicate: bool = False,
) -> RealUserInputRecordV1:
    text = value if isinstance(value, str) else ""
    token = _digest(f"rejected|{ingress_kind}|{session_ref}|{cycle_ref}|{text}")
    return RealUserInputRecordV1(
        input_id=f"s1-input:{token}",
        ingress_kind=ingress_kind,
        raw_input_ref=f"raw-user-input:{token}",
        normalized_content="",
        session_ref=session_ref,
        cycle_ref=cycle_ref,
        sensitivity=sensitivity,
        correction_ref=correction_ref,
        trace_ref=f"trace:s1-real-input:{token}",
        provenance_refs=(f"prov:s1-real-input:{token}",),
    )


def adapt_user_input(
    value: str,
    *,
    ingress_kind: str = "USER_INPUT",
    session_ref: str = "session:s1",
    cycle_ref: str = "",
    sensitivity: str = "NORMAL",
    correction_ref: str = "",
    seen_input_ids: Iterable[str] = (),
) -> RealUserInputAdapterResultV1:
    """Adapt a user-provided payload into the existing ProductLoopInputV1.

    The adapter has no hidden mutable registry. Duplicate detection is supplied
    by the caller through the immutable ``seen_input_ids`` boundary.
    """

    seen = frozenset(seen_input_ids)
    if ingress_kind not in SUPPORTED_REAL_INGRESS_KINDS:
        record = _rejected_record(value, ingress_kind, session_ref, cycle_ref, sensitivity, correction_ref, "UNSUPPORTED_INGRESS_TYPE")
        return RealUserInputAdapterResultV1(False, False, "UNSUPPORTED_INGRESS_TYPE", record, None)
    try:
        normalized = normalize_user_text(value)
    except ValueError:
        record = _rejected_record(value, ingress_kind, session_ref, cycle_ref, sensitivity, correction_ref, "INPUT_NOT_TEXT")
        return RealUserInputAdapterResultV1(False, False, "INPUT_NOT_TEXT", record, None)
    if not normalized:
        record = _rejected_record(value, ingress_kind, session_ref, cycle_ref, sensitivity, correction_ref, "EMPTY_INPUT")
        return RealUserInputAdapterResultV1(False, False, "EMPTY_INPUT", record, None)
    if len(normalized) > MAX_INPUT_LENGTH:
        record = _rejected_record(value, ingress_kind, session_ref, cycle_ref, sensitivity, correction_ref, "INPUT_TOO_LARGE")
        return RealUserInputAdapterResultV1(False, False, "INPUT_TOO_LARGE", record, None)
    if ingress_kind == "USER_CORRECTION" and not correction_ref:
        record = _rejected_record(value, ingress_kind, session_ref, cycle_ref, sensitivity, correction_ref, "CORRECTION_LINEAGE_REQUIRED")
        return RealUserInputAdapterResultV1(False, False, "CORRECTION_LINEAGE_REQUIRED", record, None)

    token = _digest(f"{ingress_kind}|{session_ref}|{cycle_ref}|{correction_ref}|{normalized}")
    record = RealUserInputRecordV1(
        input_id=f"s1-input:{token}",
        ingress_kind=ingress_kind,
        raw_input_ref=f"raw-user-input:{token}",
        normalized_content=normalized,
        session_ref=session_ref,
        cycle_ref=cycle_ref,
        sensitivity=sensitivity,
        correction_ref=correction_ref,
        trace_ref=f"trace:s1-real-input:{token}",
        provenance_refs=(f"prov:s1-real-input:{token}",),
    )
    if record.input_id in seen:
        return RealUserInputAdapterResultV1(False, True, "DUPLICATE_INPUT", record, None)

    product_input = ProductLoopInputV1(
        scenario_id=cycle_ref or f"S1-{token}",
        title="S1 real user input ingress",
        ingress_kind=ingress_kind,
        source_ref=record.input_id,
        requires_action=False,
        user_correction=ingress_kind == "USER_CORRECTION",
        correction_ref=record.correction_ref,
        synthetic_only=True,
        controlled_integration_only=True,
        candidate_only=True,
    )
    return RealUserInputAdapterResultV1(True, False, "", record, product_input)


__all__ = ["adapt_user_input", "normalize_user_text"]
