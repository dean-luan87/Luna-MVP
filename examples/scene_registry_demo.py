# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Registry 最小使用示例

目标：
- 验证状态机与渐变切换
- 验证稳定性闸门
- 验证候选逻辑

运行方式：
python examples/scene_registry_demo.py
"""

import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world_model.scene.scene_registry import SceneRegistry, SceneAnchors, EnvironmentContext
from core.world_model.scene.scene_types import SceneSegment, SceneGeometry
from core.world_model.scene.position_state import PositionState


def main():
    """主函数：演示 SceneRegistry 的状态机"""
    
    # 创建场景段
    scenes = [
        SceneSegment(
            "A",
            SceneGeometry("RECT", {"x1": 0, "y1": 0, "x2": 10, "y2": 10}),
            "sidewalk",
            ["B"],
            ["rain_sensitive"],
            []
        ),
        SceneSegment(
            "B",
            SceneGeometry("RECT", {"x1": 10, "y1": 0, "x2": 20, "y2": 10}),
            "crossing",
            ["A"],
            ["low_visibility"],
            []
        ),
    ]

    # 初始化 SceneRegistry
    reg = SceneRegistry(scenes)
    env = EnvironmentContext(season="WINTER", time_of_day="DAY", weather="CLEAR")

    print("=" * 70)
    print("Scene Registry 状态机演示")
    print("=" * 70)
    print()

    # 1. 稳定位置，在 Scene A
    print("1️⃣ 稳定位置，在 Scene A")
    print("-" * 70)
    ps = PositionState((2, 2), stability_score=0.9)
    st = reg.update(ps, SceneAnchors(), env)
    print(f"  Active: {st.active_scene_id}, Relevance: {st.active_relevance:.2f}")
    print(f"  Candidate: {st.candidate_scene_id}, Relevance: {st.candidate_relevance:.2f}")
    print(f"  Position Stable: {st.position_stable}")
    print()

    # 2. 移动到 Scene B（渐变切换）
    print("2️⃣ 移动到 Scene B（渐变切换）")
    print("-" * 70)
    ps = PositionState((12, 2), stability_score=0.9)
    for i in range(10):
        st = reg.update(ps, SceneAnchors(), env)
        print(f"  Step {i+1}: Active={st.active_scene_id} (rel={st.active_relevance:.2f}), "
              f"Candidate={st.candidate_scene_id} (rel={st.candidate_relevance:.2f})")
        time.sleep(0.1)
    print()

    # 3. 不稳定位置：冻结演化
    print("3️⃣ 不稳定位置：冻结演化")
    print("-" * 70)
    ps = PositionState((12, 2), stability_score=0.2)
    st = reg.update(ps, SceneAnchors(), env)
    print(f"  Active: {st.active_scene_id}, Relevance: {st.active_relevance:.2f}")
    print(f"  Candidate: {st.candidate_scene_id}, Relevance: {st.candidate_relevance:.2f}")
    print(f"  Position Stable: {st.position_stable}")
    print()

    print("=" * 70)
    print("✅ 演示完成")
    print("=" * 70)


if __name__ == "__main__":
    main()


