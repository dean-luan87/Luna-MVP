from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_model_router")
"""
Model Router 测试脚本

用于测试模型路由器的各项功能
"""

import sys
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 测试场景
TEST_CASES = [
    {
        "name": "危险场景（强制 L1）",
        "text": "停下",
        "context": {"critical_flag": True},
        "expected_model": "L1",
        "expected_reason": "critical"
    },
    {
        "name": "视觉警报（强制 L1）",
        "text": "前面有什么",
        "context": {"vision_alert": True},
        "expected_model": "L1",
        "expected_reason": "critical"
    },
    {
        "name": "简单导航（L1）",
        "text": "往左走",
        "context": {},
        "expected_model": "L1",
        "expected_reason": "simple_nav"
    },
    {
        "name": "方向询问（L1）",
        "text": "我应该往哪个方向走？",
        "context": {},
        "expected_model": "L1",
        "expected_reason": "simple_nav"
    },
    {
        "name": "确认类（L1）",
        "text": "是不是继续往前走？",
        "context": {},
        "expected_model": "L1",
        "expected_reason": "simple_nav"
    },
    {
        "name": "复杂语义（L2）",
        "text": "我应该去哪一个窗口挂号？",
        "context": {},
        "expected_model": "L2",
        "expected_reason": "complex_semantic"
    },
    {
        "name": "多步骤意图（L2）",
        "text": "先去711再去医院",
        "context": {},
        "expected_model": "L2",
        "expected_reason": "complex_semantic"
    },
    {
        "name": "情绪表达（L2）",
        "text": "我有点紧张，你帮我一下",
        "context": {},
        "expected_model": "L2",
        "expected_reason": "complex_semantic"
    },
]


def test_router_without_models():
    """测试路由器（不使用真实模型，模拟调用）"""
    log.info("=" * 60")
    log.info("测试 1: 路由器逻辑（无模型）")
    log.info("=" * 60")

    from model_router import ModelRouter

    # 创建模拟的 L1 和 L2 函数
    def mock_l1(text: str):
        """模拟 L1 模型"""
        # 简单的意图分类
        text_lower = text.lower()
        if any(word in text_lower for word in ["往左", "往右", "向前", "继续", "停下"]):
            intent = "simple_nav"
        elif any(word in text_lower for word in ["方向", "哪里", "哪边"]):
            intent = "orientation"
        elif any(word in text_lower for word in ["是吗", "对不对"]):
            intent = "confirm"
        else:
            intent = "complex_semantic"

        return {
            "text": f"[L1 响应] {text}",
            "intent": intent,
            "confidence": 0.8
        }

    def mock_l2(text: str):
        """模拟 L2 模型"""
        return {
            "text": f"[L2 响应] {text}"
        }

    router = ModelRouter(l1_model=mock_l1, l2_model=mock_l2)

    # 运行测试用例
    for i, test_case in enumerate(TEST_CASES, 1):
        log.info(f"\n测试 {i}: {test_case['name']}")
        log.info(f"  输入: {test_case['text']}")
        log.info(f"  上下文: {test_case['context']}")

        result = router.route(test_case['text'], test_case['context'])

        log.info(f"  结果: model={result.get('model')}, reason={result.get('reason')}")
        if 'response' in result:
            log.info(f"  响应: {result['response'].get('text', 'N/A')}")

        # 验证结果
        if result.get('model') == test_case['expected_model']:
            log.info(f"  ✅ 模型选择正确")
        else:
            log.info(f"  ❌ 模型选择错误，期望 {test_case['expected_model']}，得到 {result.get('model')}")

        if result.get('reason') == test_case['expected_reason']:
            log.info(f"  ✅ 路由原因正确")
        else:
            log.info(f"  ⚠️ 路由原因不同，期望 {test_case['expected_reason']}，得到 {result.get('reason')}")


def test_router_fallback():
    """测试降级机制"""
    log.info("\n" + "=" * 60)
    log.info("测试 2: 降级机制")
    log.info("=" * 60")

    from model_router import ModelRouter

    # 测试 L2 失败时降级到 L1
    def mock_l1(text: str):
        # 意图分类时返回复杂语义，确保路由到 L2
        if "分类" in text:
            return {"text": "[L1 分类]", "intent": "complex_semantic", "confidence": 0.8}
        # 实际处理时返回 L1 响应
        return {"text": "[L1 降级响应]", "intent": "simple_nav", "confidence": 0.8}

    def mock_l2_error(text: str):
        return {"error": "模拟 L2 错误"}

    router = ModelRouter(l1_model=mock_l1, l2_model=mock_l2_error)

    # 使用会被识别为复杂语义的文本
    result = router.route("我应该去哪个医院？", {})
    log.info(f"输入: 我应该去哪个医院？")
    log.info(f"结果: model={result.get('model')}, reason={result.get('reason')}")
    
    if result.get('model') == 'L1' and 'fallback' in result.get('reason', ''):
        log.info("  ✅ 降级机制正常")
    else:
        log.info(f"  ⚠️ 降级机制: 期望 L1+fallback，实际 {result.get('model')}+{result.get('reason')}")
        
    # 测试 L2 异常时的降级
    def mock_l2_exception(text: str):
        raise Exception("模拟 L2 异常")

    router2 = ModelRouter(l1_model=mock_l1, l2_model=mock_l2_exception)
    result2 = router2.route("复杂问题测试", {})
    log.info(f"\n测试 L2 异常降级:")
    log.info(f"  输入: 复杂问题测试")
    log.info(f"  结果: model={result2.get('model')}, reason={result2.get('reason')}")
    
    if result2.get('model') == 'L1' and ('fallback' in result2.get('reason', '') or 'exception' in result2.get('reason', '')):
        log.info("  ✅ L2 异常降级机制正常")
    else:
        log.info("  ⚠️ L2 异常降级机制需要检查")


def test_router_no_models():
    """测试无模型情况"""
    log.info("\n" + "=" * 60)
    log.info("测试 3: 无模型情况")
    log.info("=" * 60")

    from model_router import ModelRouter

    router = ModelRouter(l1_model=None, l2_model=None)

    result = router.route("测试", {})
    log.info(f"结果: {result}")
    
    if result.get('model') == 'ERROR':
        log.info("  ✅ 无模型错误处理正常")
    else:
        log.info("  ❌ 无模型错误处理异常")


if __name__ == "__main__":
    log.info("🚀 Model Router 测试开始\n")

    try:
        test_router_without_models()
        test_router_fallback()
        test_router_no_models()

        log.info("\n" + "=" * 60)
        log.info("✅ 所有测试完成")
        log.info("=" * 60")

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

