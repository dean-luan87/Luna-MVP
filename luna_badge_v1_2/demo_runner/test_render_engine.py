"""
Render Engine Test (C-3 Skeleton)

最小单测：验证导入无错、对象可实例化、最小路由可跑
"""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.renderer import (
    RenderedMessage,
    RenderEngine,
)
from expression.calibrator import ExpressionProtocol
from expression.context import EmbodimentProfile, DistanceUnit, DirectionReference, Precision


def test_imports():
    """测试导入"""
    print("=" * 60)
    print("测试场景 1: 导入测试")
    print("=" * 60)
    
    assert RenderedMessage is not None
    assert RenderEngine is not None
    
    print("✅ 所有导入成功")
    print("\n✅ 测试场景 1 通过")


def test_render_engine_instantiation():
    """测试渲染器引擎实例化"""
    print("\n" + "=" * 60)
    print("测试场景 2: 渲染器引擎实例化")
    print("=" * 60)
    
    engine = RenderEngine()
    assert engine is not None
    
    # 创建意图
    intent = {
        "intent_type": "navigation",
        "action": "turn_left",
        "distance_m": 10.0,
        "direction": "left"
    }
    
    # 创建协议和配置
    protocol = ExpressionProtocol.GUIDED
    embodiment = EmbodimentProfile(
        name="blind",
        distance_unit=DistanceUnit.STEP,
        direction_reference=DirectionReference.BODY_RELATIVE,
        precision=Precision.MEDIUM
    )
    
    # 执行渲染
    message = engine.render(intent, protocol, embodiment)
    
    assert message is not None
    assert message.text is not None
    assert message.protocol == protocol
    assert message.embodiment == "blind"
    
    print(f"  渲染文本: {message.text}")
    print(f"  协议: {message.protocol.value}")
    print(f"  配置: {message.embodiment}")
    print("\n✅ 测试场景 2 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Render Engine Test (Skeleton)")
    print("=" * 60)
    
    try:
        test_imports()
        test_render_engine_instantiation()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






