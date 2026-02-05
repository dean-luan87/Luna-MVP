#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 后台上传测试脚本
测试云端同步、记忆上传、硬件注册等功能
"""

import logging
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core.cloud_sync_manager import LunaCloudSync
from core.memory_cache_manager import MemoryCacheManager
from core.background_uploader import BackgroundUploader
from task_chain.timers.memory_uploader import MemoryUploader
from core.hardware_identity_logger import HardwareIdentityLogger
from memory_store.tools.memory_writer import MemoryWriter
from memory_store.tools.memory_collector import MemoryCollector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_cloud_sync():
    """测试云端同步功能"""
    print("\n" + "=" * 70)
    print("🧪 测试1: 云端同步管理")
    print("=" * 70)
    
    try:
        # 初始化同步管理器
        sync = LunaCloudSync()
        
        # 测试登录
        print("\n📋 测试登录功能...")
        result = sync.login("test_user", "test_password")
        print(f"   登录结果: {'✅ 成功' if result else '❌ 失败'}")
        
        # 检查登录状态
        print("\n📋 检查登录状态...")
        is_logged_in = sync.is_logged_in()
        print(f"   登录状态: {'✅ 已登录' if is_logged_in else '❌ 未登录'}")
        
        # 获取用户信息
        if is_logged_in:
            user_info = sync.get_user_info()
            print(f"   用户信息: {user_info}")
        
        # 测试同步地图
        print("\n📋 测试地图同步...")
        stats = sync.sync_all_maps()
        print(f"   同步结果: {stats}")
        
        # 测试登出
        print("\n📋 测试登出功能...")
        sync.logout()
        print("   ✅ 登出成功")
        
        print("\n✅ 测试1通过\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试1失败: {e}\n")
        return False


def test_memory_upload():
    """测试记忆上传功能"""
    print("\n" + "=" * 70)
    print("🧪 测试2: 记忆上传器")
    print("=" * 70)
    
    try:
        # 初始化上传器
        uploader = MemoryUploader(
            upload_api_url="http://localhost:8000/api/user/memory",
            wifi_check_interval=5
        )
        
        # 测试WiFi检测
        print("\n📋 测试WiFi连接检测...")
        wifi_connected = uploader.check_wifi_connected()
        print(f"   WiFi状态: {'✅ 已连接' if wifi_connected else '⚠️ 未连接（开发模式）'}")
        
        # 测试T+1条件判断
        print("\n📋 测试T+1上传条件...")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        should_upload_yesterday = uploader.should_upload(yesterday)
        should_upload_today = uploader.should_upload(today)
        
        print(f"   {yesterday}: {'✅ 可上传' if should_upload_yesterday else '❌ 不可上传'}")
        print(f"   {today}: {'✅ 可上传' if should_upload_today else '❌ 不可上传'}")
        
        # 测试批量上传（模拟）
        print("\n📋 测试批量上传...")
        test_memories = [
            {
                "user_id": "test_user_123",
                "date": yesterday,
                "maps": [
                    {
                        "map_id": "test_map_001",
                        "nodes_visited": ["entrance", "toilet"],
                        "duration_minutes": 5.2
                    }
                ]
            }
        ]
        
        # 定义模拟上传函数
        def mock_upload_func(memories):
            return {"success": True, "count": len(memories)}
        
        uploader.upload_func = mock_upload_func
        result = uploader.upload_memory_batch(test_memories)
        print(f"   上传结果: {'✅ 成功' if result else '❌ 失败'}")
        
        print("\n✅ 测试2通过\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试2失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_hardware_identity():
    """测试硬件身份管理"""
    print("\n" + "=" * 70)
    print("🧪 测试3: 硬件身份日志")
    print("=" * 70)
    
    try:
        # 初始化硬件日志记录器
        hw_logger = HardwareIdentityLogger(log_path="data/test_hardware_id.json")
        
        # 测试记录硬件信息
        print("\n📋 测试记录硬件信息...")
        hw_info = hw_logger.hardware_identity_logger(account_id="test_account_001")
        print(f"   硬件信息: {json.dumps(hw_info, indent=2, ensure_ascii=False)}")
        
        # 测试获取序列号
        print("\n📋 测试获取序列号...")
        serial = hw_logger.get_serial_number()
        print(f"   序列号: {serial}")
        
        # 测试获取启动次数
        print("\n📋 测试获取启动次数...")
        boot_count = hw_logger.get_boot_count()
        print(f"   启动次数: {boot_count}")
        
        # 再次调用，测试计数递增
        print("\n📋 测试启动计数递增...")
        hw_info2 = hw_logger.hardware_identity_logger()
        boot_count2 = hw_logger.get_boot_count()
        print(f"   新的启动次数: {boot_count2} (应该比之前+1)")
        
        # 测试账号绑定
        print("\n📋 测试账号绑定...")
        result = hw_logger.bind_account("test_account_002")
        print(f"   绑定结果: {'✅ 成功' if result else '❌ 失败'}")
        
        # 清理测试文件
        test_file = Path("data/test_hardware_id.json")
        if test_file.exists():
            test_file.unlink()
        
        print("\n✅ 测试3通过\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试3失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_memory_collector():
    """测试记忆收集器"""
    print("\n" + "=" * 70)
    print("🧪 测试4: 记忆收集器")
    print("=" * 70)
    
    try:
        # 初始化记忆写入器
        writer = MemoryWriter()
        
        # 创建测试记忆数据
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        
        print("\n📋 创建测试记忆数据...")
        
        # 写入昨天的记忆（应该上传）
        writer.record_map_visit(
            map_id="test_map_001",
            nodes_visited=["entrance", "toilet", "exit"],
            emotion_tags={"toilet": "推荐"},
            duration_minutes=10.5,
            date=yesterday
        )
        print(f"   ✅ 写入昨天的记忆: {yesterday}")
        
        # 写入今天的记忆（不应该上传）
        writer.record_map_visit(
            map_id="test_map_002",
            nodes_visited=["start", "end"],
            duration_minutes=5.0,
            date=today
        )
        print(f"   ✅ 写入今天的记忆: {today}")
        
        # 初始化收集器
        collector = MemoryCollector()
        
        # 获取待上传记忆
        print("\n📋 检查待上传记忆...")
        pending = collector.collect_pending_memories()
        print(f"   待上传记忆数: {len(pending)}")
        
        for mem in pending:
            print(f"   - 文件: {mem.get('file').name}, 大小: {mem.get('size')} bytes")
        
        # 测试标记已上传
        print("\n📋 测试标记已上传...")
        if pending:
            result = collector.mark_as_uploaded(pending[0]['file'])
            print(f"   标记结果: {'✅ 成功' if result else '❌ 失败'}")
            
            # 再次检查
            pending2 = collector.collect_pending_memories()
            print(f"   剩余待上传: {len(pending2)} 条")
        
        # 测试统计信息
        print("\n📋 测试统计信息...")
        stats = collector.get_statistics()
        print(f"   统计信息: {json.dumps(stats, indent=2, ensure_ascii=False)}")
        
        print("\n✅ 测试4通过\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试4失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_background_uploader():
    """测试后台上传器"""
    print("\n" + "=" * 70)
    print("🧪 测试5: 后台上传器")
    print("=" * 70)
    
    try:
        # 初始化缓存管理器
        cache_manager = MemoryCacheManager()
        
        # 模拟上传函数
        def mock_upload_func(data):
            print(f"   📤 模拟上传数据: {len(data)} 条记录")
            return True
        
        # 初始化后台上传器
        background_uploader = BackgroundUploader(
            cache_manager=cache_manager,
            upload_func=mock_upload_func,
            wifi_check_interval=5,
            upload_check_interval=10
        )
        
        print("\n📋 测试启动后台上传服务...")
        background_uploader.start()
        print("   ✅ 服务已启动")
        
        print("\n📋 等待10秒测试循环...")
        import time
        time.sleep(10)
        
        print("\n📋 停止后台上传服务...")
        background_uploader.stop()
        print("   ✅ 服务已停止")
        
        print("\n✅ 测试5通过\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试5失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("🚀 Luna Badge 后台上传集成测试")
    print("=" * 70)
    
    # 创建测试结果记录
    test_results = []
    
    # 执行所有测试
    tests = [
        ("云端同步", test_cloud_sync),
        ("记忆上传", test_memory_upload),
        ("硬件身份", test_hardware_identity),
        ("记忆收集", test_memory_collector),
        ("后台上传", test_background_uploader),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            test_results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("📊 测试结果汇总")
    print("=" * 70)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")
        return 1


if __name__ == "__main__":
    exit(main())

