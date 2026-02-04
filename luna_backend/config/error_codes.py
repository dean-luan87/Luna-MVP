# config/error_codes.py
# 统一错误码规范（Luna Badge 1.2.0）
#
# 设计目标：
#   1）通过错误码立刻知道：哪个模块（视觉 / 导航 / 音频...）+ 哪一类问题（未初始化 / 参数错误 / 处理失败）
#   2）统一结构，便于前后端 & 日志 & 监控系统使用
#   3）兼容现有 api_error 调用方式（既支持 key，也支持直接传字符串）

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, Optional


@unique
class ErrorCategory(str, Enum):
    SYSTEM = "SYS"          # 系统级（初始化 / 依赖 / 未知异常）
    VISION = "VIS"          # 通用视觉
    STEP = "STEP"           # 台阶检测
    SIGNBOARD = "SBD"       # 标识牌检测
    HAZARD = "HAZ"          # 危险区域检测
    FACILITY = "FAC"        # 公共设施检测
    TRAFFIC_LIGHT = "TL"    # 红绿灯检测
    CROWD = "CRD"           # 人群密度
    QUEUE = "QUE"           # 排队检测
    DOORPLATE = "DPT"       # 门牌号识别
    MAP = "MAP"             # 本地地图 / 小范围地图
    NAVIGATION = "NAV"      # 导航整体（路径规划 / 状态管理）
    AUDIO = "AUD"           # 语音识别
    TTS = "TTS"             # 语音合成
    CONFIG = "CFG"          # 配置 / 参数错误
    UNKNOWN = "UNK"         # 未归类


@dataclass(frozen=True)
class ErrorCodeSpec:
    # 例如： VIS-1001
    code: str
    category: ErrorCategory
    http_status: int
    # 面向开发 / 日志的说明（英文或中英均可）
    message: str
    # 面向用户的友好提示（可选）
    user_message: Optional[str] = None


# ========== 核心错误码注册表 ==========

ERROR_REGISTRY: Dict[str, ErrorCodeSpec] = {}


def register_error(
    key: str,
    code: str,
    category: ErrorCategory,
    http_status: int,
    message: str,
    user_message: Optional[str] = None,
) -> ErrorCodeSpec:
    """
    注册一个错误码。

    key:   在代码中使用的 key，例如 "VISION_ENGINE_NOT_INITIALIZED"
    code:  对外暴露的错误编号，例如 "VIS-1001"
    """
    spec = ErrorCodeSpec(
        code=code,
        category=category,
        http_status=http_status,
        message=message,
        user_message=user_message or message,
    )
    ERROR_REGISTRY[key] = spec
    return spec


# ========== 通用 / 系统级错误 ==========

DEFAULT_INTERNAL_ERROR = register_error(
    key="SYS_INTERNAL_ERROR",
    code="SYS-0001",
    category=ErrorCategory.SYSTEM,
    http_status=500,
    message="Internal server error",
    user_message="服务器开小差了，请稍后再试。",
)

register_error(
    key="SYS_BAD_REQUEST",
    code="SYS-0002",
    category=ErrorCategory.SYSTEM,
    http_status=400,
    message="Bad request",
    user_message="请求参数有误，请检查后重试。",
)

register_error(
    key="SYS_UNAUTHORIZED",
    code="SYS-0003",
    category=ErrorCategory.SYSTEM,
    http_status=401,
    message="Unauthorized",
    user_message="未授权访问。",
)

register_error(
    key="SYS_FORBIDDEN",
    code="SYS-0004",
    category=ErrorCategory.SYSTEM,
    http_status=403,
    message="Forbidden",
    user_message="没有权限执行此操作。",
)


# ========== 通用视觉模块（/api/recognize 等） ==========

register_error(
    key="VISION_ENGINE_NOT_INITIALIZED",
    code="VIS-1001",
    category=ErrorCategory.VISION,
    http_status=500,
    message="Vision engine is not initialized",
    user_message="视觉模块暂时不可用。",
)

register_error(
    key="VISION_IMAGE_MISSING",
    code="VIS-1002",
    category=ErrorCategory.VISION,
    http_status=400,
    message="No image uploaded",
    user_message="未上传图片。",
)

register_error(
    key="VISION_IMAGE_DECODE_FAILED",
    code="VIS-1003",
    category=ErrorCategory.VISION,
    http_status=400,
    message="Failed to decode image",
    user_message="图片格式不支持或已损坏。",
)

register_error(
    key="VISION_PROCESSING_FAILED",
    code="VIS-1004",
    category=ErrorCategory.VISION,
    http_status=500,
    message="Vision processing failed",
    user_message="视觉分析失败，请稍后重试。",
)


# ========== 台阶检测 ==========

register_error(
    key="STEP_DETECTOR_NOT_INITIALIZED",
    code="STEP-1001",
    category=ErrorCategory.STEP,
    http_status=500,
    message="Step detector is not initialized",
    user_message="台阶检测模块暂时不可用。",
)

register_error(
    key="STEP_IMAGE_MISSING",
    code="STEP-1002",
    category=ErrorCategory.STEP,
    http_status=400,
    message="No image uploaded for step detection",
    user_message="未上传用于台阶检测的图片。",
)

register_error(
    key="STEP_IMAGE_DECODE_FAILED",
    code="STEP-1003",
    category=ErrorCategory.STEP,
    http_status=400,
    message="Failed to decode image for step detection",
    user_message="台阶检测图片格式错误或损坏。",
)

register_error(
    key="STEP_DETECTION_FAILED",
    code="STEP-1004",
    category=ErrorCategory.STEP,
    http_status=500,
    message="Step detection failed",
    user_message="台阶检测失败，请稍后重试。",
)


# ========== 标识牌检测 ==========

register_error(
    key="SIGNBOARD_DETECTOR_NOT_INITIALIZED",
    code="SBD-1001",
    category=ErrorCategory.SIGNBOARD,
    http_status=500,
    message="Signboard detector is not initialized",
    user_message="标识牌检测模块暂时不可用。",
)

register_error(
    key="SIGNBOARD_IMAGE_MISSING",
    code="SBD-1002",
    category=ErrorCategory.SIGNBOARD,
    http_status=400,
    message="No image uploaded for signboard detection",
    user_message="未上传用于标识牌检测的图片。",
)

register_error(
    key="SIGNBOARD_IMAGE_DECODE_FAILED",
    code="SBD-1003",
    category=ErrorCategory.SIGNBOARD,
    http_status=400,
    message="Failed to decode image for signboard detection",
    user_message="标识牌检测图片格式错误或损坏。",
)

register_error(
    key="SIGNBOARD_DETECTION_FAILED",
    code="SBD-1004",
    category=ErrorCategory.SIGNBOARD,
    http_status=500,
    message="Signboard detection failed",
    user_message="标识牌检测失败，请稍后重试。",
)


# ========== 危险检测 ==========

register_error(
    key="HAZARD_DETECTOR_NOT_INITIALIZED",
    code="HAZ-1001",
    category=ErrorCategory.HAZARD,
    http_status=500,
    message="Hazard detector is not initialized",
    user_message="危险检测模块暂时不可用。",
)

register_error(
    key="HAZARD_IMAGE_MISSING",
    code="HAZ-1002",
    category=ErrorCategory.HAZARD,
    http_status=400,
    message="No image uploaded for hazard detection",
    user_message="未上传用于危险检测的图片。",
)

register_error(
    key="HAZARD_IMAGE_DECODE_FAILED",
    code="HAZ-1003",
    category=ErrorCategory.HAZARD,
    http_status=400,
    message="Failed to decode image for hazard detection",
    user_message="危险检测图片格式错误或损坏。",
)

register_error(
    key="HAZARD_DETECTION_FAILED",
    code="HAZ-1004",
    category=ErrorCategory.HAZARD,
    http_status=500,
    message="Hazard detection failed",
    user_message="危险检测失败，请稍后重试。",
)


# ========== 公共设施检测 ==========

register_error(
    key="FACILITY_DETECTOR_NOT_INITIALIZED",
    code="FAC-1001",
    category=ErrorCategory.FACILITY,
    http_status=500,
    message="Facility detector is not initialized",
    user_message="公共设施检测模块暂时不可用。",
)

register_error(
    key="FACILITY_IMAGE_MISSING",
    code="FAC-1002",
    category=ErrorCategory.FACILITY,
    http_status=400,
    message="No image uploaded for facility detection",
    user_message="未上传用于公共设施检测的图片。",
)

register_error(
    key="FACILITY_IMAGE_DECODE_FAILED",
    code="FAC-1003",
    category=ErrorCategory.FACILITY,
    http_status=400,
    message="Failed to decode image for facility detection",
    user_message="公共设施检测图片格式错误或损坏。",
)

register_error(
    key="FACILITY_DETECTION_FAILED",
    code="FAC-1004",
    category=ErrorCategory.FACILITY,
    http_status=500,
    message="Facility detection failed",
    user_message="公共设施检测失败，请稍后重试。",
)


# ========== 红绿灯检测 ==========

register_error(
    key="TRAFFIC_LIGHT_DETECTOR_NOT_INITIALIZED",
    code="TL-1001",
    category=ErrorCategory.TRAFFIC_LIGHT,
    http_status=500,
    message="Traffic light detector is not initialized",
    user_message="红绿灯检测模块暂时不可用。",
)

register_error(
    key="TRAFFIC_LIGHT_IMAGE_MISSING",
    code="TL-1002",
    category=ErrorCategory.TRAFFIC_LIGHT,
    http_status=400,
    message="No image uploaded for traffic light detection",
    user_message="未上传用于红绿灯检测的图片。",
)

register_error(
    key="TRAFFIC_LIGHT_IMAGE_DECODE_FAILED",
    code="TL-1003",
    category=ErrorCategory.TRAFFIC_LIGHT,
    http_status=400,
    message="Failed to decode image for traffic light detection",
    user_message="红绿灯检测图片格式错误或损坏。",
)

register_error(
    key="TRAFFIC_LIGHT_DETECTION_FAILED",
    code="TL-1004",
    category=ErrorCategory.TRAFFIC_LIGHT,
    http_status=500,
    message="Traffic light detection failed",
    user_message="红绿灯检测失败，请稍后重试。",
)


# ========== 人群密度检测 ==========

register_error(
    key="CROWD_DENSITY_DETECTOR_NOT_INITIALIZED",
    code="CRD-1001",
    category=ErrorCategory.CROWD,
    http_status=500,
    message="Crowd density detector is not initialized",
    user_message="人群密度检测模块暂时不可用。",
)

register_error(
    key="CROWD_DENSITY_IMAGE_MISSING",
    code="CRD-1002",
    category=ErrorCategory.CROWD,
    http_status=400,
    message="No image uploaded for crowd density detection",
    user_message="未上传用于人群密度检测的图片。",
)

register_error(
    key="CROWD_DENSITY_IMAGE_DECODE_FAILED",
    code="CRD-1003",
    category=ErrorCategory.CROWD,
    http_status=400,
    message="Failed to decode image for crowd density detection",
    user_message="人群密度检测图片格式错误或损坏。",
)

register_error(
    key="CROWD_DENSITY_DETECTION_FAILED",
    code="CRD-1004",
    category=ErrorCategory.CROWD,
    http_status=500,
    message="Crowd density detection failed",
    user_message="人群密度检测失败，请稍后重试。",
)


# ========== 排队检测 ==========

register_error(
    key="QUEUE_DETECTOR_NOT_INITIALIZED",
    code="QUE-1001",
    category=ErrorCategory.QUEUE,
    http_status=500,
    message="Queue detector is not initialized",
    user_message="排队检测模块暂时不可用。",
)

register_error(
    key="QUEUE_IMAGE_MISSING",
    code="QUE-1002",
    category=ErrorCategory.QUEUE,
    http_status=400,
    message="No image uploaded for queue detection",
    user_message="未上传用于排队检测的图片。",
)

register_error(
    key="QUEUE_IMAGE_DECODE_FAILED",
    code="QUE-1003",
    category=ErrorCategory.QUEUE,
    http_status=400,
    message="Failed to decode image for queue detection",
    user_message="排队检测图片格式错误或损坏。",
)

register_error(
    key="QUEUE_DETECTION_FAILED",
    code="QUE-1004",
    category=ErrorCategory.QUEUE,
    http_status=500,
    message="Queue detection failed",
    user_message="排队检测失败，请稍后重试。",
)


# ========== 门牌号识别 ==========

register_error(
    key="DOORPLATE_READER_NOT_INITIALIZED",
    code="DPT-1001",
    category=ErrorCategory.DOORPLATE,
    http_status=500,
    message="Doorplate reader is not initialized",
    user_message="门牌号识别模块暂时不可用。",
)

register_error(
    key="DOORPLATE_IMAGE_MISSING",
    code="DPT-1002",
    category=ErrorCategory.DOORPLATE,
    http_status=400,
    message="No image uploaded for doorplate recognition",
    user_message="未上传用于门牌号识别的图片。",
)

register_error(
    key="DOORPLATE_IMAGE_DECODE_FAILED",
    code="DPT-1003",
    category=ErrorCategory.DOORPLATE,
    http_status=400,
    message="Failed to decode image for doorplate recognition",
    user_message="门牌号识别图片格式错误或损坏。",
)

register_error(
    key="DOORPLATE_RECOGNITION_FAILED",
    code="DPT-1004",
    category=ErrorCategory.DOORPLATE,
    http_status=500,
    message="Doorplate recognition failed",
    user_message="门牌号识别失败，请稍后重试。",
)


# ========== 本地地图 / 场景地图 ==========

register_error(
    key="LOCAL_MAP_GENERATOR_NOT_INITIALIZED",
    code="MAP-1001",
    category=ErrorCategory.MAP,
    http_status=500,
    message="Local map generator is not initialized",
    user_message="本地地图模块暂时不可用。",
)

register_error(
    key="LOCAL_MAP_BAD_REQUEST",
    code="MAP-1002",
    category=ErrorCategory.MAP,
    http_status=400,
    message="Invalid parameters for local map generation",
    user_message="本地地图请求参数错误。",
)

register_error(
    key="LOCAL_MAP_GENERATION_FAILED",
    code="MAP-1003",
    category=ErrorCategory.MAP,
    http_status=500,
    message="Local map generation failed",
    user_message="本地地图生成失败，请稍后重试。",
)


# ========== 导航视觉引导（visual_guidance） ==========

register_error(
    key="NAV_VISUAL_GUIDANCE_NOT_AVAILABLE",
    code="NAV-2001",
    category=ErrorCategory.NAVIGATION,
    http_status=500,
    message="Visual guidance is not available",
    user_message="视觉导航暂时不可用。",
)

register_error(
    key="NAV_VISUAL_GUIDANCE_IMAGE_MISSING",
    code="NAV-2002",
    category=ErrorCategory.NAVIGATION,
    http_status=400,
    message="No image uploaded for visual guidance",
    user_message="未上传用于视觉导航的图片。",
)

register_error(
    key="NAV_VISUAL_GUIDANCE_IMAGE_DECODE_FAILED",
    code="NAV-2003",
    category=ErrorCategory.NAVIGATION,
    http_status=400,
    message="Failed to decode image for visual guidance",
    user_message="视觉导航图片格式错误或损坏。",
)

register_error(
    key="NAV_VISUAL_GUIDANCE_FAILED",
    code="NAV-2004",
    category=ErrorCategory.NAVIGATION,
    http_status=500,
    message="Visual guidance processing failed",
    user_message="视觉导航分析失败，请稍后重试。",
)


# ========== 帮助函数 ==========

def get_error_spec(key_or_code: str) -> ErrorCodeSpec:
    """
    通过 key 或 code 获取错误定义。

    key 形式： "VISION_ENGINE_NOT_INITIALIZED"
    code 形式："VIS-1001"

    如果找不到，返回 DEFAULT_INTERNAL_ERROR
    """
    if not key_or_code:
        return DEFAULT_INTERNAL_ERROR

    # 1) 先按 key 查
    spec = ERROR_REGISTRY.get(key_or_code)
    if spec:
        return spec

    # 2) 再按 code 查（如前端只回传 "VIS-1001"）
    for _key, value in ERROR_REGISTRY.items():
        if value.code == key_or_code:
            return value

    return DEFAULT_INTERNAL_ERROR


# ========== 向后兼容：保留旧的ERR类和ERROR_MESSAGES ==========

class ERR:
    """向后兼容的错误码类"""
    # 通用
    BAD_REQUEST = 100001
    INTERNAL_ERROR = 100500
    
    # 视觉
    VISION_NOT_READY = 200001
    VISION_INIT_FAILED = 200002
    VISION_INFERENCE_ERROR = 200003
    
    # 导航
    NAV_NOT_READY = 400001
    NAV_INVALID_INPUT = 400002
    NAV_ROUTE_ERROR = 400003
    NAV_ENGINE_ERROR = 400004
    
    # TTS
    TTS_ENGINE_ERROR = 500001
    TTS_SYNTH_FAIL = 500002
    TTS_TIMEOUT = 500003


# 向后兼容：ERROR_MESSAGES字典
ERROR_MESSAGES = {
    ERR.BAD_REQUEST: "请求参数错误",
    ERR.INTERNAL_ERROR: "内部服务器错误",
    ERR.VISION_NOT_READY: "视觉引擎未就绪",
    ERR.VISION_INIT_FAILED: "视觉引擎初始化失败",
    ERR.VISION_INFERENCE_ERROR: "视觉推理失败",
    ERR.NAV_NOT_READY: "导航引擎未就绪",
    ERR.NAV_INVALID_INPUT: "导航输入无效",
    ERR.NAV_ROUTE_ERROR: "路径规划错误",
    ERR.NAV_ENGINE_ERROR: "导航引擎错误",
    ERR.TTS_ENGINE_ERROR: "TTS引擎错误",
    ERR.TTS_SYNTH_FAIL: "TTS合成失败",
    ERR.TTS_TIMEOUT: "TTS超时",
}

# 向后兼容：ERROR_CODES字典（从ERROR_REGISTRY生成）
ERROR_CODES = {key: spec.code for key, spec in ERROR_REGISTRY.items()}


def get_error_message(code: int) -> str:
    """向后兼容：通过数字错误码获取消息"""
    return ERROR_MESSAGES.get(code, "未知错误")


def get_module_name(code: int) -> str:
    """向后兼容：通过数字错误码获取模块名"""
    code_str = str(code)
    if code_str.startswith('1'):
        return '通用'
    elif code_str.startswith('2'):
        return '视觉'
    elif code_str.startswith('3'):
        return '音频'
    elif code_str.startswith('4'):
        return '导航'
    elif code_str.startswith('5'):
        return 'TTS'
    elif code_str.startswith('6'):
        return '场景记忆'
    return '未知'
