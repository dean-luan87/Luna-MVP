"""
Output Router Test (C-4 Skeleton)

最小单测：验证导入无错、对象可实例化、最小路由可跑
"""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.adapters import (
    OutputChannel,
    OutputRouter,
)
from expression.renderer import RenderedMessage
from expression.calibrator import ExpressionProtocol


def test_imports():
    """测试导入"""
    print("=" * 60)
    print("测试场景 1: 导入测试")
    print("=" * 60)
    
    assert OutputChannel is not None
    assert OutputRouter is not None
    
    print("✅ 所有导入成功")
    print("\n✅ 测试场景 1 通过")


def test_output_router_instantiation():
    """测试输出路由器实例化"""
    print("\n" + "=" * 60)
    print("测试场景 2: 输出路由器实例化")
    print("=" * 60)
    
    router = OutputRouter(default_channel=OutputChannel.DEBUG)
    assert router is not None
    
    # 创建渲染消息
    message = RenderedMessage(
        text="测试消息",
        tags={"intent_type": "navigation"},
        protocol=ExpressionProtocol.CONSENSUS,
        embodiment="default"
    )
    
    # 执行路由
    result = router.route(message)
    
    assert result is not None
    assert "channel" in result
    assert "payload" in result
    assert result["channel"] == OutputChannel.DEBUG.value
    
    print(f"  输出通道: {result['channel']}")
    print(f"  负载: {result['payload']}")
    print("\n✅ 测试场景 2 通过")


def test_output_channel_enum():
    """测试输出通道枚举"""
    print("\n" + "=" * 60)
    print("测试场景 3: 输出通道枚举")
    print("=" * 60)
    
    assert OutputChannel.DEBUG is not None
    assert OutputChannel.VOICE_TEXT is not None
    
    print(f"  DEBUG: {OutputChannel.DEBUG.value}")
    print(f"  VOICE_TEXT: {OutputChannel.VOICE_TEXT.value}")
    print("\n✅ 测试场景 3 通过")


def main():
    """主函数"""
    print("=" * 60)
    print("Output Router Test (Skeleton)")
    print("=" * 60)
    
    try:
        test_imports()
        test_output_router_instantiation()
        test_output_channel_enum()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()






