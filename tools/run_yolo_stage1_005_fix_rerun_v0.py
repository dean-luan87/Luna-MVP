#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-005-Fix — YOLO runtime dependency diagnosis, optional ultralytics install,
bootstrap real Phase-004 approval gate (from 003), re-run Phase-005 10-frame dry-run, verify.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

TOOLS_DIR = Path(__file__).resolve().parent
# 使用 resolve()：从 Workspace-Min 经 symlink 调用本脚本时，默认仓库根应对齐到真实 Luna-Core 根。
REPO_ROOT = str(TOOLS_DIR.parent)

PHASE = "Phase-Mainline-GuardedTrial-005-Fix"


def _validate_static_config_for_bootstrap(cfg: Path, repo: Path) -> Optional[Dict[str, Any]]:
    if not cfg.is_dir():
        return {
            "error": "static_config_root_not_a_dir",
            "resolved": str(cfg),
            "repo_root_used": str(repo),
            "hint": "相对路径会拼在 --repo-root（默认：本脚本所在仓库根）之后；若在 Luna-Workspace-Min 下跑，请改用 "
            "003 目录的绝对路径，或传入 --repo-root 指向含 logs/ 的 Luna-Core 根目录。",
        }
    runbook = cfg / "yolo_stage1_10_frame_dry_run_runbook.json"
    if not runbook.is_file():
        return {
            "error": "missing_runbook_in_static_config_root",
            "resolved": str(cfg),
            "expected_file": str(runbook),
            "repo_root_used": str(repo),
        }
    return None


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _try_import_versions() -> Dict[str, Any]:
    rows: Dict[str, Any] = {}

    mods = [
        ("numpy", "numpy", "__version__"),
        ("cv2", "cv2", "__version__"),
        ("torch", "torch", "__version__"),
    ]
    for key, mod, attr in mods:
        try:
            m = __import__(mod)
            rows[key] = {"ok": True, "version": str(getattr(m, attr))}
        except Exception as e:  # noqa: BLE001
            rows[key] = {"ok": False, "error": f"{type(e).__name__}: {e}"}

    try:
        u = __import__("ultralytics")
        ver = getattr(u, "__version__", "")
        rows["ultralytics"] = {"ok": True, "version": str(ver)}
    except Exception as e:  # noqa: BLE001
        rows["ultralytics"] = {"ok": False, "error": f"{type(e).__name__}: {e}"}

    for key, mod in (("seaborn", "seaborn"), ("pandas", "pandas")):
        try:
            m = __import__(mod)
            rows[key] = {"ok": True, "version": str(getattr(m, "__version__", ""))}
        except Exception as e:  # noqa: BLE001
            rows[key] = {"ok": False, "error": f"{type(e).__name__}: {e}"}

    return rows


def _pip_install_yolo_hub_runtime() -> Tuple[int, str, str]:
    # torch.hub ultralytics/yolov5 commonly imports seaborn; manifest lists seaborn/pandas with OpenCV trials.
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "ultralytics>=8.0.0",
            "seaborn>=0.13.0",
            "pandas>=2.0.0",
        ],
        cwd=str(Path(REPO_ROOT).resolve()),
        capture_output=True,
        text=True,
        timeout=900,
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--repo-root",
        default="",
        help="解析相对 --output-root / --static-config-root / --approval-root 时使用的仓库根（默认：本脚本上级目录）",
    )
    ap.add_argument("--output-root", default="", help="Fix pack root (default logs/yolo_stage1_005_fix_rerun_<UTC>)")
    ap.add_argument("--approval-root", default="", help="Phase-004 gate directory (if set, skips bootstrap)")
    ap.add_argument(
        "--static-config-root",
        default="",
        help="Phase-003 static config root — required when --approval-root omitted to bootstrap real 004",
    )
    ap.add_argument("--input-video", required=True, help="Real offline video .mp4/.mov/.mkv/.avi")
    ap.add_argument(
        "--install-ultralytics",
        "--install-yolo-hub-runtime",
        dest="install_yolo_hub_runtime",
        action="store_true",
        help=(
            "After diagnosis, pip install ultralytics/seaborn/pandas when any hub-side import is missing "
            "(torch.hub yolov5 stack)"
        ),
    )
    ap.add_argument("--skip-rerun", action="store_true", help="Only diagnose / optional install / bootstrap gate")
    args = ap.parse_args()

    repo = Path(args.repo_root.strip()).resolve() if args.repo_root.strip() else Path(REPO_ROOT).resolve()
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"yolo_stage1_005_fix_rerun_{_utc_tag()}"
    if not out.is_absolute():
        out = (repo / out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    video = Path(args.input_video.strip()).expanduser()
    if not video.is_absolute():
        video = Path.cwd() / video
    video = video.resolve()

    report: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo),
        "script_repo_root_default": str(Path(REPO_ROOT).resolve()),
        "output_root": str(out),
        "input_video": str(video),
        "pip_install_ultralytics_requested": bool(args.install_yolo_hub_runtime),
        "imports_before": {},
        "imports_after": {},
        "pip_install": {"attempted": False, "returncode": None, "stdout_tail": "", "stderr_tail": ""},
        "approval_root_used": "",
        "bootstrap_004_command": [],
        "execution_005": {},
        "verification": {},
    }

    report["imports_before"] = _try_import_versions()

    notes_lines = [
        f"# {PHASE}",
        "",
        "## 依赖诊断（执行任何安装前）",
        "",
        "```json",
        json.dumps(report["imports_before"], ensure_ascii=False, indent=2),
        "```",
        "",
    ]

    hub_missing = (
        not report["imports_before"].get("ultralytics", {}).get("ok")
        or not report["imports_before"].get("seaborn", {}).get("ok")
        or not report["imports_before"].get("pandas", {}).get("ok")
    )
    if args.install_yolo_hub_runtime and hub_missing:
        report["pip_install"]["attempted"] = True
        rc, so, se = _pip_install_yolo_hub_runtime()
        report["pip_install"]["returncode"] = rc
        report["pip_install"]["stdout_tail"] = (so or "")[-4000:]
        report["pip_install"]["stderr_tail"] = (se or "")[-4000:]
        notes_lines.extend(
            [
                "## pip install (ultralytics + seaborn + pandas)",
                "",
                f"- returncode: {rc}",
                "",
            ]
        )
    elif hub_missing:
        notes_lines.append(
            "未执行 `--install-ultralytics` / `--install-yolo-hub-runtime`；"
            "hub 侧依赖缺失时 005 试跑将 NO_GO。"
        )
        notes_lines.append("")

    report["imports_after"] = _try_import_versions()

    # Resolve approval root
    appr: Path
    if args.approval_root.strip():
        appr = Path(args.approval_root.strip()).expanduser()
        if not appr.is_absolute():
            appr = (repo / appr).resolve()
        else:
            appr = appr.resolve()
        if not appr.is_dir():
            _write_json(out / "yolo_stage1_dependency_fix_report.json", {**report, "error": "approval_root_not_dir"})
            (out / "dependency_fix_notes.md").write_text("\n".join(notes_lines + [f"**错误**: approval-root 不可读 `{appr}`"]), encoding="utf-8")
            print(json.dumps({"ok": False, "error": "approval_root_not_dir", "path": str(appr)}, ensure_ascii=False))
            return 2
        report["approval_root_used"] = str(appr)
    else:
        cfg = Path(args.static_config_root.strip()).expanduser() if args.static_config_root.strip() else None
        if not cfg or not str(cfg):
            _write_json(out / "yolo_stage1_dependency_fix_report.json", {**report, "error": "need_approval_or_static_config"})
            (out / "dependency_fix_notes.md").write_text("\n".join(notes_lines + ["缺少 `--approval-root` 或 `--static-config-root`。"]), encoding="utf-8")
            print(json.dumps({"ok": False, "error": "need_approval_root_or_static_config_root"}, ensure_ascii=False))
            return 2
        if not cfg.is_absolute():
            cfg = (repo / cfg).resolve()
        else:
            cfg = cfg.resolve()
        bad = _validate_static_config_for_bootstrap(cfg, repo)
        if bad:
            _write_json(out / "yolo_stage1_dependency_fix_report.json", {**report, "bootstrap_preflight": bad})
            (out / "dependency_fix_notes.md").write_text(
                "\n".join(notes_lines + ["## Bootstrap 预检失败", "", f"```json\n{json.dumps(bad, ensure_ascii=False, indent=2)}\n```"]),
                encoding="utf-8",
            )
            print(json.dumps({"ok": False, "error": "bootstrap_004_preflight_failed", **bad}, ensure_ascii=False))
            return 2

        prepare_py = TOOLS_DIR / "prepare_yolo_stage1_10_frame_approval_gate_v0.py"
        if not prepare_py.is_file():
            err = {"error": "missing_prepare_script", "expected": str(prepare_py)}
            _write_json(out / "yolo_stage1_dependency_fix_report.json", {**report, "bootstrap_preflight": err})
            print(json.dumps({"ok": False, **err}, ensure_ascii=False))
            return 2

        appr = out / "approval_gate_004_bootstrapped"
        cmd = [
            sys.executable,
            str(prepare_py),
            "--static-config-root",
            str(cfg),
            "--input-video",
            str(video),
            "--output-root",
            str(appr),
        ]
        report["bootstrap_004_command"] = cmd
        notes_lines.extend(["## Bootstrap Phase-004（真实 gate 目录）", "", f"- `{' '.join(cmd)}`", ""])
        r = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            so = r.stdout or ""
            se = r.stderr or ""
            report["bootstrap_error"] = {
                "returncode": r.returncode,
                "stdout_tail": so[-4000:],
                "stderr_tail": se[-4000:],
                "note": "prepare 多数错误（如 static_config_root 不存在）走 stdout JSON，请查看 stdout_tail。",
            }
            _write_json(out / "yolo_stage1_dependency_fix_report.json", report)
            (out / "dependency_fix_notes.md").write_text("\n".join(notes_lines + [f"bootstrap 失败: {report['bootstrap_error']}"]), encoding="utf-8")
            print(json.dumps({"ok": False, "error": "bootstrap_004_failed", "detail": report["bootstrap_error"]}, ensure_ascii=False))
            return r.returncode or 2
        report["approval_root_used"] = str(appr.resolve())

    exec_out = out / "yolo_stage1_10_frame_dry_run_execution_005_rerun"
    dry_cmd = [
        sys.executable,
        str(TOOLS_DIR / "run_yolo_stage1_10_frame_dry_run_v0.py"),
        "--approval-root",
        report["approval_root_used"],
        "--input-video",
        str(video),
        "--output-root",
        str(exec_out),
    ]
    report["execution_005"]["command"] = dry_cmd

    if args.skip_rerun:
        report["execution_005"]["skipped"] = True
        report["execution_005"]["reason"] = "--skip-rerun"
        _write_json(out / "yolo_stage1_dependency_fix_report.json", report)
        (out / "dependency_fix_notes.md").write_text("\n".join(notes_lines), encoding="utf-8")
        _write_json(
            out / "yolo_stage1_10_frame_rerun_summary.json",
            {
                "phase": PHASE,
                "skipped": True,
                "dependency_report_path": str(out / "yolo_stage1_dependency_fix_report.json"),
                "imports_after": report["imports_after"],
            },
        )
        _write_json(out / "yolo_stage1_10_frame_rerun_verification_result.json", {"skipped": True})
        print(json.dumps({"ok": True, "output_root": str(out), "skip_rerun": True}, ensure_ascii=False))
        return 0

    notes_lines.extend(["## Phase-005 重跑", "", f"- `{' '.join(dry_cmd)}`", ""])
    r5 = subprocess.run(dry_cmd, cwd=str(repo), capture_output=True, text=True, timeout=600)
    report["execution_005"]["returncode"] = r5.returncode
    report["execution_005"]["stdout"] = (r5.stdout or "")[-4000:]
    report["execution_005"]["stderr"] = (r5.stderr or "")[-4000:]

    summ_path = exec_out / "yolo_stage1_10_frame_dry_run_summary.json"
    execution_summary: Optional[Dict[str, Any]] = None
    if summ_path.is_file():
        try:
            execution_summary = json.loads(summ_path.read_text(encoding="utf-8"))
        except Exception:
            execution_summary = None

    v_spec = importlib.util.spec_from_file_location(
        "verify_yolo_stage1_10_frame_dry_run_v0",
        str(TOOLS_DIR / "verify_yolo_stage1_10_frame_dry_run_v0.py"),
    )
    if v_spec is None or v_spec.loader is None:
        report["verification"] = {"error": "cannot_load_verifier"}
        _write_json(out / "yolo_stage1_dependency_fix_report.json", report)
        return 2
    v_mod = importlib.util.module_from_spec(v_spec)
    v_spec.loader.exec_module(v_mod)
    v_ok, v_report = v_mod.verify(output_root=exec_out)
    report["verification"] = {"artifact_ok": v_ok, **v_report}

    _write_json(out / "yolo_stage1_dependency_fix_report.json", report)

    rerun_summary = {
        "phase": PHASE,
        "approval_root": report["approval_root_used"],
        "input_video": str(video),
        "execution_output_root": str(exec_out),
        "imports_after": report["imports_after"],
        "execution_dry_run_summary": execution_summary,
        "trial_verdict": v_report.get("trial_verdict"),
        "artifact_integrity": v_report.get("artifact_integrity"),
        "post_trial_recommendation": (execution_summary or {}).get("post_trial_recommendation"),
    }
    _write_json(out / "yolo_stage1_10_frame_rerun_summary.json", rerun_summary)
    _write_json(
        out / "yolo_stage1_10_frame_rerun_verification_result.json",
        {
            "phase": PHASE,
            "execution_output_root": str(exec_out),
            "ok": v_ok,
            **v_report,
        },
    )

    notes_lines.extend(
        [
            "## 005 执行结果摘要",
            "",
            f"- execution_output_root: `{exec_out}`",
            f"- artifact_integrity: **{v_report.get('artifact_integrity')}**",
            f"- trial_verdict: **{v_report.get('trial_verdict')}**",
            f"- post_trial_recommendation: `{(execution_summary or {}).get('post_trial_recommendation')}`",
            "",
            "GO 需同时满足 trial_verdict=GO 且 post_trial_recommendation=GO_next_window；仅 artifact_integrity=GO 不足。",
            "",
        ]
    )
    (out / "dependency_fix_notes.md").write_text("\n".join(notes_lines), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "output_root": str(out),
                "execution_output_root": str(exec_out),
                "approval_root": report["approval_root_used"],
                "artifact_integrity": v_report.get("artifact_integrity"),
                "trial_verdict": v_report.get("trial_verdict"),
                "post_trial_recommendation": (execution_summary or {}).get("post_trial_recommendation"),
            },
            ensure_ascii=False,
        )
    )

    trial_go = v_report.get("trial_verdict") == "GO" and (execution_summary or {}).get("post_trial_recommendation") == "GO_next_window"
    return 0 if trial_go else 3


if __name__ == "__main__":
    raise SystemExit(main())
