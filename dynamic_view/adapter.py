from __future__ import annotations

from typing import List

from dynamic_view.attention import AttentionManager, AttentionWindow


class DynamicViewAttentionAdapter:
    """
    Dynamic View 的唯一接入点：
    - 只接收 AttentionWindow
    - 不改实体生成逻辑
    """

    def __init__(self, attention_manager: AttentionManager):
        self.attn = attention_manager

    def set_attention_windows(self, windows: List[AttentionWindow]):
        self.attn.set(windows)
