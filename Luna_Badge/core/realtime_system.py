"""
Luna Badge 实时响应系统核心模块
实现机器人式低延迟高效反馈架构
"""

import time
import threading
import queue
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


@dataclass
class FrameEvent:
    """时间同步事件"""
    timestamp: float
    source: str  # 'camera' | 'microphone'
    sequence: int
    kind: str  # 'frame' | 'audio'
    payload: Any = None


class TimeSyncBus:
    """时间同步总线 - 对齐多模态时间戳（增强版：带环形缓冲池）"""
    
    def __init__(self, buffer_size: int = 128):
        self.listeners: List[Callable[[FrameEvent], None]] = []
        self.lock = threading.Lock()
        self.sequence = 0
        self.buffer: List[Optional[FrameEvent]] = [None] * buffer_size
        self.buffer_size = buffer_size
        self.head = 0
    
    def emit(self, source: str, kind: str, payload: Any = None):
        """发送事件（增强版：自动管理序列号和缓冲）"""
        event = FrameEvent(
            timestamp=time.time(),
            source=source,
            sequence=self.sequence,
            kind=kind,
            payload=payload
        )
        self.sequence = (self.sequence + 1) % 1000000
        
        # 写入环形缓冲
        with self.lock:
            self.buffer[self.head % self.buffer_size] = event
            self.head += 1
            
            # 通知所有监听器
            for listener in self.listeners:
                try:
                    listener(event)
                except Exception as e:
                    logger.error(f"事件监听器错误: {e}")
    
    def on(self, callback: Callable[[FrameEvent], None]):
        """注册事件监听器"""
        with self.lock:
            self.listeners.append(callback)
    
    def off(self, callback: Callable[[FrameEvent], None]):
        """移除事件监听器"""
        with self.lock:
            if callback in self.listeners:
                self.listeners.remove(callback)
    
    def get_recent_events(self, count: int = 10) -> List[FrameEvent]:
        """获取最近的事件"""
        with self.lock:
            events = []
            start = max(0, self.head - count)
            for i in range(start, self.head):
                event = self.buffer[i % self.buffer_size]
                if event:
                    events.append(event)
            return events


class StateEstimator:
    """状态估计器 - 平滑与预测感知结果（增强版：含滞回逻辑）"""
    
    def __init__(self, alpha: float = 0.6, hysteresis_up: int = 3, hysteresis_down: int = 5):
        """
        Args:
            alpha: EMA平滑系数 (0-1)，越大越敏感
            hysteresis_up: 上升滞回阈值
            hysteresis_down: 下降滞回阈值
        """
        self.alpha = alpha
        self.last_value = 0.0
        self.current_value = 0.0
        self.update_count = 0
        self.stable_count = 0
        self.hysteresis_up = hysteresis_up
        self.hysteresis_down = hysteresis_down
    
    def update(self, new_value: float) -> float:
        """更新状态值（EMA平滑 + 滞回）"""
        self.update_count += 1
        self.last_value = self.current_value
        
        if self.update_count == 1:
            self.current_value = new_value
        else:
            # EMA: value = alpha * new + (1-alpha) * old
            self.current_value = self.alpha * new_value + (1 - self.alpha) * self.current_value
        
        # 滞回逻辑：比较新值和当前EMA值
        if new_value > self.current_value:
            self.stable_count = min(self.stable_count + 1, self.hysteresis_up)
        elif new_value < self.current_value:
            self.stable_count = max(self.stable_count - 1, -self.hysteresis_down)
        # 如果相等，保持当前计数
        
        return self.current_value
    
    def get(self) -> float:
        """获取当前估计值"""
        return self.current_value
    
    @property
    def stable_high(self) -> bool:
        """是否稳定在高位"""
        return self.stable_count >= self.hysteresis_up
    
    @property
    def stable_low(self) -> bool:
        """是否稳定在低位"""
        return self.stable_count <= -self.hysteresis_down
    
    def reset(self):
        """重置状态"""
        self.last_value = 0.0
        self.current_value = 0.0
        self.update_count = 0
        self.stable_count = 0


class RTScheduler:
    """实时调度器 - 高低优先级任务队列（增强版：性能监控）"""
    
    def __init__(self):
        self.high_priority_queue = queue.Queue()
        self.low_priority_queue = queue.Queue()
        self.is_running = False
        self.worker_thread = None
        self.lock = threading.Lock()
        self.metrics = {
            'p50': 0.0,
            'p95': 0.0,
            'p99': 0.0,
            'history': []
        }
    
    def start(self):
        """启动调度器"""
        if self.is_running:
            return
        
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        logger.info("✅ 实时调度器已启动")
    
    def stop(self):
        """停止调度器"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2.0)
        logger.info("🛑 实时调度器已停止")
    
    def enqueue_high(self, job: Callable[[], Any]):
        """添加高优先级任务"""
        self.high_priority_queue.put(job)
    
    def enqueue_low(self, job: Callable[[], Any]):
        """添加低优先级任务"""
        self.low_priority_queue.put(job)
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        with self.lock:
            return {
                'p50': self.metrics['p50'],
                'p95': self.metrics['p95'],
                'p99': self.metrics['p99'],
                'count': len(self.metrics['history'])
            }
    
    def _update_metrics(self, duration: float):
        """更新性能指标"""
        with self.lock:
            history = self.metrics['history']
            history.append(duration)
            
            # 保持最近100个记录
            if len(history) > 100:
                history.pop(0)
            
            # 计算百分位数
            if history:
                sorted_history = sorted(history)
                count = len(sorted_history)
                self.metrics['p50'] = sorted_history[int(count * 0.5)] if count > 0 else 0
                self.metrics['p95'] = sorted_history[int(count * 0.95)] if count > 0 else 0
                self.metrics['p99'] = sorted_history[int(count * 0.99)] if count > 0 else 0
    
    def _worker_loop(self):
        """工作循环"""
        while self.is_running:
            try:
                # 优先处理高优先级任务
                if not self.high_priority_queue.empty():
                    job = self.high_priority_queue.get(timeout=0.1)
                elif not self.low_priority_queue.empty():
                    job = self.low_priority_queue.get(timeout=0.1)
                else:
                    time.sleep(0.01)  # 避免CPU空转
                    continue
                
                # 执行任务并记录性能
                start_time = time.time()
                try:
                    result = job()
                    if hasattr(result, '__await__'):  # 异步任务
                        import asyncio
                        asyncio.create_task(result)
                except Exception as e:
                    logger.error(f"任务执行错误: {e}")
                
                # 记录执行时间
                execution_time = (time.time() - start_time) * 1000  # 转换为毫秒
                self._update_metrics(execution_time)
                
                # 如果任务执行时间过长，让出CPU
                if execution_time > 16:  # 超过16ms
                    time.sleep(0.001)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"调度器错误: {e}")


class EventPolicyGraph:
    """事件策略图 - 声明式策略触发系统（增强版：动作执行）"""
    
    def __init__(self):
        self.rules: List[Dict[str, Any]] = []
        self.cooldowns: Dict[str, float] = {}
        self.actions: Dict[str, Callable[[], None]] = {}
        self.lock = threading.Lock()
    
    def load_rules(self, rules: List[Dict[str, Any]]):
        """加载策略规则"""
        with self.lock:
            self.rules = sorted(rules, key=lambda r: r.get('priority', 0), reverse=True)
        logger.info(f"✅ 加载了 {len(self.rules)} 条策略规则")
    
    def register_actions(self, action_map: Dict[str, Callable[[], None]]):
        """注册动作映射"""
        with self.lock:
            self.actions.update(action_map)
        logger.info(f"✅ 注册了 {len(action_map)} 个动作")
    
    def eval(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        评估上下文并返回触发的动作
        
        Args:
            context: 上下文字典，包含 vision, audio 等状态
            
        Returns:
            触发的动作列表，每个元素包含 rule 和 acts
        """
        triggered = []
        now = time.time()
        
        with self.lock:
            for rule in self.rules:
                try:
                    # 检查条件
                    if not self._check_condition(rule.get('when', ''), context):
                        continue
                    
                    # 检查冷却时间
                    rule_key = rule.get('when', '')
                    cooldown_ms = rule.get('cooldownMs', 0)
                    if cooldown_ms > 0:
                        last_trigger = self.cooldowns.get(rule_key, 0)
                        if (now - last_trigger) * 1000 < cooldown_ms:
                            continue
                        self.cooldowns[rule_key] = now
                    
                    # 执行动作
                    rule_actions = rule.get('do', [])
                    executed_actions = []
                    
                    for action in rule_actions:
                        if isinstance(action, str):
                            # 解析动作：格式为 "action:param" 或 "action"
                            parts = action.split(':', 1)
                            action_name = parts[0]
                            action_param = parts[1] if len(parts) > 1 else None
                            
                            # 执行注册的动作
                            if action_name in self.actions:
                                try:
                                    if action_param:
                                        # 如果有参数，尝试调用
                                        self.actions[action_name](action_param)
                                    else:
                                        self.actions[action_name]()
                                    executed_actions.append(action)
                                except Exception as e:
                                    logger.warning(f"动作执行错误: {action_name}, {e}")
                            else:
                                logger.warning(f"未注册的动作: {action_name}")
                    
                    if executed_actions:
                        triggered.append({
                            'rule': rule_key,
                            'actions': executed_actions
                        })
                
                except Exception as e:
                    logger.warning(f"规则评估错误: {e}")
                    continue
        
        return triggered
    
    def _check_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """检查条件表达式（增强版：支持get()方法）"""
        if not condition:
            return False
        
        try:
            # 将条件转换为可执行的Python表达式
            # 处理 vision.get('xxx', default) 格式
            expr = condition
            
            # 替换字典访问为实际值
            for key, value in context.items():
                if isinstance(value, dict):
                    # 处理 vision.get('stepDetected', False) == True
                    # 先替换 get() 调用
                    import re
                    pattern = rf"{key}\.get\(['\"]([^'\"]+)['\"],\s*([^)]+)\)"
                    matches = re.findall(pattern, expr)
                    for sub_key, default_val in matches:
                        actual_value = value.get(sub_key, eval(default_val) if default_val.strip() in ['True', 'False', 'None'] else default_val)
                        expr = expr.replace(f"{key}.get('{sub_key}', {default_val})", str(actual_value))
                        expr = expr.replace(f'{key}.get("{sub_key}", {default_val})', str(actual_value))
                    
                    # 处理简单的 vision.xxx 格式
                    for sub_key, sub_value in value.items():
                        # 避免重复替换
                        if f"{key}.{sub_key}" in expr and f"{key}.get(" not in expr:
                            expr = expr.replace(f"{key}.{sub_key}", str(sub_value))
                else:
                    expr = expr.replace(key, str(value))
            
            # 执行表达式
            result = eval(expr, {"__builtins__": {}}, {})
            return bool(result)
        except Exception as e:
            logger.warning(f"条件检查错误: {condition}, {e}")
            return False


class GracefulDegrader:
    """优雅降级器 - 根据延迟/内存动态降级（增强版：完善监控）"""
    
    class DegradeLevel(Enum):
        NORMAL = "normal"
        MEDIUM = "medium"
        LOW = "low"
    
    def __init__(self, 
                 monitor_callback: Callable[[], Dict[str, float]],
                 apply_callback: Callable[[DegradeLevel], None]):
        """
        Args:
            monitor_callback: 返回 {p95: 延迟p95值(ms), heap: 内存占用(MB), fps: 帧率}
            apply_callback: 应用降级级别的回调函数
        """
        self.monitor_callback = monitor_callback
        self.apply_callback = apply_callback
        self.last_adjust_time = 0
        self.current_level = self.DegradeLevel.NORMAL
        self.adjust_interval = 3.0  # 3秒调整一次
    
    def check(self):
        """检查并应用降级"""
        now = time.time()
        if now - self.last_adjust_time < self.adjust_interval:
            return
        
        try:
            metrics = self.monitor_callback()
            p95 = metrics.get('p95', 0)
            heap = metrics.get('heap', 0)
            fps = metrics.get('fps', 30)
            
            # 确定降级级别
            new_level = self.DegradeLevel.NORMAL
            
            if p95 > 150 or heap > 500:
                new_level = self.DegradeLevel.LOW
            elif p95 > 80 or heap > 350 or fps < 20:
                new_level = self.DegradeLevel.MEDIUM
            
            # 如果级别变化，应用降级
            if new_level != self.current_level:
                logger.info(f"📉 降级级别切换: {self.current_level.value} → {new_level.value} "
                          f"(p95={p95:.1f}ms, heap={heap:.1f}MB, fps={fps:.1f})")
                self.current_level = new_level
                self.apply_callback(new_level)
            
            self.last_adjust_time = now
        
        except Exception as e:
            logger.error(f"降级检查错误: {e}")
    
    @property
    def level(self) -> DegradeLevel:
        """获取当前降级级别"""
        return self.current_level


# 全局实例
_time_sync_bus: Optional[TimeSyncBus] = None
_rt_scheduler: Optional[RTScheduler] = None
_policy_graph: Optional[EventPolicyGraph] = None


def get_time_sync_bus() -> TimeSyncBus:
    """获取全局时间同步总线"""
    global _time_sync_bus
    if _time_sync_bus is None:
        _time_sync_bus = TimeSyncBus()
    return _time_sync_bus


def get_rt_scheduler() -> RTScheduler:
    """获取全局实时调度器"""
    global _rt_scheduler
    if _rt_scheduler is None:
        _rt_scheduler = RTScheduler()
        _rt_scheduler.start()
    return _rt_scheduler


def get_policy_graph() -> EventPolicyGraph:
    """获取全局策略图"""
    global _policy_graph
    if _policy_graph is None:
        _policy_graph = EventPolicyGraph()
    return _policy_graph

