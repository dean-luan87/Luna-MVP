from core.logging import get_logger

log = get_logger("app_controller")
"""
App Controller (v1.3.0)

应用控制器

最小可运行的 demo：从摄像头读取画面，驱动导航任务
"""

import cv2
import logging
import time

from .navigation_engine import NavigationEngine
from tasks.navigation_task import NavigationTask
from tasks.navigation_context import NavigationContext
from tasks.navigation_state import NavigationState

# 尝试导入 tracking，如果不存在则使用占位符
try:
    from core.tracking import track_event
    TRACKING_AVAILABLE = True
except ImportError:
    TRACKING_AVAILABLE = False
    logging.warning("track_event 不可用，将使用占位符")
    
    def track_event(phase: str, event_name: str, payload: dict):
        """占位符函数"""
        pass

logger = logging.getLogger(__name__)


class DummyTTS:
    """
    虚拟 TTS 管理器（用于 demo）

    实际使用中应该替换为真实的 TTS 系统
    """

    def speak(self, event: dict):
        """
        播报语音事件

        Args:
            event: SpeechEvent 字典
        """
        if event and event.get("speak"):
            text = event.get("text", "")
            style = event.get("style", "calm")
            priority = event.get("priority", 0)
            
            # 简单打印即可
            log.info(f"[TTS] [{style.upper()}] [{priority}] {text}")


class AppController:
    """
    应用控制器

    最小可运行的 demo：从摄像头读取画面，驱动导航任务
    """

    def __init__(self, target: str = "测试目的地", target_location=None):
        """
        初始化应用控制器

        Args:
            target: 导航目标名称
            target_location: 导航目标位置（可选）
        """
        # 初始化导航引擎
        self.engine = NavigationEngine()

        # 初始化 TTS 管理器（虚拟版）
        self.tts = DummyTTS()

        # 创建导航上下文
        context = NavigationContext(
            target=target,
            target_location=target_location
        )

        # 创建导航任务
        self.nav_task = NavigationTask(
            context=context,
            navigation_engine=self.engine,
            logger_instance=None,
            tts_manager=self.tts
        )

        logger.info(f"应用控制器初始化完成，目标: {target}")

    def run_navigation_demo(self, camera_index: int = 0):
        """
        运行导航 demo

        Args:
            camera_index: 摄像头索引（默认 0）
        """
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            logger.error(f"摄像头打开失败: {camera_index}")
            log.info(f"[AppController] 摄像头打开失败，请检查摄像头是否连接")
            return

        logger.info("摄像头打开成功，开始导航 demo")
        log.info("\n" + "=" * 80)
        log.info("🚀 Luna Badge 导航 Demo 启动")
        log.info("=" * 80")
        log.info("💡 提示:")
        log.info("   - 按 'q' 键退出")
        log.info("   - 导航语音将显示在控制台")
        log.info("-" * 80")

        try:
            track_event("navigation", "navigation_demo_start", {
                "target": self.nav_task.context.target,
            })
        except Exception:
            pass

        # 启动导航任务
        if not self.nav_task.start():
            logger.error("导航任务启动失败")
            cap.release()
            return

        frame_count = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("无法读取摄像头画面")
                    break

                frame_count += 1

                # 交给导航任务处理
                speech_event = self.nav_task.update(frame)

                # 每 30 帧打印一次状态
                if frame_count % 30 == 0:
                    state = self.nav_task.get_state()
                    context = self.nav_task.get_context()
                    log.info(f"\n📊 帧 #{frame_count}: 状态={state.value}, 处理帧数={context.frame_count}")

                # Demo：按下 'q' 退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("用户按 'q' 退出")
                    log.info("\n👋 用户退出")
                    break

                # 检查任务状态
                if self.nav_task.get_state() in (NavigationState.STOPPED, NavigationState.ARRIVED):
                    logger.info(f"导航任务结束，状态: {self.nav_task.get_state().value}")
                    break

        except KeyboardInterrupt:
            logger.info("用户中断")
            log.info("\n\n👋 用户中断")

        finally:
            # 停止导航任务
            if self.nav_task.get_state() == NavigationState.ACTIVE:
                self.nav_task.stop()

            try:
                track_event("navigation", "navigation_demo_end", {
                    "frame_count": frame_count,
                    "final_state": self.nav_task.get_state().value,
                })
            except Exception:
                pass

            cap.release()
            cv2.destroyAllWindows()

            log.info("\n" + "=" * 80)
            log.info(f"✅ 导航 Demo 结束")
            log.info(f"   总帧数: {frame_count}")
            log.info(f"   任务状态: {self.nav_task.get_state().value}")
            log.info(f"   处理帧数: {self.nav_task.get_context().frame_count}")
            log.info("=" * 80")

    def pause_navigation(self):
        """
        暂停导航

        Returns:
            bool: 是否成功暂停
        """
        return self.nav_task.pause(reason="user_request")

    def resume_navigation(self):
        """
        恢复导航

        Returns:
            bool: 是否成功恢复
        """
        return self.nav_task.resume()

    def stop_navigation(self):
        """
        停止导航

        Returns:
            bool: 是否成功停止
        """
        return self.nav_task.stop(reason="user_request")

    def get_task_state(self) -> NavigationState:
        """
        获取任务状态

        Returns:
            NavigationState: 当前状态
        """
        return self.nav_task.get_state()

