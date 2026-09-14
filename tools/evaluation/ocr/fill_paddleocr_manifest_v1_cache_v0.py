#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-CacheFill-001 — Offline cache fill / probe (optional copy or authorized download).

No PaddleOCR(). No OCR inference. No routing changes.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
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


def _constraints() -> Dict[str, Any]:
    return {
        "network_download_invoked": False,
        "paddleocr_constructor_invoked": False,
        "paddleocr_inference_invoked": False,
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "mainline_side_effect": False,
        "midplatform_invoked": False,
        "scene_delta_invoked": False,
        "world_context_evidence_invoked": False,
    }


def _count_files(d: Path) -> int:
    if not d.is_dir():
        return 0
    return sum(1 for p in d.rglob("*") if p.is_file())


def _copy_role_tree(src_root: Path, ref: str, dest: Path) -> List[str]:
    actions: List[str] = []
    src = src_root / ref
    if not src.is_dir():
        return actions
    dest.mkdir(parents=True, exist_ok=True)
    for item in sorted(src.iterdir()):
        if item.is_file():
            dst = dest / item.name
            shutil.copy2(item, dst)
            actions.append(f"copied:{item}->{dst}")
    return actions


def _download_one(url: str, dest: Path) -> None:
    req = Request(url, headers={"User-Agent": "Luna-PaddleOCR-ManifestV1-CacheFill-001/0"})
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(req, timeout=300) as resp:
        data = resp.read()
    dest.write_bytes(data)


def _download_from_manifest(
    model_root: Path,
    url_manifest: Path,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    ok: List[Dict[str, Any]] = []
    err: List[str] = []
    doc = json.loads(url_manifest.read_text(encoding="utf-8"))
    entries = doc.get("entries") if isinstance(doc.get("entries"), list) else []
    for e in entries:
        if not isinstance(e, dict):
            continue
        role = str(e.get("role") or "").strip()
        target_ref = str(e.get("target_ref") or role).strip()
        url = str(e.get("url") or "").strip()
        if not url or url.lower() == "null":
            err.append(f"no_url_for:{role}:{target_ref}")
            continue
        fname = url.rstrip("/").split("/")[-1].split("?")[0] or "download.bin"
        dest = model_root / target_ref / fname
        try:
            _download_one(url, dest)
            ok.append({"role": role, "target_ref": target_ref, "url": url, "dest": str(dest)})
        except Exception as ex:
            err.append(f"download_failed:{role}:{target_ref}:{ex}")
    return ok, err


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--prepare-root", required=True, help="Absolute output root of CachePrepare-001.")
    ap.add_argument("--output-root", default="")
    ap.add_argument("--copy-from", default="", help="Absolute local directory with det/rec/cls (or ref-named) subtrees.")
    ap.add_argument("--allow-download", action="store_true")
    ap.add_argument("--download-url-manifest", default="", help="JSON with entries[].{role,target_ref,url}")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    prepare = _require_abs(args.prepare_root, "--prepare-root")
    cand_path = prepare / "paddleocr_current_api_model_manifest_v1.candidate.json"
    manual_path = prepare / "paddleocr_manifest_v1_manual_copy_instructions.md"
    if not cand_path.is_file():
        raise SystemExit(f"ERROR: candidate manifest missing: {cand_path}")

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_manifest_v1_cache_fill_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    candidate = json.loads(cand_path.read_text(encoding="utf-8"))
    model_root = Path(str(candidate.get("model_root") or "").strip()).expanduser().resolve()
    det_r = str(candidate.get("det_model_ref") or "det").strip()
    rec_r = str(candidate.get("rec_model_ref") or "rec").strip()
    cls_r = str(candidate.get("cls_model_ref") or "cls").strip()

    constraints = _constraints()
    copy_actions: List[str] = []
    download_records: List[Dict[str, Any]] = []
    download_errs: List[str] = []
    network_invoked = False

    copy_from = Path(args.copy_from).expanduser().resolve() if args.copy_from.strip() else None
    if copy_from is not None:
        if not copy_from.is_dir():
            raise SystemExit(f"ERROR: --copy-from must be a directory: {copy_from}")
        for ref in (det_r, rec_r, cls_r):
            dest = model_root / ref
            copy_actions.extend(_copy_role_tree(copy_from, ref, dest))

    download_authorized = bool(args.allow_download)
    url_manifest = Path(args.download_url_manifest).expanduser().resolve() if args.download_url_manifest.strip() else None
    if download_authorized:
        if url_manifest is None or not url_manifest.is_file():
            download_errs.append("allow_download_requires_existing_download_url_manifest")
        else:
            ok, errs = _download_from_manifest(model_root, url_manifest)
            download_records.extend(ok)
            download_errs.extend(errs)
            network_invoked = bool(ok) or any(x.startswith("download_failed:") for x in errs)

    constraints["network_download_invoked"] = network_invoked

    matrix_rows: List[Dict[str, Any]] = []
    missing: List[Dict[str, Any]] = []
    all_nonempty = True
    for role, ref in (("det", det_r), ("rec", rec_r), ("cls", cls_r)):
        d = model_root / ref
        n = _count_files(d)
        exists = d.exists()
        row = {
            "role": role,
            "ref": ref,
            "path": str(d),
            "exists": exists,
            "is_dir": d.is_dir(),
            "file_count": n,
        }
        matrix_rows.append(row)
        if not exists or not d.is_dir() or n == 0:
            all_nonempty = False
            missing.append(
                {
                    "role": role,
                    "ref": ref,
                    "path": str(d),
                    "reason": "missing_or_empty" if exists else "missing_directory",
                }
            )

    fill_verdict = "GO" if all_nonempty and not download_errs else "CONDITIONAL_GO"
    if download_errs and any("allow_download_requires" not in x for x in download_errs):
        fill_verdict = "CONDITIONAL_GO"

    next_actions = [
        f"Ensure model files exist under: {model_root / det_r}, {model_root / rec_r}, {model_root / cls_r}",
        "Then run: run_paddleocr_manifest_v1_snapshot_v0.py --manifest <candidate.json> --repo-root <REPO>",
        "Then run: verify_paddleocr_manifest_v1_snapshot_v0.py --snapshot-root <SNAP_OUT>",
    ]
    if not manual_path.is_file():
        next_actions.append(f"(optional) manual instructions missing at {manual_path}")

    dl_report = {
        "download_authorized": download_authorized,
        "download_source": str(url_manifest) if url_manifest else None,
        "download_time": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "network_request_invoked": network_invoked,
        "downloads_ok": download_records,
        "download_errors": download_errs,
        "copy_from": str(copy_from) if copy_from else None,
        "copy_actions": copy_actions,
    }

    summary = {
        "schema": "paddleocr_manifest_v1_cache_fill_summary_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CacheFill-001",
        "cache_fill_verdict": fill_verdict,
        "repo_root": str(repo),
        "prepare_root": str(prepare),
        "output_root": str(out),
        "candidate_manifest": str(cand_path),
        "model_root": str(model_root),
        "all_role_directories_nonempty": all_nonempty,
        "next_manual_actions": next_actions,
        "constraints": constraints,
    }

    _write_json(out / "paddleocr_manifest_v1_cache_fill_summary.json", summary)
    _write_json(
        out / "paddleocr_manifest_v1_cache_fill_file_matrix.json",
        {"schema": "paddleocr_manifest_v1_cache_fill_file_matrix_v0", "phase": summary["phase"], "rows": matrix_rows},
    )
    _write_json(
        out / "paddleocr_manifest_v1_cache_fill_missing_report.json",
        {"schema": "paddleocr_manifest_v1_cache_fill_missing_report_v0", "phase": summary["phase"], "missing": missing},
    )
    _write_json(out / "paddleocr_manifest_v1_cache_fill_download_report.json", dl_report)

    (out / "paddleocr_manifest_v1_cache_fill_notes.md").write_text(
        "\n".join(
            [
                "# PaddleOCR Manifest v1 Cache Fill v0",
                "",
                f"- **output_root**: `{out}`",
                f"- **model_root**: `{model_root}`",
                "",
                "## 边界",
                "",
                "- **不** `PaddleOCR()`、**不** OCR、**不**改 routing。",
                f"- **network_request_invoked**: `{network_invoked}`",
                "",
                f"- **cache_fill_verdict**: `{fill_verdict}`",
                "",
                "## Next",
                "",
                *[f"- {a}" for a in next_actions],
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "cache_fill_verdict": fill_verdict}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
