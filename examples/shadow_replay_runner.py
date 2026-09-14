# -*- coding: utf-8 -*-
"""
Shadow Replay Runner（影子回放运行器）

职责：
- 让旧系统"看视频但不说话、不干预、不影响任何状态"
- 只读式运行旧功能（legacy navigation, OCR, decision）
- 不影响 C1 状态机和 Pipeline 执行节律
- 只输出日志和对比结果

核心原则：
- ✅ 被动消费同一帧源
- ✅ 输出日志 / 结果
- ❌ 不能影响 C1 的状态机
- ❌ 不能改变 Pipeline 的执行节律
- ❌ 出错就吞，成功就记

放置位置：
- examples/shadow_replay_runner.py（仅测试态）
- 不是正式能力，只服务于工程验证
"""

import time
from typing import Dict, Any, Optional, List, Callable


class ShadowReplayRunner:
    """
    影子回放运行器
    
    让旧系统"看视频但不说话、不干预、不影响任何状态"
    """
    
    def __init__(
        self,
        legacy_yolo,
        legacy_ocr=None,
        legacy_decider=None,
        logger=None,
    ):
        """
        初始化 Shadow Replay Runner
        
        Args:
            legacy_yolo: 旧 YOLO 检测器
            legacy_ocr: 旧 OCR 处理器（可选）
            legacy_decider: 旧决策器（可选）
            logger: 日志记录器（可选，需实现 log_shadow 方法）
        """
        self.legacy_yolo = legacy_yolo
        self.legacy_ocr = legacy_ocr
        self.legacy_decider = legacy_decider
        self.logger = logger
        self.frame_id = 0
    
    def process(self, frame):
        """
        处理单帧（只读，不影响主系统）
        
        Args:
            frame: 图像帧
        """
        self.frame_id += 1
        
        # 1. Legacy YOLO 检测
        objects = []
        try:
            if self.legacy_yolo:
                objects = self.legacy_yolo.detect(frame)
        except Exception as e:
            objects = []
            self._log_error("yolo", e)
        
        # 2. Legacy OCR 提取
        texts = []
        try:
            if self.legacy_ocr:
                texts = self.legacy_ocr.extract_text(frame)
        except Exception as e:
            texts = []
            self._log_error("ocr", e)
        
        # 3. Legacy 决策（可选）
        decision = None
        try:
            if self.legacy_decider:
                decision = self.legacy_decider.decide(objects, texts)
        except Exception as e:
            decision = None
            self._log_error("decision", e)
        
        # 4. 记录日志
        self._log({
            "ts": time.time(),
            "frame_id": self.frame_id,
            "legacy_objects_cnt": len(objects),
            "legacy_texts_cnt": len(texts),
            "legacy_decision": decision,
        })
    
    def _log(self, payload: Dict[str, Any]):
        """
        记录日志
        
        Args:
            payload: 日志内容
        """
        if self.logger:
            try:
                self.logger.log_shadow(payload)
            except Exception:
                # 日志失败不影响主流程
                pass
    
    def _log_error(self, module: str, err: Exception):
        """
        记录错误日志
        
        Args:
            module: 模块名称
            err: 异常对象
        """
        if self.logger:
            try:
                self.logger.log_shadow({
                    "frame_id": self.frame_id,
                    "error_module": module,
                    "error": str(err),
                })
            except Exception:
                # 日志失败不影响主流程
                pass


class ShadowLogger:
    """
    Shadow 日志记录器
    
    记录 Shadow Replay 的日志到文件
    """
    
    def __init__(self, log_file: str):
        """
        初始化日志记录器
        
        Args:
            log_file: 日志文件路径
        """
        self.log_file = log_file
        import json
        self.json = json
    
    def log_shadow(self, payload: Dict[str, Any]):
        """
        记录 Shadow 日志
        
        Args:
            payload: 日志内容
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(self.json.dumps(payload, default=str) + "\n")
        except Exception:
            # 日志写入失败不影响主流程
            pass
