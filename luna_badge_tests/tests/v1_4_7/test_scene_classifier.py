"""
测试：SceneClassifier 的场景识别与 Registry 集成行为。

覆盖点：
- OCR 中包含地铁站名 + 关键词 → 识别为 subway 场景 + 对应 tag；
- OCR 中包含医院相关词汇 → 识别为 hospital 场景；
- objects 中存在地铁相关标签 → 识别为 subway 场景；
- 与 SceneRegistry 集成：根据 scene/tag 找到对应 ScenePackRef；
- 无匹配时返回 scene=None；
- scene 不在 registry 中时 classify_with_registry 返回 None。
"""

from pathlib import Path

import pytest

from task_engine.scene.scene_classifier import SceneClassifier, SceneGuess
from task_engine.scene.scene_registry import SceneRegistry, ScenePackRef, SceneKey


@pytest.fixture
def classifier() -> SceneClassifier:
    # 使用默认配置即可
    return SceneClassifier(min_confidence=0.5)


def test_classify_subway_with_ocr_and_tag(classifier: SceneClassifier) -> None:
    ocr = "我现在在静安寺站这边，准备进地铁去人民广场。"

    guess: SceneGuess = classifier.classify(ocr_text=ocr)

    assert guess.scene == "subway"
    # 默认配置中为静安寺站配置了 tag alias
    assert guess.tag == "静安寺站"
    assert guess.confidence >= 0.5
    assert guess.scores["subway"] >= guess.scores["hospital"]


def test_classify_hospital_with_ocr_keywords(classifier: SceneClassifier) -> None:
    ocr = "我在医院门诊大厅，准备去挂号。"

    guess: SceneGuess = classifier.classify(ocr_text=ocr)

    assert guess.scene == "hospital"
    # 没有配置具体医院 tag 时，tag 应为空
    assert guess.tag is None
    assert guess.confidence >= 0.5
    assert guess.scores["hospital"] > 0.0


def test_classify_subway_with_objects_only(classifier: SceneClassifier) -> None:
    # 没有 OCR，仅靠 objects 推断
    # 使用更低的 min_confidence，因为仅靠 objects 得分可能不够高
    low_conf_classifier = SceneClassifier(min_confidence=0.1)
    objects = ["metro_sign", "escalator"]

    guess: SceneGuess = low_conf_classifier.classify(objects=objects)

    assert guess.scene == "subway"
    assert guess.confidence >= 0.2  # 来自 objects 的加分
    assert guess.tag is None


def test_classify_unknown_scene_returns_none(classifier: SceneClassifier) -> None:
    ocr = "今天在家里看电视，什么地铁医院都没去。"

    guess: SceneGuess = classifier.classify(ocr_text=ocr)

    # 文本中没有命中任何默认关键词，score 可能为 0
    # confidence < 0.5，scene 应为 None
    assert guess.scene is None
    assert guess.tag is None


def test_classify_with_registry_returns_tag_specific_pack(tmp_path: Path) -> None:
    classifier = SceneClassifier(min_confidence=0.5)
    registry = SceneRegistry()

    # 为 subway 注册默认包和静安寺站专属包
    default_ref = registry.register(scene="subway", pack_id="packs/subway/default.json", tag=None)
    jingan_ref = registry.register(scene="subway", pack_id="packs/subway/jingan_temple.json", tag="静安寺站")

    ocr = "我在静安寺站这边等你，一会儿一起进地铁。"

    ref = classifier.classify_with_registry(registry, ocr_text=ocr)

    # 由于 OCR 中命中"静安寺站"，应优先匹配 tag 场景包
    assert ref is not None
    assert isinstance(ref, ScenePackRef)
    assert ref.pack_id == jingan_ref.pack_id


def test_classify_with_registry_returns_none_when_scene_not_registered(tmp_path: Path) -> None:
    classifier = SceneClassifier(min_confidence=0.5)
    registry = SceneRegistry()

    # registry 中只注册 subway，没有 hospital
    registry.register(scene="subway", pack_id="packs/subway/default.json", tag=None)

    ocr = "我在医院门诊大厅准备挂号。"

    ref = classifier.classify_with_registry(registry, ocr_text=ocr)

    # classifier 会判断为 hospital，但 registry 中没有 hospital 注册
    assert ref is None

