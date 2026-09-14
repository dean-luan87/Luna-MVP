#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001 — generic prechain archive."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict

WS_ROOT = Path(__file__).resolve().parents[3]
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
    ap.add_argument(
        "--roots-json",
        default="",
        help="Optional JSON: { source_type: { dryrun_root, generic_trace_root, ... } }",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.scene_delta_generic_chain_closure_v0 import (
        DEFAULT_GENERIC_CHAIN_ROOTS,
        run_generic_chain_closure_v0,
    )

    roots_by_source: Dict[str, Dict[str, str]] = {
        k: dict(v) for k, v in DEFAULT_GENERIC_CHAIN_ROOTS.items()
    }
    if args.roots_json.strip():
        rp = Path(args.roots_json).expanduser()
        if not rp.is_absolute():
            rp = (WS_ROOT / rp).resolve()
        rp = _require_abs(str(rp), "--roots-json")
        custom = json.loads(rp.read_text(encoding="utf-8"))
        if isinstance(custom, dict):
            for st, cfg in custom.items():
                if isinstance(cfg, dict):
                    roots_by_source[str(st)] = {str(k): str(v) for k, v in cfg.items()}

    summary, phase_matrix, lineage, nw, cap, non_claims, followups, errs = run_generic_chain_closure_v0(
        roots_by_source
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "scene_delta_generic_chain_closure_summary.json", summary)
    _write_json(out / "scene_delta_generic_chain_phase_matrix.json", phase_matrix)
    _write_json(out / "scene_delta_generic_chain_lineage_matrix.json", lineage)
    _write_json(out / "scene_delta_generic_no_write_boundary_matrix.json", nw)
    _write_json(out / "scene_delta_generic_capability_closure_report.json", cap)
    _write_json(out / "scene_delta_generic_non_claims_report.json", non_claims)
    _write_json(out / "scene_delta_generic_open_followups.json", followups)

    (out / "scene_delta_generic_chain_closure_notes.md").write_text(
        "# Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001\n\n"
        "Read-only **closure** for OCR + Vision **Scene Delta generic executor prechain** "
        "(dry-run → generic trace stub → generic mock handshake → generic contract conformance). "
        "**No** executor, **no** writes, **no** DB/WAL/fact/WorldModel/AI/provider.\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "scene_delta_generic_chain_closure_errors.json", {"errors": errs})

    ok = not errs
    print(
        json.dumps(
            {
                "scene_delta_generic_chain_closure_smoke_root": str(out),
                "source_types": summary.get("source_types"),
                "status": "success" if ok else "failed",
                "error_count": len(errs),
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
