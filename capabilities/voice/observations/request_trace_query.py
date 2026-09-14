# -*- coding: utf-8 -*-
"""
对已抽取的 RequestTraceChain 列表做结构化过滤（无 DB、无全文检索）。

输入必须是抽链产物，不直接扫原始 observation 文件。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_summary import (
    RequestTraceSummary,
    build_request_trace_summary,
    normalize_chain_type_for_query,
)


def normalize_chain_type_filter(s: str) -> str:
    """CLI 传入的 chain_type 与 summary.chain_type（短名）对齐。"""
    s = s.strip()
    if not s:
        return s
    if s.endswith("_chain"):
        return normalize_chain_type_for_query(s)
    long_map = {
        "success": "success_chain",
        "provider_fallback": "provider_fallback_chain",
        "legacy_rollback": "legacy_rollback_chain",
    }
    if s in long_map:
        return normalize_chain_type_for_query(long_map[s])
    if s in ("failed_chain", "suppressed_chain", "unknown"):
        return normalize_chain_type_for_query(s)
    return s


@dataclass
class TraceQuery:
    request_id: Optional[str] = None
    trace_id: Optional[str] = None
    chain_type: Optional[str] = None
    provider_name: Optional[str] = None
    final_execution_mode: Optional[str] = None
    status: Optional[str] = None
    failure_type: Optional[str] = None
    has_fallback: Optional[bool] = None
    has_rollback: Optional[bool] = None
    start_after: Optional[float] = None
    start_before: Optional[float] = None


def _failure_matches(filter_val: str, summary: RequestTraceSummary, chain: RequestTraceChain) -> bool:
    fv = filter_val.strip().lower()
    if not fv:
        return True
    pet = (summary.primary_error_type or "").lower()
    ft = (summary.failure_type or "").lower()
    if fv == pet or fv == ft:
        return True
    if fv in pet or fv in ft:
        return True
    for e in chain.errors:
        if fv in (e.error_type or "").lower() or fv in (e.error_reason or "").lower():
            return True
    return False


def _status_matches(filter_val: str, summary: RequestTraceSummary, chain: RequestTraceChain) -> bool:
    fv = filter_val.strip().lower()
    if summary.status.lower() == fv:
        return True
    if chain.status.lower() == fv:
        return True
    # 别名
    if fv == "ok" and chain.status == "ok":
        return True
    if fv == "success" and summary.status == "success":
        return True
    return False


def _chain_type_matches(filter_val: str, summary: RequestTraceSummary, chain: RequestTraceChain) -> bool:
    want = normalize_chain_type_filter(filter_val)
    if not want:
        return True
    if summary.chain_type == want:
        return True
    if normalize_chain_type_for_query(chain.chain_type) == want:
        return True
    return False


def _time_in_range(
    started: Optional[float],
    start_after: Optional[float],
    start_before: Optional[float],
) -> bool:
    if started is None:
        return start_after is None and start_before is None
    if start_after is not None and started < start_after:
        return False
    if start_before is not None and started > start_before:
        return False
    return True


def matches_query(chain: RequestTraceChain, summary: RequestTraceSummary, q: TraceQuery) -> bool:
    if q.request_id is not None and chain.request_id != q.request_id:
        return False
    if q.trace_id is not None and chain.trace_id != q.trace_id:
        return False
    if q.chain_type is not None and not _chain_type_matches(q.chain_type, summary, chain):
        return False
    if q.provider_name is not None and (chain.provider_name or "") != q.provider_name:
        return False
    if q.final_execution_mode is not None and chain.final_execution_mode != q.final_execution_mode:
        return False
    if q.status is not None and not _status_matches(q.status, summary, chain):
        return False
    if q.failure_type is not None and not _failure_matches(q.failure_type, summary, chain):
        return False
    if q.has_fallback is not None and summary.has_fallback != q.has_fallback:
        return False
    if q.has_rollback is not None and summary.has_rollback != q.has_rollback:
        return False
    if not _time_in_range(chain.started_at, q.start_after, q.start_before):
        return False
    return True


def filter_chains(chains: List[RequestTraceChain], q: TraceQuery) -> List[RequestTraceChain]:
    out: List[RequestTraceChain] = []
    for c in chains:
        s = build_request_trace_summary(c)
        if matches_query(c, s, q):
            out.append(c)
    return out


def filter_summaries(chains: List[RequestTraceChain], q: TraceQuery) -> List[RequestTraceSummary]:
    return [build_request_trace_summary(c) for c in filter_chains(chains, q)]


def load_chains_from_json_files(paths: List[str]) -> List[RequestTraceChain]:
    """从多个 JSON 文件加载；每文件一个对象，或顶层为 list。"""
    import json
    from pathlib import Path

    chains: List[RequestTraceChain] = []
    for p in paths:
        path = Path(p)
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("request_id"):
                    chains.append(RequestTraceChain.from_dict(item))
        elif isinstance(data, dict) and data.get("request_id"):
            chains.append(RequestTraceChain.from_dict(data))
    return chains


def load_chains_from_directory(dir_path: str, pattern: str = "*.json") -> List[RequestTraceChain]:
    from pathlib import Path

    root = Path(dir_path)
    if not root.is_dir():
        return []
    paths = sorted(root.glob(pattern))
    return load_chains_from_json_files([str(p) for p in paths])


def load_chains_from_archive_directory(archive_dir: str, pattern: str = "*.json") -> List[RequestTraceChain]:
    """
    从归档目录加载抽链产物（只读归档，不扫原始日志）。

    archive_dir 支持两种输入：
    1) 指向某一天目录：.../YYYY-MM-DD/（内部有 chains/）
    2) 指向 voice 根目录：.../whitebox_archive/voice/（内部是多个 YYYY-MM-DD）
    """
    from pathlib import Path

    root = Path(archive_dir)
    if not root.exists():
        return []

    chains_dirs: List[Path] = []
    if (root / "chains").is_dir():
        chains_dirs.append(root / "chains")
    else:
        # 限定在归档目录内部查找 chains 子目录
        for p in sorted(root.rglob("chains")):
            if p.is_dir():
                chains_dirs.append(p)

    all_paths: List[str] = []
    for cd in chains_dirs:
        all_paths.extend([str(p) for p in sorted(cd.glob(pattern))])

    return load_chains_from_json_files(all_paths)
