#!/usr/bin/env python3
"""
测试新日志系统
验证日志功能是否正常工作
"""
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.logging import get_logger


def test_basic_logging():
    """测试基本日志功能"""
    log = get_logger("test_module")
    log.info("=== 测试基本日志功能 ===")
    
    log.debug("这是一条 DEBUG 日志")
    log.info("这是一条 INFO 日志")
    log.warning("这是一条 WARNING 日志")
    log.error("这是一条 ERROR 日志")
    
    log.info("✅ 基本日志测试完成")


def test_test_mode_logging():
    """测试测试模式日志"""
    log = get_logger("test_vision", test_mode=True)
    log.info("\n=== 测试测试模式日志 ===")
    
    log.info("这是测试模式的日志")
    log.debug("测试模式 DEBUG 日志")
    
    log.info("✅ 测试模式日志测试完成")


def test_async_logging():
    """测试异步日志写入"""
    log = get_logger("async_test")
    log.info("\n=== 测试异步日志写入 ===")
    
    # 快速写入多条日志
    for i in range(10):
        log.info(f"异步日志测试 {i+1}/10")
    
    # 等待异步写入完成
    log.flush()
    time.sleep(0.5)
    
    log.info("✅ 异步日志测试完成")


def test_exception_logging():
    """测试异常日志"""
    log = get_logger("exception_test")
    log.info("\n=== 测试异常日志 ===")
    
    try:
        raise ValueError("这是一个测试异常")
    except Exception:
        log.exception("捕获到异常")
    
    log.info("✅ 异常日志测试完成")


def test_log_rotation():
    """测试日志轮转"""
    log = get_logger("rotation_test")
    log.info("\n=== 测试日志轮转 ===")
    
    # 写入一些日志
    for i in range(5):
        log.info(f"轮转测试日志 {i+1}")
    
    log.flush()
    
    # 检查日志文件是否存在
    from core.logging.log_config import LogConfig
    config = LogConfig()
    log_dir = config.get_log_dir()
    
    log_files = list(log_dir.glob("rotation_test*.log"))
    log.info(f"找到 {len(log_files)} 个日志文件")
    
    if log_files:
        latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
        log.info(f"最新日志文件: {latest_log}")
        log.info(f"文件大小: {latest_log.stat().st_size} 字节")
    
    log.info("✅ 日志轮转测试完成")


def main():
    """运行所有测试"""
    log = get_logger("test_main")
    log.info("=" * 50)
    log.info("新日志系统测试")
    log.info("=" * 50)
    
    try:
        test_basic_logging()
        test_test_mode_logging()
        test_async_logging()
        test_exception_logging()
        test_log_rotation()
        
        log.info("\n" + "=" * 50)
        log.info("✅ 所有日志系统测试通过！")
        log.info("=" * 50)
        
        # 显示日志文件位置
        from core.logging.log_config import LogConfig
        config = LogConfig()
        log.info(f"\n系统日志目录: {config.get_log_dir()}")
        log.info(f"测试日志目录: {config.get_log_dir(test_mode=True)}")
        
        return 0
    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

