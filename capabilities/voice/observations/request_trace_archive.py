# -*- coding: utf-8 -*-
"""
RequestTraceChain / Summary / Issue / Diagnostic 的本地归档写入器（最小实现）。

约定目录结构（推荐）：
whitebox_archive/
  voice/
    YYYY-MM-DD/
      chains/
      summaries/
      issues/
      diagnostics/
      manifests/

本模块只做：
- 写入本地文件
- 更新最小 manifest
- 保留策略占位（archive_tier）
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from capabilities.voice.observations.request_trace_archive_manifest import (
    RequestTraceArchiveManifest,
    compute_archive_tier,
)
from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_diagnostic_summary import (
    RequestTraceDiagnosticSummary,
)
from capabilities.voice.observations.request_trace_issue import RequestTraceIssue
from capabilities.voice.observations.request_trace_summary import (
    RequestTraceSummary,
    build_request_trace_summary,
)


def default_archive_root() -> Path:
    # 放在 workspace 下，便于本地常备与复制
    return Path(__file__).resolve().parents[3] / "whitebox_archive"


def _safe_id(s: str) -> str:
    return str(s).replace("/", "_").replace("\\", "_").replace(" ", "_")


def make_chain_id(chain: RequestTraceChain) -> str:
    trace = chain.trace_id or "no_trace"
    return f"{_safe_id(chain.request_id)}__{_safe_id(trace)}"


def _parse_date_str(archive_date: Optional[str]) -> str:
    if archive_date:
        return archive_date
    return str(date.today())


def _load_manifest(manifest_path: Path) -> Optional[RequestTraceArchiveManifest]:
    if not manifest_path.is_file():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return RequestTraceArchiveManifest.from_dict(data)
    except (OSError, json.JSONDecodeError):
        return None
    return None


def _save_manifest(manifest_path: Path, manifest: RequestTraceArchiveManifest) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )


@dataclass
class ArchiveWriteResult:
    chain_id: str
    archive_date: str
    chain_path: str
    summary_path: str
    issue_path: Optional[str] = None
    diagnostic_path: Optional[str] = None
    manifest_path: str = ""


def archive_request_trace(
    *,
    chain: RequestTraceChain,
    issue: Optional[RequestTraceIssue] = None,
    diagnostic: Optional[RequestTraceDiagnosticSummary] = None,
    archive_root: Optional[Path] = None,
    archive_date: Optional[str] = None,
) -> ArchiveWriteResult:
    archive_root = archive_root or default_archive_root()
    archive_date_n = _parse_date_str(archive_date)

    day_dir = archive_root / "voice" / archive_date_n
    chains_dir = day_dir / "chains"
    summaries_dir = day_dir / "summaries"
    issues_dir = day_dir / "issues"
    diagnostics_dir = day_dir / "diagnostics"
    manifests_dir = day_dir / "manifests"
    manifest_path = manifests_dir / "manifest.json"

    chain_id = make_chain_id(chain)

    # summary：尽量避免回退到 analyzer 重跑，本轮只做最小推断摘要落盘
    summary: RequestTraceSummary = build_request_trace_summary(chain)

    chains_dir.mkdir(parents=True, exist_ok=True)
    summaries_dir.mkdir(parents=True, exist_ok=True)
    if issue:
        issues_dir.mkdir(parents=True, exist_ok=True)
    if diagnostic:
        diagnostics_dir.mkdir(parents=True, exist_ok=True)

    chain_path = chains_dir / f"{chain_id}.json"
    summary_path = summaries_dir / f"{chain_id}.json"
    issue_path: Optional[Path] = issues_dir / f"{chain_id}.json" if issue else None
    diagnostic_path: Optional[Path] = diagnostics_dir / f"{chain_id}.json" if diagnostic else None

    chain_path.write_text(json.dumps(chain.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    summary_path.write_text(
        json.dumps(summary.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if issue and issue_path:
        issue_path.write_text(json.dumps(issue.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    if diagnostic and diagnostic_path:
        diagnostic_path.write_text(
            json.dumps(diagnostic.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # 更新 manifest（去重写入）
    manifest = _load_manifest(manifest_path)
    if manifest is None:
        manifest = RequestTraceArchiveManifest(date=archive_date_n)
        manifest.created_at = manifest.created_at or None
        manifest.updated_at = None

    # 更新时间与 tier 计算（每次写入都重新算，避免长时间运行漂移）
    from time import time as _time

    manifest.updated_at = _time()
    manifest.archive_tier = compute_archive_tier(day=archive_date_n)

    if chain_id not in manifest.chain_ids:
        manifest.chain_ids.append(chain_id)
        manifest.total_chain_count = len(manifest.chain_ids)

        provider = chain.provider_name or "unknown_provider"
        manifest.provider_counts[provider] = int(manifest.provider_counts.get(provider) or 0) + 1

        # issue_type_counts：优先从 issue；缺失则使用 summary.primary_error_type
        it = issue.primary_issue_type if issue else (summary.primary_error_type or "unknown_failure")
        it = it or "unknown_failure"
        manifest.issue_type_counts[it] = int(manifest.issue_type_counts.get(it) or 0) + 1

        if summary.has_rollback:
            manifest.rollback_count = int(manifest.rollback_count) + 1
        if summary.has_fallback:
            manifest.fallback_count = int(manifest.fallback_count) + 1

    _save_manifest(manifest_path, manifest)

    return ArchiveWriteResult(
        chain_id=chain_id,
        archive_date=archive_date_n,
        chain_path=str(chain_path),
        summary_path=str(summary_path),
        issue_path=str(issue_path) if issue_path else None,
        diagnostic_path=str(diagnostic_path) if diagnostic_path else None,
        manifest_path=str(manifest_path),
    )


def load_issue_from_dict(d: Dict[str, Any]) -> RequestTraceIssue:
    return RequestTraceIssue(
        request_id=str(d.get("request_id", "")),
        trace_id=d.get("trace_id"),
        chain_type=str(d.get("chain_type", "")),
        provider_name=d.get("provider_name"),
        final_execution_mode=d.get("final_execution_mode"),
        final_status=str(d.get("final_status", "")),
        primary_issue_type=str(d.get("primary_issue_type", "")),
        primary_issue_reason=str(d.get("primary_issue_reason", "")),
        secondary_issue_type=d.get("secondary_issue_type"),
        secondary_issue_reason=d.get("secondary_issue_reason"),
        failed_stage=d.get("failed_stage"),
        severity=str(d.get("severity") or "info"),
        has_fallback=bool(d.get("has_fallback", False)),
        has_rollback=bool(d.get("has_rollback", False)),
        recommended_checkpoints=list(d.get("recommended_checkpoints") or []),
        notes=list(d.get("notes") or []),
    )


def load_diagnostic_from_dict(d: Dict[str, Any]) -> RequestTraceDiagnosticSummary:
    return RequestTraceDiagnosticSummary(
        request_id=str(d.get("request_id", "")),
        chain_type=str(d.get("chain_type") or ""),
        provider_name=d.get("provider_name"),
        final_execution_mode=d.get("final_execution_mode"),
        final_status=str(d.get("final_status") or ""),
        primary_issue_type=str(d.get("primary_issue_type") or ""),
        primary_issue_reason=str(d.get("primary_issue_reason") or ""),
        failed_stage=d.get("failed_stage"),
        severity=str(d.get("severity") or ""),
        summary_text=str(d.get("summary_text") or ""),
        recommended_checkpoints=list(d.get("recommended_checkpoints") or []),
    )

