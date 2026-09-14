# -*- coding: utf-8 -*-
"""
RequestTraceChain 归档的最小 manifest / 索引对象（无服务化、无数据库）。

每一天一个 manifest：
- 统计当天归档的链数量
- provider 分布
- issue_type 分布（优先从 archived issue；缺失则退化到链上推断的错误类型）
- fallback / rollback 次数
- archive_tier：hot / pending_backup（T+1 备份占位）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional


@dataclass
class RequestTraceArchiveManifest:
    date: str  # YYYY-MM-DD
    version: str = "v1"
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

    total_chain_count: int = 0
    chain_ids: List[str] = field(default_factory=list)

    provider_counts: Dict[str, int] = field(default_factory=dict)
    issue_type_counts: Dict[str, int] = field(default_factory=dict)
    rollback_count: int = 0
    fallback_count: int = 0

    # 本轮只做占位：不实现真实备份调度
    # hot：近 15 天
    # pending_backup：超过 15 天，等待 T+1 备份
    archive_tier: str = "hot"
    backup_status: str = "pending"  # pending | requested | completed (占位)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "total_chain_count": self.total_chain_count,
            "chain_ids": list(self.chain_ids),
            "provider_counts": dict(self.provider_counts),
            "issue_type_counts": dict(self.issue_type_counts),
            "rollback_count": self.rollback_count,
            "fallback_count": self.fallback_count,
            "archive_tier": self.archive_tier,
            "backup_status": self.backup_status,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RequestTraceArchiveManifest":
        m = cls(
            date=str(d.get("date", "")),
            version=str(d.get("version", "v1")),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            total_chain_count=int(d.get("total_chain_count") or 0),
            chain_ids=list(d.get("chain_ids") or []),
            provider_counts=dict(d.get("provider_counts") or {}),
            issue_type_counts=dict(d.get("issue_type_counts") or {}),
            rollback_count=int(d.get("rollback_count") or 0),
            fallback_count=int(d.get("fallback_count") or 0),
            archive_tier=str(d.get("archive_tier") or "hot"),
            backup_status=str(d.get("backup_status") or "pending"),
        )
        # 兼容：若旧 manifest 没有 backup_status 字段
        if not getattr(m, "backup_status", None):
            m.backup_status = "pending"
        return m


def compute_archive_tier(*, day: str, now: Optional[date] = None) -> str:
    """按要求的“近 15 天常备 / 超过 15 天进入 T+1 备份占位”计算。"""
    if now is None:
        now = date.today()
    try:
        d = datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        return "hot"
    age_days = (now - d).days
    if age_days <= 15:
        return "hot"
    return "pending_backup"

