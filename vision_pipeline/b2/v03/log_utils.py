# vision_pipeline/b2/v03/log_utils.py
# B2 v0.3 日志工具：人类可读 + 工程可审计

import time
from typing import List, Optional, Dict
from enum import Enum


class LogLevel(str, Enum):
    """日志级别"""
    TICK = "TICK"
    FACTOR = "FACTOR"
    EVAL = "EVAL"  # 评估但未升级（HOLD）
    DECISION = "DECISION"
    INVALIDATE = "INVALIDATE"


class B2Logger:
    """
    B2 v0.3 统一日志记录器
    - 人类可读的时间格式
    - 结构化的日志输出
    - 不干扰性能、不污染C
    """
    
    def __init__(self, mode: str = "video", base_ts: Optional[float] = None, enable: bool = True):
        """
        :param mode: "video" 或 "realtime"
        :param base_ts: 视频模式的基准时间戳（用于计算偏移）
        :param enable: 是否启用日志
        """
        self.mode = mode
        self.base_ts = base_ts
        self.enable = enable
        
        # 用于跟踪因子变化（避免重复打印）
        self._last_factor_states = {}
    
    def format_ts(self, ts: float) -> str:
        """格式化时间戳为人类可读格式"""
        if not self.enable:
            return ""
        
        if self.mode == "video" and self.base_ts is not None:
            offset = ts - self.base_ts
            m = int(offset // 60)
            s = int(offset % 60)
            return f"{m:02d}:{s:02d}"
        else:
            return time.strftime("%H:%M:%S", time.localtime(ts))
    
    def _log(self, level: LogLevel, ts: float, message: str, indent: int = 0):
        """内部日志方法"""
        if not self.enable:
            return
        
        time_str = self.format_ts(ts)
        prefix = "[B2-v0.3]" + "[" + level.value + "]" + f"[{time_str}]"
        indent_str = "  " * indent
        
        print(f"{prefix} {indent_str}{message}")
    
    def tick(self, ts: float, window_size: float, active_factors: List[str]):
        """TICK 日志：每个 tick 一行，极简"""
        if not active_factors:
            factors_str = "none"
        else:
            factors_str = ",".join(active_factors)
        
        self._log(LogLevel.TICK, ts, f"window={window_size:.0f}s factors={factors_str}")
    
    def factor(self, ts: float, factor_name: str, change_desc: str, direction: str = "↑"):
        """
        FACTOR 日志：只在因子变化时打印
        :param ts: 时间戳
        :param factor_name: 因子名称
        :param change_desc: 变化描述（人类可读）
        :param direction: "↑" 或 "↓"
        """
        # 检查是否重复（避免同一变化重复打印）
        key = f"{factor_name}:{change_desc}"
        if key in self._last_factor_states:
            return
        
        self._last_factor_states[key] = ts
        self._log(LogLevel.FACTOR, ts, f"{factor_name} {direction} {change_desc}")
    
    def eval_hold(self, ts: float, scores: Dict[str, float], reason: str = ""):
        """
        EVAL 日志：评估但未升级（HOLD）
        :param ts: 时间戳
        :param scores: 因子分数字典
        :param reason: 未升级的原因
        """
        scores_str = " ".join([f"{k}={v:.2f}" for k, v in scores.items()])
        reason_str = f" ({reason})" if reason else ""
        self._log(LogLevel.EVAL, ts, f"scores: {scores_str} decision: HOLD{reason_str}")
    
    def decision(
        self,
        ts: float,
        decision_type: str,
        main_factor: str,
        confidence: float,
        reason: str
    ):
        """
        DECISION 日志：关键输出（最重要）
        
        NOTE:
        - NOTICE == NO_OP == SILENT（不进入 timeline）
        - timeline 不一定有记录（只有行为影响时才记录）
        - 此日志用于内部调试，NOTICE 也会记录但不对外输出
        
        :param ts: 时间戳
        :param decision_type: INTERRUPT / CONDITION_CHANGE / NOTICE
            - INTERRUPT: 需要立即改变行为（NEED_STOP / NEED_DETOUR）
            - CONDITION_CHANGE: 需要调整行为（NEED_SLOW_DOWN / PATH_UNCERTAIN）
            - NOTICE: 不影响行为（NO_OP / SILENT，等价于无影响，不写入 timeline）
        :param main_factor: 主因子名称
        :param confidence: 置信度
        :param reason: 原因（人类可读）
        """
        self._log(LogLevel.DECISION, ts, decision_type)
        self._log(LogLevel.DECISION, ts, f"└─ main: {main_factor}", indent=1)
        self._log(LogLevel.DECISION, ts, f"└─ confidence: {confidence:.2f}", indent=1)
        self._log(LogLevel.DECISION, ts, f"└─ reason: {reason}", indent=1)
    
    def invalidate(self, ts: float, reason: str):
        """
        INVALIDATE 日志：世界作废 / 重置
        :param ts: 时间戳
        :param reason: 作废原因（人类可读）
        """
        self._log(LogLevel.INVALIDATE, ts, reason)
        # 清空因子状态缓存（因为世界被重置）
        self._last_factor_states.clear()
    
    def clear_factor_cache(self):
        """清空因子状态缓存（用于世界重置）"""
        self._last_factor_states.clear()

