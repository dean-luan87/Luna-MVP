# -*- coding: utf-8 -*-
"""Document Surface — controlled validation v1."""

from __future__ import annotations

from typing import Any, Dict, List

FORBIDDEN_OCR_KEYS = frozenset({"ocr_text", "text_content", "recognized_text", "ocr_result"})
FORBIDDEN_FACT_KEYS = frozenset({"owner_fact", "document_type_fact", "invoice_fact", "contract_fact", "receipt_fact"})


def _is_guard_key(key: str) -> bool:
    kl = str(key).lower()
    return (
        kl.startswith("no_")
        or "not_" in kl
        or kl in {"not_fact", "candidate_only", "ocr_called", "vlm_called", "layout_called"}
    )


def _is_fact_key(key: str) -> bool:
    if _is_guard_key(key):
        return False
    kl = str(key).lower()
    return kl in FORBIDDEN_FACT_KEYS


def _walk_forbidden_keys(obj: Any, found: List[str], forbidden: frozenset, *, key_predicate) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not _is_guard_key(k) and key_predicate(str(k)):
                found.append(str(k))
            _walk_forbidden_keys(v, found, forbidden, key_predicate=key_predicate)
    elif isinstance(obj, list):
        for item in obj:
            _walk_forbidden_keys(item, found, forbidden, key_predicate=key_predicate)


def validate_controlled_outputs(outputs: Dict[str, Any]) -> Dict[str, Any]:
    ocr_hits: List[str] = []
    fact_hits: List[str] = []
    _walk_forbidden_keys(outputs, ocr_hits, FORBIDDEN_OCR_KEYS, key_predicate=lambda k: k.lower() in FORBIDDEN_OCR_KEYS)
    _walk_forbidden_keys(
        outputs,
        fact_hits,
        FORBIDDEN_FACT_KEYS,
        key_predicate=_is_fact_key,
    )

    schema_ok = outputs.get("candidate_only") is True and outputs.get("not_fact") is True
    surfaces = outputs.get("document_surface_candidates") or []
    for s in surfaces:
        if s.get("candidate_only") is not True or s.get("not_fact") is not True:
            schema_ok = False

    abort_reason = None
    if ocr_hits:
        abort_reason = "output_contains_ocr_text"
    elif fact_hits:
        abort_reason = "output_contains_fact"
    elif not schema_ok:
        abort_reason = "candidate_output_schema_invalid"

    return {
        "validation_status_candidate": "passed" if not abort_reason else "aborted",
        "schema_compliant": schema_ok and not abort_reason,
        "no_ocr_leak": len(ocr_hits) == 0,
        "no_fact_output": len(fact_hits) == 0,
        "no_fallback": outputs.get("fallback_attempted") is not True,
        "abort_reason": abort_reason,
        "candidate_only": True,
        "not_fact": True,
    }
