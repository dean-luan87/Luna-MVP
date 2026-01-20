# -*- coding: utf-8 -*-
"""
v1.8.5: Fact Candidate Pool（事实候选池）

职责：
- 承接 Memory → 候选事实
- 管理事实候选的演化（support_count, conflict_count, confidence）
- 判定候选是否可升级为 PROMOTABLE

防污染原则：
- 用户输入只能作为弱 source：不会单独推动 PROMOTABLE
- confidence 慢升快降
- 必须满足 N_support + N_sources + MIN_SPAN + MAX_CONFLICT 才 PROMOTABLE

⚠️ v1.8.5 Phase B: 视觉隔离护栏

CandidatePool 是视觉事实进入世界模型的唯一合法入口。

原则（写死）：
- world_model 只接受"结构化事实"
- 不接受 frame / image / bbox / ocr_text
- 所有视觉事实必须通过 CandidatePool.upsert_observation() 进入
"""

import json
import time
import hashlib
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.common.gates import should_freeze_world_writes

STATUS_PENDING = "PENDING"
STATUS_PROMOTABLE = "PROMOTABLE"
STATUS_REJECTED = "REJECTED"
STATUS_CONSUMED = "CONSUMED"


@dataclass
class FactCandidate:
    """
    事实候选
    
    字段说明：
    - candidate_id: 候选唯一标识（稳定 hash）
    - claim_type: 声明类型（road_blocked / shop_closed / flooded）
    - scene_id: 场景 ID（必填）
    - map_id: 地图单元 ID（可选）
    - scope: 适用范围（JSON 字典）
    - statement: 声明描述（可选）
    - status: 状态（PENDING / PROMOTABLE / REJECTED / CONSUMED）
    - confidence: 置信度 [0.0 ~ 1.0]
    - support_count: 支持次数
    - conflict_count: 冲突次数
    - unique_sources: 唯一来源列表（vision / system / external_map / user_report）
    - first_seen_ts: 首次出现时间戳
    - last_seen_ts: 最后出现时间戳
    - last_reason: 最后原因（可选）
    """
    candidate_id: str
    claim_type: str
    scene_id: str
    map_id: Optional[str]
    scope: Dict[str, Any]  # {"scene_id":..., "map_id":..., "geo":...}
    statement: Optional[str]
    status: str
    confidence: float
    support_count: int
    conflict_count: int
    unique_sources: List[str]  # ["vision","system","external_map","user_report"]
    first_seen_ts: float
    last_seen_ts: float
    last_reason: Optional[str] = None


class FactCandidatePool:
    """
    事实候选池
    
    防污染原则：
    - 用户输入只能作为弱 source：不会单独推动 PROMOTABLE
    - confidence 慢升快降
    - 必须满足 N_support + N_sources + MIN_SPAN + MAX_CONFLICT 才 PROMOTABLE
    """
    
    def __init__(
        self,
        db: WorldModelDB,
        n_support: int = 3,
        n_sources: int = 2,
        min_span_s: float = 30 * 60,  # 30 分钟
        max_conflict: int = 1,
        candidate_ttl_s: float = 24 * 3600,  # 24 小时
    ):
        """
        初始化事实候选池
        
        Args:
            db: 数据库实例
            n_support: 最小支持次数（默认 3）
            n_sources: 最小唯一来源数（默认 2）
            min_span_s: 最小时间跨度（秒，默认 30 分钟）
            max_conflict: 最大冲突次数（默认 1）
            candidate_ttl_s: 候选过期时间（秒，默认 24 小时）
        """
        self.db = db
        self.n_support = n_support
        self.n_sources = n_sources
        self.min_span_s = min_span_s
        self.max_conflict = max_conflict
        self.candidate_ttl_s = candidate_ttl_s
    
    def upsert_observation(
        self,
        claim_type: str,
        scene_id: str,
        map_id: Optional[str],
        scope: Dict[str, Any],
        source: str,
        is_conflict: bool = False,
        statement: Optional[str] = None,
        now_ts: Optional[float] = None,
        reason: Optional[str] = None,
        position_state: Optional[PositionState] = None,
    ) -> FactCandidate:
        """
        更新或插入观察结果
        
        Args:
            claim_type: 声明类型
            scene_id: 场景 ID
            map_id: 地图单元 ID（可选）
            scope: 适用范围
            source: 来源（vision / system / external_map / user_report）
            is_conflict: 是否为冲突
            statement: 声明描述（可选）
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
            reason: 原因（可选）
            position_state: 位置状态（可选，用于重定位闸门）
        
        Returns:
            FactCandidate: 更新后的候选
        """
        now = now_ts or time.time()
        
        # 统一 Gate 规则（包 B：失衡/漂移/重定位 → 禁止升级，防止错位污染）
        if position_state and should_freeze_world_writes(position_state):
            # 如果被闸门阻止，抛出异常（由调用方处理）
            raise ValueError("world_write_frozen: cannot upsert observation during freeze")
        
        # Natural key: (claim_type + scene_id + map_id) 作为一期简化（后面可加 geo hash）
        natural = f"{claim_type}::{scene_id}::{map_id or ''}"
        candidate_id = self._stable_id(natural)
        
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM fact_candidates WHERE candidate_id=?",
                (candidate_id,),
            ).fetchone()
            
            if row is None:
                # 创建新候选
                fc = FactCandidate(
                    candidate_id=candidate_id,
                    claim_type=claim_type,
                    scene_id=scene_id,
                    map_id=map_id,
                    scope=scope,
                    statement=statement,
                    status=STATUS_PENDING,
                    confidence=0.10,  # 初始低
                    support_count=1,
                    conflict_count=1 if is_conflict else 0,
                    unique_sources=[source],
                    first_seen_ts=now,
                    last_seen_ts=now,
                    last_reason=reason,
                )
                conn.execute(
                    """
                    INSERT INTO fact_candidates(
                      candidate_id, claim_type, scene_id, map_id, scope_json, statement, status,
                      confidence, support_count, conflict_count, unique_sources_json,
                      first_seen_ts, last_seen_ts, last_reason
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        fc.candidate_id, fc.claim_type, fc.scene_id, fc.map_id,
                        json.dumps(fc.scope, ensure_ascii=False),
                        fc.statement, fc.status,
                        fc.confidence, fc.support_count, fc.conflict_count,
                        json.dumps(fc.unique_sources, ensure_ascii=False),
                        fc.first_seen_ts, fc.last_seen_ts, fc.last_reason,
                    ),
                )
                return fc
            
            # 更新现有候选
            unique_sources = json.loads(row["unique_sources_json"])
            if source not in unique_sources:
                unique_sources.append(source)
            
            support_count = int(row["support_count"]) + (0 if is_conflict else 1)
            conflict_count = int(row["conflict_count"]) + (1 if is_conflict else 0)
            
            # confidence：慢升快降
            confidence = float(row["confidence"])
            if is_conflict:
                confidence = max(0.0, confidence - 0.15)
            else:
                # user_report 不提升 confidence（防污染）
                if source != "user_report":
                    confidence = min(1.0, confidence + 0.05)
            
            first_seen = float(row["first_seen_ts"])
            span_ok = (now - first_seen) >= self.min_span_s
            sources_ok = len(unique_sources) >= self.n_sources
            support_ok = support_count >= self.n_support
            conflict_ok = conflict_count <= self.max_conflict
            
            status = row["status"]
            if status not in (STATUS_CONSUMED, STATUS_REJECTED):
                status = STATUS_PROMOTABLE if (span_ok and sources_ok and support_ok and conflict_ok) else STATUS_PENDING
            
            conn.execute(
                """
                UPDATE fact_candidates SET
                  scope_json=?, statement=COALESCE(?, statement),
                  status=?, confidence=?, support_count=?, conflict_count=?,
                  unique_sources_json=?, last_seen_ts=?, last_reason=?
                WHERE candidate_id=?
                """,
                (
                    json.dumps(scope, ensure_ascii=False),
                    statement,
                    status, confidence, support_count, conflict_count,
                    json.dumps(unique_sources, ensure_ascii=False),
                    now, reason,
                    candidate_id,
                ),
            )
            
            return self.get(candidate_id)
    
    def register_conflict(
        self,
        scene_id: str,
        map_id: Optional[str],
        claim_type: str,
        source: str,
        statement: Optional[str] = None,
        now_ts: Optional[float] = None,
        position_state: Optional[PositionState] = None,
    ) -> FactCandidate:
        """
        v1.8.5 Phase C 包 C：注册冲突信号（用户报告）
        
        规则：
        - 用户报告只增 conflict_count，不动 confidence
        - 必须满足统一 Gate 规则（由调用方检查）
        
        Args:
            scene_id: 场景 ID
            map_id: 地图单元 ID（可选）
            claim_type: 声明类型
            source: 来源（user_report）
            statement: 声明描述（可选）
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
            position_state: 位置状态（可选，用于重定位闸门）
        
        Returns:
            FactCandidate: 更新后的候选
        """
        now = now_ts or time.time()
        
        # 统一 Gate 规则（包 B：失衡/漂移/重定位 → 禁止升级，防止错位污染）
        if position_state and should_freeze_world_writes(position_state):
            raise ValueError("world_write_frozen: cannot register conflict during freeze")
        
        # 使用 upsert_observation，但标记为冲突
        return self.upsert_observation(
            claim_type=claim_type,
            scene_id=scene_id,
            map_id=map_id,
            scope={"scene_id": scene_id, "map_id": map_id},
            source=source,
            is_conflict=True,  # 标记为冲突
            statement=statement,
            now_ts=now,
            reason="from_user_report_router_conflict",
            position_state=position_state,
        )
    
    def cleanup_expired(self, now_ts: Optional[float] = None) -> int:
        """
        清理过期的候选（必须补，防系统性隐患）
        
        规则：
        - 如果 now - last_seen_ts > candidate_ttl_s，则标记为 REJECTED
        - 只处理 PENDING 和 PROMOTABLE 状态的候选
        
        Args:
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            int: 清理的候选数量
        """
        now = now_ts or time.time()
        
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT candidate_id, last_seen_ts FROM fact_candidates "
                "WHERE status IN (?,?)",
                (STATUS_PENDING, STATUS_PROMOTABLE),
            ).fetchall()
            
            expired = [
                r["candidate_id"]
                for r in rows
                if now - float(r["last_seen_ts"]) > self.candidate_ttl_s
            ]
            
            for cid in expired:
                conn.execute(
                    "UPDATE fact_candidates SET status=?, last_reason=? WHERE candidate_id=?",
                    (STATUS_REJECTED, "expired_no_recent_support", cid),
                )
            
            return len(expired)
    
    def fetch_promotables(self, limit: int = 50, cleanup_before: bool = True) -> List[FactCandidate]:
        """
        获取可升级的候选列表
        
        Args:
            limit: 最大返回数量
            cleanup_before: 是否在获取前先清理过期候选（默认 True）
        
        Returns:
            List[FactCandidate]: 可升级的候选列表
        """
        # 在获取前先清理过期候选（防系统性隐患）
        if cleanup_before:
            self.cleanup_expired()
        
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM fact_candidates WHERE status=? ORDER BY last_seen_ts DESC LIMIT ?",
                (STATUS_PROMOTABLE, limit),
            ).fetchall()
        return [self._row_to_fc(r) for r in rows]
    
    def mark_consumed(self, candidate_id: str, reason: str = "consumed") -> None:
        """
        标记候选为已消费
        
        Args:
            candidate_id: 候选 ID
            reason: 原因（可选）
        """
        with self.db.connect() as conn:
            conn.execute(
                "UPDATE fact_candidates SET status=?, last_reason=? WHERE candidate_id=?",
                (STATUS_CONSUMED, reason, candidate_id),
            )
    
    def get(self, candidate_id: str) -> FactCandidate:
        """
        获取候选
        
        Args:
            candidate_id: 候选 ID
        
        Returns:
            FactCandidate: 候选对象
        
        Raises:
            KeyError: 如果候选不存在
        """
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM fact_candidates WHERE candidate_id=?", (candidate_id,)).fetchone()
        if row is None:
            raise KeyError(candidate_id)
        return self._row_to_fc(row)
    
    @staticmethod
    def _stable_id(natural_key: str) -> str:
        """
        生成稳定 ID（用于可回归、可对比、可追责）
        
        Args:
            natural_key: 自然键
        
        Returns:
            str: 稳定 ID（SHA256 前 24 位）
        """
        return hashlib.sha256(natural_key.encode("utf-8")).hexdigest()[:24]
    
    @staticmethod
    def _row_to_fc(row) -> FactCandidate:
        """
        将数据库行转换为 FactCandidate
        
        Args:
            row: 数据库行
        
        Returns:
            FactCandidate: 候选对象
        """
        return FactCandidate(
            candidate_id=row["candidate_id"],
            claim_type=row["claim_type"],
            scene_id=row["scene_id"],
            map_id=row["map_id"],
            scope=json.loads(row["scope_json"]),
            statement=row["statement"],
            status=row["status"],
            confidence=float(row["confidence"]),
            support_count=int(row["support_count"]),
            conflict_count=int(row["conflict_count"]),
            unique_sources=json.loads(row["unique_sources_json"]),
            first_seen_ts=float(row["first_seen_ts"]),
            last_seen_ts=float(row["last_seen_ts"]),
            last_reason=row["last_reason"],
        )

