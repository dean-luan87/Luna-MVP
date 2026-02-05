"""
测试：SceneRegistry 注册与查询行为。

覆盖点：
- 默认场景包（tag=None）注册与查找
- tag 级别场景包注册与查找
- 精确匹配 + 默认回落逻辑
- list_scenes / list_tags 行为
- overwrite 标志行为
"""

import pytest

from task_engine.scene.scene_registry import SceneRegistry, scene_registry, ScenePackRef


@pytest.fixture
def fresh_registry() -> SceneRegistry:
    """每个测试用一个全新的 registry 实例，避免状态污染。"""
    reg = SceneRegistry()
    return reg


def test_register_and_get_default_scene_pack(fresh_registry: SceneRegistry) -> None:
    reg = fresh_registry

    ref = reg.register(scene="subway", pack_id="packs/subway/scene_pack.json")

    assert ref.key.scene == "subway"
    assert ref.key.tag is None
    assert ref.pack_id == "packs/subway/scene_pack.json"

    found = reg.get("subway")
    assert found is not None
    assert found.pack_id == "packs/subway/scene_pack.json"


def test_register_tag_specific_scene_pack_and_fallback(fresh_registry: SceneRegistry) -> None:
    reg = fresh_registry

    # 默认地铁场景包
    reg.register(scene="subway", pack_id="packs/subway/default.json", tag=None)

    # 静安寺站专属包
    reg.register(scene="subway", pack_id="packs/subway/jingan_temple.json", tag="静安寺站")

    # 精确匹配 tag
    ref_tag = reg.get("subway", tag="静安寺站")
    assert ref_tag is not None
    assert ref_tag.pack_id == "packs/subway/jingan_temple.json"

    # 其他 tag（未注册）应回落默认
    ref_default = reg.get("subway", tag="人民广场站")
    assert ref_default is not None
    assert ref_default.pack_id == "packs/subway/default.json"

    # 不带 tag 时，也应该返回默认
    ref_without_tag = reg.get("subway")
    assert ref_without_tag is not None
    assert ref_without_tag.pack_id == "packs/subway/default.json"


def test_require_raises_when_not_found(fresh_registry: SceneRegistry) -> None:
    reg = fresh_registry

    with pytest.raises(KeyError):
        reg.require("hospital")

    reg.register(scene="hospital", pack_id="packs/hospital/default.json")
    assert reg.require("hospital").pack_id == "packs/hospital/default.json"


def test_list_scenes_and_tags(fresh_registry: SceneRegistry) -> None:
    reg = fresh_registry

    reg.register(scene="subway", pack_id="packs/subway/default.json")
    reg.register(scene="subway", pack_id="packs/subway/jingan_temple.json", tag="静安寺站")
    reg.register(scene="hospital", pack_id="packs/hospital/default.json")
    reg.register(scene="hospital", pack_id="packs/hospital/hongkou.json", tag="虹口医院")

    scenes = reg.list_scenes()
    assert scenes == ["hospital", "subway"]

    subway_tags = reg.list_tags("subway")
    assert subway_tags == ["静安寺站"]

    hospital_tags = reg.list_tags("hospital")
    assert hospital_tags == ["虹口医院"]

    # 未知 scene 返回空列表
    assert reg.list_tags("mall") == []


def test_overwrite_flag_controls_replace_behavior(fresh_registry: SceneRegistry) -> None:
    reg = fresh_registry

    ref1 = reg.register(scene="subway", pack_id="packs/subway/v1.json", tag=None, overwrite=True)
    assert reg.get("subway").pack_id == "packs/subway/v1.json"

    # overwrite=False 时不覆盖
    ref2 = reg.register(scene="subway", pack_id="packs/subway/v2.json", tag=None, overwrite=False)
    # 返回的是旧的 ref1
    assert ref2 is ref1
    assert reg.get("subway").pack_id == "packs/subway/v1.json"

    # overwrite=True 时覆盖
    ref3 = reg.register(scene="subway", pack_id="packs/subway/v3.json", tag=None, overwrite=True)
    assert reg.get("subway").pack_id == "packs/subway/v3.json"
    assert ref3 is not ref1


def test_module_level_scene_registry_can_be_used() -> None:
    # 使用模块级单例注册一个简单场景包（测试不会依赖其初始状态）
    scene_registry.clear()
    scene_registry.register(scene="subway", pack_id="packs/subway/scene_pack.json")

    ref = scene_registry.get("subway")
    assert ref is not None
    assert ref.pack_id == "packs/subway/scene_pack.json"

    scene_registry.clear()
