"""
Navigation Logic module.

根据 SceneState 做简单导航决策：
- 检查前方是否有障碍
- 生成一段文字提示
"""

from typing import Optional

from core.scene_output import SceneState


class NavigationEngine:
    def __init__(self):
        # TODO: 未来可引入配置，例如不同模式下的提示策略
        pass

    def update(self, scene_state: SceneState) -> None:
        """
        更新内部场景状态。
        """
        self._scene_state: SceneState = scene_state

    def decide(self) -> Optional[str]:
        """
        根据当前场景状态生成导航提示文本。
        v1.2 使用极简规则：
          - 如果存在 obstacle，则提示前方有障碍
          - 否则返回 None
        """
        if not hasattr(self, "_scene_state"):
            return None

        obstacles = [
            obj for obj in self._scene_state.objects
            if obj.get("class") == "obstacle"
        ]

        if obstacles:
            return "前方可能有障碍物，请注意避让。"
        return None














