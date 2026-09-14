#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-007 — Verifier for OCR eligibility gate simulation v0.

Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty_jsonl(path: Path) -> bool:
    if not path.is_file():
        return False
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            return True
    return False


def _forbidden_in_tree(root: Path) -> List[str]:
    forbidden = ("MidPlatform", "SceneDelta", "WorldContextEvidence", "WorldContext")
    hits: List[str] = []
    for p in root.iterdir():
        if not p.is_file():
            continue
        if p.suffix not in (".json", ".jsonl", ".md"):
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for tok in forbidden:
            if tok in txt:
                hits.append(f"forbidden_token:{p.name}:{tok}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boundary-eval-root", required=True)
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    br = Path(args.boundary_eval_root).expanduser().resolve()
    dr = Path(args.dataset_root).expanduser().resolve()
    oroot = Path(args.output_root).expanduser().resolve()

    blockers: List[str] = []

    def need_file(rel: str) -> None:
        p = oroot / rel
        if not p.is_file():
            blockers.append(f"missing:{rel}")

    if not br.is_dir():
        blockers.append("boundary_eval_root_not_dir")
    else:
        for fn in (
            "ocr_capability_boundary_map.json",
            "ocr_capability_boundary_sample_matrix.json",
        ):
            if not (br / fn).is_file():
                blockers.append(f"boundary_missing:{fn}")

    if not dr.is_dir():
        blockers.append("dataset_root_not_dir")
    elif not (dr / "boundary_case_manifest.jsonl").is_file():
        blockers.append("dataset_manifest_missing")

    if not oroot.is_dir():
        blockers.append("output_root_not_dir")

    for rel in (
        "ocr_evidence_routing_pack.json",
        "ocr_false_text_risk_after_gate_report.json",
        "ocr_eligibility_accuracy_after_gate_report.json",
        "ocr_distortion_prevention_report.json",
        "ocr_route_confusion_matrix.json",
        "ocr_eligibility_gate_trace.jsonl",
        "ocr_eligibility_gate_replay.jsonl",
    ):
        need_file(rel)

    pack: Dict[str, Any] = {}
    if not blockers:
        pack = _read_json(oroot / "ocr_evidence_routing_pack.json")
        if not isinstance(pack, dict):
            blockers.append("routing_pack_not_object")
        else:
            for k in (
                "eligible_text_evidence",
                "conditional_text_evidence",
                "symbol_evidence",
                "glyph_evidence",
                "layout_evidence",
                "rejected_or_uncertain_evidence",
            ):
                if k not in pack or not isinstance(pack.get(k), list):
                    blockers.append(f"routing_pack_bad_list:{k}")

        ftr = _read_json(oroot / "ocr_false_text_risk_after_gate_report.json")
        if int(ftr.get("non_ocr_entered_eligible_text_count", -1)) != 0:
            blockers.append("non_ocr_entered_eligible_text_count_not_zero")

        dist = _read_json(oroot / "ocr_distortion_prevention_report.json")
        if dist.get("distortion_prevention_passed") is not True:
            blockers.append("distortion_prevention_not_passed")

        for k in ("runtime_integration", "whitebox_integration", "mainline_side_effect"):
            if pack.get(k) is not False:
                blockers.append(f"integration_flag:{k}")

        if not _nonempty_jsonl(oroot / "ocr_eligibility_gate_trace.jsonl"):
            blockers.append("trace_empty")
        if not _nonempty_jsonl(oroot / "ocr_eligibility_gate_replay.jsonl"):
            blockers.append("replay_empty")

        blockers.extend(_forbidden_in_tree(oroot))

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-EvaluationTools-OCR-007",
        "verdict": verdict,
        "blockers": blockers,
        "boundary_eval_root": str(br),
        "dataset_root": str(dr),
        "output_root": str(oroot),
    }
    (oroot / "ocr_eligibility_gate_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
