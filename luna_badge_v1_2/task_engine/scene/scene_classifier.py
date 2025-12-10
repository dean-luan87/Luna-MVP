from __future__ import annotations

"""
SceneClassifier: 场景识别（地铁 / 医院 / 商场等），输出 SceneGuess。

职责（v1 版本）：
- 基于 OCR 文本、识别到的物体标签（YOLO 等）、可选的 GPS 文本提示，推断当前场景与场景标签；
- 输出 SceneGuess（scene, tag, confidence, scores）；
- 提供基于 SceneRegistry 的集成方法 classify_with_registry，用于直接拿到 ScenePackRef。

设计原则：
- 规则 + 评分机制（可配置），默认内置 subway / hospital 的关键字与标签；
- 不做外部 API 调用（GPS 只作为字符串 hint），后续可以在此基础上替换为更智能的实现。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from task_engine.scene.scene_registry import SceneRegistry, ScenePackRef


@dataclass
class SceneGuess:
    """
    场景识别结果。

    - scene: 场景主类，例如 "subway"、"hospital"，没有足够信心时为 None；
    - tag: 场景标签，例如 "静安寺站"、"虹口医院"，若无法判断则为 None；
    - confidence: [0, 1] 区间的置信度；
    - scores: 评分细节，例如：
        {
            "subway": 0.9,
            "hospital": 0.3
        }
    """

    scene: Optional[str]
    tag: Optional[str]
    confidence: float
    scores: Dict[str, float] = field(default_factory=dict)


class SceneClassifier:
    """
    场景识别器。

    输入：
        - ocr_text: OCR 识别到的文本（整段）；
        - objects: 识别到的物体标签列表（如 YOLO 输出的类别名）；
        - gps_hint: 与位置相关的文本提示（如某个地名、POI 名称的字符串）；
        - history_tags: 历史访问过的场景标签（简单用于加一点权重）。

    输出：
        - SceneGuess（scene, tag, confidence, scores）

    可配置：
        - scene_keywords: 每个 scene 对应的一组"场景关键字"（出现在 OCR / gps_hint）；
        - scene_objects: 每个 scene 对应的一组"物体标签关键字"（出现在 objects）；
        - tag_aliases:   每个 scene 下，tag 对应的一组"别名关键字"（出现在 OCR / gps_hint）。
    """

    def __init__(
        self,
        *,
        scene_keywords: Optional[Dict[str, List[str]]] = None,
        scene_objects: Optional[Dict[str, List[str]]] = None,
        tag_aliases: Optional[Dict[str, Dict[str, List[str]]]] = None,
        min_confidence: float = 0.5,
    ) -> None:
        # 默认关键字配置：可以后续在构建时注入覆盖
        self._scene_keywords: Dict[str, List[str]] = scene_keywords or {
            "subway": ["地铁", "地铁站", "号线", "站台"],
            "hospital": ["医院", "挂号", "门诊", "急诊", "护士站"],
        }

        self._scene_objects: Dict[str, List[str]] = scene_objects or {
            "subway": ["metro_sign", "rail", "platform", "ticket_gate"],
            "hospital": ["hospital_sign", "red_cross", "nurse", "register_desk"],
        }

        # tag_aliases[scene][tag] = [alias1, alias2, ...]
        self._tag_aliases: Dict[str, Dict[str, List[str]]] = tag_aliases or {
            "subway": {
                "静安寺站": ["静安寺站", "静安寺 地铁"],
            },
            "hospital": {
                "虹口医院": ["虹口医院", "虹口 区 中心 医院"],
            },
        }

        self._min_confidence: float = float(min_confidence)

    # ---------- 公共 API ----------

    def classify(
        self,
        *,
        ocr_text: Optional[str] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
        history_tags: Optional[List[str]] = None,
    ) -> SceneGuess:
        """
        规则 + 评分方式进行场景识别。

        评分策略（v1 版本）：
        - OCR / gps_hint 中命中 tag alias：+0.6（tag 对应 scene 同时受益）；
        - OCR / gps_hint 中命中 scene 关键字：每命中一次 +0.3（累加，最大不超过 1.0）；
        - objects 中命中 scene 物体标签：每命中一次 +0.2（累加，最大不超过 1.0）；
        - history_tags 命中 tag：+0.2（小权重，鼓励历史使用场景）。

        最终：
        - confidence = 该 scene 的总分（上限 1.0）；
        - 若最高分 < min_confidence，则返回 scene=None / tag=None。
        """
        ocr_text = (ocr_text or "").strip()
        gps_hint = (gps_hint or "").strip()
        objects = objects or []
        history_tags = history_tags or []

        # 统一小写处理英文部分，中文不影响
        merged_text = (ocr_text + " " + gps_hint).strip()

        # 初始化分数结构
        scene_scores: Dict[str, float] = {scene: 0.0 for scene in self._scene_keywords.keys()}
        tag_scores: Dict[str, Dict[str, float]] = {
            scene: {tag: 0.0 for tag in tags.keys()} for scene, tags in self._tag_aliases.items()
        }

        # 1) tag alias 匹配（OCR + gps_hint）
        if merged_text:
            for scene, tags in self._tag_aliases.items():
                for tag, aliases in tags.items():
                    for alias in aliases:
                        if alias and alias in merged_text:
                            # tag 被命中，对应 scene 加 0.6，tag 自身加 0.6
                            scene_scores.setdefault(scene, 0.0)
                            scene_scores[scene] += 0.6
                            tag_scores.setdefault(scene, {})
                            tag_scores[scene].setdefault(tag, 0.0)
                            tag_scores[scene][tag] += 0.6

        # 2) scene 关键字匹配（OCR + gps_hint）
        if merged_text:
            for scene, keywords in self._scene_keywords.items():
                for kw in keywords:
                    if kw and kw in merged_text:
                        scene_scores.setdefault(scene, 0.0)
                        scene_scores[scene] += 0.3

        # 3) objects 物体标签匹配
        if objects:
            obj_set = set(objects)
            for scene, obj_keywords in self._scene_objects.items():
                for ok in obj_keywords:
                    if ok in obj_set:
                        scene_scores.setdefault(scene, 0.0)
                        scene_scores[scene] += 0.2

        # 4) 历史 tag 匹配
        for scene, tags in self._tag_aliases.items():
            for tag in tags.keys():
                if tag in history_tags:
                    scene_scores.setdefault(scene, 0.0)
                    scene_scores[scene] += 0.2
                    tag_scores.setdefault(scene, {})
                    tag_scores[scene].setdefault(tag, 0.0)
                    tag_scores[scene][tag] += 0.2

        # 分数裁剪到 [0, 1]
        for scene in list(scene_scores.keys()):
            scene_scores[scene] = max(0.0, min(1.0, scene_scores[scene]))

        # 找出最高分 scene
        best_scene: Optional[str] = None
        best_score: float = 0.0
        for scene, score in scene_scores.items():
            if score > best_score:
                best_score = score
                best_scene = scene

        if best_scene is None or best_score < self._min_confidence:
            # 没有足够信心的场景
            return SceneGuess(scene=None, tag=None, confidence=best_score, scores=scene_scores)

        # 在该 scene 下，尝试选择最高分的 tag
        best_tag: Optional[str] = None
        per_scene_tags = tag_scores.get(best_scene, {})
        best_tag_score = 0.0
        for tag, score in per_scene_tags.items():
            if score > best_tag_score:
                best_tag_score = score
                best_tag = tag

        # 如果 tag 分太低，也可以选择忽略 tag（这里简单策略：>0 即保留）
        if best_tag_score <= 0.0:
            best_tag = None

        return SceneGuess(
            scene=best_scene,
            tag=best_tag,
            confidence=best_score,
            scores=scene_scores,
        )

    def classify_with_registry(
        self,
        registry: SceneRegistry,
        *,
        ocr_text: Optional[str] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
        history_tags: Optional[List[str]] = None,
        require_registered: bool = False,
    ) -> Optional[ScenePackRef]:
        """
        在 classify 的基础上，通过 SceneRegistry 找到对应的 ScenePackRef。

        :param registry: 已注册的 SceneRegistry 实例
        :param require_registered:
            - True: 若找不到对应 ScenePackRef，则返回 None；
            - False: 与 True 相同（当前语义一致，预留未来扩展）。
        """
        guess = self.classify(
            ocr_text=ocr_text,
            objects=objects,
            gps_hint=gps_hint,
            history_tags=history_tags,
        )

        if guess.scene is None:
            return None

        # 先尝试 scene + tag 精确匹配，找不到则回落默认
        ref = registry.get(guess.scene, guess.tag)
        if ref is None and not require_registered:
            return None

        return ref
