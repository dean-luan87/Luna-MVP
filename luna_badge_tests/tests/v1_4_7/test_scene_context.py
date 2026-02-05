"""
测试：SceneContext 与 SceneContextManager 的行为。

覆盖点：
- 基于 SceneGuess + ScenePackRef 构建 SceneContext；
- update_from_guess 的更新与 history_tags 追加逻辑；
- has_scene_changed 的场景变化判断；
- attach_environment / attach_user_intent 的元数据合并逻辑；
- to_dict 的结构与 pack_ref/时间字段转换；
- SceneContextManager 的 get/set/clear 行为。
"""

from datetime import datetime
from typing import Optional

from task_engine.scene.scene_classifier import SceneGuess
from task_engine.scene.scene_context import SceneContext, SceneContextManager, scene_context_manager
from task_engine.scene.scene_registry import SceneKey, ScenePackRef


def _make_guess(scene: Optional[str], tag: Optional[str], confidence: float) -> SceneGuess:
    return SceneGuess(scene=scene, tag=tag, confidence=confidence, scores={scene or "unknown": confidence})


def _make_pack_ref(scene: str, tag: Optional[str], pack_id: str = "packs/demo.json") -> ScenePackRef:
    key = SceneKey(scene=scene, tag=tag)
    return ScenePackRef(key=key, pack_id=pack_id, meta={"source": "test"})


def test_context_from_guess_and_pack_ref() -> None:
    guess = _make_guess("subway", "静安寺站", 0.9)
    pack_ref = _make_pack_ref("subway", "静安寺站")

    ctx = SceneContext.from_guess(
        guess,
        pack_ref=pack_ref,
        ocr_text="我在静安寺站这边。",
        objects=["metro_sign"],
        gps_hint="静安寺地铁站",
        history_tags=["静安寺站"],
        metadata={"foo": "bar"},
    )

    assert ctx.scene == "subway"
    assert ctx.tag == "静安寺站"
    assert ctx.confidence == 0.9
    assert ctx.pack_ref is pack_ref
    assert ctx.ocr_text == "我在静安寺站这边。"
    assert "metro_sign" in ctx.objects
    assert ctx.gps_hint == "静安寺地铁站"
    assert "静安寺站" in ctx.history_tags
    assert ctx.metadata["foo"] == "bar"
    assert isinstance(ctx.last_updated_at, datetime)


def test_update_from_guess_appends_history_tag() -> None:
    guess1 = _make_guess("subway", "静安寺站", 0.8)
    pack_ref1 = _make_pack_ref("subway", "静安寺站")

    # 初始创建时传入 history_tags，包含 "静安寺站"
    ctx = SceneContext.from_guess(guess1, pack_ref=pack_ref1, history_tags=["静安寺站"])

    # 新的 guess，tag 不同
    guess2 = _make_guess("subway", "人民广场站", 0.85)
    pack_ref2 = _make_pack_ref("subway", "人民广场站")

    ctx.update_from_guess(
        guess2,
        pack_ref=pack_ref2,
        ocr_text="我到了人民广场站。",
        objects=["metro_sign", "escalator"],
        gps_hint="人民广场",
        append_history_tag=True,
    )

    assert ctx.scene == "subway"
    assert ctx.tag == "人民广场站"
    assert ctx.pack_ref is pack_ref2
    assert "人民广场站" in ctx.history_tags
    # 原来的 tag 也应存在（因为 update_from_guess 会追加，不会覆盖）
    assert "静安寺站" in ctx.history_tags
    assert ctx.ocr_text == "我到了人民广场站。"
    assert "escalator" in ctx.objects
    assert ctx.gps_hint == "人民广场"
    assert isinstance(ctx.last_updated_at, datetime)


def test_has_scene_changed_compares_scene_tag_and_confidence() -> None:
    guess1 = _make_guess("subway", "静安寺站", 0.8)
    ctx = SceneContext.from_guess(guess1)

    # scene / tag 完全相同，置信度变化在阈值内
    guess_same = _make_guess("subway", "静安寺站", 0.85)
    assert ctx.has_scene_changed(guess_same, confidence_delta_threshold=0.1) is False

    # 置信度变化超过阈值
    guess_diff_conf = _make_guess("subway", "静安寺站", 0.3)
    assert ctx.has_scene_changed(guess_diff_conf, confidence_delta_threshold=0.1) is True

    # scene 不同
    guess_other_scene = _make_guess("hospital", "虹口医院", 0.9)
    assert ctx.has_scene_changed(guess_other_scene) is True

    # tag 不同
    guess_other_tag = _make_guess("subway", "人民广场站", 0.8)
    assert ctx.has_scene_changed(guess_other_tag) is True


def test_attach_environment_and_user_intent() -> None:
    guess = _make_guess("hospital", "虹口医院", 0.9)
    ctx = SceneContext.from_guess(guess)

    ctx.attach_environment({"light": "low", "noise": "high"})
    ctx.attach_environment({"network": "4G"})

    env = ctx.metadata.get("environment")
    assert isinstance(env, dict)
    assert env["light"] == "low"
    assert env["noise"] == "high"
    assert env["network"] == "4G"

    ctx.attach_user_intent({"goal": "挂号", "priority": "high"})
    ctx.attach_user_intent({"sub_goal": "先找咨询台"})

    intent = ctx.metadata.get("user_intent")
    assert isinstance(intent, dict)
    assert intent["goal"] == "挂号"
    assert intent["priority"] == "high"
    assert intent["sub_goal"] == "先找咨询台"


def test_to_dict_serialization() -> None:
    guess = _make_guess("hospital", "虹口医院", 0.95)
    pack_ref = _make_pack_ref("hospital", "虹口医院", pack_id="packs/hospital/hongkou.json")

    ctx = SceneContext.from_guess(guess, pack_ref=pack_ref)
    ctx.attach_environment({"light": "medium"})

    data = ctx.to_dict()

    assert data["scene"] == "hospital"
    assert data["tag"] == "虹口医院"
    assert data["confidence"] == 0.95
    assert isinstance(data["pack_ref"], dict)
    assert data["pack_ref"]["pack_id"] == "packs/hospital/hongkou.json"
    assert "last_updated_at" in data
    assert isinstance(data["metadata"], dict)
    assert "environment" in data["metadata"]


def test_scene_context_manager_get_set_clear() -> None:
    manager = SceneContextManager()

    assert manager.get_current() is None

    guess = _make_guess("subway", "静安寺站", 0.9)
    ctx = SceneContext.from_guess(guess)

    manager.set_current(ctx)
    current = manager.get_current()
    assert current is ctx

    manager.clear()
    assert manager.get_current() is None

    # 验证模块级单例可用
    scene_context_manager.clear()
    scene_context_manager.set_current(ctx)
    assert scene_context_manager.get_current() is ctx
    scene_context_manager.clear()
    assert scene_context_manager.get_current() is None

