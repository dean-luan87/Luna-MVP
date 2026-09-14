# -*- coding: utf-8 -*-
"""
v1.8.5: Memory Registry（记忆注册表）

⚠️ v1.8.5 Phase B: 视觉隔离护栏

MemoryRegistry 禁止接收原始视觉数据。

Forbidden:
- ❌ 不接受 frame / image / bbox / ocr_text
- ❌ 不接受 raw_text（除非来自 UserReportRouter）
- ✅ 只接受结构化输入：ExperienceMemory, UserReportEvent

违规接口检查：
- 所有 public 方法如果参数包含 image/frame/bbox/raw_text，标记为 TODO/DEPRECATED

职责：
- 把"用户体验 / 偏好 / 事实候选信号"拆干净，安全地喂给 CandidatePool
- 不污染 Library 和 Map

设计铁律：
- 位置不稳定，不写任何新 Memory
- 体验 ≠ 事实
- 用户反馈永远不能直通 Library

数据流位置：
Vision / GPS / System / User Feedback
              ↓
        MemoryRegistry
        ├── EXPERIENCE → MemoryTable（体验资产）
        ├── PREFERENCE → MemoryTable（偏好）
        └── FACT_SIGNAL → FactCandidatePool
                                ↓
                         LibraryRegistry

MemoryRegistry 是"入口整流器"，不是事实源。
"""

import time
import json
import hashlib
from typing import Dict, Any, Optional

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from core.world_model.common.db import WorldModelDB
from core.world_model.common.types import PositionState
from core.world_model.common.gates import should_freeze_world_writes
from core.world_model.memory.candidate_pool import FactCandidatePool


@dataclass
class ExperienceMemory:
    """
    体验记忆（不适 / 偏好）
    
    字段说明：
    - scene_id: 场景 ID
    - discomfort_score: 不适评分 [0.0 ~ 1.0]
    - tags: 标签列表（slippery / unsafe / crowded）
    - confidence: 置信度 [0.0 ~ 1.0]
    - last_seen_ts: 最后出现时间戳
    """
    scene_id: str
    discomfort_score: float
    tags: List[str]
    confidence: float = 0.5
    last_seen_ts: float = 0.0


class MemoryRegistry:
    """
    记忆注册表
    
    设计铁律：
    - 位置不稳定，不写任何新 Memory
    - 体验 ≠ 事实
    - 用户反馈永远不能直通 Library
    
    最小工程职责（P0）：
    1. 稳定性闸门（位置不稳，不写）
    2. 反馈分类（体验 / 偏好 / 事实信号）
    3. 体验与偏好安全落盘
    4. 事实信号转候选（送 CandidatePool）
    """
    
    def __init__(self, db: WorldModelDB, candidate_pool: FactCandidatePool):
        """
        初始化记忆注册表
        
        Args:
            db: 数据库实例
            candidate_pool: 事实候选池实例
        """
        self.db = db
        self.pool = candidate_pool
        self._ensure_tables()
    
    def _ensure_tables(self) -> None:
        """确保数据库表存在"""
        with self.db.connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS experience_memories (
              memory_id TEXT PRIMARY KEY,
              scene_id TEXT NOT NULL,
              map_id TEXT,
              tags_json TEXT NOT NULL,        -- ["slippery","crowded"]
              valence TEXT NOT NULL,          -- POSITIVE / NEGATIVE
              intensity REAL NOT NULL,        -- 0~1
              source TEXT NOT NULL,           -- vision / user / system
              created_ts REAL NOT NULL,
              last_seen_ts REAL NOT NULL
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
              pref_id TEXT PRIMARY KEY,
              pref_type TEXT NOT NULL,        -- avoid / prefer
              tags_json TEXT NOT NULL,
              weight REAL NOT NULL,           -- 0~1
              created_ts REAL NOT NULL,
              last_updated_ts REAL NOT NULL
            )
            """)
    
    def update(
        self,
        scene_id: str,
        map_id: Optional[str],
        position_state: PositionState,
        feedback: Dict[str, Any],
        now_ts: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        更新记忆注册表（主入口）
        
        Args:
            scene_id: 场景 ID
            map_id: 地图单元 ID（可选）
            position_state: 位置状态
            feedback: 反馈数据
                - type: EXPERIENCE / PREFERENCE / FACT_SIGNAL
                - 其他字段根据 type 不同而不同
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            Dict[str, Any]: 更新结果（written, reason/kind）
        """
        now = now_ts or time.time()
        
        # Layer 1：统一 Gate 规则（包 B：失衡/漂移/重定位 → 禁止写入，防止错位污染）
        if should_freeze_world_writes(position_state):
            return {"written": 0, "reason": "world_write_frozen"}
        
        fb_type = feedback.get("type")
        
        if fb_type == "EXPERIENCE":
            self._write_experience(scene_id, map_id, feedback, now)
            return {"written": 1, "kind": "experience"}
        
        if fb_type == "PREFERENCE":
            self._write_preference(feedback, now)
            return {"written": 1, "kind": "preference"}
        
        if fb_type == "FACT_SIGNAL":
            self._emit_fact_candidate(scene_id, map_id, feedback, now, position_state)
            return {"written": 1, "kind": "fact_candidate"}
        
        return {"written": 0, "reason": "unknown_feedback"}
    
    def _write_experience(
        self,
        scene_id: str,
        map_id: Optional[str],
        fb: Dict[str, Any],
        now: float,
    ) -> None:
        """
        写入体验记忆
        
        Args:
            scene_id: 场景 ID
            map_id: 地图单元 ID（可选）
            fb: 反馈数据
                - tags: 标签列表（如 ["slippery", "crowded"]）
                - valence: 情感倾向（POSITIVE / NEGATIVE / NEUTRAL）
                - intensity: 强度 [0.0 ~ 1.0]
                - source: 来源（vision / user / system）
            now: 当前时间戳
        """
        tags = fb.get("tags", [])
        valence = fb.get("valence", "NEUTRAL")
        intensity = float(fb.get("intensity", 0.5))
        source = fb.get("source", "user")
        
        key = f"{scene_id}:{map_id}:{sorted(tags)}:{valence}"
        memory_id = self._stable_id(key)
        
        with self.db.connect() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO experience_memories(
              memory_id, scene_id, map_id, tags_json, valence,
              intensity, source, created_ts, last_seen_ts
            ) VALUES(?,?,?,?,?,?,?,?,?)
            """, (
                memory_id,
                scene_id,
                map_id,
                json.dumps(tags, ensure_ascii=False),
                valence,
                intensity,
                source,
                now,
                now,
            ))
    
    def _write_preference(self, fb: Dict[str, Any], now: float) -> None:
        """
        写入偏好
        
        Args:
            fb: 反馈数据
                - pref_type: 偏好类型（avoid / prefer）
                - tags: 标签列表
                - weight: 权重 [0.0 ~ 1.0]
            now: 当前时间戳
        """
        pref_type = fb.get("pref_type")
        tags = fb.get("tags", [])
        weight = float(fb.get("weight", 0.5))
        
        key = f"{pref_type}:{sorted(tags)}"
        pref_id = self._stable_id(key)
        
        with self.db.connect() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO preferences(
              pref_id, pref_type, tags_json, weight,
              created_ts, last_updated_ts
            ) VALUES(?,?,?,?,?,?)
            """, (
                pref_id,
                pref_type,
                json.dumps(tags, ensure_ascii=False),
                weight,
                now,
                now,
            ))
    
    def _emit_fact_candidate(
        self,
        scene_id: str,
        map_id: Optional[str],
        fb: Dict[str, Any],
        now: float,
        position_state: PositionState,
    ) -> None:
        """
        发出事实候选信号（转 CandidatePool）
        
        Args:
            scene_id: 场景 ID
            map_id: 地图单元 ID（可选）
            fb: 反馈数据
                - claim_type: 声明类型（road_blocked / shop_closed / flooded）
                - source: 来源（user_report / vision / system）
                - is_conflict: 是否为冲突
                - statement: 声明描述（可选）
            now: 当前时间戳
        """
        try:
            self.pool.upsert_observation(
                claim_type=fb["claim_type"],
                scene_id=scene_id,
                map_id=map_id,
                scope={"scene_id": scene_id, "map_id": map_id},
                source=fb.get("source", "user_report"),
                is_conflict=fb.get("is_conflict", False),
                statement=fb.get("statement"),
                now_ts=now,
                reason="from_memory_registry",
                position_state=position_state,
            )
        except ValueError as e:
            if "world_write_frozen" in str(e):
                # 统一 Gate 阻止，静默忽略
                pass
            else:
                raise
    
    def get_experience_hints(
        self,
        scene_id: str,
        limit: int = 10,
    ) -> List[ExperienceMemory]:
        """
        获取体验记忆提示（主观体验，极高价值）
        
        MemoryRegistry 不做什么（比做什么更重要）：
        - ❌ 不修改 Map
        - ❌ 不切 Scene
        - ❌ 不立刻影响决策
        
        它只做一件事：
        当 Scene / Task 询问时，提供"这个地方对你来说如何"
        
        Args:
            scene_id: 场景 ID
            limit: 最大返回数量
        
        Returns:
            List[ExperienceMemory]: 体验记忆列表
        """
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT scene_id, tags_json, valence, intensity, last_seen_ts
                FROM experience_memories
                WHERE scene_id = ?
                ORDER BY last_seen_ts DESC
                LIMIT ?
                """,
                (scene_id, limit),
            ).fetchall()
        
        hints: List[ExperienceMemory] = []
        for r in rows:
            # 将 valence 和 intensity 转换为 discomfort_score
            discomfort = float(r["intensity"]) if r["valence"] == "NEGATIVE" else 0.0
            
            hints.append(
                ExperienceMemory(
                    scene_id=r["scene_id"],
                    discomfort_score=discomfort,
                    tags=json.loads(r["tags_json"]),
                    confidence=0.8,  # 默认置信度（体验记忆的置信度基于强度）
                    last_seen_ts=float(r["last_seen_ts"]),
                )
            )
        
        return hints
    
    @staticmethod
    def _stable_id(key: str) -> str:
        """
        生成稳定 ID（用于可回归、可对比、可追责）
        
        Args:
            key: 自然键
        
        Returns:
            str: 稳定 ID（SHA256 前 24 位）
        """
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]

