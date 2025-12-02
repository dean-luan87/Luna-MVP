# core/error_codes.py

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class ErrorInfo:
    code: str
    message: str
    category: str
    suggestion: str = ""


# 顶层错误码表：一期先做基础覆盖，后面可以扩展
ERROR_CODES: Dict[str, ErrorInfo] = {
    # 系统级
    "SYS-0001": ErrorInfo(
        code="SYS-0001",
        category="system",
        message="System initialization failed",
        suggestion="Check config files and required services, then restart Luna Badge."
    ),
    "SYS-0002": ErrorInfo(
        code="SYS-0002",
        category="system",
        message="Unexpected system error",
        suggestion="Capture logs and report to maintainer."
    ),

    # 视觉
    "VIS-2001": ErrorInfo(
        code="VIS-2001",
        category="vision",
        message="YOLO pipeline error",
        suggestion="Check camera stream & YOLO service health."
    ),
    "VIS-2002": ErrorInfo(
        code="VIS-2002",
        category="vision",
        message="OCR engine error",
        suggestion="Check OCR service and network."
    ),

    # 导航
    "NAV-3001": ErrorInfo(
        code="NAV-3001",
        category="navigation",
        message="Path planning failed",
        suggestion="Try re-planning route or switch to safe mode."
    ),
    "NAV-3002": ErrorInfo(
        code="NAV-3002",
        category="navigation",
        message="Navigation runtime crashed",
        suggestion="Auto-recovery will restart navigation; if repeated, check environment logs."
    ),

    # 任务链
    "TASK-6001": ErrorInfo(
        code="TASK-6001",
        category="task",
        message="Task chain executor error",
        suggestion="Inspect last task payload and executor output."
    ),

    # APIs
    "API-8001": ErrorInfo(
        code="API-8001",
        category="api",
        message="Invalid request payload",
        suggestion="Check request body against API spec."
    ),
    "API-8002": ErrorInfo(
        code="API-8002",
        category="api",
        message="Backend service unavailable",
        suggestion="Retry later or check backend health."
    ),
}


def get_error_info(code: str) -> Optional[ErrorInfo]:
    return ERROR_CODES.get(code)



