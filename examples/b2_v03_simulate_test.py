# examples/b2_v03_simulate_test.py

import time
from vision_pipeline.b2.v03.b2_v03 import B2v03


def fake_perception(path=None, env=None, people=None, events=None):
    """
    构造一个 perception 快照（符合 factors.py 期望的格式）
    """
    return {
        "path": path or {"surface": "concrete", "has_path": True},
        "env": env or {"scene": "road", "density": "low", "indoor": False},
        "people": people or {"count": 1, "moving": False},
        "events": events or []
    }


def run_simulation():
    # 使用实时模式（因为模拟测试没有视频时间轴）
    b2 = B2v03(debug=True, log_mode="realtime")

    base_ts = time.time()

    # 模拟一个连续的时间线，后面的 tick 能看到前面的帧
    # 窗口是 [now+1s, now+8s]，所以我们需要足够多的帧来填充窗口
    
    timeline = [
        # ---- 稳定马路（多帧累积）----
        (0.0, fake_perception(
            path={"surface": "concrete", "has_path": True},
            env={"scene": "road", "density": "low", "indoor": False},
            people={"count": 1, "moving": False},
        )),
        (1.0, fake_perception(
            path={"surface": "concrete", "has_path": True},
            env={"scene": "road", "density": "low", "indoor": False},
            people={"count": 1, "moving": False},
        )),
        (2.0, fake_perception(
            path={"surface": "concrete", "has_path": True},
            env={"scene": "road", "density": "low", "indoor": False},
            people={"count": 1, "moving": False},
        )),
        (3.0, fake_perception(
            path={"surface": "concrete", "has_path": True},
            env={"scene": "road", "density": "low", "indoor": False},
            people={"count": 1, "moving": False},
        )),

        # ---- 路面变化 ----
        (4.0, fake_perception(
            path={"surface": "gravel", "has_path": True},
            env={"scene": "road", "density": "low", "indoor": False},
            people={"count": 2, "moving": False},
        )),
        (5.0, fake_perception(
            path={"surface": "gravel", "has_path": True},
            env={"scene": "road", "density": "low", "indoor": False},
            people={"count": 2, "moving": False},
        )),

        # ---- 人群 & 环境变化 ----
        (6.0, fake_perception(
            path={"surface": "gravel", "has_path": True},
            env={"scene": "market", "density": "high", "indoor": False},
            people={"count": 8, "moving": True},
        )),
        (7.0, fake_perception(
            path={"surface": "gravel", "has_path": True},
            env={"scene": "market", "density": "high", "indoor": False},
            people={"count": 12, "moving": True},
        )),

        # ---- 突发事件 ----
        (8.0, fake_perception(
            path={"surface": "concrete", "has_path": False},
            env={"scene": "road", "density": "mid", "indoor": False},
            people={"count": 5, "moving": True},
            events=[{"type": "construction", "severity": "high"}]
        )),
        (9.0, fake_perception(
            path={"surface": "concrete", "has_path": False},
            env={"scene": "road", "density": "mid", "indoor": False},
            people={"count": 5, "moving": True},
            events=[{"type": "construction", "severity": "high"}]
        )),
    ]

    print("=" * 60)
    print("B2 v0.3 模拟 tick 测试")
    print("=" * 60)
    print()

    for offset, perception in timeline:
        ts = base_ts + offset
        print(f"[TICK] ts={ts:.2f} (offset={offset:.1f}s)")
        
        result = b2.tick(ts, perception)

        if result:
            print("\n=== B2 OUTPUT ===")
            print(f"  level: {result['level']}")
            print(f"  main_factor: {result['main_factor']}")
            print(f"  factors: {list(result['factors'].keys())}")
            print()
        else:
            print("  (no output)\n")


if __name__ == "__main__":
    run_simulation()

