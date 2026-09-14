"""Read-only import preflight and session baseline for full regression.

The import portion only imports canonical modules.  It does not call a
runner, verifier, cognition engine, provider, model, observation, action, or
archive writer.  When requested, the baseline portion records observable file
metadata so the later audit can distinguish artifacts produced by the
current terminal session from pre-existing history.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Sequence
from uuid import uuid4


IMPORT_TARGETS = (
    "capabilities.midplatform.core.execution_mode_v1",
    "capabilities.midplatform.core.observation_gateway",
    "capabilities.midplatform.core.a_route_orchestration",
    "capabilities.midplatform.core.cognitive_state_formation",
    "capabilities.evaluation.a_route_cognitive_whitebox_foundation",
    "capabilities.evaluation.level1_cognitive_evaluation_run",
    "capabilities.evaluation.level1_cognitive_evaluation_run.archive_v1",
    "capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1",
    "capabilities.evaluation.level1_cognitive_evaluation_run.audit_full_regression_v1",
)

TRACKED_OUTPUTS = (
    "capabilities/evaluation/dataset_registry/registry_declaration_v1.json",
    "_eval_out/level1_cognitive_evaluation_run_boundary_v1/runner_summary_v1.json",
    "_eval_out/a_route_perception_observation_gateway_controlled_integration_v1/observation_gateway_result_v1.json",
    "_eval_out/cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_result_v1.json",
    "_eval_out/a_route_controlled_replay_runtime_enablement_v1/runner_summary_v1.json",
    "_eval_out/a_route_cognitive_whitebox_trace_and_execution_profile_foundation_v1/synthetic_cognitive_whitebox_runner_v1.json",
    "_eval_out/level1_replay_evaluation_whitebox_archive_governance_integration_v1/runner_summary_v1.json",
    "_eval_out/level1_minimum_sufficient_cognition_loop_controlled_replay_v1/runner_summary_v1.json",
)
ARCHIVE_ROOT = Path("evaluation_archive/level1_cognitive_runs")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tracked_files(repository_root: Path) -> Iterable[Path]:
    for relative in TRACKED_OUTPUTS:
        path = repository_root / relative
        if path.is_file():
            yield path
    archive_root = repository_root / ARCHIVE_ROOT
    if archive_root.is_dir():
        yield from sorted(path for path in archive_root.glob("*.json") if path.is_file())


def _baseline(repository_root: Path) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for path in _tracked_files(repository_root):
        relative = str(path.relative_to(repository_root))
        stat = path.stat()
        result[relative] = {
            "sha256": _sha256(path),
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }
    return result


def build_preflight_result_v1(repository_root: Path) -> Dict[str, Any]:
    imported = []
    errors = []
    for module_name in IMPORT_TARGETS:
        try:
            importlib.import_module(module_name)
            imported.append(module_name)
        except Exception as exc:  # pragma: no cover - exercised by user terminal
            errors.append({
                "module": module_name,
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
    return {
        "status": "IMPORTS_PASS" if not errors else "IMPORTS_FAIL",
        "repository_root": str(repository_root),
        "import_targets": list(IMPORT_TARGETS),
        "imported_modules": imported,
        "import_errors": errors,
    }


def write_session_manifest_v1(repository_root: Path, path: Path) -> Dict[str, Any]:
    path = path if path.is_absolute() else repository_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "full-regression-session-manifest-v1",
        "session_id": "full-regression-session:" + uuid4().hex,
        "repository_root": str(repository_root),
        "tracked_output_paths": list(TRACKED_OUTPUTS),
        "archive_root": str(ARCHIVE_ROOT),
        "baseline_files": _baseline(repository_root),
        "timestamp": None,
        "timestamp_availability": "unavailable",
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return {"session_manifest": str(path), "session_id": payload["session_id"], "baseline_file_count": len(payload["baseline_files"])}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import-only full-regression preflight")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--session-manifest", type=Path)
    args = parser.parse_args(argv)
    repository_root = args.repo_root.resolve()
    result = build_preflight_result_v1(repository_root)
    if result["status"] == "IMPORTS_PASS" and args.session_manifest:
        result.update(write_session_manifest_v1(repository_root, args.session_manifest))
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "IMPORTS_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
