# -*- coding: utf-8 -*-
"""Local Runner Bridge — job store v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    jobs_store_dir,
    job_output_dir,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_job_id() -> str:
    return f"job_{uuid4().hex[:12]}"


def new_asset_id() -> str:
    return f"asset_{uuid4().hex[:12]}"


def job_path(job_id: str) -> Path:
    return jobs_store_dir() / f"{job_id}.json"


def save_job(job: Dict[str, Any]) -> Path:
    job["updated_at"] = _now()
    path = job_path(job["job_id"])
    path.write_text(json.dumps(job, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out_copy = job_output_dir(job["job_id"]) / "job_record.json"
    out_copy.write_text(json.dumps(job, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def load_job(job_id: str) -> Optional[Dict[str, Any]]:
    path = job_path(job_id)
    if not path.is_file():
        alt = job_output_dir(job_id) / "job_record.json"
        if alt.is_file():
            path = alt
        else:
            return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_job_ids() -> List[str]:
    return sorted(p.stem for p in jobs_store_dir().glob("job_*.json"))


def update_job_status(job_id: str, status: str, status_reason: str, **extra: Any) -> Optional[Dict[str, Any]]:
    job = load_job(job_id)
    if job is None:
        return None
    job["status"] = status
    job["status_reason"] = status_reason
    job.update(extra)
    save_job(job)
    return job
