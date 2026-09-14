#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Implementation-001 — Verifier for shadow OcrEvidencePack serialization outputs.
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

from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import OCR_EVIDENCE_PACK_VERSION  # noqa: E402
from capabilities.ocr_bridge.ocr_evidence_pack_shadow_serializer_v0 import (  # noqa: E402
    FORBIDDEN_SOURCE_PREFIXES,
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _nonempty_jsonl(path: Path) -> bool:
    if not path.is_file():
        return False
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            return True
    return False


def _collect_strings(obj: Any, out: List[str]) -> None:
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_strings(v, out)


def _forged_refs_in_pack(pack: Dict[str, Any]) -> List[str]:
    bad: List[str] = []
    strings: List[str] = []
    _collect_strings(pack, strings)
    for s in strings:
        low = s.lower()
        if any(low.startswith(p) for p in FORBIDDEN_SOURCE_PREFIXES):
            bad.append(s)
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    root = Path(args.output_root).expanduser().resolve()
    blockers: List[str] = []

    required = [
        "ocr_evidence_pack_shadow_summary.json",
        "ocr_evidence_pack_shadow.json",
        "ocr_evidence_pack_shadow_validation_report.json",
        "ocr_evidence_pack_shadow_source_ref_report.json",
        "ocr_evidence_pack_shadow_forwarding_block_report.json",
        "ocr_bridge_shadow_trace.jsonl",
        "ocr_bridge_shadow_replay.jsonl",
        "ocr_bridge_shadow_audit.jsonl",
        "ocr_bridge_shadow_notes.md",
    ]
    for fn in required:
        if not (root / fn).is_file():
            blockers.append(f"A_missing:{fn}")

    pack: Dict[str, Any] = {}
    if not blockers:
        data = _read_json(root / "ocr_evidence_pack_shadow.json")
        if not isinstance(data, dict) or "pack" not in data:
            blockers.append("B_bad_shadow_json_shape")
        else:
            pack = data["pack"]
            if not isinstance(pack, dict):
                blockers.append("B_pack_not_object")
            elif pack.get("pack_version") != OCR_EVIDENCE_PACK_VERSION:
                blockers.append("C_bad_pack_version")

        val = _read_json(root / "ocr_evidence_pack_shadow_validation_report.json")
        if not isinstance(val, dict):
            blockers.append("D_validation_report_bad")
        elif val.get("validation_passed") is not True:
            blockers.append("D_validation_not_passed")

        if not isinstance(_read_json(root / "ocr_evidence_pack_shadow_source_ref_report.json"), dict):
            blockers.append("E_source_ref_report_bad")

        fwd = _read_json(root / "ocr_evidence_pack_shadow_forwarding_block_report.json")
        if not isinstance(fwd, dict):
            blockers.append("F_forwarding_block_bad")
        else:
            if fwd.get("midplatform_forwarding_enabled") is not False:
                blockers.append("G_forwarding_not_false")
            if fwd.get("fact_text_layer_enabled") is not False:
                blockers.append("H_fact_layer_not_false")
            if fwd.get("runtime_side_effect") is not False:
                blockers.append("I_runtime_side_effect_not_false")

        sm = _read_json(root / "ocr_evidence_pack_shadow_summary.json")
        if isinstance(sm, dict):
            c = sm.get("constraints") or {}
            if c.get("ocr_provider_invoked") is not False:
                blockers.append("J_provider")
            if c.get("midplatform_invoked") is not False:
                blockers.append("K_midplatform")
            if c.get("scene_delta_invoked") is not False:
                blockers.append("L_scene_delta")
            if c.get("world_context_invoked") is not False:
                blockers.append("L_world_context")
            if c.get("world_write_invoked") is not False:
                blockers.append("M_world_write")
            if c.get("hive_upload_invoked") is not False:
                blockers.append("M_hive_upload")
            if c.get("qianwen_invoked") is not False:
                blockers.append("N_qwen")
            if c.get("tts_invoked") is not False:
                blockers.append("N_tts")
            if c.get("playback_invoked") is not False:
                blockers.append("N_playback")

        if isinstance(pack, dict) and pack:
            forged = _forged_refs_in_pack(pack)
            if forged:
                blockers.append(f"O_forged_runtime_like:{forged[:3]}")

            ref_rep = _read_json(root / "ocr_evidence_pack_shadow_source_ref_report.json")
            missing = ref_rep.get("missing_source_refs") if isinstance(ref_rep, dict) else []
            mode = str((pack.get("midplatform_contract") or {}).get("forwarding_mode") or "")
            if isinstance(missing, list) and missing and mode == "eligible_text_only":
                blockers.append("P_missing_refs_but_eligible_only")

        if not _nonempty_jsonl(root / "ocr_bridge_shadow_trace.jsonl"):
            blockers.append("Q_empty_trace")
        if not _nonempty_jsonl(root / "ocr_bridge_shadow_replay.jsonl"):
            blockers.append("Q_empty_replay")
        if not _nonempty_jsonl(root / "ocr_bridge_shadow_audit.jsonl"):
            blockers.append("Q_empty_audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-OCRBridge-Implementation-001",
        "verdict": verdict,
        "blockers": blockers,
        "output_root": str(root),
    }
    (root / "ocr_evidence_pack_shadow_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
