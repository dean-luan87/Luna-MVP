#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Lightweight-Real-Provider-Adapter-001 — lightweight real OCR adapter smoke (RapidOCR optional)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

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


def _gen_png(path: Path, w: int, h: int) -> None:
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (int(w), int(h)), (40, 80, 120)).save(path, format="PNG")


class _EnvFrame:
    def __init__(self, updates: Dict[str, str]) -> None:
        self.updates = updates
        self._prev: Dict[str, Any] = {}

    def __enter__(self) -> "_EnvFrame":
        for k, v in self.updates.items():
            self._prev[k] = os.environ.get(k, _MISSING)
            os.environ[k] = v
        return self

    def __exit__(self, *args: object) -> None:
        for k, old in self._prev.items():
            if old is _MISSING:
                os.environ.pop(k, None)
            else:
                os.environ[k] = old


_MISSING = object()


def _run_case(
    *,
    ws: Path,
    gov: Path,
    out: Path,
    case_id: str,
    env_updates: Dict[str, str],
    img_w: int,
    img_h: int,
) -> Dict[str, Any]:
    with _EnvFrame(env_updates):
        from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
        from capabilities.ocr_runtime.ocr_provider_registry_v0 import build_default_ocr_provider_registry_v0
        from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

        img = out / f"_lw_smoke_{case_id}.png"
        _gen_png(img, img_w, img_h)
        req = OCRRequestV0(
            image_path=str(img),
            input_type="image_path",
            latency_budget_ms=8000,
            allow_full_image=True if img_w > 2048 or img_h > 2048 else False,
        )
        return run_ocr_mainline_bridge_v0(
            req,
            governance_config_path=gov,
            workspace_root=ws,
            normalization_pipeline_enabled=True,
            normalization_work_dir=out / f"_work_{case_id}",
        )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    gov = Path(args.governance_config).expanduser() if args.governance_config.strip() else (ws / "configs/ocr/ocr_image_input_governance_v0.example.json")
    if not gov.is_absolute():
        gov = (ws / gov).resolve()
    gov = _require_abs(str(gov), "--governance-config")

    base = {
        "LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0": "true",
        "LUNA_ENABLE_OCR_STUB_PROVIDER_V0": "true",
        "LUNA_ENABLE_OCR_REAL_PROVIDER_V0": "false",
        "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0": "false",
        "LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0": "false",
        "LUNA_ENABLE_OCR_TILE_PLANNER_V0": "false",
    }

    cases: List[Dict[str, Any]] = []

    ra = _run_case(ws=ws, gov=gov, out=out, case_id="A", env_updates=base, img_w=512, img_h=512)
    _write_json(out / "ocr_lightweight_provider_case_a_result.json", ra)
    cases.append({"case": "A_default_stub", "status": ra.get("status"), "selected": (ra.get("audit") or {}).get("selected_provider")})

    rb = _run_case(
        ws=ws,
        gov=gov,
        out=out,
        case_id="B",
        env_updates={
            **base,
            "LUNA_ENABLE_OCR_REAL_PROVIDER_V0": "true",
            "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0": "true",
        },
        img_w=512,
        img_h=512,
    )
    _write_json(out / "ocr_lightweight_provider_case_b_result.json", rb)

    with _EnvFrame({**base, "LUNA_ENABLE_OCR_REAL_PROVIDER_V0": "true", "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0": "true"}):
        from capabilities.ocr_runtime.ocr_provider_registry_v0 import build_default_ocr_provider_registry_v0

        reg_snap = build_default_ocr_provider_registry_v0().snapshot()
    _write_json(out / "ocr_lightweight_provider_registry_snapshot.json", reg_snap)

    rep_b = rb.get("provider_selection_report") if isinstance(rb.get("provider_selection_report"), dict) else {}
    _write_json(out / "ocr_lightweight_provider_selection_report.json", rep_b)
    _write_json(out / "ocr_lightweight_provider_result.json", rb)
    bp = rb.get("bridge_pack") if isinstance(rb.get("bridge_pack"), dict) else {}
    _write_json(out / "ocr_lightweight_provider_bridge_pack.json", bp)
    aud_b = rb.get("audit") if isinstance(rb.get("audit"), dict) else {}
    _write_json(out / "ocr_lightweight_provider_audit_report.json", aud_b)

    rc = _run_case(
        ws=ws,
        gov=gov,
        out=out,
        case_id="C",
        env_updates={
            **base,
            "LUNA_ENABLE_OCR_REAL_PROVIDER_V0": "true",
            "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0": "true",
            "LUNA_OCR_RAPIDOCR_FORCE_UNAVAILABLE_V0": "true",
        },
        img_w=512,
        img_h=512,
    )
    _write_json(out / "ocr_lightweight_provider_case_c_result.json", rc)
    cases.append({"case": "C_forced_unavailable", "status": rc.get("status"), "real_invoked": (rc.get("audit") or {}).get("real_provider_invoked")})

    rd = _run_case(
        ws=ws,
        gov=gov,
        out=out,
        case_id="D",
        env_updates={
            **base,
            "LUNA_ENABLE_OCR_REAL_PROVIDER_V0": "true",
            "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0": "true",
        },
        img_w=3000,
        img_h=5334,
    )
    _write_json(out / "ocr_lightweight_provider_case_d_result.json", rd)
    cases.append({"case": "D_oversized_edge_policy", "status": rd.get("status"), "real_invoked": (rd.get("audit") or {}).get("real_provider_invoked")})

    cases.insert(1, {"case": "B_real_flags_small", "status": rb.get("status"), "real_invoked": aud_b.get("real_provider_invoked"), "selected": aud_b.get("selected_provider")})

    summary = {
        "schema": "ocr_lightweight_provider_adapter_smoke_summary_v0",
        "phase": "Phase-OCR-Lightweight-Real-Provider-Adapter-001",
        "output_root": str(out),
        "cases": cases,
        "case_b_text_joined_preview": str((rb.get("ocr_evidence") or {}).get("text_joined") or "")[:200],
    }
    _write_json(out / "ocr_lightweight_provider_adapter_smoke_summary.json", summary)

    (out / "ocr_lightweight_provider_notes.md").write_text(
        "# Phase-OCR-Lightweight-Real-Provider-Adapter-001\n\n"
        "Lightweight RapidOCR path behind `LUNA_ENABLE_OCR_REAL_PROVIDER_V0` + "
        "`LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0`; max edge `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX` (default 512). "
        "PaddleOCR runtime remains off. No MidPlatform / WorldModel.\n",
        encoding="utf-8",
    )
    print(json.dumps({"ocr_lightweight_provider_smoke_root": str(out), "status": "success"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
