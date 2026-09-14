#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Real-Provider-Adapter-Selection-001 — provider registry + selection skeleton smoke (no real OCR)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _ensure_smoke_image(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image

        Image.new("RGB", (512, 512), (200, 200, 200)).save(path, format="PNG")
    except Exception as e:
        raise SystemExit(f"ERROR: cannot create smoke image (PIL required): {e}") from e


class _EnvFrame:
    def __init__(self, updates: Dict[str, str]) -> None:
        self.updates = updates
        self._prev: Dict[str, Optional[str]] = {}

    def __enter__(self) -> "_EnvFrame":
        for k, v in self.updates.items():
            self._prev[k] = os.environ.get(k)
            os.environ[k] = v
        return self

    def __exit__(self, *args: object) -> None:
        for k, old in self._prev.items():
            if old is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = old


def _run_bridge_case(
    *,
    ws: Path,
    gov: Path,
    out: Path,
    case_id: str,
    env_updates: Dict[str, str],
    request_kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    with _EnvFrame(env_updates):
        from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
        from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

        img = out / f"_provider_sel_smoke_{case_id}.png"
        _ensure_smoke_image(img)
        req = OCRRequestV0(
            image_path=str(img),
            input_type="image_path",
            latency_budget_ms=4000,
            **request_kwargs,
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

    base_env: Dict[str, str] = {
        "LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0": "true",
        "LUNA_ENABLE_OCR_STUB_PROVIDER_V0": "true",
        "LUNA_ENABLE_OCR_REAL_PROVIDER_V0": "false",
        "LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0": "false",
        "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0": "false",
        "LUNA_ENABLE_OCR_TILE_PLANNER_V0": "false",
    }

    from capabilities.ocr_runtime.ocr_provider_registry_v0 import build_default_ocr_provider_registry_v0

    reg = build_default_ocr_provider_registry_v0()
    _write_json(out / "ocr_provider_registry_snapshot.json", reg.snapshot())

    cases: List[Dict[str, Any]] = []

    # Case A — default stub path
    ra = _run_bridge_case(ws=ws, gov=gov, out=out, case_id="A", env_updates=base_env, request_kwargs={})
    _write_json(out / "ocr_provider_selection_case_a_result.json", ra)
    cases.append({"case": "A_default_stub", "status": ra.get("status"), "error": ra.get("error")})

    # Case B — heavy signal but real provider disabled → must stay stub, no real invoke
    rb = _run_bridge_case(
        ws=ws,
        gov=gov,
        out=out,
        case_id="B",
        env_updates=base_env,
        request_kwargs={"allow_heavy_ocr": True},
    )
    _write_json(out / "ocr_provider_selection_case_b_result.json", rb)
    cases.append({"case": "B_heavy_request_real_disabled", "status": rb.get("status"), "error": rb.get("error")})

    # Case C — paddle runtime flag without real provider flag → hard reject in bridge
    rc = _run_bridge_case(
        ws=ws,
        gov=gov,
        out=out,
        case_id="C",
        env_updates={**base_env, "LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0": "true"},
        request_kwargs={},
    )
    _write_json(out / "ocr_provider_selection_case_c_result.json", rc)
    cases.append({"case": "C_paddle_flag_without_real", "status": rc.get("status"), "error": rc.get("error")})

    rep_a = ra.get("provider_selection_report") if isinstance(ra.get("provider_selection_report"), dict) else {}
    aud_a = ra.get("audit") if isinstance(ra.get("audit"), dict) else {}
    sel_keys = (
        "selected_provider",
        "selected_provider_level",
        "provider_selection_reason_codes",
        "real_provider_requested",
        "real_provider_allowed",
        "real_provider_invoked",
        "paddleocr_runtime_provider_enabled",
        "rapidocr_runtime_provider_enabled",
        "fallback_to_stub",
        "provider_registry_snapshot",
    )
    audit_sel = {k: aud_a.get(k) for k in sel_keys}

    _write_json(out / "ocr_provider_selection_report.json", rep_a)
    _write_json(out / "ocr_provider_selection_audit_report.json", audit_sel)

    summary = {
        "schema": "ocr_provider_selection_smoke_summary_v0",
        "phase": "Phase-OCR-Real-Provider-Adapter-Selection-001",
        "output_root": str(out),
        "cases": cases,
        "case_a_selected_provider": rep_a.get("selected_provider"),
        "case_b_fallback_to_stub": (rb.get("audit") or {}).get("fallback_to_stub") if isinstance(rb.get("audit"), dict) else None,
        "case_c_expected_bridge_error": True,
    }
    _write_json(out / "ocr_provider_selection_smoke_summary.json", summary)
    print(json.dumps({"ocr_provider_selection_smoke_root": str(out), "status": "success"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
