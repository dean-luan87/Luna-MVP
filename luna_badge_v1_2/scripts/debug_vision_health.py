"""
Debug Vision Health: 模型健康快照调试脚本

用于在本地跑一跑模型健康快照，方便理解和验证效果。
"""

import sys
import os
from pprint import pprint

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.multi_model_engine import MultiModelEngine, ModelSpec
from core.vision.vision_task_orchestrator import VisionTask


def fake_runner_good(task: VisionTask):
    """模拟高成功率、高置信度模型"""
    return [{"label": "person", "score": 0.9}]


def fake_runner_bad(task: VisionTask):
    """模拟经常失败的模型"""
    raise RuntimeError("model error")


def fake_runner_medium(task: VisionTask):
    """模拟中等表现的模型"""
    return [{"label": "person", "score": 0.6}]


def main():
    """主函数"""
    mme = MultiModelEngine(max_workers=4)

    # 调整参数以便快速看到效果
    mme.min_calls_for_adjust = 10
    mme.auto_disable_threshold = 0.2
    mme.weight_adjust_alpha = 0.5

    mme.register_model("detect", ModelSpec(name="good_model", runner=fake_runner_good, weight=1.0))
    mme.register_model("detect", ModelSpec(name="bad_model", runner=fake_runner_bad, weight=1.0))
    mme.register_model("detect", ModelSpec(name="medium_model", runner=fake_runner_medium, weight=1.0))

    print("=== 开始模拟调用 ===")

    # 模拟多次调用
    for i in range(30):
        task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"t{i}")
        result = mme.run(task)
        if i % 10 == 9:
            print(f"已完成 {i+1} 次调用")

    print("\n=== Model Health Snapshot ===")
    snapshot = mme.get_model_health_snapshot()
    pprint(snapshot)

    print("\n=== 模型状态 ===")
    for spec in mme._registry.get("detect", []):
        stats = mme._score_logger.get_stats("detect", spec.name)
        print(f"{spec.name}: enabled={spec.enabled}, weight={spec.weight:.3f}, "
              f"success_rate={stats.success_rate:.3f}, total_calls={stats.total_calls}")


if __name__ == "__main__":
    main()

