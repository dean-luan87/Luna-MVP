#!/usr/bin/env python3
"""
视觉管线集成点
v1.4.2: 整合 camera_router, vision_scheduler, vision_fail_safe
"""
import time
import logging
from typing import Optional, Dict, Any, Tuple

from core.vision.camera_router import CameraRouter, CameraId
from core.vision.vision_scheduler import VisionScheduler, SchedulerContext
from core.vision.vision_fail_safe import VisionFailSafe
from core.config.config_center import ConfigCenter

logger = logging.getLogger(__name__)


class VisionPipeline:
    """
    视觉管线：整合摄像头、调度器、降级机制、模型切换
    """
    
    def __init__(
        self,
        camera_router: Optional[CameraRouter] = None,
        vision_scheduler: Optional[VisionScheduler] = None,
        vision_fail_safe: Optional[VisionFailSafe] = None,
        model_predict: Optional[callable] = None,
        model_tiny_predict: Optional[callable] = None,
        recovery_center: Optional[Any] = None,
    ):
        """
        初始化视觉管线
        
        Args:
            camera_router: 摄像头路由器（如果为 None 则自动创建）
            vision_scheduler: 视觉调度器（如果为 None 则自动创建）
            vision_fail_safe: 视觉降级（如果为 None 则自动创建）
            model_predict: 模型推理函数 frame -> results
        """
        self.camera_router = camera_router or CameraRouter()
        self.vision_scheduler = vision_scheduler or VisionScheduler()
        self.vision_fail_safe = vision_fail_safe or VisionFailSafe()
        self.model_predict = model_predict  # 主模型
        self.model_tiny_predict = model_tiny_predict  # Tiny 模型
        self.recovery_center = recovery_center
        
        self.last_infer_ts = 0.0
        self.frame_count = 0
        self.error_count = 0
        
        # 设置降级回调
        self.vision_fail_safe.set_degraded_callback(self._on_degraded)
        self.vision_fail_safe.set_critical_callback(self._on_critical)
        
        logger.info("[VISION_PIPELINE] Initialized")
    
    def _on_degraded(self) -> None:
        """降级回调"""
        logger.error("[VISION_PIPELINE] Vision enters degraded mode, switching to Tiny model")
        # 模型切换逻辑在 infer() 中实现
    
    def _on_critical(self) -> None:
        """严重错误回调"""
        logger.critical("[VISION_PIPELINE] Vision enters critical mode")
        # 可以触发 SafeMode 等
    
    def get_frame(self, context: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Any], CameraId]:
        """
        获取摄像头帧（带调度和错误处理）
        
        Args:
            context: 上下文信息（用于摄像头选择）
        
        Returns:
            (frame, camera_id): 帧数据和摄像头ID
        """
        # 决定用哪个摄像头
        cam_id = self.camera_router.select_camera(context)
        logger.debug(f"[VISION_PIPELINE] Selected camera: {cam_id}")
        
        # 获取帧
        frame, active_cam = self.camera_router.get_frame()
        
        if frame is None:
            logger.warning(f"[VISION_PIPELINE] Camera {active_cam} returned empty frame")
            self.vision_fail_safe.report_camera_error()
            self.error_count += 1
            return None, active_cam
        
        self.frame_count += 1
        return frame, active_cam
    
    def should_infer(
        self,
        cpu_load: float,
        motion_detected: bool,
        task_priority: int,
    ) -> bool:
        """
        判断是否应该执行推理
        
        Args:
            cpu_load: CPU 负载 (0.0 ~ 1.0)
            motion_detected: 是否检测到移动
            task_priority: 任务优先级 (1~10)
        
        Returns:
            是否应该推理
        """
        now = time.time()
        scheduler_ctx = SchedulerContext(
            cpu_load=cpu_load,
            motion_detected=motion_detected,
            task_priority=task_priority,
            last_infer_ts=self.last_infer_ts,
            now_ts=now,
        )
        
        should = self.vision_scheduler.should_infer(scheduler_ctx)
        if should:
            logger.debug(f"[VISION_PIPELINE] Should infer: mode={self.vision_scheduler.get_mode()}")
        return should
    
    def infer(self, frame: Any) -> Optional[Dict[str, Any]]:
        """
        执行推理（带错误处理和模型切换）
        
        Args:
            frame: 输入帧
        
        Returns:
            推理结果，如果失败则返回 None
        """
        # 根据降级状态选择模型
        fail_safe_state = self.vision_fail_safe.get_state()
        
        if fail_safe_state == "degraded" and self.model_tiny_predict:
            # 使用 Tiny 模型
            current_model = self.model_tiny_predict
            logger.debug("[VISION_PIPELINE] Using Tiny model (degraded mode)")
        elif fail_safe_state == "critical" and self.model_tiny_predict:
            # 严重模式也使用 Tiny 模型
            current_model = self.model_tiny_predict
            logger.debug("[VISION_PIPELINE] Using Tiny model (critical mode)")
        else:
            # 使用主模型
            current_model = self.model_predict
            if current_model is None:
                logger.error("[VISION_PIPELINE] model_predict not set")
                return None
        
        try:
            # 更新心跳
            if self.recovery_center:
                self.recovery_center.update_heartbeat("vision")
            
            # 设置超时（如果模型支持）
            start_ts = time.time()
            results = current_model(frame)
            infer_time = time.time() - start_ts
            
            # 检查是否超时（阈值从配置读取）
            timeout_threshold = ConfigCenter.get("vision.infer_timeout", 0.8)
            if infer_time > timeout_threshold:
                logger.warning(f"[VISION_PIPELINE] Inference timeout: {infer_time:.3f}s > {timeout_threshold}s")
                self.vision_fail_safe.report_infer_timeout()
                return None
            
            self.last_infer_ts = time.time()
            self.error_count = 0
            logger.debug(f"[VISION_PIPELINE] Inference success: {infer_time:.3f}s, model={'tiny' if fail_safe_state != 'normal' else 'main'}")
            return results
            
        except TimeoutError as e:
            logger.error(f"[VISION_PIPELINE] Inference timeout error: {e}")
            self.vision_fail_safe.report_infer_timeout()
            self.error_count += 1
            return None
            
        except Exception as e:
            logger.exception(f"[VISION_PIPELINE] Inference error: {e}")
            self.vision_fail_safe.report_model_error()
            self.error_count += 1
            return None
    
    def process_frame(
        self,
        context: Optional[Dict[str, Any]] = None,
        cpu_load: float = 0.5,
        motion_detected: bool = True,
        task_priority: int = 5,
    ) -> Optional[Dict[str, Any]]:
        """
        处理单帧（完整流程）
        
        Args:
            context: 上下文信息
            cpu_load: CPU 负载
            motion_detected: 是否检测到移动
            task_priority: 任务优先级
        
        Returns:
            推理结果，如果跳过或失败则返回 None
        """
        # 1. 获取帧
        frame, cam_id = self.get_frame(context)
        if frame is None:
            return None
        
        # 2. 调度判断
        if not self.should_infer(cpu_load, motion_detected, task_priority):
            return None
        
        # 3. 执行推理
        results = self.infer(frame)
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "frame_count": self.frame_count,
            "error_count": self.error_count,
            "last_infer_ts": self.last_infer_ts,
            "fail_safe_state": self.vision_fail_safe.get_state(),
            "scheduler_mode": self.vision_scheduler.get_mode(),
            "active_camera": self.camera_router.get_active_camera(),
        }
    
    def release(self) -> None:
        """释放资源"""
        self.camera_router.release()
        logger.info("[VISION_PIPELINE] Released")

