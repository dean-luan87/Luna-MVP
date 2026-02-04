# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Interfaces（世界模型接口）

职责：
- 定义外部系统与世界模型的接口
- UserReportEvent：用户报告事件（一期接口）
"""

from .user_report_iface import UserReportEvent

__all__ = [
    "UserReportEvent",
]


