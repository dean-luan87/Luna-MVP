from __future__ import annotations

"""
SceneRegistry: 管理所有场景包（ScenePack）的注册与查找。

核心概念：
- scene: 场景主类，例如 "subway", "hospital"
- tag:   场景标签，例如 "静安寺站", "虹口医院"（可选）
- pack_id: 场景包标识，一般对应某个 JSON / YAML / Python 配置文件路径或 ID

设计原则：
- 一个 scene 可以有一个"默认场景包"（tag=None），也可以有多个 tag 级别的场景包；
- 查找时，优先返回 tag 级别，其次回落到默认场景包；
- 不做 IO，仅做"映射管理"，真正加载交给 ScenePackLoader。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Iterable


@dataclass(frozen=True)
class SceneKey:
    """场景唯一键：Scene + 可选 SceneTag。"""

    scene: str
    tag: Optional[str] = None


@dataclass
class ScenePackRef:
    """
    对场景包的一个引用。

    - pack_id 通常是一个路径（如 JSON 文件路径）或逻辑 ID
    - meta 可附带一些补充信息（如版本、优先级、说明）
    """

    key: SceneKey
    pack_id: str
    meta: Dict[str, object] = field(default_factory=dict)


class SceneRegistry:
    """
    SceneRegistry 负责管理所有场景包的注册与查找。

    内部采用两级结构：
    - 第一层：按 scene 分类
    - 第二层：按 tag 分类，tag 可以为 None（表示默认场景包）

    示例结构：
    {
        "subway": {
            None: ScenePackRef(... 默认地铁场景包 ...),
            "静安寺站": ScenePackRef(... 静安寺地铁站专属包 ...)
        },
        "hospital": {
            None: ScenePackRef(... 默认医院场景包 ...),
            "虹口医院": ScenePackRef(... 虹口医院专属包 ...)
        }
    }
    """

    def __init__(self) -> None:
        # _data[scene][tag] = ScenePackRef
        self._data: Dict[str, Dict[Optional[str], ScenePackRef]] = {}

    # ---------- 注册相关 ----------

    def register(
        self,
        scene: str,
        pack_id: str,
        tag: Optional[str] = None,
        meta: Optional[Dict[str, object]] = None,
        overwrite: bool = True,
    ) -> ScenePackRef:
        """
        注册一个场景包。

        :param scene: 场景主类，例如 "subway" / "hospital"
        :param pack_id: 场景包标识，一般是一个路径或逻辑 ID
        :param tag: 场景标签，例如 "静安寺站" / "虹口医院"，为 None 时表示默认场景包
        :param meta: 附加信息（可选）
        :param overwrite: 是否覆盖已有注册（默认覆盖）
        """
        scene = scene.strip()
        if not scene:
            raise ValueError("scene 不能为空")

        tag = tag.strip() if isinstance(tag, str) else tag
        meta = dict(meta) if meta is not None else {}

        key = SceneKey(scene=scene, tag=tag)
        ref = ScenePackRef(key=key, pack_id=pack_id, meta=meta)

        scene_map = self._data.setdefault(scene, {})
        if not overwrite and tag in scene_map:
            # 不覆盖时，直接返回已有引用
            return scene_map[tag]

        scene_map[tag] = ref
        return ref

    # ---------- 查询相关 ----------

    def get(self, scene: str, tag: Optional[str] = None) -> Optional[ScenePackRef]:
        """
        按 scene + 可选 tag 查找场景包。

        查找策略：
        1. 若 tag 不为 None，优先返回 (scene, tag) 的精确匹配；
        2. 否则或找不到时，尝试返回 (scene, None) 默认场景包；
        3. 若都不存在，返回 None。
        """
        scene = scene.strip()
        if not scene:
            return None

        scene_map = self._data.get(scene)
        if not scene_map:
            return None

        # 优先 tag 精确匹配
        if tag is not None:
            tag = tag.strip()
            if tag in scene_map:
                return scene_map[tag]

        # 回落默认场景包
        return scene_map.get(None)

    def require(self, scene: str, tag: Optional[str] = None) -> ScenePackRef:
        """
        get 的严格版本：若未找到则抛出异常。
        """
        ref = self.get(scene, tag)
        if ref is None:
            raise KeyError(f"ScenePack not found for scene={scene!r}, tag={tag!r}")
        return ref

    # ---------- 枚举相关 ----------

    def list_scenes(self) -> List[str]:
        """列出所有已注册的 scene 名称。"""
        return sorted(self._data.keys())

    def list_tags(self, scene: str) -> List[str]:
        """
        列出某个 scene 下所有已注册的 tag（不包括 None）。

        若 scene 不存在，返回空列表。
        """
        scene_map = self._data.get(scene)
        if not scene_map:
            return []
        tags: List[str] = [
            t for t in scene_map.keys() if t is not None
        ]
        # 保持稳定顺序（便于测试）
        return sorted(tags)

    def iter_scene_packs(self) -> Iterable[ScenePackRef]:
        """遍历所有注册的 ScenePackRef。"""
        for scene, tag_map in self._data.items():
            for tag, ref in tag_map.items():
                yield ref

    # ---------- 管理相关 ----------

    def clear(self) -> None:
        """清空所有注册（通常用于测试）。"""
        self._data.clear()


# 模块级默认实例，方便在系统其他部分直接使用
scene_registry = SceneRegistry()
