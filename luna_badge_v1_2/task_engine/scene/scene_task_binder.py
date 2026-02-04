"""
SceneTaskBinder: 场景 → 任务建议的绑定器

职责：
- 根据 SceneContext（scene + tag）给出推荐的任务元数据
- 支持精确匹配（scene, tag）和回退匹配（scene, None）
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional

from task_engine.scene.scene_context import SceneContext


@dataclass
class SceneTaskBinder:
    """
    场景 → 任务建议的简单绑定器。

    映射规则：
    - (scene, tag) 精确匹配
    - 若找不到 tag，回退到 (scene, None)
    """

    # key: (scene, tag or None) → value: task_meta 片段
    mapping: Dict[Tuple[str, Optional[str]], dict] = field(default_factory=dict)

    def suggest_task(self, ctx: SceneContext) -> Optional[dict]:
        """
        根据 SceneContext 建议任务元数据。

        Args:
            ctx: SceneContext 实例

        Returns:
            Optional[dict]: 推荐的任务元数据，如果没有匹配则返回 None
        """
        if not ctx.scene:
            return None

        # 1. 尝试 tag 精确命中
        key_exact = (ctx.scene, ctx.tag)
        if key_exact in self.mapping:
            return self._build_task_meta(ctx, self.mapping[key_exact])

        # 2. 回退 scene 级别
        key_scene = (ctx.scene, None)
        if key_scene in self.mapping:
            return self._build_task_meta(ctx, self.mapping[key_scene])

        return None

    @staticmethod
    def _build_task_meta(ctx: SceneContext, base_meta: dict) -> dict:
        """
        注入一些标准字段，方便 TaskChainManager 使用。

        Args:
            ctx: SceneContext 实例
            base_meta: 基础任务元数据

        Returns:
            dict: 完整的任务元数据
        """
        meta = dict(base_meta)
        meta.setdefault("scene", ctx.scene)
        if ctx.tag:
            meta.setdefault("scene_tag", ctx.tag)
        return meta


def create_default_scene_task_binder() -> SceneTaskBinder:
    """
    创建一个默认配置的 SceneTaskBinder。

    映射规则：
    - subway → subway_enter
    - hospital → hospital_enter

    可后续改为从 scene_pack.json 读取。

    Returns:
        SceneTaskBinder: 配置好的绑定器实例
    """
    mapping = {
        ("subway", None): {
            "task_name": "subway_enter",
            "ask_required": True,
        },
        ("hospital", None): {
            "task_name": "hospital_enter",
            "ask_required": True,
        },
    }
    return SceneTaskBinder(mapping=mapping)












