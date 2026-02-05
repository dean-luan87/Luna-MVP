from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("test_realtime_smoke")
"""
实时测试后端健康检查（冒烟测试）

前提：先用 bash realtime_lab/scripts/run_all_realtime.sh 启动服务
"""

import json
import time

import requests


def test_realtime_backend_health():
    """简单冒烟：后端 /health 必须可用"""
    resp = requests.get("http://localhost:5001/health", timeout=3)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "model" in data
    assert "total_frames" in data
    assert "avg_latency_ms" in data


if __name__ == "__main__":
    test_realtime_backend_health()
    log.info("✅ 健康检查通过")

