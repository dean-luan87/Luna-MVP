#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备上报接口（Telemetry）
v2.0: 从真实设备收集数据 → 指标分析 → 反馈优化
"""

from flask import Blueprint, request, jsonify
import time
import json
import os
import logging
from collections import Counter

logger = logging.getLogger(__name__)

telemetry_api = Blueprint("telemetry_api", __name__)

# 简单：落到一个本地 jsonl 或 sqlite，后续可接入真正日志系统
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "device_logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "telemetry_events.jsonl")


@telemetry_api.route("/event", methods=["POST"])
def telemetry_event():
    """
    设备上报事件：
    {
      "device_id": "...",
      "event_type": "vision_warning / navigation_step / tts_error / scene_mismatch",
      "payload": {...},
      "ts": 1234567890 (可选)
    }
    """
    try:
        data = request.get_json() or {}
        data["server_ts"] = time.time()
        
        # 验证必要字段
        if not data.get("event_type"):
            return jsonify({
                "success": False,
                "error": "缺少 event_type"
            }), 400
        
        # 写入日志文件
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        
        logger.debug(f"收到设备上报事件: {data.get('event_type')}")
        
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"处理设备上报事件失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@telemetry_api.route("/metrics", methods=["GET"])
def telemetry_metrics():
    """
    简单统计：按 event_type 计数
    后面可以扩展成更复杂的指标。
    """
    counter = Counter()
    
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify({
                "success": True,
                "data": {}
            })
        
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                    et = d.get("event_type", "unknown")
                    counter[et] += 1
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        logger.error(f"读取指标失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
    return jsonify({
        "success": True,
        "data": dict(counter)
    })


