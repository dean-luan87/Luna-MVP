# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Database（数据库封装）

职责：
- SQLite 数据库连接与表结构管理
- 提供强一致、可追责、无需额外依赖的持久化

原则：
- 使用 SQLite（强一致、可追责、无需额外依赖）
- 所有表结构版本化（schema_version）
- 支持可回归、可对比、可追责
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator

DEFAULT_DB_PATH = os.environ.get("LUNA_WM_DB_PATH", "artifacts/world_model/world_model.db")


def ensure_parent_dir(path: str) -> None:
    """确保父目录存在"""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


class WorldModelDB:
    """
    World Model 数据库封装（SQLite）
    
    职责：
    - 管理数据库连接
    - 初始化表结构
    - 提供事务上下文管理器
    
    原则：
    - 强一致、可追责、无需额外依赖
    - 所有表结构版本化
    """
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """
        初始化数据库
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        ensure_parent_dir(self.db_path)
        self._init_db()
    
    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """
        数据库连接上下文管理器
        
        Yields:
            sqlite3.Connection: 数据库连接
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def _init_db(self) -> None:
        """初始化数据库表结构"""
        with self.connect() as conn:
            # 事实候选表
            conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_candidates (
              candidate_id TEXT PRIMARY KEY,
              claim_type TEXT NOT NULL,
              scene_id TEXT NOT NULL,
              map_id TEXT,
              scope_json TEXT NOT NULL,
              statement TEXT,
              status TEXT NOT NULL,                 -- PENDING / PROMOTABLE / REJECTED / CONSUMED
              confidence REAL NOT NULL,
              support_count INTEGER NOT NULL,
              conflict_count INTEGER NOT NULL,
              unique_sources_json TEXT NOT NULL,    -- JSON array
              first_seen_ts REAL NOT NULL,
              last_seen_ts REAL NOT NULL,
              last_reason TEXT
            )
            """)
            
            # 知识条目表
            conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
              item_id TEXT PRIMARY KEY,
              item_type TEXT NOT NULL,              -- FACT / RULE / POI_INFO / SAFETY_NOTE
              scene_id TEXT,
              map_id TEXT,
              scope_json TEXT NOT NULL,
              statement TEXT NOT NULL,
              tags_json TEXT NOT NULL,              -- JSON array
              confidence REAL NOT NULL,
              lifecycle_state TEXT NOT NULL,        -- ACTIVE / PASSIVE / DEPRECATED
              source_set_json TEXT NOT NULL,         -- JSON array
              evidence_refs_json TEXT NOT NULL,      -- JSON array
              valid_from_ts REAL NOT NULL,
              valid_to_ts REAL,
              last_verified_ts REAL NOT NULL,
              schema_version TEXT NOT NULL
            )
            """)
            
            # 索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_fc_scene_claim ON fact_candidates(scene_id, claim_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_ki_scene ON knowledge_items(scene_id)")


