#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-RuntimeReadiness-006 — Read-only regression & closure summary for RuntimeReadiness 001–005.

Does not connect runtime, providers, or expand whitebox productization.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

PHASE = "Phase-Mainline-RuntimeReadiness-006"

DEFAULT_ROOTS: Dict[str, str] = {
    "001": "logs/mainline_runtime_readiness_001_20260506_final",
    "002": "logs/mainline_guarded_trial_definition_002_20260506_final",
    "003": "logs/mainline_guarded_trial_wiring_path_003_final",
    "004": "logs/mainline_guarded_trial_hook_in_004_final",
}

STAGE_NAME = "request_trace.stage.runtime_readiness.guarded_trial_hook"
STAGE_NS = "mainline_runtime_readiness_v0"

REQUIRED_REPO_MODULES_003 = [
    "capabilities/runtime_readiness/guarded_trial_gate_v0.py",
    "capabilities/runtime_readiness/guarded_trial_trw_validator_v0.py",
    "capabilities/runtime_readiness/guarded_trial_abort_rollback_hooks_v0.py",
]

REQUIRED_HOOK_WRAPPERS = [
    "capabilities/runtime_readiness/yolo_guarded_trial_hook_v0.py",
    "capabilities/runtime_readiness/ocr_guarded_trial_hook_v0.py",
    "capabilities/runtime_readiness/qwen_voice_guarded_trial_hook_v0.py",
]


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _repo(rel: str) -> Path:
    return Path(REPO_ROOT) / rel


def _resolve_root(repo: Path, rel: Optional[str]) -> Optional[Path]:
    if not rel:
        return None
    p = Path(rel)
    if not p.is_absolute():
        p = (repo / p).resolve()
    return p if p.is_dir() else None


def _glob_latest_005(repo: Path) -> Optional[Path]:
    globs = list(repo.glob("logs/mainline_guarded_trial_hook_observability_005_*"))
    if not globs:
        return None
    return max(globs, key=lambda p: p.stat().st_mtime)


def _phase001_files(root: Path) -> Dict[str, bool]:
    keys = {
        "mainline_runtime_readiness_summary.json": (root / "mainline_runtime_readiness_summary.json").is_file(),
    }
    return keys


def _phase002_files(root: Path) -> Dict[str, bool]:
    return {
        "mainline_guarded_trial_summary.json": (root / "mainline_guarded_trial_summary.json").is_file(),
        "mainline_guarded_trial_matrix.json": (root / "mainline_guarded_trial_matrix.json").is_file(),
    }


def _phase003_files(root: Path) -> Dict[str, bool]:
    return {
        "mainline_guarded_trial_wiring_summary.json": (root / "mainline_guarded_trial_wiring_summary.json").is_file(),
    }


def _phase004_files(root: Path) -> Dict[str, bool]:
    return {
        "mainline_guarded_trial_hook_in_summary.json": (root / "mainline_guarded_trial_hook_in_summary.json").is_file(),
        "mainline_guarded_trial_hook_results.json": (root / "mainline_guarded_trial_hook_results.json").is_file(),
    }


def _phase005_files(root: Path) -> Dict[str, bool]:
    return {
        "mainline_guarded_trial_hook_observability_summary.json": (
            root / "mainline_guarded_trial_hook_observability_summary.json"
        ).is_file(),
        "mainline_guarded_trial_hook_request_trace_stages.json": (
            root / "mainline_guarded_trial_hook_request_trace_stages.json"
        ).is_file(),
        "mainline_guarded_trial_hook_observability_matrix.json": (
            root / "mainline_guarded_trial_hook_observability_matrix.json"
        ).is_file(),
    }


def _extract_trials_from_004(hook_results_path: Path) -> Tuple[List[str], List[str], Dict[str, Any]]:
    """Returns (capabilities seen in default_env, trial_names, aggregate flags)."""
    caps: List[str] = []
    trials: List[str] = []
    blob = _load_json(hook_results_path)
    meta = {
        "default_env_all_enabled_false": True,
        "default_env_all_no_op_true": True,
        "default_env_side_effect_ok": True,
        "default_env_rows_seen": 0,
        "has_default_env_data": False,
        "all_runtime_invoked_false": True,
        "all_provider_invoked_false": True,
        "all_playback_invoked_false": True,
        "all_world_write_invoked_false": True,
        "all_navigation_action_null": True,
    }
    if not isinstance(blob, list):
        return caps, trials, meta
    for row in blob:
        if not isinstance(row, dict) or row.get("scenario") != "default_env":
            continue
        hr = row.get("hook_result")
        if not isinstance(hr, dict):
            continue
        cap = str(hr.get("capability") or "")
        if cap:
            caps.append(cap)
        tn = str(hr.get("trial_name") or "")
        if tn:
            trials.append(tn)
        if hr.get("enabled") is not False:
            meta["default_env_all_enabled_false"] = False
        if hr.get("no_op") is not True:
            meta["default_env_all_no_op_true"] = False
        if hr.get("provider_invoked") is True or hr.get("playback_invoked") is True:
            meta["default_env_side_effect_ok"] = False
        if int(hr.get("downstream_invocation_count") or 0) != 0:
            meta["default_env_side_effect_ok"] = False
        if hr.get("world_write_invoked") is True:
            meta["default_env_side_effect_ok"] = False
        if hr.get("navigation_action") is not None:
            meta["default_env_side_effect_ok"] = False
        meta["default_env_rows_seen"] = meta.get("default_env_rows_seen", 0) + 1
        if hr.get("runtime_invoked") is True:
            meta["default_env_side_effect_ok"] = False
        if hr.get("runtime_invoked") is not False:
            meta["all_runtime_invoked_false"] = False
        if hr.get("provider_invoked") is not False:
            meta["all_provider_invoked_false"] = False
        if hr.get("playback_invoked") is not False:
            meta["all_playback_invoked_false"] = False
        if hr.get("world_write_invoked") is not False:
            meta["all_world_write_invoked_false"] = False
        if hr.get("navigation_action") is not None:
            meta["all_navigation_action_null"] = False
    meta["has_default_env_data"] = meta.get("default_env_rows_seen", 0) > 0
    return caps, trials, meta


def _extract_005_observability(root: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "stage_name_present": False,
        "stage_namespace_ok": False,
        "trials_in_stages": [],
        "side_effect_ok_all": None,
        "summary_verdict": None,
    }
    stages_path = root / "mainline_guarded_trial_hook_request_trace_stages.json"
    summ_path = root / "mainline_guarded_trial_hook_observability_summary.json"
    audit_path = root / "mainline_guarded_trial_hook_side_effect_audit_export.json"
    if summ_path.is_file():
        s = _load_json(summ_path)
        out["summary_verdict"] = (s or {}).get("verdict")
    if stages_path.is_file():
        stages = _load_json(stages_path)
        if isinstance(stages, list) and stages:
            out["stage_name_present"] = all(
                isinstance(x, dict) and x.get("stage_name") == STAGE_NAME for x in stages
            )
            out["stage_namespace_ok"] = all(
                isinstance(x, dict) and x.get("stage_namespace") == STAGE_NS for x in stages
            )
            out["trials_in_stages"] = [x.get("trial_name") for x in stages if isinstance(x, dict)]
    if audit_path.is_file():
        au = _load_json(audit_path)
        if isinstance(au, list):
            out["side_effect_ok_all"] = all(x.get("side_effect_ok") is True for x in au if isinstance(x, dict))
    return out


def _global_kill_from_002(root: Optional[Path]) -> Dict[str, Any]:
    out = {"represented": False, "flag_name": "LUNA_DISABLE_ALL_GUARDED_TRIALS", "source": None}
    if root is None or not root.is_dir():
        return out
    env_path = root / "mainline_guarded_trial_env_flag_matrix.json"
    summ_path = root / "mainline_guarded_trial_summary.json"
    if env_path.is_file():
        out["represented"] = True
        out["source"] = str(env_path)
        try:
            data = _load_json(env_path)
            out["matrix_has_kill_switch_entry"] = json.dumps(data, ensure_ascii=False).find(
                "LUNA_DISABLE_ALL_GUARDED_TRIALS"
            ) >= 0
        except Exception:
            out["matrix_has_kill_switch_entry"] = False
    elif summ_path.is_file():
        txt = summ_path.read_text(encoding="utf-8")
        out["represented"] = "LUNA_DISABLE_ALL_GUARDED_TRIALS" in txt
        out["source"] = str(summ_path)
    return out


def _repo_anchor_checks(repo: Path) -> Dict[str, Any]:
    mods = {m: (_repo(m).is_file()) for m in REQUIRED_REPO_MODULES_003}
    hooks = {h: (_repo(h).is_file()) for h in REQUIRED_HOOK_WRAPPERS}
    docs = {
        "LUNA_MAINLINE_RUNTIME_READINESS_REVIEW_V0.md": _repo(
            "docs/architecture/LUNA_MAINLINE_RUNTIME_READINESS_REVIEW_V0.md"
        ).is_file(),
    }
    return {"gate_modules_present": mods, "hook_wrappers_present": hooks, "phase001_doc_present": docs["LUNA_MAINLINE_RUNTIME_READINESS_REVIEW_V0.md"]}


def _compute_verdict(
    *,
    missing_roots: List[str],
    phase_files: Dict[str, Dict[str, bool]],
    caps_default: List[str],
    meta_004: Dict[str, Any],
    obs_005: Dict[str, Any],
    kill_002: Dict[str, Any],
    anchor: Dict[str, Any],
    r005_present: bool,
) -> Tuple[str, List[str]]:
    notes: List[str] = []
    need_caps = {"yolo", "ocr", "qwen_voice"}
    have_caps = set(caps_default)
    trials_005 = obs_005.get("trials_in_stages") or []
    trials_set = set(trials_005) if trials_005 else set()
    expected_trials = {
        "yolo_guarded_trial_v1",
        "ocr_guarded_trial_v1",
        "qwen_voice_governed_entry_trial_v1",
    }

    # Hard NO_GO: populated default_env violates invariants
    if meta_004.get("has_default_env_data"):
        if meta_004.get("default_env_all_enabled_false") is False:
            return "NO_GO", ["default_env has enabled!=false"]
        if meta_004.get("default_env_all_no_op_true") is False:
            return "NO_GO", ["default_env has no_op!=true"]
        if meta_004.get("default_env_side_effect_ok") is False:
            return "NO_GO", ["004 default_env side-effect invariant failed"]

    # Hard NO_GO: 005 audit reports failed side effects
    if obs_005.get("side_effect_ok_all") is False:
        return "NO_GO", ["005 side_effect_ok not all true"]

    # Hard NO_GO: stages file present but schema mismatch
    if phase_files.get("005", {}).get("mainline_guarded_trial_hook_request_trace_stages.json"):
        if not obs_005.get("stage_name_present") or not obs_005.get("stage_namespace_ok"):
            return "NO_GO", ["005 RequestTrace stage schema mismatch"]

    three_ok = need_caps.issubset(have_caps) or expected_trials.issubset(trials_set)
    if not three_ok:
        if meta_004.get("has_default_env_data") or r005_present:
            return "NO_GO", ["expected three guarded trials not confirmed from 004/005"]
        notes.append("three-trial evidence unavailable (repo-only); see capability_matrix")

    if not kill_002.get("represented"):
        gate_py = _repo("capabilities/runtime_readiness/guarded_trial_gate_v0.py")
        if gate_py.is_file() and "LUNA_DISABLE_ALL_GUARDED_TRIALS" in gate_py.read_text(encoding="utf-8"):
            notes.append("global kill switch represented via repo gate module (002 log root optional)")
        else:
            return "NO_GO", ["global kill switch not represented in logs or gate module"]

    if missing_roots:
        notes.append(f"missing_roots={missing_roots}")
        return "CONDITIONAL_GO", notes

    if not three_ok:
        return "CONDITIONAL_GO", notes

    return "GO", notes


def run_regression(
    *,
    repo: Path,
    out_root: Path,
    root_001: Optional[str],
    root_002: Optional[str],
    root_003: Optional[str],
    root_004: Optional[str],
    root_005: Optional[str],
) -> Dict[str, Any]:
    r001 = _resolve_root(repo, root_001)
    r002 = _resolve_root(repo, root_002)
    r003 = _resolve_root(repo, root_003)
    r004 = _resolve_root(repo, root_004)
    r005 = _resolve_root(repo, root_005) if root_005 else _glob_latest_005(repo)

    roots_map = {"001": r001, "002": r002, "003": r003, "004": r004, "005": r005}
    missing_roots = [k for k, v in roots_map.items() if v is None]

    phase_files: Dict[str, Dict[str, bool]] = {}
    if r001:
        phase_files["001"] = _phase001_files(r001)
    if r002:
        phase_files["002"] = _phase002_files(r002)
    if r003:
        phase_files["003"] = _phase003_files(r003)
    if r004:
        phase_files["004"] = _phase004_files(r004)
    if r005:
        phase_files["005"] = _phase005_files(r005)

    caps: List[str] = []
    trials_004: List[str] = []
    meta_004: Dict[str, Any] = {
        "has_default_env_data": False,
        "default_env_all_enabled_false": True,
        "default_env_all_no_op_true": True,
        "default_env_side_effect_ok": True,
    }
    if r004 and (r004 / "mainline_guarded_trial_hook_results.json").is_file():
        caps, trials_004, meta_004 = _extract_trials_from_004(r004 / "mainline_guarded_trial_hook_results.json")

    obs_005 = _extract_005_observability(r005) if r005 else {}
    kill_002 = _global_kill_from_002(r002)
    anchor = _repo_anchor_checks(repo)

    verdict, verdict_notes = _compute_verdict(
        missing_roots=missing_roots,
        phase_files=phase_files,
        caps_default=caps,
        meta_004=meta_004,
        obs_005=obs_005,
        kill_002=kill_002,
        anchor=anchor,
        r005_present=bool(r005),
    )

    # Phase matrix rows
    phase_matrix: List[Dict[str, Any]] = []
    for pid, label in [
        ("001", "Runtime Readiness Review"),
        ("002", "Guarded Trial Definition"),
        ("003", "Wiring Path Mapping / Gate modules"),
        ("004", "Hook-In default no-op"),
        ("005", "Hook Observability / RequestTrace alignment"),
    ]:
        rp = roots_map.get(pid)
        pf = phase_files.get(pid, {})
        represented = bool(rp and pf and any(pf.values()))
        if pid == "003" and not represented:
            represented = all(anchor["gate_modules_present"].values())
        if pid == "001" and not represented:
            represented = bool(anchor.get("phase001_doc_present"))
        phase_matrix.append(
            {
                "phase_id": f"Phase-Mainline-RuntimeReadiness-{pid}",
                "label": label,
                "root_resolved": str(rp) if rp else None,
                "artifacts_present": pf,
                "represented": represented,
            }
        )

    capability_matrix: List[Dict[str, Any]] = []
    for cap, tn in [
        ("yolo", "yolo_guarded_trial_v1"),
        ("ocr", "ocr_guarded_trial_v1"),
        ("qwen_voice", "qwen_voice_governed_entry_trial_v1"),
    ]:
        hook_path = (
            "capabilities/runtime_readiness/qwen_voice_guarded_trial_hook_v0.py"
            if cap == "qwen_voice"
            else f"capabilities/runtime_readiness/{cap}_guarded_trial_hook_v0.py"
        )
        capability_matrix.append(
            {
                "capability": cap,
                "trial_name": tn,
                "definition_002": bool(r002 and (r002 / "mainline_guarded_trial_summary.json").is_file()),
                "gate_module_003": all(anchor["gate_modules_present"].values()),
                "hook_wrapper_in_repo": anchor["hook_wrappers_present"].get(hook_path, False),
                "hook_result_default_env_004": cap in caps,
                "observability_stage_005": tn in (obs_005.get("trials_in_stages") or []),
            }
        )

    gate_hook_matrix = {
        "global_kill_switch": kill_002,
        "default_env_from_004": {
            "capabilities": caps,
            "trial_names": trials_004,
            "meta": meta_004,
        },
        "default_env_invariants": {
            "all_enabled_false": bool(meta_004.get("default_env_all_enabled_false")),
            "all_no_op_true": bool(meta_004.get("default_env_all_no_op_true")),
            "all_side_effect_clear": bool(meta_004.get("default_env_side_effect_ok")),
            "has_default_env_data": bool(meta_004.get("has_default_env_data")),
            "all_runtime_invoked_false": bool(meta_004.get("all_runtime_invoked_false", True)),
            "all_provider_invoked_false": bool(meta_004.get("all_provider_invoked_false", True)),
            "all_playback_invoked_false": bool(meta_004.get("all_playback_invoked_false", True)),
            "all_world_write_invoked_false": bool(meta_004.get("all_world_write_invoked_false", True)),
            "all_navigation_action_null": bool(meta_004.get("all_navigation_action_null", True)),
        },
        "request_trace_from_005": {
            "stage_name": STAGE_NAME,
            "stage_namespace": STAGE_NS,
            "trials_in_stages": obs_005.get("trials_in_stages"),
            "summary_verdict": obs_005.get("summary_verdict"),
            "stage_schema_ok": bool(obs_005.get("stage_name_present") and obs_005.get("stage_namespace_ok")),
        },
    }

    observability_minimal = {
        "whitebox_scope": "minimal_observability_only",
        "allows": [
            "RequestTrace shadow stage visible (005)",
            "side-effect audit export",
            "reason / no_op / global kill visibility",
            "non-empty trace/replay/whitebox jsonl (004/005 tooling)",
        ],
        "forbids_next_in_this_closure": [
            "whitebox backend product",
            "whitebox UI",
            "complex query system",
            "field dictionary expansion",
        ],
        "future_phase": "Phase-Whitebox-Observability-001 System Whitebox Consolidation v0 (not started)",
    }

    boundary_summary = {
        "runtime_readiness_status": "closed_v0",
        "scope": "guarded_trial_readiness_layer",
        "real_runtime_activation_allowed": False,
        "real_qwen_invocation_allowed": False,
        "real_tts_invocation_allowed": False,
        "real_playback_allowed": False,
        "default_trial_enabled": False,
        "global_kill_switch_required": True,
        "whitebox_scope": "minimal_observability_only",
        "meaning": [
            "R2–R3 prerequisite definitions, gate, hook, observability closure complete",
            "Next phases may discuss controlled trial execution — not in this phase",
            "Does not mean production runtime, provider, or playback are enabled",
        ],
    }

    closure_recommendation = {
        "phase": PHASE,
        "runtime_readiness_status": "closed_v0",
        "verdict": {
            "mainline_runtime_readiness_closure": verdict,
            "real_runtime_activation": "NO_GO",
            "whitebox_productization": "NO_GO",
        },
        "verdict_notes": verdict_notes,
        "missing_roots": missing_roots,
        "anchors": anchor,
        "next_recommended_phase": "Controlled guarded trial execution planning (separate phase; not auto-enabled)",
    }

    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo.resolve()),
        "runtime_readiness_status": "closed_v0",
        "missing_roots": missing_roots,
        "phase_roots": {k: str(v) if v else None for k, v in roots_map.items()},
        "verdict": closure_recommendation["verdict"],
        "verdict_notes": verdict_notes,
        "boundary_summary": boundary_summary,
        "inputs_note": "Historical output roots may be absent; see missing_roots and repo anchors.",
    }

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "mainline_runtime_readiness_regression_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_readiness_phase_matrix.json").write_text(
        json.dumps(phase_matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_readiness_capability_matrix.json").write_text(
        json.dumps(capability_matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_readiness_gate_hook_matrix.json").write_text(
        json.dumps(gate_hook_matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_readiness_observability_matrix.json").write_text(
        json.dumps(observability_minimal, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_readiness_boundary_summary.json").write_text(
        json.dumps(boundary_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_readiness_closure_recommendation.json").write_text(
        json.dumps(closure_recommendation, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    notes = [
        f"# {PHASE} — regression notes",
        "",
        f"- output_root: `{out_root}`",
        f"- missing_roots: {missing_roots}",
        f"- closure verdict: {verdict}",
        "",
        "Read-only aggregation; no runtime, no provider, no whitebox UI/backend.",
        "",
    ]
    (out_root / "regression_notes.md").write_text("\n".join(notes), encoding="utf-8")

    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="")
    ap.add_argument("--root-001", default=DEFAULT_ROOTS["001"])
    ap.add_argument("--root-002", default=DEFAULT_ROOTS["002"])
    ap.add_argument("--root-003", default=DEFAULT_ROOTS["003"])
    ap.add_argument("--root-004", default=DEFAULT_ROOTS["004"])
    ap.add_argument("--root-005", default="", help="Optional explicit 005 root; default: latest logs/mainline_guarded_trial_hook_observability_005_*")
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"mainline_runtime_readiness_regression_006_{_utc_tag()}"
    r005 = args.root_005.strip() or None

    summary = run_regression(
        repo=repo,
        out_root=out,
        root_001=args.root_001 or None,
        root_002=args.root_002 or None,
        root_003=args.root_003 or None,
        root_004=args.root_004 or None,
        root_005=r005,
    )
    print(json.dumps({"ok": True, "output_root": str(out), "verdict": summary.get("verdict")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
