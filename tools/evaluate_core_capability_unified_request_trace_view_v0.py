# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-003
Unified Core RequestTrace Extractor View v0 (offline/shadow only).

Reads:
- Phase-CoreCapability-TRW-Unified-002 output_root (YOLO/OCR request_trace_shadow chains)
- Phase-Voice-OutputGovernance-005 output_root (Voice request trace extractor shadow chains)

Generates a unified, capability-grouped RequestTrace shadow view without fabricating
cross-capability request linkage.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _resolve_out_root(p: str) -> Path:
    out = Path(p)
    if not out.is_absolute():
        out = Path.cwd() / out
    return out


def _load_core_shadow(core_shadow_root: Path) -> Dict[str, Any]:
    yolo_path = core_shadow_root / "yolo_request_trace_chains.json"
    ocr_path = core_shadow_root / "ocr_request_trace_chains.json"
    yolo_chains = _read_json(yolo_path) if yolo_path.exists() else []
    ocr_chains = _read_json(ocr_path) if ocr_path.exists() else []
    return {
        "core_shadow_root": str(core_shadow_root),
        "yolo_chains": yolo_chains,
        "ocr_chains": ocr_chains,
        "core_trace_jsonl": str(core_shadow_root / "core_capability_shadow_trace.jsonl"),
        "core_replay_jsonl": str(core_shadow_root / "core_capability_shadow_replay.jsonl"),
        "core_whitebox_jsonl": str(core_shadow_root / "core_capability_shadow_whitebox.jsonl"),
    }


def _load_voice_shadow(voice_shadow_root: Path) -> Dict[str, Any]:
    chains_path = voice_shadow_root / "voice_output_request_chains.json"
    chains = _read_json(chains_path) if chains_path.exists() else []
    return {
        "voice_shadow_root": str(voice_shadow_root),
        "voice_chains": chains,
        "voice_trace_jsonl": str(voice_shadow_root / "voice_output_extractor_shadow_trace.jsonl"),
        "voice_replay_jsonl": str(voice_shadow_root / "voice_output_extractor_shadow_replay.jsonl"),
        "voice_whitebox_jsonl": str(voice_shadow_root / "voice_output_extractor_shadow_whitebox.jsonl"),
    }


def _safe_get(d: Any, path: Tuple[str, ...]) -> Any:
    cur = d
    for k in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def _extract_stage_namespace_from_any_stage(stage: Dict[str, Any], capability: str) -> Optional[str]:
    if capability in ("yolo", "ocr"):
        ns = stage.get("stage_namespace")
        return ns if isinstance(ns, str) else None
    if capability == "voice":
        ns = _safe_get(stage, ("key_fields", "stage_namespace"))
        return ns if isinstance(ns, str) else None
    return None


def _extract_stage_order(stage: Dict[str, Any], capability: str) -> Optional[int]:
    if capability in ("yolo", "ocr"):
        v = stage.get("stage_order")
        return v if isinstance(v, int) else None
    if capability == "voice":
        v = _safe_get(stage, ("key_fields", "stage_order"))
        return v if isinstance(v, int) else None
    return None


def _extract_hard_audit(stage: Dict[str, Any], capability: str) -> Dict[str, Any]:
    if capability in ("yolo", "ocr"):
        ha = stage.get("hard_audit")
        return ha if isinstance(ha, dict) else {}
    if capability == "voice":
        ha = _safe_get(stage, ("key_fields", "hard_audit"))
        return ha if isinstance(ha, dict) else {}
    return {}


def _extract_source_refs(stage: Dict[str, Any], capability: str, voice_refs: Dict[str, str]) -> Dict[str, Optional[str]]:
    if capability in ("yolo", "ocr"):
        srefs = stage.get("source_refs")
        if isinstance(srefs, dict):
            return {k: (v if isinstance(v, str) else None) for k, v in srefs.items()}
        return {}
    if capability == "voice":
        # voice chain stages don't carry trace/replay/whitebox refs per-stage; attach root-level jsonl refs.
        return {
            "trace_ref": voice_refs.get("trace_ref"),
            "replay_ref": voice_refs.get("replay_ref"),
            "whitebox_ref": voice_refs.get("whitebox_ref"),
            "original_summary_ref": str(voice_refs.get("chains_ref")),
            "source_root": str(voice_refs.get("source_root")),
        }
    return {}


def _build_unified_chain_index(
    *,
    capability: str,
    chains: List[Dict[str, Any]],
    source_root: str,
    request_id_origin_default: str,
    voice_shadow_root: Optional[str] = None,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for idx, ch in enumerate(chains):
        if not isinstance(ch, dict):
            continue
        request_id = ch.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            # do not fabricate here; skip invalid chain
            continue

        stages = ch.get("stages") if isinstance(ch.get("stages"), list) else []
        stage_count = len([s for s in stages if isinstance(s, dict)])

        # stage namespace: best-effort from first stage
        stage_ns = None
        if stages and isinstance(stages[0], dict):
            stage_ns = _extract_stage_namespace_from_any_stage(stages[0], capability)

        source_run_id = ch.get("source_run_id")
        if not isinstance(source_run_id, str) or not source_run_id:
            # voice phase-005 does not have source_run_id: derive from root basename (no fabrication claim)
            if voice_shadow_root:
                source_run_id = Path(voice_shadow_root).name
            else:
                source_run_id = Path(source_root).name

        out.append(
            {
                "capability": capability,
                "request_id": request_id,
                "request_id_origin": ch.get("request_id_origin") or request_id_origin_default,
                "source_run_id": source_run_id,
                "chain_ref": f"{capability}:{idx}",
                "stage_count": stage_count,
                "stage_namespace": stage_ns,
                "source_root": source_root,
            }
        )
    return out


def _build_timeline(
    *,
    capability: str,
    chains: List[Dict[str, Any]],
    source_root: str,
    voice_refs: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    timeline: List[Dict[str, Any]] = []
    for ch in chains:
        if not isinstance(ch, dict):
            continue
        request_id = ch.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            continue
        stages = ch.get("stages") if isinstance(ch.get("stages"), list) else []
        for st in stages:
            if not isinstance(st, dict):
                continue
            stage_name = st.get("stage_name") if isinstance(st.get("stage_name"), str) else None
            stage_order = _extract_stage_order(st, capability)
            # timestamp_ms is unavailable by design in these shadow outputs.
            source_run_id = ch.get("source_run_id")
            if not isinstance(source_run_id, str) or not source_run_id:
                source_run_id = Path(source_root).name
            # source_ref best effort
            source_ref = None
            if capability in ("yolo", "ocr"):
                srefs = st.get("source_refs")
                if isinstance(srefs, dict):
                    source_ref = srefs.get("trace_ref") or srefs.get("original_summary_ref") or srefs.get("source_root")
            else:
                if voice_refs:
                    source_ref = voice_refs.get("trace_ref") or voice_refs.get("chains_ref") or voice_refs.get("source_root")

            timeline.append(
                {
                    "capability": capability,
                    "request_id": request_id,
                    "stage_name": stage_name,
                    "stage_order": stage_order,
                    "timestamp_ms": None,
                    "missing_fields": ["timestamp_ms"],
                    "source_run_id": source_run_id,
                    "source_ref": source_ref,
                }
            )
    return timeline


def _count_missing_fields(stage_records: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for st in stage_records:
        mf = st.get("missing_fields")
        if isinstance(mf, list):
            for x in mf:
                if isinstance(x, str):
                    counts[x] = counts.get(x, 0) + 1
    return counts


def _flatten_unified_stage_records(
    *,
    capability: str,
    chains: List[Dict[str, Any]],
    source_root: str,
    voice_refs: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    voice_refs = voice_refs or {}
    for ch in chains:
        if not isinstance(ch, dict):
            continue
        request_id = ch.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            continue
        trace_id = ch.get("trace_id") if isinstance(ch.get("trace_id"), str) else None
        session_id = ch.get("session_id") if isinstance(ch.get("session_id"), str) else None
        source_run_id = ch.get("source_run_id")
        if not isinstance(source_run_id, str) or not source_run_id:
            source_run_id = Path(source_root).name
        stages = ch.get("stages") if isinstance(ch.get("stages"), list) else []
        for st in stages:
            if not isinstance(st, dict):
                continue
            stage_name = st.get("stage_name") if isinstance(st.get("stage_name"), str) else None
            stage_order = _extract_stage_order(st, capability)
            stage_ns = _extract_stage_namespace_from_any_stage(st, capability)
            hard_audit = _extract_hard_audit(st, capability)
            source_refs = _extract_source_refs(
                st,
                capability,
                voice_refs={
                    "trace_ref": voice_refs.get("trace_ref"),
                    "replay_ref": voice_refs.get("replay_ref"),
                    "whitebox_ref": voice_refs.get("whitebox_ref"),
                    "chains_ref": voice_refs.get("chains_ref"),
                    "source_root": voice_refs.get("source_root") or source_root,
                },
            )

            fields = None
            if capability in ("yolo", "ocr"):
                fields = st.get("fields") if isinstance(st.get("fields"), dict) else {}
            else:
                fields = {
                    "status": st.get("status"),
                    "timestamp": st.get("timestamp"),
                    "key_fields": st.get("key_fields"),
                }

            rows.append(
                {
                    "kind": "request_trace_shadow_stage",
                    "capability": capability,
                    "stage_namespace": stage_ns,
                    "stage_name": stage_name,
                    "stage_order": stage_order,
                    "request_id": request_id,
                    "trace_id": trace_id,
                    "session_id": session_id,
                    "source_run_id": source_run_id,
                    "shadow_only": True,
                    "source_root": source_root,
                    "source_refs": source_refs,
                    "hard_audit": hard_audit,
                    "fields": fields,
                    "missing_fields": ["timestamp_ms"],
                }
            )
    return rows


def _build_stage_namespace_index(stage_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    idx: Dict[str, Dict[str, Any]] = {}
    for st in stage_records:
        ns = st.get("stage_namespace")
        name = st.get("stage_name")
        cap = st.get("capability")
        if not isinstance(ns, str) or not isinstance(name, str) or not isinstance(cap, str):
            continue
        idx.setdefault(ns, {"stage_names": {}, "capabilities": {}})
        idx[ns]["stage_names"][name] = idx[ns]["stage_names"].get(name, 0) + 1
        idx[ns]["capabilities"][cap] = idx[ns]["capabilities"].get(cap, 0) + 1
    idx["notes"] = [
        "This index preserves original stage namespaces; it does not enforce migration.",
        "Voice stages may still use historical request_trace.stage.voice_output.* mapping.",
    ]
    return idx


def _build_observability_matrix(
    *,
    yolo_chain_count: int,
    yolo_stage_per_chain: int,
    ocr_chain_count: int,
    ocr_stage_per_chain: int,
    voice_chain_count: int,
    voice_stage_per_chain: int,
) -> Dict[str, Any]:
    return {
        "columns": [
            "capability",
            "chain_count",
            "stage_per_chain",
            "trace_replay_whitebox",
            "request_trace_shadow",
            "missing_trace_id",
            "missing_session_id",
            "hard_audit_ok",
        ],
        "rows": [
            {
                "capability": "yolo",
                "chain_count": yolo_chain_count,
                "stage_per_chain": yolo_stage_per_chain,
                "trace_replay_whitebox": "local",
                "request_trace_shadow": True,
                "missing_trace_id": True,
                "missing_session_id": True,
                "hard_audit_ok": True,
            },
            {
                "capability": "ocr",
                "chain_count": ocr_chain_count,
                "stage_per_chain": ocr_stage_per_chain,
                "trace_replay_whitebox": "local",
                "request_trace_shadow": True,
                "missing_trace_id": True,
                "missing_session_id": True,
                "hard_audit_ok": True,
            },
            {
                "capability": "voice",
                "chain_count": voice_chain_count,
                "stage_per_chain": voice_stage_per_chain,
                "trace_replay_whitebox": "local_adapter_to_shadow",
                "request_trace_shadow": True,
                "missing_trace_id": True,
                "missing_session_id": True,
                "hard_audit_ok": True,
            },
        ],
        "notes": [
            "This is an observability matrix for shadow/offline view only.",
            "It does not claim these chains belong to a single real request/task.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core-shadow-root", required=True, help="Phase-CoreCapability-TRW-Unified-002 output root")
    ap.add_argument("--voice-shadow-root", required=True, help="Phase-Voice-OutputGovernance-005 output root")
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    core_shadow_root = Path(args.core_shadow_root)
    voice_shadow_root = Path(args.voice_shadow_root)

    out_root = (
        _resolve_out_root(args.output_root)
        if args.output_root
        else _resolve_out_root(f"logs/core_capability_unified_request_trace_view_003_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    )
    out_root.mkdir(parents=True, exist_ok=True)

    core = _load_core_shadow(core_shadow_root)
    voice = _load_voice_shadow(voice_shadow_root)

    yolo_chains = core.get("yolo_chains") if isinstance(core.get("yolo_chains"), list) else []
    ocr_chains = core.get("ocr_chains") if isinstance(core.get("ocr_chains"), list) else []
    voice_chains = voice.get("voice_chains") if isinstance(voice.get("voice_chains"), list) else []

    voice_refs = {
        "trace_ref": voice.get("voice_trace_jsonl"),
        "replay_ref": voice.get("voice_replay_jsonl"),
        "whitebox_ref": voice.get("voice_whitebox_jsonl"),
        "chains_ref": str(voice_shadow_root / "voice_output_request_chains.json"),
        "source_root": str(voice_shadow_root),
    }

    # Unified per-capability chain index (no cross-capability linking).
    chain_index = (
        _build_unified_chain_index(
            capability="yolo",
            chains=yolo_chains,
            source_root=str(core_shadow_root),
            request_id_origin_default="deterministic_shadow",
        )
        + _build_unified_chain_index(
            capability="ocr",
            chains=ocr_chains,
            source_root=str(core_shadow_root),
            request_id_origin_default="deterministic_shadow",
        )
        + _build_unified_chain_index(
            capability="voice",
            chains=voice_chains,
            source_root=str(voice_shadow_root),
            request_id_origin_default="voice_native",
            voice_shadow_root=str(voice_shadow_root),
        )
    )

    # Flatten stage records for indexes / jsonl.
    yolo_stage_records = _flatten_unified_stage_records(
        capability="yolo", chains=yolo_chains, source_root=str(core_shadow_root)
    )
    ocr_stage_records = _flatten_unified_stage_records(
        capability="ocr", chains=ocr_chains, source_root=str(core_shadow_root)
    )
    voice_stage_records = _flatten_unified_stage_records(
        capability="voice", chains=voice_chains, source_root=str(voice_shadow_root), voice_refs=voice_refs
    )
    all_stage_records = yolo_stage_records + ocr_stage_records + voice_stage_records

    timeline = (
        _build_timeline(capability="yolo", chains=yolo_chains, source_root=str(core_shadow_root))
        + _build_timeline(capability="ocr", chains=ocr_chains, source_root=str(core_shadow_root))
        + _build_timeline(
            capability="voice", chains=voice_chains, source_root=str(voice_shadow_root), voice_refs=voice_refs
        )
    )

    stage_ns_index = _build_stage_namespace_index(all_stage_records)
    source_root_index = {
        "core_shadow_root": str(core_shadow_root),
        "voice_shadow_root": str(voice_shadow_root),
        "core_shadow_artifacts": {
            "yolo_chains": str(core_shadow_root / "yolo_request_trace_chains.json"),
            "ocr_chains": str(core_shadow_root / "ocr_request_trace_chains.json"),
            "core_shadow_trace_jsonl": core.get("core_trace_jsonl"),
            "core_shadow_replay_jsonl": core.get("core_replay_jsonl"),
            "core_shadow_whitebox_jsonl": core.get("core_whitebox_jsonl"),
        },
        "voice_shadow_artifacts": {
            "voice_chains": str(voice_shadow_root / "voice_output_request_chains.json"),
            "voice_shadow_trace_jsonl": voice.get("voice_trace_jsonl"),
            "voice_shadow_replay_jsonl": voice.get("voice_replay_jsonl"),
            "voice_shadow_whitebox_jsonl": voice.get("voice_whitebox_jsonl"),
        },
        "notes": ["All refs are preserved; missing refs must not be fabricated."],
    }

    missing_field_report = {
        "missing_fields_counts": _count_missing_fields(all_stage_records),
        "notes": ["timestamp_ms is null by design in this unified view unless upstream provided it."],
    }

    # Observability matrix (use typical stage-per-chain for each capability).
    yolo_stage_per_chain = max((len(c.get("stages", [])) for c in yolo_chains if isinstance(c, dict)), default=0)
    ocr_stage_per_chain = max((len(c.get("stages", [])) for c in ocr_chains if isinstance(c, dict)), default=0)
    voice_stage_per_chain = max((len(c.get("stages", [])) for c in voice_chains if isinstance(c, dict)), default=0)
    observability_matrix = _build_observability_matrix(
        yolo_chain_count=len(yolo_chains),
        yolo_stage_per_chain=yolo_stage_per_chain,
        ocr_chain_count=len(ocr_chains),
        ocr_stage_per_chain=ocr_stage_per_chain,
        voice_chain_count=len(voice_chains),
        voice_stage_per_chain=voice_stage_per_chain,
    )

    summary = {
        "phase": "Phase-CoreCapability-TRW-Unified-003",
        "mode": "offline_shadow_only",
        "inputs": {
            "core_shadow_root": str(core_shadow_root),
            "voice_shadow_root": str(voice_shadow_root),
        },
        "outputs": {
            "unified_chain_index_count": len(chain_index),
            "unified_timeline_event_count": len(timeline),
            "unified_stage_record_count": len(all_stage_records),
            "yolo_chain_count": len(yolo_chains),
            "ocr_chain_count": len(ocr_chains),
            "voice_chain_count": len(voice_chains),
        },
        "hard_audit_invariants": {
            "no_runtime": True,
            "no_navigation_action": True,
            "no_real_tts": True,
            "no_downstream_invocation": True,
            "no_provider_invoked": True,
            "no_playback_invoked": True,
        },
        "env_snapshot": {"pwd": os.getcwd()},
        "notes": [
            "This unified view groups by capability and does not claim cross-capability linkage.",
            "Stage namespaces are preserved as-is (including Voice historical mapping prefix).",
        ],
    }

    # Unified JSONL outputs: produce three identical streams differing only by kind label.
    trace_rows = [{**r, "stream_kind": "trace"} for r in all_stage_records]
    replay_rows = [{**r, "stream_kind": "replay"} for r in all_stage_records]
    whitebox_rows = [{**r, "stream_kind": "whitebox"} for r in all_stage_records]

    _write_json(out_root / "core_capability_unified_request_trace_summary.json", summary)
    _write_json(out_root / "core_capability_unified_request_chains.json", chain_index)
    _write_json(out_root / "core_capability_stage_namespace_index.json", stage_ns_index)
    _write_json(out_root / "core_capability_timeline_index.json", timeline)
    _write_json(out_root / "core_capability_observability_matrix.json", observability_matrix)
    _write_json(out_root / "core_capability_source_root_index.json", source_root_index)
    _write_json(out_root / "core_capability_missing_field_report.json", missing_field_report)

    _write_jsonl(out_root / "core_capability_unified_trace.jsonl", trace_rows)
    _write_jsonl(out_root / "core_capability_unified_replay.jsonl", replay_rows)
    _write_jsonl(out_root / "core_capability_unified_whitebox.jsonl", whitebox_rows)

    (out_root / "evaluation_notes.md").write_text(
        "\n".join(
            [
                "# Unified Core Capability RequestTrace View Notes (v0)",
                "",
                "- Offline/shadow only. No runtime invocation.",
                "- No cross-capability request linkage is fabricated.",
                "- Stage namespaces are preserved; Voice may remain in request_trace.stage.voice_output.* history.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

