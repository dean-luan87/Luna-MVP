# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-002
OCR RequestTrace Shadow Adapter v0 (offline/shadow only).

Reads OCR local TRW / benchmark / offline source policy outputs and converts
them into RequestTrace shadow stage records grouped into chains.

Hard boundaries:
- Read-only adapter (does not modify source root).
- Does not invoke runtime, navigation, TTS, playback.
- semantic_interpretation_enabled is always False in hard_audit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


STAGE_NAMESPACE = "core_capability_request_trace_v0"

OCR_STAGES: List[Tuple[str, int]] = [
    ("request_trace.stage.perception.ocr.source_policy_selection", 0),
    ("request_trace.stage.perception.ocr.input_region", 1),
    ("request_trace.stage.perception.ocr.provider_invocation", 2),
    ("request_trace.stage.perception.ocr.raw_text_result", 3),
    ("request_trace.stage.perception.ocr.length_segmentation", 4),
    ("request_trace.stage.perception.ocr.reading_order", 5),
    ("request_trace.stage.perception.ocr.observability_envelope", 6),
]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _maybe_read_json(path: Optional[Path]) -> Any:
    if not path or not path.exists():
        return None
    try:
        return _read_json(path)
    except Exception:
        return None


def _source_run_id_from_root(root: Path) -> str:
    return root.name


def _deterministic_request_id(source_run_id: str, sample_id: str) -> str:
    return f"shadow_req_{source_run_id}_{sample_id}"


@dataclass(frozen=True)
class OcrShadowStageV0:
    stage_namespace: str
    stage_name: str
    stage_order: int
    request_id: str
    trace_id: Optional[str]
    session_id: Optional[str]
    source_run_id: str
    provider_selected: Optional[str]
    source_policy_id: Optional[str]
    missing_fields: List[str] = field(default_factory=list)
    source_refs: Dict[str, Optional[str]] = field(default_factory=dict)
    hard_audit: Dict[str, Any] = field(default_factory=dict)
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OcrShadowChainV0:
    request_id: str
    trace_id: Optional[str]
    session_id: Optional[str]
    source_run_id: str
    request_id_origin: str  # inherited|deterministic_shadow
    provider_selected: Optional[str]
    source_policy_id: Optional[str]
    stages: List[Dict[str, Any]]
    notes: List[str] = field(default_factory=list)


def load_ocr_local_outputs_v0(ocr_root: str) -> Dict[str, Any]:
    """
    Loads minimal OCR local outputs from an offline source policy root.
    Expected structure:
    - ocr_benchmark_summary.json
    - trace/<provider>_trace.jsonl
    - replay/<provider>_replay.jsonl
    - whitebox/<provider>_whitebox.jsonl
    - raw_outputs/<provider>/ocr_sample_XXX.json
    """
    root = Path(ocr_root)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"ocr_root not found: {ocr_root}")

    source_run_id = _source_run_id_from_root(root)

    summary_path = root / "ocr_benchmark_summary.json"
    summary = _maybe_read_json(summary_path) or {}

    provider_selected = summary.get("provider_selected")
    source_policy_id = (
        (summary.get("ocr_offline_source_selection") or {}).get("source_policy_id")
        or summary.get("source_policy_id")
        or (summary.get("selection_audit") or {}).get("source_policy_id")
    )

    trace_ref = summary.get("trace_ref") or summary.get("artifacts", {}).get("trace")
    replay_ref = summary.get("replay_ref") or summary.get("artifacts", {}).get("replay")
    whitebox_ref = summary.get("whitebox_ref") or summary.get("artifacts", {}).get("whitebox")

    # Prefer explicit refs in summary; otherwise discover per-provider jsonl files.
    trace_files = list(root.glob("trace/*_trace.jsonl"))
    replay_files = list(root.glob("replay/*_replay.jsonl"))
    whitebox_files = list(root.glob("whitebox/*_whitebox.jsonl"))

    # Raw sample outputs
    raw_samples = list(root.glob("raw_outputs/*/ocr_sample_*.json"))

    return {
        "ocr_root": str(root),
        "source_run_id": source_run_id,
        "summary_path": str(summary_path) if summary_path.exists() else None,
        "summary": summary,
        "provider_selected": provider_selected,
        "source_policy_id": source_policy_id,
        "trace_files": [str(p) for p in sorted(trace_files)],
        "replay_files": [str(p) for p in sorted(replay_files)],
        "whitebox_files": [str(p) for p in sorted(whitebox_files)],
        "raw_samples": [str(p) for p in sorted(raw_samples)],
        "declared_refs": {
            "trace_ref": trace_ref if isinstance(trace_ref, str) else None,
            "replay_ref": replay_ref if isinstance(replay_ref, str) else None,
            "whitebox_ref": whitebox_ref if isinstance(whitebox_ref, str) else None,
        },
    }


def _sample_id_from_path(p: Path) -> str:
    # ocr_sample_030.json -> 030
    stem = p.stem
    for prefix in ("ocr_sample_", "sample_", "frame_"):
        if stem.startswith(prefix):
            return stem[len(prefix) :]
    return stem


def build_ocr_request_trace_stage_v0(
    *,
    stage_name: str,
    stage_order: int,
    request_id: str,
    source_run_id: str,
    provider_selected: Optional[str],
    source_policy_id: Optional[str],
    source_refs: Dict[str, Optional[str]],
    sample_fields: Dict[str, Any],
) -> OcrShadowStageV0:
    missing = ["trace_id", "session_id"]
    hard = {
        "semantic_interpretation_enabled": False,
        "allows_execute_now": False,
        "downstream_invocation_count": 0,
        "real_tts_invoked": False,
        "navigation_action": None,
    }
    return OcrShadowStageV0(
        stage_namespace=STAGE_NAMESPACE,
        stage_name=stage_name,
        stage_order=stage_order,
        request_id=request_id,
        trace_id=None,
        session_id=None,
        source_run_id=source_run_id,
        provider_selected=provider_selected,
        source_policy_id=source_policy_id,
        missing_fields=missing,
        source_refs=dict(source_refs),
        hard_audit=hard,
        fields=dict(sample_fields),
    )


def build_ocr_request_trace_chain_v0(
    *,
    source_run_id: str,
    request_id: str,
    request_id_origin: str,
    provider_selected: Optional[str],
    source_policy_id: Optional[str],
    source_refs: Dict[str, Optional[str]],
    sample_fields: Dict[str, Any],
) -> OcrShadowChainV0:
    stages: List[Dict[str, Any]] = []
    for stage_name, stage_order in OCR_STAGES:
        st = build_ocr_request_trace_stage_v0(
            stage_name=stage_name,
            stage_order=stage_order,
            request_id=request_id,
            source_run_id=source_run_id,
            provider_selected=provider_selected,
            source_policy_id=source_policy_id,
            source_refs=source_refs,
            sample_fields=sample_fields,
        )
        stages.append(asdict(st))
    return OcrShadowChainV0(
        request_id=request_id,
        trace_id=None,
        session_id=None,
        source_run_id=source_run_id,
        request_id_origin=request_id_origin,
        provider_selected=provider_selected,
        source_policy_id=source_policy_id,
        stages=stages,
        notes=["shadow_only:true", "semantic_interpretation_enabled:false", "allows_execute_now:false"],
    )


def run_ocr_request_trace_shadow_adapter_v0(ocr_root: str) -> Dict[str, Any]:
    loaded = load_ocr_local_outputs_v0(ocr_root)
    source_run_id = str(loaded.get("source_run_id") or "")
    provider_selected = loaded.get("provider_selected")
    source_policy_id = loaded.get("source_policy_id")

    # choose the first discovered files as refs (preserve originals; do not fabricate)
    trace_ref = None
    replay_ref = None
    whitebox_ref = None
    if isinstance(loaded.get("trace_files"), list) and loaded["trace_files"]:
        trace_ref = loaded["trace_files"][0]
    if isinstance(loaded.get("replay_files"), list) and loaded["replay_files"]:
        replay_ref = loaded["replay_files"][0]
    if isinstance(loaded.get("whitebox_files"), list) and loaded["whitebox_files"]:
        whitebox_ref = loaded["whitebox_files"][0]

    src_refs_base = {
        "trace_ref": trace_ref,
        "replay_ref": replay_ref,
        "whitebox_ref": whitebox_ref,
        "original_summary_ref": loaded.get("summary_path"),
        "source_root": loaded.get("ocr_root"),
    }

    miss = [k for k, v in src_refs_base.items() if not v]
    missing_source_refs = [{"missing_source_refs": miss}] if miss else []

    raw_samples = loaded.get("raw_samples") if isinstance(loaded.get("raw_samples"), list) else []
    chains: List[Dict[str, Any]] = []
    for raw_path in raw_samples:
        p = Path(raw_path)
        sample_id = _sample_id_from_path(p)
        request_id = _deterministic_request_id(source_run_id, sample_id)
        sample_obj = _maybe_read_json(p) if p.exists() else None

        sample_fields = {
            "sample_id": sample_id,
            "raw_output_ref": str(p),
            "raw_text_candidate_count": (
                len(sample_obj.get("raw_text_candidates", []))
                if isinstance(sample_obj, dict) and isinstance(sample_obj.get("raw_text_candidates"), list)
                else None
            ),
            "bbox_count": (
                len(sample_obj.get("bboxes", []))
                if isinstance(sample_obj, dict) and isinstance(sample_obj.get("bboxes"), list)
                else None
            ),
        }

        # Include per-sample source refs without fabricating missing refs.
        src_refs = dict(src_refs_base)
        src_refs["original_sample_ref"] = str(p)

        ch = build_ocr_request_trace_chain_v0(
            source_run_id=source_run_id,
            request_id=request_id,
            request_id_origin="deterministic_shadow",
            provider_selected=provider_selected if isinstance(provider_selected, str) else None,
            source_policy_id=source_policy_id if isinstance(source_policy_id, str) else None,
            source_refs=src_refs,
            sample_fields=sample_fields,
        )
        chains.append(asdict(ch))

    return {
        "capability": "ocr",
        "ocr_root": str(loaded.get("ocr_root") or ""),
        "source_run_id": source_run_id,
        "provider_selected": provider_selected,
        "source_policy_id": source_policy_id,
        "chain_count": len(chains),
        "missing_source_refs": missing_source_refs,
        "chains": chains,
    }

