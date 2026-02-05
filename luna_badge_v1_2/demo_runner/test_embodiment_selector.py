"""
Embodiment Selector Test (C-2 Skeleton)

最小单测：验证导入无错、对象可实例化、枚举存在
"""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.context import (
    EmbodimentProfile,
    EmbodimentSelector,
    DistanceUnit,
    DirectionReference,
    Precision,
)


def test_imports():
    """测试导入"""
    print("=" * 60)
    print("测试场景 1: 导入测试")
    print("=" * 60)
    
    assert EmbodimentProfile is not None
    assert EmbodimentSelector is not None
    assert DistanceUnit is not None
    assert DirectionReference is not None
    assert Precision is not None
    
    print("✅ 所有导入成功")
    print("\n✅ 测试场景 1 通过")


def test_embodiment_profile_creation():
    """测试身体形态配置创建"""
    print("\n" + "=" * 60)
    print("测试场景 2: 身体形态配置创建")
    print("=" * 60)
    
    profile = EmbodimentProfile(
        name="blind",
        distance_unit=DistanceUnit.STEP,
        direction_reference=DirectionReference.BODY_RELATIVE,
        precision=Precision.MEDIUM
    )
    
    assert profile.name == "blind"
    assert profile.distance_unit == DistanceUnit.STEP
    assert profile.direction_reference == DirectionReference.BODY_RELATIVE
    assert profile.precision == Precision.MEDIUM
    
    print(f"  配置: {profile.name}, {profile.distance_unit.value}, {profile.direction_reference.value}")
    print("\n✅ 测试场景 2 通过")


def test_embodiment_selector():
    """测试身体形态选择器"""
    print("\n" + "=" * 60)
    print("测试场景 3: 身体形态选择器")
    print("=" * 60)
    
    selector = EmbodimentSelector()
    
    # 选择 blind 配置
    profile = selector.select("blind")
    assert profile is not None
    assert profile.name == "blind"
    
    # 获取当前配置
    current = selector.get_current()
    assert current == profile
    
    print(f"  当前配置: {current.name}")
    print("\n✅ 测试场景 3 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Embodiment Selector Test (Skeleton)")
    print("=" * 60)
    
    try:
        test_imports()
        test_embodiment_profile_creation()
        test_embodiment_selector()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






