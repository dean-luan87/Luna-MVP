#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-CacheMaterialize-001 — Orchestrate cache fill → snapshot → verifiers (no PaddleOCR(), no OCR).

Optional --copy-from or authorized --allow-download. Subprocess isolation per step.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS_OCR = Path(__file__).resolve().parent


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_stdout_json(stdout: str) -> Dict[str, Any]:
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)
    raise ValueError("no_json_line_in_stdout")


def _run_step(
    label: str,
    argv: List[str],
) -> Tuple[int, str, str, Dict[str, Any]]:
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    out = proc.stdout or ""
    err = proc.stderr or ""
    meta: Dict[str, Any] = {}
    try:
        meta = _parse_stdout_json(out)
    except Exception as e:
        meta = {"_parse_error": str(e), "stdout_tail": out[-2000:]}
    return proc.returncode, out, err, meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--prepare-root", required=True, help="Frozen CachePrepare-001 output root.")
    ap.add_argument("--output-root", default="")
    ap.add_argument("--copy-from", default="", help="Optional absolute local tree with det/rec/cls content.")
    ap.add_argument("--allow-download", action="store_true")
    ap.add_argument("--download-url-manifest", default="", help="Required with --allow-download when fetching.")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    prepare = _require_abs(args.prepare_root, "--prepare-root")
    cand = prepare / "paddleocr_current_api_model_manifest_v1.candidate.json"
    if not cand.is_file():
        raise SystemExit(f"ERROR: candidate manifest missing: {cand}")

    py = sys.executable
    fill_py = TOOLS_OCR / "fill_paddleocr_manifest_v1_cache_v0.py"
    snap_py = TOOLS_OCR / "run_paddleocr_manifest_v1_snapshot_v0.py"
    ver_snap_py = TOOLS_OCR / "verify_paddleocr_manifest_v1_snapshot_v0.py"
    ver_comp_py = TOOLS_OCR / "verify_paddleocr_manifest_v1_cache_fill_completion_v0.py"

    if args.output_root.strip():
        mat_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        mat_root = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_manifest_v1_cache_materialize_001_{stamp}").resolve()
    mat_root.mkdir(parents=True, exist_ok=True)

    steps: List[Dict[str, Any]] = []

    fill_argv = [py, str(fill_py), "--repo-root", str(repo), "--prepare-root", str(prepare), "--output-root", str(mat_root / "fill")]
    if args.copy_from.strip():
        fill_argv.extend(["--copy-from", str(_require_abs(args.copy_from, "--copy-from"))])
    if args.allow_download:
        fill_argv.append("--allow-download")
        if args.download_url_manifest.strip():
            fill_argv.extend(["--download-url-manifest", str(_require_abs(args.download_url_manifest, "--download-url-manifest"))])

    code, out, err, fill_meta = _run_step("fill", fill_argv)
    steps.append({"step": "fill", "exit_code": code, "stderr_tail": err[-1500:], "stdout_json": fill_meta})
    fill_root = Path(fill_meta.get("output_root", "")) if isinstance(fill_meta.get("output_root"), str) else mat_root / "fill"
    if not fill_root.is_dir():
        fill_root = mat_root / "fill"

    snap_argv = [
        py,
        str(snap_py),
        "--repo-root",
        str(repo),
        "--manifest",
        str(cand),
        "--output-root",
        str(mat_root / "snapshot"),
    ]
    code2, out2, err2, snap_meta = _run_step("snapshot", snap_argv)
    steps.append({"step": "snapshot", "exit_code": code2, "stderr_tail": err2[-1500:], "stdout_json": snap_meta})
    snap_root = Path(snap_meta.get("output_root", "")) if isinstance(snap_meta.get("output_root"), str) else mat_root / "snapshot"
    if not snap_root.is_dir():
        snap_root = mat_root / "snapshot"

    ver_snap_argv = [py, str(ver_snap_py), "--repo-root", str(repo), "--snapshot-root", str(snap_root)]
    code3, out3, err3, ver_snap_meta = _run_step("verify_snapshot", ver_snap_argv)
    steps.append({"step": "verify_snapshot", "exit_code": code3, "stderr_tail": err3[-1500:], "stdout_json": ver_snap_meta})

    ver_comp_argv = [
        py,
        str(ver_comp_py),
        "--repo-root",
        str(repo),
        "--prepare-root",
        str(prepare),
        "--fill-root",
        str(fill_root),
        "--snapshot-root",
        str(snap_root),
        "--output-root",
        str(mat_root / "completion"),
    ]
    code4, out4, err4, comp_meta = _run_step("verify_completion", ver_comp_argv)
    steps.append({"step": "verify_completion", "exit_code": code4, "stderr_tail": err4[-1500:], "stdout_json": comp_meta})

    co = comp_meta.get("completion_output_root")
    if isinstance(co, str) and co.strip():
        completion_root = Path(co).expanduser().resolve()
    else:
        completion_root = (mat_root / "completion").resolve()
    comp_sum_p = completion_root / "paddleocr_manifest_v1_cache_fill_completion_summary.json"
    comp_summary: Dict[str, Any] = {}
    if comp_sum_p.is_file():
        comp_summary = json.loads(comp_sum_p.read_text(encoding="utf-8"))

    snap_sum_p = snap_root / "paddleocr_manifest_v1_snapshot_summary.json"
    pinned_p = snap_root / "paddleocr_manifest_v1_pinned_manifest_candidate.json"
    snap_summary: Dict[str, Any] = {}
    pinned: Dict[str, Any] = {}
    if snap_sum_p.is_file():
        snap_summary = json.loads(snap_sum_p.read_text(encoding="utf-8"))
    if pinned_p.is_file():
        pinned = json.loads(pinned_p.read_text(encoding="utf-8"))

    materialize_verdict = str(comp_summary.get("completion_verdict") or "CONDITIONAL_GO")
    if not comp_sum_p.is_file():
        materialize_verdict = "CONDITIONAL_GO"
    if code3 != 0 and materialize_verdict == "GO":
        materialize_verdict = "NO_GO"
    if code4 == 2:
        materialize_verdict = "NO_GO"

    summary = {
        "schema": "paddleocr_manifest_v1_cache_materialize_summary_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CacheMaterialize-001",
        "materialize_verdict": materialize_verdict,
        "repo_root": str(repo),
        "prepare_root": str(prepare),
        "candidate_manifest": str(cand),
        "materialize_output_root": str(mat_root),
        "fill_root": str(fill_root),
        "snapshot_root": str(snap_root),
        "completion_root": str(completion_root),
        "snapshot_summary_verdict": snap_summary.get("verdict"),
        "pinning_complete": pinned.get("pinning_complete"),
        "missing_ref_count": comp_summary.get("missing_ref_count"),
        "sha256_entry_count": comp_summary.get("sha256_entry_count"),
        "completion_verdict": comp_summary.get("completion_verdict"),
        "completion_blockers": comp_summary.get("blockers"),
        "step_exit_codes": {"fill": code, "snapshot": code2, "verify_snapshot": code3, "verify_completion": code4},
        "steps": steps,
        "constraints": {
            "paddleocr_constructor_invoked": False,
            "paddleocr_inference_invoked": False,
            "ocr_routing_changed": False,
            "rapidocr_replaced": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "midplatform_invoked": False,
        },
    }
    _write_json(mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json", summary)

    (mat_root / "paddleocr_manifest_v1_cache_materialize_notes.md").write_text(
        "\n".join(
            [
                "# PaddleOCR Manifest v1 Cache Materialize v0",
                "",
                f"- **materialize_output_root**: `{mat_root}`",
                f"- **materialize_verdict**: `{materialize_verdict}`",
                "",
                "## 链式步骤",
                "",
                "1. `fill_paddleocr_manifest_v1_cache_v0.py`",
                "2. `run_paddleocr_manifest_v1_snapshot_v0.py`（manifest = candidate）",
                "3. `verify_paddleocr_manifest_v1_snapshot_v0.py`",
                "4. `verify_paddleocr_manifest_v1_cache_fill_completion_v0.py`",
                "",
                "## 边界",
                "",
                "- **不** `PaddleOCR()`、**不** OCR、**不**改 routing、**不**替换 RapidOCR。",
                "- **不**伪造 sha256；pinning 以 snapshot 输出为准。",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"materialize_output_root": str(mat_root), "materialize_verdict": materialize_verdict}, ensure_ascii=False))
    return 0 if materialize_verdict == "GO" else (2 if materialize_verdict == "NO_GO" else 0)


if __name__ == "__main__":
    raise SystemExit(main())
