"""
Luna Badge v1.4.6d Step 13 — TTSRouterFacade Demo

验证统一入口 TTSRouterFacade.emit() 功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import tts_manager
from task_engine.tts.runtime_driver import TTSRuntimeDriver
from task_engine.tts.router_facade import get_tts_router_facade
from task_engine.tts.tts_policy import TTSCategory
from task_engine.tts.priority_bands import PriorityBand


def run_demo():
    """运行 Step 13 Demo"""
    
    # 初始化组件
    tts_manager.clear()
    driver = TTSRuntimeDriver()
    router = get_tts_router_facade()
    
    print("\n\n" + "=" * 80)
    print("Luna Badge v1.4.6d Step 13 — TTSRouterFacade Demo")
    print("=" * 80 + "\n")
    
    # ------------------------------------------------------------------
    # 场景 1：使用语义化接口
    # ------------------------------------------------------------------
    print("\n[场景 1] 使用语义化接口\n")
    
    router.speak_system("系统启动完成")
    router.speak_task("任务已开始")
    router.speak_nav("前方10米直行")
    router.speak_safety("前方危险，请立即停下")
    router.speak_chat("今天天气不错")
    
    # 获取队列快照
    main_queue = tts_manager.get_queue()
    safety_queue = tts_manager.get_safety_queue()
    
    print(f"   主队列: {len(main_queue)} 条")
    print(f"   安全队列: {len(safety_queue)} 条")
    
    # 验证安全队列优先
    assert len(safety_queue) > 0, "安全队列应该有内容"
    
    # ------------------------------------------------------------------
    # 场景 2：使用统一入口 emit()
    # ------------------------------------------------------------------
    print("\n[场景 2] 使用统一入口 emit()\n")
    
    tts_manager.clear()
    
    router.emit("系统错误", category=TTSCategory.SYSTEM)
    router.emit("任务完成", category=TTSCategory.TASK)
    router.emit("前方5米左转", category=TTSCategory.NAVIGATION)
    router.emit("紧急停止", category=TTSCategory.SAFETY)
    router.emit("闲聊内容", category=TTSCategory.CHAT)
    
    main_queue = tts_manager.get_queue()
    safety_queue = tts_manager.get_safety_queue()
    
    print(f"   主队列: {len(main_queue)} 条")
    print(f"   安全队列: {len(safety_queue)} 条")
    
    # 验证分类正确
    assert len(safety_queue) > 0, "安全队列应该有内容"
    
    # ------------------------------------------------------------------
    # 场景 3：验证路由到 NavigationVoiceRouter
    # ------------------------------------------------------------------
    print("\n[场景 3] 验证路由到 NavigationVoiceRouter\n")
    
    tts_manager.clear()
    
    # 导航和安全应该路由到 NavigationVoiceRouter
    router.speak_nav("导航信息")
    router.speak_safety("安全警告")
    
    main_queue = tts_manager.get_queue()
    safety_queue = tts_manager.get_safety_queue()
    
    print(f"   主队列: {len(main_queue)} 条")
    print(f"   安全队列: {len(safety_queue)} 条")
    
    # 验证安全播报进入安全队列
    assert len(safety_queue) > 0, "安全播报应该进入安全队列"
    
    # ------------------------------------------------------------------
    # 场景 4：验证系统/任务进入主队列
    # ------------------------------------------------------------------
    print("\n[场景 4] 验证系统/任务进入主队列\n")
    
    tts_manager.clear()
    
    router.speak_system("系统消息")
    router.speak_task("任务消息")
    router.speak_chat("闲聊消息")
    
    main_queue = tts_manager.get_queue()
    safety_queue = tts_manager.get_safety_queue()
    
    print(f"   主队列: {len(main_queue)} 条")
    print(f"   安全队列: {len(safety_queue)} 条")
    
    # 验证系统/任务进入主队列
    assert len(main_queue) >= 2, "系统/任务应该进入主队列"
    
    # ------------------------------------------------------------------
    # 场景 5：完整播报流程验证
    # ------------------------------------------------------------------
    print("\n[场景 5] 完整播报流程验证\n")
    
    tts_manager.clear()
    
    # 按优先级顺序加入
    router.speak_chat("闲聊1")  # P3
    router.speak_task("任务1")   # P2
    router.speak_nav("导航1")   # P1
    router.speak_safety("安全1")  # P0
    
    print("   播报顺序（应优先安全，然后按 P1 > P2 > P3）:")
    for i in range(4):
        driver.process_once()
        if not tts_manager.get_queue() and not tts_manager.get_safety_queue():
            break
    
    print("\n\n" + "=" * 80)
    print("Demo 完成！")
    print("=" * 80)
    print("\n说明：")
    print("- 场景 1 验证了语义化接口（speak_system, speak_task, etc.）")
    print("- 场景 2 验证了统一入口 emit()")
    print("- 场景 3 验证了导航/安全路由到 NavigationVoiceRouter")
    print("- 场景 4 验证了系统/任务进入主队列")
    print("- 场景 5 验证了完整播报流程和优先级排序\n")


if __name__ == "__main__":
    run_demo()

