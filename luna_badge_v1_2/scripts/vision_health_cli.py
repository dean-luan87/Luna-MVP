"""
Vision Health CLI: 视觉健康命令行调试工具

用于本地调试和查看模型健康状态。
"""

import sys
import os
from pprint import pprint

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.multi_model_engine import MultiModelEngine, ModelSpec
from core.vision.vision_debug_service import VisionDebugService
from core.vision.vision_task_orchestrator import VisionTask


def fake_good(task: VisionTask):
    """模拟高成功率模型"""
    return [{"label": "person", "score": 0.9}]


def fake_bad(task: VisionTask):
    """模拟低成功率模型"""
    raise RuntimeError("fail")


def fake_medium(task: VisionTask):
    """模拟中等表现模型"""
    return [{"label": "person", "score": 0.6}]


def main():
    """主函数"""
    engine = MultiModelEngine(max_workers=4)

    # 调整参数以便快速看到效果
    engine.min_calls_for_adjust = 10
    engine.auto_disable_threshold = 0.2
    engine.weight_adjust_alpha = 0.5

    engine.register_model("detect", ModelSpec(name="good_model", runner=fake_good, weight=1.0))
    engine.register_model("detect", ModelSpec(name="bad_model", runner=fake_bad, weight=1.0))
    engine.register_model("detect", ModelSpec(name="medium_model", runner=fake_medium, weight=1.0))

    print("=== 开始模拟调用 ===")

    # 模拟调用
    for i in range(20):
        task = VisionTask(task_type="detect", payload={"image": f"test_{i}"}, task_id=f"t{i}")
        engine.run(task)
        if i % 5 == 4:
            print(f"已完成 {i+1} 次调用")

    debug = VisionDebugService(engine)
    snapshot = debug.get_health()

    print("\n=== Vision Model Health Snapshot ===")
    pprint(snapshot.to_dict())

    print("\n=== 按任务类型查看 ===")
    detect_block = debug.get_model_block("detect")
    if detect_block:
        print("Detect 任务模型:")
        for model_name, stats in detect_block.items():
            print(f"  {model_name}:")
            print(f"    - enabled: {stats.get('enabled')}")
            print(f"    - weight: {stats.get('weight', 0):.3f}")
            print(f"    - success_rate: {stats.get('success_rate', 0):.3f}")
            print(f"    - total_calls: {stats.get('total_calls', 0)}")
            print(f"    - avg_conf: {stats.get('avg_conf', 0):.3f}")


if __name__ == "__main__":
    main()

