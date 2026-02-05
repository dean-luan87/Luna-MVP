"""
Calibrator Engine Test (C-2.5 Skeleton)

最小单测：验证导入无错、对象可实例化、枚举存在
"""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.calibrator import (
    ExpressionProtocol,
    CalibratorInput,
    CalibratorOutput,
    CalibratorEngine,
    EmotionEngineHooks,
)
from expression.context import EmbodimentProfile, DistanceUnit, DirectionReference, Precision


def test_imports():
    """测试导入"""
    print("=" * 60)
    print("测试场景 1: 导入测试")
    print("=" * 60)
    
    assert ExpressionProtocol is not None
    assert CalibratorInput is not None
    assert CalibratorOutput is not None
    assert CalibratorEngine is not None
    assert EmotionEngineHooks is not None
    
    print("✅ 所有导入成功")
    print("\n✅ 测试场景 1 通过")


def test_calibrator_engine_instantiation():
    """测试校准器引擎实例化"""
    print("\n" + "=" * 60)
    print("测试场景 2: 校准器引擎实例化")
    print("=" * 60)
    
    engine = CalibratorEngine()
    assert engine is not None
    
    # 创建输入
    embodiment = EmbodimentProfile(
        name="blind",
        distance_unit=DistanceUnit.STEP,
        direction_reference=DirectionReference.BODY_RELATIVE,
        precision=Precision.MEDIUM
    )
    
    input_data = CalibratorInput(
        intent={"intent_type": "navigation", "action": "turn_left"},
        embodiment=embodiment
    )
    
    # 执行校准
    output = engine.calibrate(input_data)
    
    assert output is not None
    assert output.protocol is not None
    assert output.verbosity_level >= 0
    assert output.lexicon_profile is not None
    
    print(f"  输出协议: {output.protocol.value}")
    print(f"  冗余度级别: {output.verbosity_level}")
    print(f"  词库配置: {output.lexicon_profile}")
    print(f"  原因: {output.reason}")
    print("\n✅ 测试场景 2 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Calibrator Engine Test (Skeleton)")
    print("=" * 60)
    
    try:
        test_imports()
        test_calibrator_engine_instantiation()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






