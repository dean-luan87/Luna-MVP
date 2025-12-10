import time
import threading
import sys
import os
import atexit
from dataclasses import dataclass
from typing import Optional

# 添加项目根目录到路径
# 确保当前目录（luna_badge_v1_2）在路径中，优先于项目根目录
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
# 再添加项目根目录
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# 调试：检查 modules 是否能找到
if __name__ == '__main__':
    import logging
    _debug_logger = logging.getLogger('main.debug')
    _debug_logger.debug(f"Script dir: {_script_dir}")
    _debug_logger.debug(f"Project root: {_project_root}")
    _debug_logger.debug(f"modules/voice.py exists: {os.path.exists(os.path.join(_script_dir, 'modules', 'voice.py'))}")

from infra.logging_manager import get_logger
from core.system.system_monitor import SystemMonitor
from core.system.safe_mode import SafeModeManager, SafeModeContext
from core.system.system_recovery_center import RecoveryCenter
from core.vision.camera_router import CameraRouter, DummyCameraManager
from core.vision.vision_scheduler import VisionScheduler, SchedulerContext
from core.vision.vision_fail_safe import VisionFailSafe, FailSafeConfig
from core.task.task_transition_manager import (
    TaskTransitionManager,
    TaskContext,
    PositionState,
    UserIntentState,
)
from core.task.multi_target_buffer import MultiTargetBuffer, Target
from core.task.query_bus import QueryBus, Query
from navigation.navigation_controller import NavigationController, NavState
from speech.intent_parser import IntentParser
from speech.speech_pipeline import SpeechPipeline, DummyASR, DummyTTS

# 导入新的 TTS 模块（A 方案：使用 macOS say 命令）
from modules.voice_av import Voice
from Luna_Badge.core.tts_manager import TTSManager

logger = get_logger("main")

# 启动静音保护：启动后 2 秒内禁止任何语音触发
VOICE_READY = False

# =========================
# 单实例进程锁（防止多开）
# =========================
_LUNA_LOCK_PATH = "/tmp/luna_badge_main.lock"


def _acquire_single_instance_lock():
    """
    简单 PID 锁：
    - 如果 lock 文件存在，直接拒绝启动，提示用户
    - 避免出现多个 main.py + 多个 TTS 子进程并行
    """
    if os.path.exists(_LUNA_LOCK_PATH):
        try:
            with open(_LUNA_LOCK_PATH, "r") as f:
                old_pid_str = f.read().strip()
            old_pid = int(old_pid_str) if old_pid_str else None
        except Exception:
            old_pid = None

        # 提示信息尽量明确
        msg = f"Luna Badge 已在运行（lock={_LUNA_LOCK_PATH}"
        if old_pid:
            msg += f", pid={old_pid}"
        msg += "），本次启动已被拒绝。"
        print(msg)
        logger.error(msg)
        sys.exit(1)

    # 正常写入当前 PID
    try:
        with open(_LUNA_LOCK_PATH, "w") as f:
            f.write(str(os.getpid()))
        logger.info(f"[LOCK] 创建单实例锁: {_LUNA_LOCK_PATH} (pid={os.getpid()})")
    except Exception as e:
        logger.error(f"[LOCK] 创建单实例锁失败，但继续运行: {e}")

    def _cleanup_lock():
        try:
            if os.path.exists(_LUNA_LOCK_PATH):
                os.remove(_LUNA_LOCK_PATH)
                logger.info(f"[LOCK] 清理单实例锁: {_LUNA_LOCK_PATH}")
        except Exception as e:
            logger.warning(f"[LOCK] 清理单实例锁失败: {e}")

    atexit.register(_cleanup_lock)


# ========== TTS 防抖器 ==========
@dataclass
class TTSGuardConfig:
    same_text_interval: float = 8.0    # 同一句话 8 秒内只说一次
    min_interval_any: float = 0.3      # 全局调用最小间隔 300ms


class TTSGuard:
    """TTS 文本级防抖器（防止重复播报）"""
    
    def __init__(self, cfg: Optional[TTSGuardConfig] = None) -> None:
        self._cfg = cfg or TTSGuardConfig()
        self._last_text: Optional[str] = None
        self._last_text_ts: float = 0.0
        self._last_any_ts: float = 0.0

    def allow(self, text: str) -> bool:
        """
        检查是否允许播报
        
        Returns:
            bool: True 允许，False 拒绝
        """
        now = time.time()
        if not text or not text.strip():
            return False

        # 全局频率限制：避免在极端情况下每帧都来一个
        if now - self._last_any_ts < self._cfg.min_interval_any:
            return False

        # 同一句话防抖：避免"已到达目的地"这类话刷屏
        if text == self._last_text and now - self._last_text_ts < self._cfg.same_text_interval:
            return False

        self._last_any_ts = now
        self._last_text_ts = now
        self._last_text = text
        return True

# 初始化状态（用于禁止启动阶段播音）
INIT_READY = False


class App:
    def __init__(self) -> None:
        # 基础组件
        self.system_monitor = SystemMonitor()

        # 语音组件 - 使用新的统一架构
        self.voice = Voice()
        self.tts_manager = TTSManager()
        self._tts_guard = TTSGuard()  # TTS 防抖器
        
        # TTS 统一调用函数（带防抖）
        def tts_say(text: str) -> None:
            """统一 TTS 播报入口（带防抖）"""
            global VOICE_READY, INIT_READY
            # 双重保护：启动阶段和初始化阶段都禁止播报
            if not INIT_READY or not VOICE_READY:
                logger.debug(f"[TTS] 初始化保护中，跳过播报: {text[:30]}...")
                return

            if not text or not text.strip():
                return

            # 文本级防抖（兜底保护）
            if not self._tts_guard.allow(text):
                logger.debug(f"[TTS] guard drop: {text[:30]}...")
                return

            self.voice.speak(text, self.tts_manager)
        
        self.intent_parser = IntentParser()
        self.query_bus = QueryBus(tts_say)

        self.asr = DummyASR()
        # 使用 DummyTTS 作为 SpeechPipeline 的接口（它只打印日志，不实际播放）
        self.speech = SpeechPipeline(
            asr=self.asr,
            tts=DummyTTS(),
            query_bus=self.query_bus,
            intent_parser=self.intent_parser,
        )

        # SafeMode（重用同一个 tts_say）
        self.safe_mode = SafeModeManager(tts_say)

        # RecoveryCenter
        self.recovery_center = RecoveryCenter(
            get_cpu_load=self.system_monitor.cpu_usage,
            safe_mode_enter=self.safe_mode.enter,
            restart_vision=self._restart_vision,
            restart_speech=self._restart_speech,
        )
        self.recovery_center.register_module("vision", timeout_seconds=5.0)
        self.recovery_center.register_module("speech", timeout_seconds=5.0)

        # 视觉模块
        self.camera_router = CameraRouter()
        self.camera_manager = DummyCameraManager()
        self.vision_scheduler = VisionScheduler()
        self.vision_fail_safe = VisionFailSafe(FailSafeConfig())

        # 任务 / 导航（重用同一个 tts_say）
        self.multi_target_buffer = MultiTargetBuffer()
        self.nav_controller = NavigationController(tts_say)
        self.task_transition_manager = TaskTransitionManager(
            ask_end_callback=self._ask_end_task
        )

        self._running = False

    # ---------- Recovery 回调 ----------

    def _restart_vision(self) -> None:
        logger.warning("[RECOVERY] restarting vision pipeline")

    def _restart_speech(self) -> None:
        logger.warning("[RECOVERY] restarting speech pipeline")

    # ---------- QueryBus 回调 ----------

    def _ask_end_task(self) -> None:
        if not self.nav_controller.has_active_target():
            return

        q = Query(
            id="end_task",
            priority=10,
            created_ts=time.time(),
            text="您已经接近目的地，需要结束当前任务吗？",
            timeout_seconds=15.0,
            on_resolved=self._handle_end_task_answer,
        )
        self.query_bus.push_query(q)

    def _handle_end_task_answer(self, result: dict) -> None:
        answer = result.get("answer")
        # 清除 ASK_END 待处理状态
        self.task_transition_manager.clear_ask_end_pending()
        
        if answer == "yes":
            self.voice.speak("好的，已结束任务。", self.tts_manager)
            self.nav_controller.stop()
        elif answer == "no":
            self.voice.speak("好的，我会继续保持导航。", self.tts_manager)
        else:
            self.voice.speak("我没有听清楚，就先继续导航。", self.tts_manager)

    # ---------- 主循环 ----------

    def start(self) -> None:
        global VOICE_READY, INIT_READY
        
        self._running = True

        # ------------------------------------------
        # 阶段 1：基础模块加载（不触发任何声卡请求）
        # ------------------------------------------
        logger.info("[INIT-1] 加载基础组件...")
        # Voice 和 TTSManager 已初始化，但禁止播放
        logger.info("[INIT-1] 基础组件加载完成")

        # ------------------------------------------
        # 阶段 2：视觉模块初始化（独立线程，不阻塞）
        # ------------------------------------------
        logger.info("[INIT-2] 视觉模块初始化中...")
        # 视觉模块已在 __init__ 中初始化，这里只是标记
        logger.info("[INIT-2] 视觉模块初始化完成")

        # ------------------------------------------
        # 阶段 3：等待所有模块就绪
        # ------------------------------------------
        logger.info("[INIT] 等待所有模块就绪...")
        # 给系统一点时间完成初始化
        time.sleep(0.5)
        
        # 标记初始化完成
        INIT_READY = True
        logger.info("[INIT] 所有模块初始化完毕，系统进入正常工作模式")

        # 启动静音保护：延迟 2 秒解锁语音
        def boot_sequence():
            global VOICE_READY
            logger.info("[BOOT] 启动静音保护，2 秒后解锁语音...")
            time.sleep(2)
            VOICE_READY = True
            logger.info("[BOOT] 语音系统已就绪")
            # 播报启动提示（此时 INIT_READY 和 VOICE_READY 都已为 True）
            status = self.voice.get_status()
            logger.info(f"[BOOT] Voice 状态: {status}")
            if status.get('available'):
                logger.info("[BOOT] 开始播报启动提示...")
                result = self.voice.speak("Luna 已启动", self.tts_manager)
                logger.info(f"[BOOT] 启动播报结果: {result}")
            else:
                logger.warning("[BOOT] Voice 不可用，跳过启动播报")
        
        boot_thread = threading.Thread(target=boot_sequence, daemon=True)
        boot_thread.start()

        # 启动语音线程（简单版本）
        speech_thread = threading.Thread(target=self.speech.loop, daemon=True)
        speech_thread.start()

        # 初始化一个示例目标
        demo_target = Target(
            id="t1", name="示例地点", lat=0.0, lng=0.0, extra={}
        )
        self.multi_target_buffer.add_target(demo_target)
        current_target = self.multi_target_buffer.start()
        if current_target:
            self.nav_controller.start(current_target)

        last_infer_ts = 0.0

        while self._running:
            now = time.time()

            # 1) 系统心跳 + 健康检查
            self.recovery_center.update_heartbeat("vision")
            self.recovery_center.update_heartbeat("speech")
            self.recovery_center.tick()
            self.query_bus.tick()

            # 2) SafeMode 下仅做基础防撞
            if self.safe_mode.is_active():
                frame = self.camera_manager.read(self.camera_router.get_active_camera())
                distance = 1.5  # 简化：假设检测到的障碍距离
                self.safe_mode.handle_frame(SafeModeContext(obstacle_distance=distance))
                time.sleep(0.05)
                continue

            # 3) 摄像头选择 & 采集
            frame = self.camera_manager.read(self.camera_router.get_active_camera())
            if frame is None:
                self.vision_fail_safe.report_camera_error()
                time.sleep(0.05)
                continue

            # 4) 调度推理节奏
            scheduler_ctx = SchedulerContext(
                cpu_load=self.system_monitor.cpu_usage(),
                motion_detected=True,
                task_priority=5,
                last_infer_ts=last_infer_ts,
                now_ts=now,
            )
            if not self.vision_scheduler.should_infer(scheduler_ctx):
                time.sleep(0.01)
                continue
            last_infer_ts = now

            # 5) 根据 FailSafe 状态选择模型
            model_name = (
                "tiny" if self.vision_fail_safe.get_state() == "degraded" else "main"
            )

            # 这里用 dummy 检测结果代替真正的模型调用
            objects = [{"type": "obstacle", "distance": 1.2, "model": model_name}]

            # 6) 导航一步
            nav_state: NavState = self.nav_controller.step(objects)

            # 7) 任务状态判断
            task_ctx = TaskContext(
                position=PositionState(
                    at_target=nav_state.at_target,
                    distance_to_target=nav_state.distance,
                    stationary_seconds=0.0,
                ),
                intent=UserIntentState(
                    want_stop=False,
                    want_continue=True,
                ),
            )
            decision = self.task_transition_manager.decide(task_ctx)

            if decision is not None:
                # END 在回调里已经 stop；ASK_END 已经发 query；KEEP 什么都不做
                pass

            time.sleep(0.05)

    def stop(self) -> None:
        self._running = False


if __name__ == "__main__":
    # 最先执行：防止多进程同时运行
    _acquire_single_instance_lock()
    
    app = App()
    try:
        app.start()
    except KeyboardInterrupt:
        logger.info("Exiting main loop by keyboard interrupt.")
        app.stop()
