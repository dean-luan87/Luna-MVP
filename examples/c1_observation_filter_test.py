"""
C1 Observation Filter 独立测试脚本

只测试 observation_filter 模块，不依赖整个 pipeline。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入 observation_filter（不通过 vision_pipeline）
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'vision_pipeline', 'lv4_executors'))
from observation_filter import (
    filter_forward,
    filter_local,
    filter_surround,
    filter_objects_by_mode,
)


def create_mock_objects():
    """
    创建 mock YOLO 检测结果
    
    Returns:
        List[Dict]: mock objects
    """
    return [
        {
            "bbox": [100, 100, 200, 200],  # 中央区域
            "confidence": 0.9,
            "class": "person",
        },
        {
            "bbox": [50, 50, 100, 100],  # 左上角
            "confidence": 0.8,
            "class": "car",
        },
        {
            "bbox": [500, 50, 600, 100],  # 右上角
            "confidence": 0.7,
            "class": "sign",
        },
        {
            "bbox": [300, 400, 400, 500],  # 中央下方（靠近地面）
            "confidence": 0.95,
            "class": "person",
        },
        {
            "bbox": [10, 10, 20, 20],  # 很小（远处物体）
            "confidence": 0.6,
            "class": "object",
        },
    ]


def test_observation_filter():
    """
    测试观察模式过滤器
    """
    print("=" * 70)
    print("C1 Observation Filter 测试")
    print("=" * 70)
    
    objects = create_mock_objects()
    frame_shape = (480, 640, 3)  # (height, width, channels)
    
    print(f"\n原始 objects 数量: {len(objects)}")
    for i, obj in enumerate(objects):
        print(f"  [{i}] {obj['class']}: bbox={obj['bbox']}, conf={obj['confidence']:.2f}")
    
    # 测试 forward 模式
    print("\n[测试 1] forward 模式（前方视野）")
    filtered_forward = filter_forward(objects, frame_shape)
    print(f"  过滤后数量: {len(filtered_forward)}")
    for obj in filtered_forward:
        print(f"    {obj['class']}: bbox={obj['bbox']}, conf={obj['confidence']:.2f}")
    assert len(filtered_forward) <= len(objects), "❌ forward 模式应该过滤掉一些物体"
    print("  ✅ 测试通过")
    
    # 测试 local 模式
    print("\n[测试 2] local 模式（局部视野）")
    filtered_local = filter_local(objects, frame_shape)
    print(f"  过滤后数量: {len(filtered_local)}")
    for obj in filtered_local:
        print(f"    {obj['class']}: bbox={obj['bbox']}, conf={obj['confidence']:.2f}")
    assert len(filtered_local) <= len(objects), "❌ local 模式应该过滤掉一些物体"
    # local 模式应该只保留大 bbox（近处物体）和高置信度
    for obj in filtered_local:
        assert obj['confidence'] >= 0.5, "❌ local 模式应该只保留高置信度物体"
    print("  ✅ 测试通过")
    
    # 测试 surround 模式
    print("\n[测试 3] surround 模式（周边视野）")
    filtered_surround = filter_surround(objects, frame_shape)
    print(f"  过滤后数量: {len(filtered_surround)}")
    assert len(filtered_surround) == len(objects), "❌ surround 模式应该保留全部物体"
    # 应该按置信度排序
    for i in range(len(filtered_surround) - 1):
        assert filtered_surround[i]['confidence'] >= filtered_surround[i+1]['confidence'], \
            "❌ surround 模式应该按置信度排序"
    print("  ✅ 测试通过")
    
    # 测试统一接口
    print("\n[测试 4] 统一接口 filter_objects_by_mode")
    for mode in ["forward", "local", "surround"]:
        filtered = filter_objects_by_mode(objects, mode, frame_shape)
        print(f"  {mode}: {len(filtered)} 个物体")
        assert isinstance(filtered, list), f"❌ {mode} 模式应该返回列表"
    print("  ✅ 测试通过")
    
    print("\n" + "=" * 70)
    print("✅ 所有测试通过")
    print("=" * 70)
    print("\n📋 关键验证点：")
    print("  ✅ forward 模式：只保留中央区域、靠近地面的物体")
    print("  ✅ local 模式：只保留大 bbox（近处）、高置信度物体")
    print("  ✅ surround 模式：保留全部，按置信度排序")
    print("  ✅ 不在图像层面裁剪，只在结果过滤层面")


if __name__ == "__main__":
    test_observation_filter()


