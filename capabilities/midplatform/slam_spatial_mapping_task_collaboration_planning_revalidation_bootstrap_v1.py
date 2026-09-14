# -*- coding: utf-8 -*-
"""Bootstrap helpers for SLAM P0 task collaboration planning revalidation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_items_v1 import (
    BOOTSTRAP_RUN_SCRIPTS,
    P0_TCP_OUTPUT,
    P0_TCP_PASS_FLAG,
    SCENE_GRAPH_P0_EXPECTED,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def evaluate_p0_visible_to_scene_graph() -> Dict[str, Any]:
    root = Path(P0_TCP_OUTPUT)
    summary = read_json(root / "summary.json")
    verifier = read_json(root / "verifier_report.json")
    visible = (
        root.is_dir()
        and (root / "summary.json").is_file()
        and (root / "verifier_report.json").is_file()
        and summary.get("final_decision") == SCENE_GRAPH_P0_EXPECTED["final_decision"]
        and summary.get(P0_TCP_PASS_FLAG) is True
        and verifier.get("verifier") == SCENE_GRAPH_P0_EXPECTED["verifier"]
    )
    return {
        "output_root": str(root),
        "artifact_present": root.is_dir() and (root / "summary.json").is_file(),
        "final_decision": summary.get("final_decision"),
        "pass_flag_value": summary.get(P0_TCP_PASS_FLAG),
        "verifier": verifier.get("verifier"),
        "p0_visible_to_scene_graph_review": visible,
    }


def _run_script(script: str) -> Dict[str, Any]:
    path = TOOLS / f"{script}.py"
    if not path.is_file():
        return {"script": script, "ok": False, "error": "script_missing"}
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    line = (proc.stdout or "").strip().split("\n")[-1] if proc.stdout else ""
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        payload = {"raw": line[:200]}
    verify = TOOLS / f"{script.replace('run_', 'verify_')}.py"
    verifier = None
    if verify.is_file():
        vproc = subprocess.run([sys.executable, str(verify)], capture_output=True, text=True)
        vline = (vproc.stdout or "").strip().split("\n")[-1] if vproc.stdout else ""
        try:
            verifier = json.loads(vline).get("verifier")
        except json.JSONDecodeError:
            verifier = "parse_error"
    return {
        "script": script,
        "ok": proc.returncode == 0,
        "final_decision": payload.get("final_decision"),
        "pass_flag": payload.get(P0_TCP_PASS_FLAG) or payload.get("slam_task_collaboration_planning_pass"),
        "verifier": verifier,
    }


def run_bootstrap_passes(*, passes: int = 3) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    go_scripts: set[str] = set()
    for pass_idx in range(1, passes + 1):
        for script in BOOTSTRAP_RUN_SCRIPTS:
            row = _run_script(script)
            row["pass"] = pass_idx
            rows.append(row)
            if row.get("verifier") == "GO":
                go_scripts.add(script)
        vis = evaluate_p0_visible_to_scene_graph()
        if vis.get("p0_visible_to_scene_graph_review"):
            break
    return rows, {
        "passes_executed": pass_idx,
        "bootstrap_go_script_count": len(go_scripts),
        "bootstrap_go_scripts": sorted(go_scripts),
        "p0_visibility": evaluate_p0_visible_to_scene_graph(),
    }


def rerun_p0_tcp_only() -> Dict[str, Any]:
    run_row = _run_script("run_slam_spatial_mapping_task_collaboration_planning_v1")
    verify_path = TOOLS / "verify_slam_spatial_mapping_task_collaboration_planning_v1.py"
    verifier = None
    if verify_path.is_file():
        vproc = subprocess.run([sys.executable, str(verify_path)], capture_output=True, text=True)
        vline = (vproc.stdout or "").strip().split("\n")[-1] if vproc.stdout else ""
        try:
            verifier = json.loads(vline).get("verifier")
        except json.JSONDecodeError:
            verifier = "parse_error"
    return {
        "run": run_row,
        "verify_verifier": verifier,
        "p0_visibility": evaluate_p0_visible_to_scene_graph(),
    }
