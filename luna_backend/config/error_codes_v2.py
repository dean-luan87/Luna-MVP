"""
错误码规范 v2.0 (v1.2.0)
使用命名空间方式组织错误码，便于管理和扩展
"""


class _ErrorNamespace:
    """错误码命名空间"""
    
    def __init__(self, prefix: str, mapping: dict):
        """
        初始化命名空间
        
        Args:
            prefix: 前缀（如 "NAV"）
            mapping: 错误码映射字典 {code_name: description}
        """
        self._prefix = prefix
        self._mapping = mapping
    
    def __getattr__(self, name: str) -> str:
        """
        获取错误码
        
        Args:
            name: 错误码名称
        
        Returns:
            完整错误码字符串（如 "NAV_MANAGER_NOT_INITIALIZED"）
        """
        if name not in self._mapping:
            raise AttributeError(f"Unknown error code: {self._prefix}_{name}")
        return f"{self._prefix}_{name}"
    
    def describe(self, name: str) -> str:
        """
        获取错误码描述
        
        Args:
            name: 错误码名称
        
        Returns:
            错误描述
        """
        return self._mapping.get(name, "")


class ErrorCode:
    """
    错误码类（命名空间方式）
    
    使用示例:
        ErrorCode.NAV.MANAGER_NOT_INITIALIZED  # 返回 "NAV_MANAGER_NOT_INITIALIZED"
        ErrorCode.NAV.describe("MANAGER_NOT_INITIALIZED")  # 返回 "导航管理器未初始化"
    """
    
    # ===== 通用 =====
    COMMON = _ErrorNamespace("COMMON", {
        "UNKNOWN": "未知错误",
        "INVALID_PARAM": "参数不合法",
        "INTERNAL": "服务器内部错误",
        "MISSING_PARAM": "缺少必要参数",
    })
    
    # ===== 视觉子系统 =====
    VISION = _ErrorNamespace("VISION", {
        "ENGINE_NOT_INITIALIZED": "视觉引擎未初始化",
        "IMAGE_INVALID": "图片格式错误或无法解析",
        "STEP_DETECTOR_NOT_INIT": "台阶检测器未初始化",
        "HAZARD_DETECTOR_NOT_INIT": "危险检测器未初始化",
        "SIGNBOARD_DETECTOR_NOT_INIT": "标识牌检测器未初始化",
        "FACILITY_DETECTOR_NOT_INIT": "公共设施检测器未初始化",
        "TRAFFIC_DETECTOR_NOT_INIT": "红绿灯检测器未初始化",
        "CROWD_DETECTOR_NOT_INIT": "人群密度检测器未初始化",
        "QUEUE_DETECTOR_NOT_INIT": "排队检测器未初始化",
        "DOORPLATE_READER_NOT_INIT": "门牌号识别器未初始化",
    })
    
    # ===== 导航子系统 =====
    NAV = _ErrorNamespace("NAV", {
        "MANAGER_NOT_INITIALIZED": "导航管理器未初始化",
        "PLANNER_NOT_INITIALIZED": "路径规划器未初始化",
        "DESTINATION_MISSING": "缺少目的地参数",
        "START_FAILED": "导航启动失败，可能已有导航在进行中",
        "STATE_INVALID": "当前导航状态不允许此操作",
        "STRATEGY_EXEC_ERROR": "导航策略执行异常",
        "STRATEGY_SELECT_ERROR": "导航策略选择异常",
        "UPDATE_ENV_INVALID": "导航环境数据不完整或非法",
        "PAUSE_FAILED": "暂停导航失败",
        "RESUME_FAILED": "恢复导航失败",
        "CANCEL_FAILED": "取消导航失败",
        "COMPLETE_FAILED": "完成导航失败",
    })
    
    # ===== TTS / 语音 =====
    TTS = _ErrorNamespace("TTS", {
        "ENGINE_NOT_INITIALIZED": "TTS引擎未初始化",
        "SYNTH_FAILED": "TTS合成失败",
        "TEXT_EMPTY": "TTS文本为空",
        "CACHE_ERROR": "TTS缓存错误",
    })
    
    # ===== 音频 =====
    AUDIO = _ErrorNamespace("AUDIO", {
        "DEVICE_ERROR": "音频设备错误",
        "STREAM_ERROR": "音频流错误",
    })


# 向后兼容：保留旧的ERR类
from .error_codes import ERR

__all__ = ['ErrorCode', 'ERR']



