# scripts/demo_v144.py
from decision_core.builder_v144 import build_decision_core_v144
from decision_core.decision_core import DecisionRequest


if __name__ == "__main__":
    core = build_decision_core_v144()

    print("=" * 60)
    print("Luna Badge v1.4.4 Demo")
    print("=" * 60)
    print()

    # 测试 1: 新任务
    print("测试 1: 新任务")
    req = DecisionRequest(
        user_id="u1",
        utterance="我想去医院看病",
        extra={"scene_type": "outdoor"},
    )
    reply = core.handle(req)
    print(f"用户: {req.utterance}")
    print(f"助手: {reply}")
    print()

    # 测试 2: 暂停任务
    print("测试 2: 暂停任务")
    req2 = DecisionRequest(
        user_id="u1",
        utterance="暂停",
        extra={},
    )
    reply2 = core.handle(req2)
    print(f"用户: {req2.utterance}")
    print(f"助手: {reply2}")
    print()

    # 测试 3: 继续任务
    print("测试 3: 继续任务")
    req3 = DecisionRequest(
        user_id="u1",
        utterance="继续",
        extra={},
    )
    reply3 = core.handle(req3)
    print(f"用户: {req3.utterance}")
    print(f"助手: {reply3}")
    print()

    # 测试 4: 取消任务（带确认）
    print("测试 4: 取消任务（带确认）")
    req4 = DecisionRequest(
        user_id="u1",
        utterance="不用去了",
        extra={},
    )
    reply4 = core.handle(req4)
    print(f"用户: {req4.utterance}")
    print(f"助手: {reply4}")
    print()

    # 测试 5: 确认取消
    print("测试 5: 确认取消")
    req5 = DecisionRequest(
        user_id="u1",
        utterance="是的",
        extra={},
    )
    reply5 = core.handle(req5)
    print(f"用户: {req5.utterance}")
    print(f"助手: {reply5}")
    print()

    print("=" * 60)
    print("✅ Demo 完成")
    print("=" * 60)

