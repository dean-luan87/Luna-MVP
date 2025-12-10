from __future__ import annotations

"""
ScenePackLoader: 负责从 JSON 文件中加载场景包（ScenePack）定义。

职责：
- 读取 JSON 文件；
- 做基础结构校验（scene / chains 等必备字段）；
- 解析为 ScenePack 数据类；
- 提供基于 ScenePackRef（SceneRegistry 注册项）的加载能力。

注意：
- 不负责将 chains 转换为 TaskChainDefinition；
- 不做业务级语义解析，只承担"配置 → 内存结构"的职责。
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json

from task_engine.scene.scene_registry import ScenePackRef


@dataclass
class ScenePack:
    """
    一个场景包的内存表示。

    - scene: 场景主类，例如 "subway"、"hospital"
    - tags: 该场景包适用的标签列表，例如 ["静安寺站"]
    - version: 版本号（可选，默认 "1.0"）
    - default_chain: 默认任务链 ID（可选）
    - chains: 任务链原始定义字典，key 为 chain_id，value 为链的配置结构
    - raw: 原始 JSON 结构，便于调试与后续扩展
    """

    scene: str
    tags: List[str]
    version: str
    chains: Dict[str, Dict[str, Any]]
    default_chain: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


class ScenePackLoader:
    """
    ScenePackLoader 从本地文件系统中加载场景包配置。

    base_dir:
        - 若 pack_id 为相对路径，则会基于 base_dir 进行拼接；
        - 若 pack_id 为绝对路径，则忽略 base_dir。
    """

    def __init__(self, base_dir: Optional[Union[str, Path]] = None) -> None:
        self._base_dir: Optional[Path] = Path(base_dir) if base_dir is not None else None

    # ---------- 路径解析 ----------

    def _resolve_path(self, pack_id: str) -> Path:
        """
        将 pack_id 解析为实际文件路径。

        规则：
        - 若 pack_id 是绝对路径，直接返回；
        - 若 pack_id 是相对路径，且设置了 base_dir，则 base_dir / pack_id；
        - 若 pack_id 是相对路径，且未设置 base_dir，则使用当前工作目录为基准。
        """
        p = Path(pack_id)
        if p.is_absolute():
            return p

        if self._base_dir is not None:
            return (self._base_dir / p).resolve()

        return p.resolve()

    # ---------- JSON 解析与校验 ----------

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"Scene pack file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in scene pack file: {path}") from e

        if not isinstance(data, dict):
            raise ValueError(f"Scene pack root must be an object, got: {type(data).__name__}")

        return data

    def _validate_and_build_pack(self, data: Dict[str, Any]) -> ScenePack:
        """
        基本结构校验与 ScenePack 构建。

        必须字段：
        - scene: str
        - chains: dict[str, dict]

        可选字段：
        - tags: list[str]
        - version: str
        - default_chain: str
        """
        if "scene" not in data or not isinstance(data["scene"], str):
            raise ValueError("Scene pack must contain a non-empty 'scene' field of type str")

        scene: str = data["scene"].strip()
        if not scene:
            raise ValueError("Scene pack 'scene' cannot be empty")

        # tags
        tags_raw = data.get("tags", [])
        if tags_raw is None:
            tags_raw = []
        if not isinstance(tags_raw, list):
            raise ValueError("'tags' field must be a list if present")
        tags: List[str] = []
        for t in tags_raw:
            if not isinstance(t, str):
                raise ValueError("All elements in 'tags' must be str")
            t = t.strip()
            if t:
                tags.append(t)

        # version
        version = data.get("version", "1.0")
        if not isinstance(version, str):
            raise ValueError("'version' field must be a str if present")

        # chains
        chains_raw = data.get("chains")
        if not isinstance(chains_raw, dict) or not chains_raw:
            raise ValueError("Scene pack must contain non-empty 'chains' object")

        chains: Dict[str, Dict[str, Any]] = {}
        for chain_id, chain_cfg in chains_raw.items():
            if not isinstance(chain_id, str) or not chain_id.strip():
                raise ValueError("Chain id must be non-empty str")
            if not isinstance(chain_cfg, dict):
                raise ValueError(f"Chain '{chain_id}' value must be an object")
            chains[chain_id.strip()] = dict(chain_cfg)

        # default_chain
        default_chain = data.get("default_chain")
        if default_chain is not None:
            if not isinstance(default_chain, str) or not default_chain.strip():
                raise ValueError("'default_chain' must be a non-empty str when present")
            default_chain = default_chain.strip()
            if default_chain not in chains:
                raise ValueError(
                    f"default_chain '{default_chain}' not found in chains keys: {list(chains.keys())}"
                )

        pack = ScenePack(
            scene=scene,
            tags=tags,
            version=version,
            chains=chains,
            default_chain=default_chain,
            raw=data,
        )
        return pack

    # ---------- 对外 API ----------

    def load_from_file(self, path: Union[str, Path]) -> ScenePack:
        """
        从指定文件路径加载场景包配置。

        path 可以是绝对路径，也可以是相对路径。
        """
        path = Path(path)
        data = self._load_json(path)
        pack = self._validate_and_build_pack(data)
        return pack

    def load_for_registry_ref(self, ref: ScenePackRef) -> ScenePack:
        """
        根据 SceneRegistry 中的 ScenePackRef 加载场景包。

        - 使用 ref.pack_id 解析路径；
        - 校验 JSON 中的 scene 字段与 ref.key.scene 一致；
        -（暂不强制校验 tag，仅作为 hint）；
        """
        path = self._resolve_path(ref.pack_id)
        data = self._load_json(path)
        pack = self._validate_and_build_pack(data)

        # 校验 scene 一致性
        if pack.scene != ref.key.scene:
            raise ValueError(
                f"Scene mismatch: pack.scene={pack.scene!r}, "
                f"registry.scene={ref.key.scene!r}, path={path}"
            )

        # tag 目前不强制匹配，仅作为后续扩展点
        # 若未来要求严格校验 tag ∈ pack.tags，可在此处补充逻辑

        return pack
