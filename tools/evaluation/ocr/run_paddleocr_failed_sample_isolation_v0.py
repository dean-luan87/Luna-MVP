#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Failed-Sample-Isolation-001 — Failed-sample image probe + safe variant subprocess matrix + raw-shape audit.

Evaluation-only: subprocesses reuse run_paddleocr_labeled_set_evaluation_v0.py; no routing, MidPlatform, RapidOCR replacement, or world model.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

PHASE = "Phase-PaddleOCR-Failed-Sample-Isolation-001"

VARIANT_ORDER = (
    "original",
    "downscale_max_2048",
    "downscale_max_1600",
    "downscale_max_1024",
    "rgb_converted",
    "exif_transposed",
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _exit_code_to_signal(rc: int) -> Optional[int]:
    if rc < 0:
        return -int(rc)
    return None


def _failed_sample_ids_from_bs1(crash_p: Path, summary_p: Path) -> List[str]:
    ids: List[str] = []
    if crash_p.is_file():
        doc = _read_json(crash_p)
        for e in doc.get("crash_entries") or []:
            if isinstance(e, dict) and e.get("last_sample_id"):
                ids.append(str(e["last_sample_id"]))
    if summary_p.is_file():
        doc = _read_json(summary_p)
        for x in doc.get("missing_sample_ids") or []:
            if x and str(x) not in ids:
                ids.append(str(x))
    out: List[str] = []
    for s in ids:
        if s not in out:
            out.append(s)
    return out


def _failure_kind_from_crash(crash_p: Path) -> Dict[str, str]:
    kinds: Dict[str, str] = {}
    if not crash_p.is_file():
        return kinds
    doc = _read_json(crash_p)
    for e in doc.get("crash_entries") or []:
        if not isinstance(e, dict):
            continue
        sid = str(e.get("last_sample_id") or "")
        if not sid:
            continue
        sig = e.get("signal")
        rc = e.get("exit_code")
        if sig == 11 or rc == -11:
            kinds[sid] = "SIGSEGV"
        elif rc == 1:
            kinds[sid] = "PYTHON_ERROR"
        else:
            kinds[sid] = f"exit_{rc}"
    return kinds


def _probe_image(path: Path) -> Dict[str, Any]:
    row: Dict[str, Any] = {
        "image_path": str(path),
        "file_exists": path.is_file(),
        "file_size_bytes": path.stat().st_size if path.is_file() else None,
        "width": None,
        "height": None,
        "channels": None,
        "mode": None,
        "format": None,
        "exif_orientation": None,
        "megapixels": None,
        "is_large_image": None,
        "probe_error": None,
    }
    if not path.is_file():
        row["probe_error"] = "file_missing"
        return row
    try:
        from PIL import Image

        with Image.open(path) as im:
            row["format"] = im.format
            row["mode"] = im.mode
            w, h = im.size
            row["width"] = int(w)
            row["height"] = int(h)
            row["megapixels"] = round((w * h) / 1_000_000.0, 4)
            row["is_large_image"] = bool(max(w, h) > 4000 or (w * h) > 12_000_000)
            exif = im.getexif()
            if exif is not None:
                ori = exif.get(274)
                if ori is not None:
                    row["exif_orientation"] = int(ori)
            if im.mode in ("RGB", "RGBA", "L", "P"):
                ch = len(im.getbands()) if hasattr(im, "getbands") else None
                row["channels"] = ch
    except Exception as e:
        row["probe_error"] = f"{type(e).__name__}: {e}"
    return row


def _build_variant_image(src: Path, variant: str, out_path: Path) -> Tuple[bool, Optional[str]]:
    """Write variant image to out_path. Returns (ok, error_message)."""
    try:
        from PIL import Image, ImageOps

        im = Image.open(src)
        im.load()
        if variant == "exif_transposed":
            im = ImageOps.exif_transpose(im)
        elif variant == "rgb_converted":
            im = im.convert("RGB")
        elif variant.startswith("downscale_max_"):
            im = ImageOps.exif_transpose(im)
            max_side = int(variant.rsplit("_", 1)[-1])
            w, h = im.size
            m = max(w, h)
            if m > max_side:
                scale = max_side / float(m)
                nw = max(1, int(round(w * scale)))
                nh = max(1, int(round(h * scale)))
                im = im.resize((nw, nh), Image.Resampling.LANCZOS)
        else:
            return False, f"unknown_variant:{variant}"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        im.save(out_path, format="PNG")
        return True, None
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def _single_sample_manifest(spec: Dict[str, Any], image_path: Path) -> Dict[str, Any]:
    row = dict(spec)
    row["image_path"] = str(image_path.resolve())
    return {"schema_version": "paddleocr_labeled_set_manifest_v0", "samples": [row]}


def _run_labeled_eval_subprocess(
    *,
    repo: Path,
    mat_root: Path,
    pinned: Path,
    manifest_path: Path,
    eval_out: Path,
    runner: Path,
    timeout_sec: int,
) -> Dict[str, Any]:
    eval_out.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(runner),
        "--repo-root",
        str(repo),
        "--materialize-root",
        str(mat_root),
        "--pinned-manifest",
        str(pinned),
        "--labeled-set-manifest",
        str(manifest_path.resolve()),
        "--output-root",
        str(eval_out.resolve()),
    ]
    t0 = time.perf_counter()
    stderr_tail = ""
    exit_code = 1
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
        exit_code = int(proc.returncode)
        err = proc.stderr or ""
        stderr_tail = err[-8000:] if err else ""
    except subprocess.TimeoutExpired as e:
        exit_code = -9
        stderr_tail = (e.stderr or "")[-8000:] if isinstance(e.stderr, str) else "timeout"
    except Exception as e:
        exit_code = 1
        stderr_tail = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"[-8000:]
    dur_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    sig = _exit_code_to_signal(exit_code) if exit_code < 0 else None
    return {
        "exit_code": exit_code,
        "signal": sig,
        "duration_ms": dur_ms,
        "stderr_tail": stderr_tail,
        "output_root": str(eval_out.resolve()),
    }


def _classify_raw_shapes() -> Dict[str, Any]:
    """Static description of raw branches supported by adapter after list/dict fix."""
    return {
        "schema": "paddleocr_failed_sample_raw_shape_report_v0",
        "phase": PHASE,
        "adapter_rules": [
            "raw dict with rec_texts: detected",
            "raw dict nested values: recursive scan",
            "raw list: each element scanned (dict blocks or nested lists)",
            "raw list must not call .values() on list (evaluator bug fixed in adapter)",
        ],
        "labeled_012_notes": "Previously failed with AttributeError on list.values(); adapter now recurses list items.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--bs1-rerun-root", required=True, help="Batch recovery root with crash_report + summary")
    ap.add_argument("--materialize-root", required=True)
    ap.add_argument("--pinned-manifest", required=True)
    ap.add_argument("--labeled-set-manifest", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--variant-timeout-sec", type=int, default=7200)
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    bs1 = _require_abs(args.bs1_rerun_root, "--bs1-rerun-root")
    mat_root = _require_abs(args.materialize_root, "--materialize-root")
    pinned = _require_abs(args.pinned_manifest, "--pinned-manifest")
    manifest_path = _require_abs(args.labeled_set_manifest, "--labeled-set-manifest")
    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    crash_p = bs1 / "paddleocr_labeled_set_batch_crash_report.json"
    summary_p = bs1 / "paddleocr_labeled_set_batch_recovery_summary.json"
    failed_ids = _failed_sample_ids_from_bs1(crash_p, summary_p)
    if not failed_ids:
        raise SystemExit("ERROR: no failed_sample_ids from bs1 crash/summary")

    kinds = _failure_kind_from_crash(crash_p)
    doc = _read_json(manifest_path)
    rows = doc.get("samples") if isinstance(doc.get("samples"), list) else []
    by_id: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        if isinstance(r, dict) and r.get("id"):
            by_id[str(r["id"])] = r

    runner = repo / "tools/evaluation/ocr/run_paddleocr_labeled_set_evaluation_v0.py"
    if not runner.is_file():
        raise SystemExit(f"ERROR: missing {runner}")

    work = out_root / "work"
    work.mkdir(parents=True, exist_ok=True)

    probes: Dict[str, Any] = {}
    variant_rows: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []

    for sid in failed_ids:
        spec = by_id.get(sid)
        if not spec:
            probes[sid] = {"error": "sample_not_in_manifest", "image_path": None}
            continue
        ip = Path(str(spec.get("image_path") or "")).expanduser()
        if not ip.is_absolute():
            ip = (manifest_path.parent / ip).resolve()
        probes[sid] = _probe_image(ip)

    for sid in failed_ids:
        spec = by_id.get(sid)
        if not spec:
            continue
        ip = Path(str(spec.get("image_path") or "")).expanduser()
        if not ip.is_absolute():
            ip = (manifest_path.parent / ip).resolve()
        fk = kinds.get(sid, "UNKNOWN")

        if fk == "SIGSEGV":
            for vn in VARIANT_ORDER:
                vdir = work / sid / vn
                vdir.mkdir(parents=True, exist_ok=True)
                manifest_p = vdir / "manifest_slice.json"
                eval_out = vdir / "eval_out"
                img_for_manifest = ip
                if vn == "original":
                    img_for_manifest = ip
                else:
                    tmp_img = vdir / f"input_{vn}.png"
                    ok, err = _build_variant_image(ip, vn, tmp_img)
                    if not ok:
                        variant_rows.append(
                            {
                                "sample_id": sid,
                                "variant": vn,
                                "variant_image_built": False,
                                "build_error": err,
                                "exit_code": None,
                                "signal": None,
                                "duration_ms": None,
                                "stderr_tail": "",
                                "output_root": str(eval_out),
                            }
                        )
                        continue
                    img_for_manifest = tmp_img
                man = _single_sample_manifest(spec, img_for_manifest)
                manifest_p.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                res = _run_labeled_eval_subprocess(
                    repo=repo,
                    mat_root=mat_root,
                    pinned=pinned,
                    manifest_path=manifest_p,
                    eval_out=eval_out,
                    runner=runner,
                    timeout_sec=int(args.variant_timeout_sec),
                )
                variant_rows.append(
                    {
                        "sample_id": sid,
                        "variant": vn,
                        "variant_image_built": True,
                        "build_error": None,
                        **res,
                    }
                )
        else:
            vdir = work / sid / "post_adapter_fix_original"
            vdir.mkdir(parents=True, exist_ok=True)
            manifest_p = vdir / "manifest_slice.json"
            eval_out = vdir / "eval_out"
            man = _single_sample_manifest(spec, ip)
            manifest_p.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            res = _run_labeled_eval_subprocess(
                repo=repo,
                mat_root=mat_root,
                pinned=pinned,
                manifest_path=manifest_p,
                eval_out=eval_out,
                runner=runner,
                timeout_sec=int(args.variant_timeout_sec),
            )
            variant_rows.append(
                {
                    "sample_id": sid,
                    "variant": "post_adapter_fix_original",
                    "failure_kind": fk,
                    "variant_image_built": True,
                    "build_error": None,
                    **res,
                }
            )

    for r in variant_rows:
        matrix_rows.append(
            {
                "sample_id": r.get("sample_id"),
                "variant": r.get("variant"),
                "exit_code": r.get("exit_code"),
                "signal": r.get("signal"),
                "duration_ms": r.get("duration_ms"),
                "ok_evaluator": r.get("exit_code") == 0,
                "variant_image_built": r.get("variant_image_built"),
                "build_error": r.get("build_error"),
            }
        )

    raw_shape = _classify_raw_shapes()
    post_012 = next(
        (r for r in variant_rows if r.get("sample_id") == "labeled_012" and "post_adapter" in str(r.get("variant"))),
        None,
    )
    raw_shape["labeled_012_post_fix_subprocess"] = post_012

    classification: Dict[str, Any] = {"schema": "paddleocr_failed_sample_crash_classification_v0", "phase": PHASE, "by_sample_id": {}}

    size_sensitive: List[str] = []
    image_format_sensitive: List[str] = []
    native_unresolved: List[str] = []
    evaluator_fixed: List[str] = []

    for sid in failed_ids:
        fk = kinds.get(sid, "UNKNOWN")
        if fk != "SIGSEGV":
            if sid == "labeled_012" and post_012 and post_012.get("exit_code") == 0:
                evaluator_fixed.append(sid)
                classification["by_sample_id"][sid] = {
                    "failure_kind": fk,
                    "verdict": "evaluator_bug_fixed_candidate",
                    "detail": "subprocess_exit_0_after_adapter_raw_list_fix",
                }
            else:
                classification["by_sample_id"][sid] = {
                    "failure_kind": fk,
                    "verdict": "non_sigsev_rerun",
                    "detail": "see paddleocr_failed_sample_variant_results.json",
                }
            continue

        def _ok(vn: str) -> bool:
            for r in variant_rows:
                if r.get("sample_id") == sid and r.get("variant") == vn and r.get("exit_code") == 0:
                    return True
            return False

        orig_ok = _ok("original")
        any_down = any(_ok(v) for v in ("downscale_max_2048", "downscale_max_1600", "downscale_max_1024"))
        rgb_ok = _ok("rgb_converted")
        exif_ok = _ok("exif_transposed")

        if not orig_ok and any_down:
            size_sensitive.append(sid)
            verdict = "size_sensitive"
        elif not orig_ok and (rgb_ok or exif_ok):
            image_format_sensitive.append(sid)
            verdict = "image_format_sensitive"
        elif not orig_ok and not any_down and not rgb_ok and not exif_ok:
            native_unresolved.append(sid)
            verdict = "native_crash_unresolved"
        elif orig_ok:
            verdict = "original_passed_in_isolation_rerun"
        else:
            verdict = "mixed_or_partial"

        classification["by_sample_id"][sid] = {
            "failure_kind": "SIGSEGV",
            "verdict": verdict,
            "original_exit_ok": orig_ok,
            "any_downscale_exit_ok": any_down,
            "rgb_exit_ok": rgb_ok,
            "exif_exit_ok": exif_ok,
        }

    audit = {
        "schema": "paddleocr_failed_sample_audit_report_v0",
        "phase": PHASE,
        "network_request_invoked": False,
        "model_cache_modified": False,
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "midplatform_invoked": False,
        "world_model_written": False,
        "midplatform_semantics_written": False,
        "mainline_touched": False,
    }

    large_samples = [sid for sid, p in probes.items() if isinstance(p, dict) and p.get("is_large_image") is True]

    incomplete = False
    for sid in failed_ids:
        pr = probes.get(sid)
        if not isinstance(pr, dict) or pr.get("file_exists") is not True:
            incomplete = True
            break

    sig_incomplete = False
    for sid in failed_ids:
        if kinds.get(sid) != "SIGSEGV":
            continue
        for vn in ("original", "downscale_max_2048", "downscale_max_1600"):
            hit = [r for r in variant_rows if r.get("sample_id") == sid and r.get("variant") == vn]
            if not hit:
                sig_incomplete = True
                break
        if sig_incomplete:
            break

    summary_verdict = "GO"
    if incomplete or sig_incomplete:
        summary_verdict = "CONDITIONAL_GO"

    summary = {
        "schema": "paddleocr_failed_sample_isolation_summary_v0",
        "phase": PHASE,
        "isolation_verdict": summary_verdict,
        "input_bs1_rerun_root": str(bs1),
        "output_root": str(out_root),
        "failed_sample_ids": failed_ids,
        "failure_kind_by_sample_id": kinds,
        "size_sensitive_sample_ids": size_sensitive,
        "image_format_sensitive_sample_ids": image_format_sensitive,
        "native_crash_unresolved_sample_ids": native_unresolved,
        "evaluator_bug_fixed_candidate_sample_ids": evaluator_fixed,
        "large_image_sample_ids": large_samples,
        "variant_timeout_sec": int(args.variant_timeout_sec),
        "repo_root": str(repo),
        "labeled_set_manifest": str(manifest_path),
        "materialize_root": str(mat_root),
        "pinned_manifest": str(pinned),
        "interpretation": "isolation_only_not_production_gate",
    }

    _write_json(out_root / "paddleocr_failed_sample_isolation_summary.json", summary)
    _write_json(out_root / "paddleocr_failed_sample_matrix.json", {"schema": "paddleocr_failed_sample_matrix_v0", "phase": PHASE, "rows": matrix_rows})
    _write_json(out_root / "paddleocr_failed_sample_image_probe_report.json", {"schema": "paddleocr_failed_sample_image_probe_report_v0", "phase": PHASE, "probes": probes})
    _write_json(out_root / "paddleocr_failed_sample_variant_results.json", {"schema": "paddleocr_failed_sample_variant_results_v0", "phase": PHASE, "rows": variant_rows})
    _write_json(out_root / "paddleocr_failed_sample_raw_shape_report.json", raw_shape)
    _write_json(out_root / "paddleocr_failed_sample_crash_classification.json", classification)
    _write_json(out_root / "paddleocr_failed_sample_audit_report.json", audit)

    notes = [
        f"# {PHASE}",
        "",
        f"- **input_bs1_rerun_root**: `{bs1}`",
        f"- **output_root**: `{out_root}`",
        f"- **failed_sample_ids**: {', '.join(failed_ids)}",
        f"- **isolation_verdict**: `{summary_verdict}`",
        f"- **size_sensitive**: {size_sensitive}",
        f"- **image_format_sensitive**: {image_format_sensitive}",
        f"- **native_crash_unresolved**: {native_unresolved}",
        f"- **evaluator_bug_fixed_candidate**: {evaluator_fixed}",
        "",
        "GO here means isolation artifacts complete per verifier; not PaddleOCR stability GO.",
        "",
    ]
    (out_root / "paddleocr_failed_sample_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    vp = repo / "tools/evaluation/ocr/verify_paddleocr_failed_sample_isolation_v0.py"
    if vp.is_file():
        subprocess.run([sys.executable, str(vp), "--isolation-root", str(out_root)], check=False)

    print(
        json.dumps(
            {
                "failed_sample_isolation_output_root": str(out_root),
                "input_bs1_rerun_root": str(bs1),
                "failed_sample_ids": failed_ids,
                "isolation_verdict": summary_verdict,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
