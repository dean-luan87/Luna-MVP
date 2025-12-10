"""
Demo: Vision → Scene → Task 推荐链路

功能：本地直接跑一遍 Vision → Scene → Task 推荐链路，打印结果。

不依赖 HTTP / WebSocket，不强依赖 TaskChainManager。
"""

import sys
import os
import time
from typing import Optional, List

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.vision.vision_event import VisionEvent
from task_engine.vision.scene_observer import SceneObserver
from task_engine.vision.vision_scene_bridge import VisionSceneTaskBridge
from task_engine.scene.scene_classifier import SceneClassifier
from task_engine.scene.scene_context import SceneContext
from task_engine.scene.scene_task_binder import create_default_scene_task_binder
from task_engine.scene.scene_classifier import SceneGuess


# === DummySceneClassifier: 用规则模拟一个最小可用的场景分类器 ===


class DummySceneClassifier(SceneClassifier):
    """
    最小可用版本：

    - 文本包含"地铁"或 objects 里有 'gate' → subway
    - 文本包含"医院" → hospital
    """

    def classify(
        self,
        *,
        ocr_text: Optional[str] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
        history_tags: Optional[List[str]] = None,
    ) -> SceneGuess:
        text = (ocr_text or "").lower()
        obj_list = objects or []

        if "地铁" in text or "gate" in obj_list:
            return SceneGuess(
                scene="subway",
                tag="generic_subway",
                confidence=0.9,
                scores={"rule": 0.9},
            )
        if "医院" in text:
            return SceneGuess(
                scene="hospital",
                tag="generic_hospital",
                confidence=0.9,
                scores={"rule": 0.9},
            )
        return SceneGuess(
            scene=None,
            tag=None,
            confidence=0.0,
            scores={},
        )


def run_demo():
    print("=== Vision → Scene → Task Demo ===")

    # 1. 准备场景上下文 & 分类器
    ctx = SceneContext()
    clf = DummySceneClassifier()
    observer = SceneObserver(classifier=clf, context=ctx)
    binder = create_default_scene_task_binder()
    bridge = VisionSceneTaskBridge(observer=observer, binder=binder)

    # 2. 模拟三个场景事件
    events = [
        VisionEvent(
            ocr_lines=["静安寺地铁站"],
            objects=["gate"],
            source="camera_front",
        ),
        VisionEvent(
            ocr_lines=["虹口医院门诊部"],
            objects=[],
            source="camera_front",
        ),
        VisionEvent(
            ocr_lines=["城市公园草地"],
            objects=["tree"],
            source="camera_front",
        ),
    ]

    for i, ev in enumerate(events, start=1):
        print(f"\n--- Event #{i} ---")
        print(f"OCR: {' / '.join(ev.ocr_lines)}")
        print(f"Objects: {ev.objects}")
        result = bridge.handle_vision_event(ev)

        print(f"Scene: {result.scene}, tag: {result.tag}, conf: {result.confidence:.2f}")
        print(f"Reason: {result.reason}")
        if result.suggested_task_meta:
            print("Suggested task_meta:")
            for k, v in result.suggested_task_meta.items():
                print(f"  - {k}: {v}")
        else:
            print("No task suggested for this event.")

        time.sleep(0.1)

    print("\n=== Demo Finished ===")


if __name__ == "__main__":
    run_demo()

