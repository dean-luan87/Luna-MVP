from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Tuple

from .types_v1 import EvaluationRunRecordV1, validate_evaluation_run_record_v1


DEFAULT_ARCHIVE_ROOT = Path("evaluation_archive/level1_cognitive_runs")
_SAFE_NAME = re.compile(r"[^A-Za-z0-9_.-]+")


class ArchiveConflictError(ValueError):
    """Raised when an existing identity would be silently overwritten."""


def archive_path_for_run_v1(run_id: str, archive_root: Path = DEFAULT_ARCHIVE_ROOT) -> Path:
    safe_id = _SAFE_NAME.sub("_", run_id).strip("_") or "invalid-run-id"
    return archive_root / f"{safe_id}.json"


def write_evaluation_run_record_v1(
    record: EvaluationRunRecordV1,
    *,
    archive_root: Path = DEFAULT_ARCHIVE_ROOT,
) -> Tuple[Path, bool]:
    errors = validate_evaluation_run_record_v1(record)
    if errors:
        raise ValueError("invalid_evaluation_run_record:" + ",".join(errors))
    path = archive_path_for_run_v1(record.evaluation_run.evaluation_run_id, archive_root)
    payload = asdict(record)
    encoded = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing != encoded:
            raise ArchiveConflictError(f"immutable_archive_identity_conflict:{path}")
        return path, False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoded, encoding="utf-8")
    return path, True


def read_evaluation_run_record_v1(path: Path) -> EvaluationRunRecordV1:
    from .types_v1 import EvaluationAvailabilityV1, EvaluationRunCandidateV1

    payload = json.loads(path.read_text(encoding="utf-8"))
    raw = payload["evaluation_run"]

    def availability(value: dict) -> EvaluationAvailabilityV1:
        return EvaluationAvailabilityV1(
            value=value.get("value"),
            availability=value.get("availability", "unavailable"),
            source_refs=tuple(value.get("source_refs") or ()),
            notes=value.get("notes", ""),
        )

    run = EvaluationRunCandidateV1(
        **{
            key: (
                availability(value)
                if key in {
                    "luna_code_version_ref",
                    "luna_config_version_ref",
                    "started_at",
                    "completed_at",
                    "comparison_eligibility",
                    "runtime_metrics",
                }
                else tuple(value) if key.endswith("_refs") else value
            )
            for key, value in raw.items()
            if key not in {"synthetic", "evaluation_only"}
        },
        synthetic=raw.get("synthetic", True),
        evaluation_only=raw.get("evaluation_only", True),
    )
    record = EvaluationRunRecordV1(
        record_id=payload["record_id"],
        record_version=payload["record_version"],
        evaluation_run=run,
        archive_owner_ref=payload.get("archive_owner_ref", "Evaluation Governance"),
        immutable_by_identity=payload.get("immutable_by_identity", True),
        append_or_supersede_only=payload.get("append_or_supersede_only", True),
        world_truth=payload.get("world_truth", False),
        runtime_state=payload.get("runtime_state", False),
        memory=payload.get("memory", False),
        experience=payload.get("experience", False),
        knowledge=payload.get("knowledge", False),
        test_board_refs=tuple(payload.get("test_board_refs") or ()),
        bounded_metadata=payload.get("bounded_metadata") or {},
    )
    errors = validate_evaluation_run_record_v1(record)
    if errors:
        raise ValueError("invalid_archived_evaluation_run_record:" + ",".join(errors))
    return record

