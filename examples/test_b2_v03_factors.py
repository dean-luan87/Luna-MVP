# examples/test_b2_v03_factors.py

from pprint import pprint
import time

from vision_pipeline.b2.v03.factors import (
    build_factor_evidences,
    FactorType
)


def make_state(ts_offset, perception):
    return {
        "ts": time.time() + ts_offset,
        "perception": perception
    }


def run_test_case(name, future_states):
    print("\n" + "=" * 60)
    print(f"TEST CASE: {name}")
    print("=" * 60)

    evidences = build_factor_evidences(future_states)

    for k, v in evidences.items():
        print(
            f"[{k.value.upper():>6}] "
            f"score={v.score:.2f} "
            f"changed={v.changed} "
            f"reason={v.reason}"
        )

    if not evidences:
        print("NO FACTOR CHANGED")


if __name__ == "__main__":

    # =========================================================
    # Case 1: 环境稳定（什么都不该触发）
    # =========================================================
    run_test_case(
        "stable road",
        [
            make_state(1, {
                "path": {"surface": "concrete", "has_path": True},
                "env": {"scene": "road", "density": "low", "indoor": False},
                "people": {"count": 1, "moving": False},
                "events": []
            }),
            make_state(4, {
                "path": {"surface": "concrete", "has_path": True},
                "env": {"scene": "road", "density": "low", "indoor": False},
                "people": {"count": 1, "moving": False},
                "events": []
            }),
        ]
    )

    # =========================================================
    # Case 2: 路面变化（但世界未变）
    # =========================================================
    run_test_case(
        "path change only",
        [
            make_state(1, {
                "path": {"surface": "concrete", "has_path": True},
                "env": {"scene": "road", "density": "low", "indoor": False},
                "people": {"count": 2, "moving": False},
                "events": []
            }),
            make_state(6, {
                "path": {"surface": "gravel", "has_path": True},
                "env": {"scene": "road", "density": "low", "indoor": False},
                "people": {"count": 2, "moving": False},
                "events": []
            }),
        ]
    )

    # =========================================================
    # Case 3: 环境渐变（人群先变，场景后确认）
    # =========================================================
    run_test_case(
        "env transition via people",
        [
            make_state(1, {
                "path": {"surface": "concrete", "has_path": True},
                "env": {"scene": "road", "density": "low", "indoor": False},
                "people": {"count": 2, "moving": False},
                "events": []
            }),
            make_state(4, {
                "path": {"surface": "concrete", "has_path": True},
                "env": {"scene": "road", "density": "high", "indoor": False},
                "people": {"count": 8, "moving": True},
                "events": []
            }),
            make_state(7, {
                "path": {"surface": "concrete", "has_path": True},
                "env": {"scene": "market", "density": "high", "indoor": False},
                "people": {"count": 12, "moving": True},
                "events": []
            }),
        ]
    )

    # =========================================================
    # Case 4: 突发事件（必须立即触发）
    # =========================================================
    run_test_case(
        "sudden blocking event",
        [
            make_state(2, {
                "path": {"surface": "concrete", "has_path": True},
                "env": {"scene": "road", "density": "low", "indoor": False},
                "people": {"count": 2, "moving": False},
                "events": []
            }),
            make_state(5, {
                "path": {"surface": "concrete", "has_path": False},
                "env": {"scene": "road", "density": "mid", "indoor": False},
                "people": {"count": 5, "moving": True},
                "events": [
                    {"type": "construction", "severity": "high"}
                ]
            }),
        ]
    )
