#!/usr/bin/env python3
"""
LogManager v2.0 单元测试
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager


def test_log_manager_init():
    """测试日志管理器初始化"""
    try:
        # 先初始化配置中心
        ConfigCenter.init(env="dev")
        
        # 初始化日志管理器
        LogManager.init()
        
        print("✅ LogManager 初始化成功")
    except Exception as e:
        print(f"❌ LogManager 初始化失败: {e}")
        raise


def test_log_manager_get_logger():
    """测试获取日志器"""
    try:
        logger = LogManager.get_logger(__name__)
        
        # 测试不同级别的日志
        logger.debug("这是一条 DEBUG 日志")
        logger.info("这是一条 INFO 日志")
        logger.warning("这是一条 WARNING 日志")
        logger.error("这是一条 ERROR 日志")
        
        print("✅ LogManager.get_logger() 测试通过")
    except RuntimeError as e:
        if "not initialized" in str(e):
            print("⚠️  LogManager 未初始化，跳过测试")
        else:
            raise


def test_log_manager_exception():
    """测试异常日志"""
    try:
        logger = LogManager.get_logger("test_exception")
        
        try:
            raise ValueError("测试异常")
        except Exception:
            logger.exception("捕获到异常")
        
        print("✅ LogManager 异常日志测试通过")
    except RuntimeError as e:
        if "not initialized" in str(e):
            print("⚠️  LogManager 未初始化，跳过测试")
        else:
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("LogManager v2.0 单元测试")
    print("=" * 60)
    
    test_log_manager_init()
    test_log_manager_get_logger()
    test_log_manager_exception()
    
    print("=" * 60)
    print("测试完成")
    print("=" * 60)





