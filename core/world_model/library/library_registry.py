# -*- coding: utf-8 -*-
"""
v1.8.5: Library Registry（图书馆注册表）

职责：
- 事实慢确认入库（承接候选池 → L1/L2 知识条目）
- 知识唤醒机制（按 Scene / Map / Task 上下文唤醒知识）
- 只供参考，不裁决

防污染原则：
- 只消费 PROMOTABLE
- 创建条目默认 PASSIVE（保守）
- confidence 慢升快降
- 场景/位置不稳定：不升级，不入库
"""

import json
import time
import hashlib
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.common.gates import should_freeze_world_writes
from core.world_model.memory.candidate_pool import FactCandidatePool, FactCandidate
from core.world_model.library.schemas import SCHEMA_VERSION, ITEM_FACT, LIFE_ACTIVE, LIFE_PASSIVE, LIFE_DEPRECATED


@dataclass
class LibraryHint:
    """
    知识提示（唤醒输出）
    
    字段说明：
    - item_id: 知识条目 ID
    - statement: 声明描述
    - confidence: 置信度 [0.0 ~ 1.0]
    - tags: 标签列表
    - scene_id: 场景 ID（可选）
    - map_id: 地图单元 ID（可选）
    - last_verified_ts: 最后验证时间戳
    """
    item_id: str
    statement: str
    confidence: float
    tags: List[str]
    scene_id: Optional[str]
    map_id: Optional[str]
    last_verified_ts: float


class LibraryRegistry:
    """
    图书馆注册表
    
    防污染原则：
    - 只消费 PROMOTABLE
    - 创建条目默认 PASSIVE（保守）
    - confidence 慢升快降
    - 场景/位置不稳定：不升级，不入库
    
    保留机制（Phase 1 文档冻结，Phase 2 实现）：
    - Library 条目软回滚：如果 now - last_verified_ts > VERIFY_TTL，则
      lifecycle_state = PASSIVE, confidence *= 0.85
    - 参数建议：FACT / SAFETY_NOTE = 7 天，RULE = 30 天
    
    注意：已在 update() 末尾自动调用 soft_rollback_stale_items()，防止陈年 ACTIVE
    """
    
    def __init__(
        self,
        db: WorldModelDB,
        candidate_pool: FactCandidatePool,
        verify_ttl_fact_s: float = 7 * 24 * 3600,  # 7 天
        verify_ttl_rule_s: float = 30 * 24 * 3600,  # 30 天
    ):
        """
        初始化图书馆注册表
        
        Args:
            db: 数据库实例
            candidate_pool: 事实候选池实例
            verify_ttl_fact_s: 事实类条目的验证过期时间（秒，默认 7 天）
            verify_ttl_rule_s: 规则类条目的验证过期时间（秒，默认 30 天）
        """
        self.db = db
        self.pool = candidate_pool
        self.verify_ttl_fact_s = verify_ttl_fact_s
        self.verify_ttl_rule_s = verify_ttl_rule_s
    
    def update(
        self,
        active_scene_id: str,
        position_state: PositionState,
        now_ts: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        更新图书馆（消费候选池中的 PROMOTABLE 项）
        
        Args:
            active_scene_id: 当前活跃场景 ID
            position_state: 位置状态
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            Dict[str, Any]: 更新结果（updated, reason）
        """
        now = now_ts or time.time()
        
        # Layer 1：统一 Gate 规则（包 B：失衡/漂移/重定位 → 禁止 consume/promote，但允许 rollback）
        if should_freeze_world_writes(position_state):
            # 允许 soft rollback，但禁止 consume/promote
            rolled = self.soft_rollback_stale_items(now_ts=now)
            return {"updated": 0, "rolled_back": rolled, "reason": "world_write_frozen"}
        
        promotables = self.pool.fetch_promotables(limit=50)
        updated = 0
        
        for c in promotables:
            if c.scene_id != active_scene_id:
                # 只在当前场景消费（一期保守），避免跨场景污染
                continue
            
            existing_id = self._find_existing_item_id(scope=c.scope, claim_type=c.claim_type)
            
            if existing_id is None:
                # 创建新 KnowledgeItem（默认 PASSIVE）
                item_id = self._stable_item_id(c.scope, c.claim_type)
                statement = c.statement or f"{c.claim_type} (unverified)"
                tags = [c.claim_type]
                
                with self.db.connect() as conn:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO knowledge_items(
                          item_id, item_type, scene_id, map_id, scope_json, statement,
                          tags_json, confidence, lifecycle_state, source_set_json, evidence_refs_json,
                          valid_from_ts, valid_to_ts, last_verified_ts, schema_version
                        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            item_id, ITEM_FACT, c.scene_id, c.map_id,
                            json.dumps(c.scope, ensure_ascii=False),
                            statement,
                            json.dumps(tags, ensure_ascii=False),
                            min(0.60, max(0.20, c.confidence)),  # 仍保守
                            LIFE_PASSIVE,
                            json.dumps(sorted(set(c.unique_sources)), ensure_ascii=False),
                            json.dumps([{"candidate_id": c.candidate_id}], ensure_ascii=False),
                            now, None, now, SCHEMA_VERSION,
                        ),
                    )
                
                self.pool.mark_consumed(c.candidate_id, reason="promoted_to_library_passive")
                updated += 1
                continue
            
            # 更新现有条目（慢升）
            with self.db.connect() as conn:
                row = conn.execute("SELECT * FROM knowledge_items WHERE item_id=?", (existing_id,)).fetchone()
                if row is None:
                    continue
                
                conf = float(row["confidence"])
                conf = min(1.0, conf + 0.03)  # 慢升
                
                lifecycle = row["lifecycle_state"]
                # 简化：达到阈值后可转 ACTIVE（仍保守）
                if conf >= 0.75:
                    lifecycle = LIFE_ACTIVE
                
                # 合并来源和证据
                sources = set(json.loads(row["source_set_json"]))
                sources.update(c.unique_sources)
                evid = json.loads(row["evidence_refs_json"])
                evid.append({"candidate_id": c.candidate_id})
                
                conn.execute(
                    """
                    UPDATE knowledge_items SET
                      confidence=?,
                      lifecycle_state=?,
                      source_set_json=?,
                      evidence_refs_json=?,
                      last_verified_ts=?
                    WHERE item_id=?
                    """,
                    (
                        conf,
                        lifecycle,
                        json.dumps(sorted(sources), ensure_ascii=False),
                        json.dumps(evid, ensure_ascii=False),
                        now,
                        existing_id,
                    ),
                )
            
            self.pool.mark_consumed(c.candidate_id, reason="merged_into_existing_knowledge")
            updated += 1
        
        # 在 update() 末尾调用一次（防止陈年 ACTIVE）
        rollback_n = self.soft_rollback_stale_items(now_ts=now)
        
        return {"updated": updated, "rolled_back": rollback_n, "reason": "ok"}
    
    def soft_rollback_stale_items(self, now_ts: Optional[float] = None) -> int:
        """
        软回滚过期的知识条目（保留机制，Phase 1 文档冻结，Phase 2 实现）
        
        规则（写死）：
        - 如果 now - last_verified_ts > VERIFY_TTL，则
          lifecycle_state = PASSIVE, confidence *= 0.85
        - 参数建议：FACT / SAFETY_NOTE = 7 天，RULE = 30 天
        
        Args:
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            int: 回滚的条目数量
        """
        now = now_ts or time.time()
        
        with self.db.connect() as conn:
            # 获取所有 ACTIVE 和 PASSIVE 状态的条目
            rows = conn.execute(
                "SELECT item_id, item_type, last_verified_ts, confidence, lifecycle_state "
                "FROM knowledge_items "
                "WHERE lifecycle_state IN (?,?)",
                (LIFE_ACTIVE, LIFE_PASSIVE),
            ).fetchall()
            
            rolled_back = 0
            for r in rows:
                item_id = r["item_id"]
                item_type = r["item_type"]
                last_verified = float(r["last_verified_ts"])
                confidence = float(r["confidence"])
                lifecycle = r["lifecycle_state"]
                
                # 根据条目类型选择 TTL
                verify_ttl = self.verify_ttl_fact_s if item_type in (ITEM_FACT, "SAFETY_NOTE") else self.verify_ttl_rule_s
                
                if now - last_verified > verify_ttl:
                    # 软回滚：降级为 PASSIVE，置信度衰减
                    new_lifecycle = LIFE_PASSIVE
                    new_confidence = max(0.0, confidence * 0.85)
                    
                    conn.execute(
                        "UPDATE knowledge_items SET lifecycle_state=?, confidence=? WHERE item_id=?",
                        (new_lifecycle, new_confidence, item_id),
                    )
                    rolled_back += 1
        
        return rolled_back
    
    def get_hints(
        self,
        active_scene_id: str,
        map_id: Optional[str] = None,
        limit: int = 10
    ) -> List[LibraryHint]:
        """
        获取知识提示（唤醒机制）
        
        Args:
            active_scene_id: 当前活跃场景 ID
            map_id: 地图单元 ID（可选）
            limit: 最大返回数量
        
        Returns:
            List[LibraryHint]: 知识提示列表
        """
        with self.db.connect() as conn:
            if map_id:
                rows = conn.execute(
                    """
                    SELECT * FROM knowledge_items
                    WHERE (scene_id=? OR scene_id IS NULL) AND (map_id=? OR map_id IS NULL)
                    AND lifecycle_state IN (?,?)
                    ORDER BY confidence DESC, last_verified_ts DESC
                    LIMIT ?
                    """,
                    (active_scene_id, map_id, LIFE_ACTIVE, LIFE_PASSIVE, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM knowledge_items
                    WHERE (scene_id=? OR scene_id IS NULL)
                    AND lifecycle_state IN (?,?)
                    ORDER BY confidence DESC, last_verified_ts DESC
                    LIMIT ?
                    """,
                    (active_scene_id, LIFE_ACTIVE, LIFE_PASSIVE, limit),
                ).fetchall()
        
        hints: List[LibraryHint] = []
        for r in rows:
            hints.append(
                LibraryHint(
                    item_id=r["item_id"],
                    statement=r["statement"],
                    confidence=float(r["confidence"]),
                    tags=json.loads(r["tags_json"]),
                    scene_id=r["scene_id"],
                    map_id=r["map_id"],
                    last_verified_ts=float(r["last_verified_ts"]),
                )
            )
        return hints
    
    def _find_existing_item_id(self, scope: Dict[str, Any], claim_type: str) -> Optional[str]:
        """
        查找现有知识条目 ID
        
        Args:
            scope: 适用范围
            claim_type: 声明类型
        
        Returns:
            Optional[str]: 现有条目 ID，如果不存在则返回 None
        """
        # 一期：用稳定 id 直接查（避免重复）
        item_id = self._stable_item_id(scope, claim_type)
        with self.db.connect() as conn:
            row = conn.execute("SELECT item_id FROM knowledge_items WHERE item_id=?", (item_id,)).fetchone()
        return row["item_id"] if row else None
    
    @staticmethod
    def _stable_item_id(scope: Dict[str, Any], claim_type: str) -> str:
        """
        生成稳定知识条目 ID（用于可回归、可对比、可追责）
        
        Args:
            scope: 适用范围
            claim_type: 声明类型
        
        Returns:
            str: 稳定 ID（SHA256 前 24 位）
        """
        key = json.dumps({"scope": scope, "claim": claim_type}, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]

