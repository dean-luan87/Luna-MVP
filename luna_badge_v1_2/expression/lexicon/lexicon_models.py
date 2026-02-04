"""
Lexicon Models (C Layer)

词库数据模型
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class LexiconEntry:
    """词库条目"""
    key: str
    value: str
    profile: str  # 词库配置名称
    tags: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}


@dataclass
class LexiconProfile:
    """词库配置"""
    name: str
    entries: Dict[str, str]  # {key: value}
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
