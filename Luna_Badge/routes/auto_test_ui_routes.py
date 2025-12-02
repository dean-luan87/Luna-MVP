#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动测试 UI 路由
用于渲染前端页面
"""

import os
from flask import Blueprint, send_from_directory

auto_test_ui = Blueprint("auto_test_ui", __name__)

FRONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "auto_test")


@auto_test_ui.route("/auto_test")
def auto_test_page():
    """渲染自动测试页面"""
    return send_from_directory(FRONT_DIR, "index.html")


@auto_test_ui.route("/auto_test/<path:filename>")
def auto_test_static(filename):
    """提供静态文件（CSS、JS）"""
    return send_from_directory(FRONT_DIR, filename)


