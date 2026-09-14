#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Weights-002 — Evaluation weights acquisition plan / optional authorized copy or download.

Default: no network, no PaddleOCR(), no OCR inference.
With --allow-download + valid URL manifest: HTTPS fetch only (explicit user URLs).
With --copy-from: copy from local tree into repo model dirs (no network).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.request import Request, urlopen

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_files(repo: Path, mf_rel: str) -> List[Dict[str, Any]]:
    mf_path = repo / mf_rel
    doc = _load_json(mf_path)
    raw = doc.get("expected_files") or []
    return [x for x in raw if isinstance(x, dict)]


def _file_matrix(repo: Path, expected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for ent in expected:
        rel = str(ent.get("relative_path") or "").strip()
        ap = (repo / rel).resolve() if rel else repo
        rows.append(
            {
                "role": ent.get("role"),
                "relative_path": rel,
                "absolute_path": str(ap),
                "exists_before": ap.is_file(),
                "exists_after": ap.is_file(),
            }
        )
    return rows


def _manual_plan(repo: Path, expected: List[Dict[str, Any]]) -> Dict[str, Any]:
    cmds = []
    for ent in expected:
        rel = str(ent.get("relative_path") or "").strip()
        dest = repo / rel
        cmds.append(
            {
                "step": "manual_copy",
                "target_relative": rel,
                "target_absolute": str(dest),
                "hint": f"mkdir -p {dest.parent} && cp <your_local_{Path(rel).name}> {dest}",
            }
        )
    return {"schema": "paddleocr_manual_acquisition_plan_v0", "commands": cmds}


def _copy_from_layout(copy_root: Path, repo: Path, expected: List[Dict[str, Any]]) -> List[str]:
    actions: List[str] = []
    for ent in expected:
        rel = str(ent.get("relative_path") or "").strip()
        if not rel:
            continue
        name = Path(rel).name
        role = str(ent.get("role") or "")
        candidates = [
            copy_root / rel,
            copy_root / Path(rel).name,
            copy_root / role / name,
        ]
        src = next((p for p in candidates if p.is_file()), None)
        dest = repo / rel
        if src is None:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dest))
        actions.append(f"copied:{src}->{dest}")
    return actions


def _download_one(url: str, dest: Path) -> None:
    req = Request(url, headers={"User-Agent": "Luna-PaddleOCR-Weights-002/0 (evaluation weights)"})
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(req, timeout=300) as resp:
        data = resp.read()
    dest.write_bytes(data)


def _authorized_downloads(
    repo: Path,
    url_manifest_path: Path,
    expected: List[Dict[str, Any]],
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    ok: List[str] = []
    doc = _load_json(url_manifest_path)
    entries = doc.get("files") if isinstance(doc.get("files"), list) else []
    by_rel = {str(e.get("relative_path") or ""): str(e.get("url") or "").strip() for e in entries if isinstance(e, dict)}
    for ent in expected:
        rel = str(ent.get("relative_path") or "").strip()
        url = by_rel.get(rel, "").strip()
        if not url or url.lower() == "null":
            errors.append(f"no_url_for:{rel}")
            continue
        dest = repo / rel
        try:
            _download_one(url, dest)
            ok.append(rel)
        except Exception as e:
            errors.append(f"download_failed:{rel}:{e}")
    return ok, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--manifest", default="configs/models/ocr/paddleocr_evaluation_readiness_manifest_v0.json")
    ap.add_argument("--model-files-manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json")
    ap.add_argument("--output-root", default="")
    ap.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow HTTPS fetch only when --download-url-manifest is provided with non-null URLs.",
    )
    ap.add_argument("--download-url-manifest", default="", help="JSON listing files[].{relative_path,url}")
    ap.add_argument("--copy-from", default="", help="Absolute path to local tree with weights to copy into repo paths.")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_weights_prepare_002_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    expected = _expected_files(repo, args.model_files_manifest.strip())
    before = _file_matrix(repo, expected)

    download_authorized = bool(args.allow_download)
    url_manifest = Path(args.download_url_manifest).expanduser().resolve() if args.download_url_manifest.strip() else None
    copy_from = Path(args.copy_from).expanduser().resolve() if args.copy_from.strip() else None

    copy_actions: List[str] = []
    download_ok: List[str] = []
    download_err: List[str] = []
    network_invoked = False

    if copy_from is not None:
        if not copy_from.is_dir():
            raise SystemExit(f"ERROR: --copy-from must be a directory: {copy_from}")
        copy_actions = _copy_from_layout(copy_from, repo, expected)

    if download_authorized:
        if url_manifest is None or not url_manifest.is_file():
            download_err.append("allow_download_requires_existing_download_url_manifest")
        else:
            download_ok, download_err = _authorized_downloads(repo, url_manifest, expected)
            network_invoked = bool(download_ok) or any(str(x).startswith("download_failed:") for x in download_err)

    after = _file_matrix(repo, expected)
    all_exist = all(r.get("exists_after") for r in after)
    missing = [r for r in after if not r.get("exists_after")]

    dl_report = {
        "download_authorized": download_authorized,
        "download_source": str(url_manifest) if url_manifest else None,
        "download_time": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "network_request_invoked": network_invoked,
        "files_downloaded": download_ok,
        "download_errors": download_err,
        "copy_from": str(copy_from) if copy_from else None,
        "copy_actions": copy_actions,
    }

    plan = _manual_plan(repo, expected)
    plan["copy_from_hint"] = (
        "If you have a local folder with det/rec/cls subfolders each containing inference.pdmodel and inference.pdiparams, "
        "use --copy-from <abs_path> (no network)."
    )
    plan["download_hint"] = (
        "To fetch over HTTPS, pass --allow-download and a JSON manifest (see "
        "configs/models/ocr/paddleocr_evaluation_weight_download_urls_v0.example.json) with non-null URLs per file."
    )

    summary = {
        "phase": "Phase-PaddleOCR-Weights-002",
        "repo_root": str(repo),
        "output_root": str(out),
        "readiness_manifest_relative": args.manifest.strip(),
        "model_files_manifest_relative": args.model_files_manifest.strip(),
        "all_expected_files_present_after": all_exist,
        "missing_count_after": len(missing),
        "readiness_posture": "GO" if all_exist else "CONDITIONAL_GO_weights_still_missing",
        "verdict": "GO" if all_exist else "CONDITIONAL_GO",
        "constraints": {
            "paddleocr_constructor_invoked": False,
            "paddleocr_inference_invoked": False,
            "rapidocr_replaced": False,
            "ocr_routing_changed": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "midplatform_invoked": False,
            "network_download_invoked": network_invoked,
        },
    }

    _write_json(out / "paddleocr_weights_prepare_summary.json", summary)
    _write_json(out / "paddleocr_weights_download_or_copy_plan.json", plan)
    _write_json(out / "paddleocr_weights_download_report.json", dl_report)
    _write_json(out / "paddleocr_weights_file_matrix.json", {"before": before, "after": after})

    notes = out / "paddleocr_weights_prepare_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# PaddleOCR Weights Prepare (Weights-002)",
                "",
                f"- **output_root**: `{out}`",
                "",
                "- Default: **no download**. Use `--copy-from` or `--allow-download` + URL manifest after explicit authorization.",
                "- **No PaddleOCR()** and **no OCR inference**.",
                "",
                f"- **all_expected_files_present_after**: `{all_exist}`",
                f"- **missing_count_after**: `{len(missing)}`",
                "",
                "After files exist, re-run `run_paddleocr_weights_snapshot_v0.py` then `verify_paddleocr_weights_snapshot_v0.py`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"], "missing_after": len(missing)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
