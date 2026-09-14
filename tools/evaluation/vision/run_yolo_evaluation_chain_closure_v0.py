#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-YOLO-Evaluation-Chain-Closure-001 — YOLO evaluation chain archive."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "vision_runtime").is_dir():
            candidates.append(parent)
    for parent in candidates:
        if (parent / "_eval_out").is_dir():
            return parent
        sibling = parent.parent / "Luna-Workspace-Min"
        if (sibling / "_eval_out").is_dir():
            return sibling
    return candidates[0] if candidates else here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--yolo-candidate-adapter-root", default="")
    ap.add_argument("--yolo-real-smoke-root", default="")
    ap.add_argument("--yolo-positive-sample-root", default="")
    ap.add_argument("--yolo-evidence-pack-integration-root", default="")
    ap.add_argument("--yolo-evidence-readonly-consumer-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    defaults = {
        "cand": WS_ROOT / "_eval_out/yolo_candidate_adapter_eval_smoke_v0",
        "real": WS_ROOT / "_eval_out/yolo_real_smoke_v0",
        "pos": WS_ROOT / "_eval_out/yolo_real_positive_sample_smoke_v0",
        "pack": WS_ROOT / "_eval_out/yolo_evidence_pack_integration_stub_smoke_v0",
        "consumer": WS_ROOT / "_eval_out/yolo_evidence_readonly_consumer_smoke_v0",
    }

    def _root(arg: str, key: str, cli: str) -> Path:
        if arg.strip():
            p = Path(arg).expanduser()
            if not p.is_absolute():
                p = (WS_ROOT / p).resolve()
            return _require_abs(str(p), f"--{cli}")
        return _require_abs(str(defaults[key]), f"default {key}")

    from capabilities.vision_runtime.yolo_evaluation_chain_closure_v0 import run_yolo_evaluation_chain_closure_v0

    summary, phase_mx, lineage, no_write, capability, non_claims, followups, audit, errs = (
        run_yolo_evaluation_chain_closure_v0(
            yolo_candidate_adapter_root=str(_root(args.yolo_candidate_adapter_root, "cand", "yolo-candidate-adapter-root")),
            yolo_real_smoke_root=str(_root(args.yolo_real_smoke_root, "real", "yolo-real-smoke-root")),
            yolo_positive_sample_root=str(_root(args.yolo_positive_sample_root, "pos", "yolo-positive-sample-root")),
            yolo_evidence_pack_integration_root=str(
                _root(args.yolo_evidence_pack_integration_root, "pack", "yolo-evidence-pack-integration-root")
            ),
            yolo_evidence_readonly_consumer_root=str(
                _root(args.yolo_evidence_readonly_consumer_root, "consumer", "yolo-evidence-readonly-consumer-root")
            ),
        )
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "yolo_evaluation_chain_closure_summary.json", summary)
    _write_json(out / "yolo_evaluation_phase_matrix.json", {"schema": "yolo_evaluation_phase_matrix_v0", "rows": phase_mx})
    _write_json(out / "yolo_evaluation_lineage_matrix.json", lineage)
    _write_json(out / "yolo_evaluation_no_write_boundary_matrix.json", no_write)
    _write_json(out / "yolo_evaluation_capability_closure_report.json", capability)
    _write_json(out / "yolo_evaluation_non_claims_report.json", non_claims)
    _write_json(out / "yolo_evaluation_open_followups.json", followups)
    _write_json(out / "yolo_evaluation_chain_closure_audit_report.json", audit)

    (out / "yolo_evaluation_chain_closure_notes.md").write_text(
        "# Phase-Vision-YOLO-Evaluation-Chain-Closure-001\n\n"
        "Archival closure for YOLO **evaluation-only** chain. No mainline; no fact writes.\n",
        encoding="utf-8",
    )

    if errs and summary.get("phase_verdict_hint") == "NO_GO":
        _write_json(out / "yolo_evaluation_chain_closure_blocking_errors.json", {"errors": errs})

    ok = summary.get("phase_verdict_hint") != "NO_GO"
    print(
        json.dumps(
            {
                "yolo_evaluation_chain_closure_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "lineage_detection_count": summary.get("lineage_detection_count"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
