#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PerfLogSpec - 性能日志 JSONL 规范

版本: 1.0.0
"""

from typing import Dict, Any, Optional
from datetime import datetime


class PerfLogSpec:
    """性能日志规范验证和转换"""
    
    PROTOCOL_VERSION = "1.0.0"
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        验证性能日志是否符合规范
        
        Returns:
            (is_valid, error_message)
        """
        # 必须字段检查
        if "ts" not in data:
            return False, "缺少必须字段: ts"
        if "event" not in data:
            return False, "缺少必须字段: event"
        if "network" not in data:
            return False, "缺少必须字段: network"
        if "rtt_ms" not in data["network"]:
            return False, "network 中缺少必须字段: rtt_ms"
        if "infer" not in data:
            return False, "缺少必须字段: infer"
        if "total_ms" not in data["infer"]:
            return False, "infer 中缺少必须字段: total_ms"
        
        # 类型检查
        if not isinstance(data["network"]["rtt_ms"], (int, float)) or data["network"]["rtt_ms"] < 0:
            return False, "network.rtt_ms 必须是非负数字"
        
        if not isinstance(data["infer"]["total_ms"], (int, float)) or data["infer"]["total_ms"] < 0:
            return False, "infer.total_ms 必须是非负数字"
        
        # 时间戳格式检查
        try:
            datetime.fromisoformat(data["ts"].replace("Z", "+00:00"))
        except Exception:
            return False, f"ts 格式无效: {data['ts']}"
        
        return True, None
    
    @staticmethod
    def parse(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析并标准化性能日志
        
        Returns:
            标准化后的性能日志
        """
        is_valid, error = PerfLogSpec.validate(data)
        if not is_valid:
            raise ValueError(f"PerfLogSpec 验证失败: {error}")
        
        result = data.copy()
        result.setdefault("protocol_version", PerfLogSpec.PROTOCOL_VERSION)
        
        return result
    
    @staticmethod
    def create(
        event: str,
        rtt_ms: float,
        total_ms: float,
        frame_id: Optional[int] = None,
        infer_ms: Optional[float] = None,
        nav_ms: Optional[float] = None,
        cpu_pct: Optional[float] = None,
        mem_pct: Optional[float] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        创建符合规范的性能日志
        
        Args:
            event: 事件类型
            rtt_ms: 网络往返延迟
            total_ms: 总推理耗时
            frame_id: 帧 ID（可选）
            infer_ms: 推理耗时（可选）
            nav_ms: 导航耗时（可选）
            cpu_pct: CPU 使用率（可选）
            mem_pct: 内存使用率（可选）
            extra: 额外信息（可选）
        
        Returns:
            符合规范的性能日志字典
        """
        log = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "protocol_version": PerfLogSpec.PROTOCOL_VERSION,
            "event": event,
            "network": {
                "rtt_ms": rtt_ms
            },
            "infer": {
                "total_ms": total_ms
            }
        }
        
        if frame_id is not None:
            log["frame_id"] = frame_id
        
        if infer_ms is not None:
            log["infer"]["infer_ms"] = infer_ms
        
        if nav_ms is not None:
            log["infer"]["nav_ms"] = nav_ms
        
        if cpu_pct is not None or mem_pct is not None:
            log["system"] = {}
            if cpu_pct is not None:
                log["system"]["cpu_pct"] = cpu_pct
            if mem_pct is not None:
                log["system"]["mem_pct"] = mem_pct
        
        if extra:
            log["extra"] = extra
        
        is_valid, error = PerfLogSpec.validate(log)
        if not is_valid:
            raise ValueError(f"创建的性能日志无效: {error}")
        
        return log


