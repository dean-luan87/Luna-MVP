#!/usr/bin/env python3
"""
Phase-RealSceneReplay-001
Validate a recorded_video_replay archive_root v0.

Hard checks:
- evidence_type=recorded_video_replay
- controlled_live=false
- pending_real_sidewalk_run=true
- input_source=recorded_video
- required_files present
- manifest hashes match (except self-hash is allowed)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional


REQUIRED_RELATIVE_FILES_V0 = [
    "run_evidence.json",
    "trace.jsonl",
    "replay.jsonl",
    "whitebox.jsonl",
    "model_candidate_trace.jsonl",
    "output_candidate_trace.jsonl",
    "operator_notes.md",
    "risk_events.jsonl",
    "post_run_summary.md",
    "archive_manifest.json",
]


def _now_ms() -> int:
    return int(time.time() * 1000)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _exists(path: str) -> bool:
    try:
        return os.path.exists(path)
    except Exception:
        return False


def _validate_archive_root(archive_root: str) -> Dict[str, Any]:
    hard: List[str] = []
    soft: List[str] = []

    missing_files: List[str] = []
    for relp in REQUIRED_RELATIVE_FILES_V0:
        if not _exists(os.path.join(archive_root, relp)):
            missing_files.append(relp)
    if missing_files:
        hard.append("missing_required_files")

    # run_evidence checks
    run_evidence_path = os.path.join(archive_root, "run_evidence.json")
    run_evidence: Optional[Dict[str, Any]] = None
    if _exists(run_evidence_path):
        try:
            run_evidence = _load_json(run_evidence_path)
        except Exception:
            hard.append("run_evidence_unparseable")
    else:
        hard.append("run_evidence_missing")

    if run_evidence is not None:
        if run_evidence.get("evidence_type") != "recorded_video_replay":
            hard.append("evidence_type_not_recorded_video_replay")
        if run_evidence.get("controlled_live") is not False:
            hard.append("controlled_live_not_false")
        if run_evidence.get("pending_real_sidewalk_run") is not True:
            hard.append("pending_real_sidewalk_run_not_true")
        if run_evidence.get("input_source") != "recorded_video":
            hard.append("input_source_not_recorded_video")

        # safety assertions
        if run_evidence.get("no_execute_leakage_assertion") is not True:
            hard.append("no_execute_assertion_failed")
        if run_evidence.get("no_default_on_assertion") is not True:
            hard.append("no_default_on_assertion_failed")
        if run_evidence.get("no_side_effect_expansion_assertion") is not True:
            hard.append("no_side_effect_expansion_assertion_failed")

        # referenced paths must exist
        ref_fields = [
            "trace_file_path",
            "replay_file_path",
            "whitebox_file_path",
            "model_candidate_trace_path",
            "output_candidate_trace_path",
            "operator_notes_path",
            "risk_events_path",
            "archive_manifest_path",
            "post_run_summary_path",
        ]
        for rf in ref_fields:
            p = run_evidence.get(rf)
            if not str(p or "").strip():
                hard.append(f"missing_path_field:{rf}")
                continue
            ap = p if os.path.isabs(p) else os.path.join(archive_root, p)
            if not _exists(ap):
                hard.append(f"referenced_file_missing:{rf}")

    # risk events none_observed requirement (must have at least one line)
    risk_path = os.path.join(archive_root, "risk_events.jsonl")
    if _exists(risk_path):
        try:
            with open(risk_path, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
            if len(lines) == 0:
                hard.append("risk_events_empty_without_none_observed")
        except Exception:
            hard.append("risk_events_unparseable")

    # manifest validation
    manifest_path = os.path.join(archive_root, "archive_manifest.json")
    manifest: Optional[Dict[str, Any]] = None
    if _exists(manifest_path):
        try:
            manifest = _load_json(manifest_path)
        except Exception:
            hard.append("manifest_unparseable")
    else:
        hard.append("manifest_missing")

    hash_mismatches: List[str] = []
    if manifest is not None:
        req = manifest.get("required_files")
        hashes = manifest.get("file_hashes")
        if not isinstance(req, list):
            hard.append("manifest_required_files_missing")
        if not isinstance(hashes, dict):
            hard.append("manifest_file_hashes_missing")
        if isinstance(req, list) and isinstance(hashes, dict):
            for relp in req:
                ap = os.path.join(archive_root, relp)
                if not _exists(ap):
                    continue
                if relp == "archive_manifest.json":
                    continue
                actual = _sha256_file(ap)
                expected = hashes.get(relp)
                if expected is None:
                    hard.append("manifest_hash_missing_for_file")
                elif str(expected) != str(actual):
                    hash_mismatches.append(relp)
        if hash_mismatches:
            hard.append("manifest_hash_mismatch")

        if manifest.get("integrity_status") != "pass":
            soft.append("integrity_status_not_pass")

    rec = "no_go" if hard else ("conditional_go" if soft else "go")
    return {
        "recommendation": rec,
        "hard_blockers": hard,
        "soft_followups": soft,
        "details": {
            "archive_root": archive_root,
            "missing_files": missing_files,
            "hash_mismatches": hash_mismatches,
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive_root", required=True)
    args = ap.parse_args()
    out = _validate_archive_root(args.archive_root)
    report = {
        "tool": "validate_recorded_sidewalk_video_archive_v0",
        "phase": "Phase-RealSceneReplay-001",
        "generated_at_ms": _now_ms(),
        "mode": "single_archive_validate",
        "result": out,
        "assertions": {
            "default_path_enabled": False,
            "full_controlled_trial_entered": False,
            "real_side_effects_expanded": False,
            "open_user_testing": False,
            "scope_expanded": False,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

