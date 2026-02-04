#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练数据自动生成模块
可一键输出 JSON 与 CSV
"""

import json
import csv
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DatasetManager:
    """训练数据自动生成模块"""
    
    def __init__(self, save_dir="test_engine/dataset/"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        logger.info(f"DatasetManager 初始化，保存目录: {self.save_dir}")
    
    def export_json(self, data: List[Dict[str, Any]], name: str) -> str:
        """
        导出为 JSON 格式
        
        Args:
            data: 数据列表
            name: 文件名（不含扩展名）
        
        Returns:
            保存的文件路径
        """
        filepath = os.path.join(self.save_dir, f"{name}.json")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"JSON 导出成功: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"JSON 导出失败: {e}")
            raise
    
    def export_csv(self, data: List[Dict[str, Any]], name: str) -> str:
        """
        导出为 CSV 格式
        
        Args:
            data: 数据列表
            name: 文件名（不含扩展名）
        
        Returns:
            保存的文件路径
        """
        filepath = os.path.join(self.save_dir, f"{name}.csv")
        
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # 写入表头
                writer.writerow([
                    "img_path", "correct", "missing", "extra", 
                    "accuracy", "precision", "recall", "f1",
                    "detections", "ocr_texts"
                ])
                
                # 写入数据
                for item in data:
                    writer.writerow([
                        item.get("img_path", ""),
                        ",".join(item.get("correct", [])),
                        ",".join(item.get("missing", [])),
                        ",".join(item.get("extra", [])),
                        item.get("accuracy", 0.0),
                        item.get("precision", 0.0),
                        item.get("recall", 0.0),
                        item.get("f1", 0.0),
                        str(len(item.get("detections", []))),
                        ",".join(item.get("ocr_texts", []))
                    ])
            
            logger.info(f"CSV 导出成功: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"CSV 导出失败: {e}")
            raise
    
    def export_both(self, data: List[Dict[str, Any]], name: str) -> Dict[str, str]:
        """
        同时导出 JSON 和 CSV
        
        Args:
            data: 数据列表
            name: 文件名（不含扩展名）
        
        Returns:
            {"json": json_path, "csv": csv_path}
        """
        json_path = self.export_json(data, name)
        csv_path = self.export_csv(data, name)
        return {"json": json_path, "csv": csv_path}


