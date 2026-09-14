#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Design-001 — Verifier for design-only OCR evidence pack outputs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

_NON_OCR_TYPES = frozenset(
    {
        "symbols_and_punctuation",
        "artistic_text",
        "stylized_digits",
        "icon_text_mix",
        "multi_panel_layout",
        "decorative_graphic_non_text",
        "vertical_text",
        "handwritten_style",
    }
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty_jsonl(path: Path) -> bool:
    if not path.is_file():
        return False
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    root = Path(args.output_root).expanduser().resolve()
    blockers: List[str] = []

    required = [
        "ocr_evidence_pack_example.json",
        "ocr_midplatform_forwarding_decision_example.json",
        "ocr_evidence_pack_validation_report.json",
        "ocr_bridge_design_trace.jsonl",
        "ocr_bridge_design_replay.jsonl",
        "bridge_design_notes.md",
    ]
    for fn in required:
        if not (root / fn).is_file():
            blockers.append(f"missing:{fn}")

    if not blockers:
        pack = _read_json(root / "ocr_evidence_pack_example.json")
        if not isinstance(pack, dict):
            blockers.append("pack_not_object")
        else:
            from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import OCR_EVIDENCE_PACK_VERSION

            if pack.get("pack_version") != OCR_EVIDENCE_PACK_VERSION:
                blockers.append("bad_pack_version")

            for k in (
                "eligible_text_evidence",
                "conditional_text_evidence",
                "symbol_evidence",
                "glyph_evidence",
                "layout_evidence",
                "rejected_or_uncertain_evidence",
            ):
                if k not in pack or not isinstance(pack.get(k), list):
                    blockers.append(f"bad_list:{k}")

            for rk in (
                "source_image_ref",
                "source_provider_ref",
                "source_quality_gate_ref",
                "source_layout_ref",
                "source_eligibility_gate_ref",
            ):
                if not str(pack.get(rk) or "").strip():
                    blockers.append(f"missing_top_ref:{rk}")

            for it in pack.get("eligible_text_evidence") or []:
                refs = it.get("source_refs") or {}
                ct = str(refs.get("eval_content_type") or "")
                if bool(it.get("should_enter_fact_text_layer")) and ct in _NON_OCR_TYPES:
                    blockers.append(f"H_non_ocr_fact:{it.get('evidence_id')}")

            for it in pack.get("conditional_text_evidence") or []:
                if bool(it.get("should_enter_fact_text_layer")):
                    blockers.append(f"I_conditional_fact:{it.get('evidence_id')}")

            for bucket in ("symbol_evidence", "glyph_evidence"):
                for it in pack.get(bucket) or []:
                    if bool(it.get("should_enter_fact_text_layer")):
                        blockers.append(f"J_symbol_glyph_fact:{bucket}:{it.get('evidence_id')}")
                    if bool(it.get("should_enter_raw_text")):
                        blockers.append(f"J_symbol_glyph_raw:{bucket}:{it.get('evidence_id')}")

            ha = pack.get("hard_audit") or {}
            for k, expected in (
                ("midplatform_invoked", False),
                ("scene_delta_invoked", False),
                ("world_context_invoked", False),
                ("runtime_integration", False),
                ("mainline_routing_changed", False),
            ):
                if ha.get(k) is not expected:
                    blockers.append(f"hard_audit:{k}")

            if ha.get("navigation_action") is not None:
                blockers.append("hard_audit:navigation_action")

    if not blockers:
        if not _nonempty_jsonl(root / "ocr_bridge_design_trace.jsonl"):
            blockers.append("trace_empty")
        if not _nonempty_jsonl(root / "ocr_bridge_design_replay.jsonl"):
            blockers.append("replay_empty")

    verdict = "GO" if not blockers else "NO_GO"
    report = {"phase": "Phase-OCRBridge-Design-001", "verdict": verdict, "blockers": blockers, "output_root": str(root)}
    (root / "ocr_bridge_contract_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
