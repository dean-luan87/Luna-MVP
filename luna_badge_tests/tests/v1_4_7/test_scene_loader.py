"""
测试：ScenePackLoader 加载 JSON 场景包的行为。

覆盖点：
- 从文件路径加载场景包（load_from_file）
- 基本字段解析（scene/tags/version/chains/default_chain）
- 结构错误时报错
- 与 SceneRegistry/ScenePackRef 集成（load_for_registry_ref）
- scene 不匹配时抛异常
"""

from pathlib import Path
import json
import pytest

from task_engine.scene.scene_pack_loader import ScenePackLoader, ScenePack
from task_engine.scene.scene_registry import SceneRegistry, ScenePackRef, SceneKey


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@pytest.fixture
def tmp_scene_dir(tmp_path: Path) -> Path:
    """为每个测试提供一个独立的临时目录，用于存放场景包 JSON。"""
    return tmp_path


def test_load_from_file_minimal_pack(tmp_scene_dir: Path) -> None:
    path = tmp_scene_dir / "subway_pack.json"
    data = {
        "scene": "subway",
        "tags": ["静安寺站"],
        "version": "1.0",
        "default_chain": "go_to_platform",
        "chains": {
            "go_to_platform": {
                "description": "前往地铁站台",
                "steps": [
                    {"action": "navigate", "target": "entrance"},
                    {"action": "follow_sign", "target": "Line1"},
                    {"action": "go_downstairs"},
                    {"action": "reach", "target": "platform"},
                ],
            },
            "find_toilet": {
                "description": "去洗手间",
                "steps": [
                    {"action": "navigate", "target": "toilet_sign"},
                    {"action": "follow_sign"},
                ],
            },
        },
    }
    _write_json(path, data)

    loader = ScenePackLoader()
    pack = loader.load_from_file(path)

    assert isinstance(pack, ScenePack)
    assert pack.scene == "subway"
    assert pack.tags == ["静安寺站"]
    assert pack.version == "1.0"
    assert pack.default_chain == "go_to_platform"
    assert "go_to_platform" in pack.chains
    assert "find_toilet" in pack.chains
    assert pack.raw["scene"] == "subway"


def test_load_from_file_missing_scene_raises(tmp_scene_dir: Path) -> None:
    path = tmp_scene_dir / "invalid_pack.json"
    data = {
        # "scene" 缺失
        "chains": {
            "dummy": {"steps": []},
        },
    }
    _write_json(path, data)

    loader = ScenePackLoader()
    with pytest.raises(ValueError):
        loader.load_from_file(path)


def test_load_from_file_missing_chains_raises(tmp_scene_dir: Path) -> None:
    path = tmp_scene_dir / "invalid_pack2.json"
    data = {
        "scene": "subway",
        # "chains" 缺失
    }
    _write_json(path, data)

    loader = ScenePackLoader()
    with pytest.raises(ValueError):
        loader.load_from_file(path)


def test_load_from_file_default_chain_must_exist(tmp_scene_dir: Path) -> None:
    path = tmp_scene_dir / "invalid_pack3.json"
    data = {
        "scene": "subway",
        "default_chain": "not_exist",
        "chains": {
            "go_to_platform": {"steps": []},
        },
    }
    _write_json(path, data)

    loader = ScenePackLoader()
    with pytest.raises(ValueError):
        loader.load_from_file(path)


def test_load_for_registry_ref_with_matching_scene(tmp_scene_dir: Path) -> None:
    # 1. 准备场景包 JSON
    path = tmp_scene_dir / "hospital_pack.json"
    data = {
        "scene": "hospital",
        "tags": ["虹口医院"],
        "chains": {
            "register": {
                "description": "挂号",
                "steps": [
                    {"action": "goto", "target": "register_counter"},
                    {"action": "queue"},
                ],
            }
        },
    }
    _write_json(path, data)

    # 2. 准备 ScenePackRef（模拟 registry 注册结果）
    key = SceneKey(scene="hospital", tag="虹口医院")
    ref = ScenePackRef(key=key, pack_id=str(path), meta={})

    # 3. 加载
    loader = ScenePackLoader()
    pack = loader.load_for_registry_ref(ref)

    assert pack.scene == "hospital"
    assert "register" in pack.chains
    assert "steps" in pack.chains["register"]


def test_load_for_registry_ref_scene_mismatch_raises(tmp_scene_dir: Path) -> None:
    # JSON 中场景为 subway
    path = tmp_scene_dir / "mismatch_pack.json"
    data = {
        "scene": "subway",
        "chains": {
            "go_to_platform": {"steps": []},
        },
    }
    _write_json(path, data)

    key = SceneKey(scene="hospital", tag=None)
    ref = ScenePackRef(key=key, pack_id=str(path), meta={})

    loader = ScenePackLoader()
    with pytest.raises(ValueError):
        loader.load_for_registry_ref(ref)
