"""
观察模式过滤器（Observation Mode Filter）

根据 observation_mode 过滤 YOLO 检测结果，而不是裁剪图像。

设计原则：
- 不在图像层面裁剪（避免边界 bug）
- YOLO / OCR 对完整 frame 更稳
- ROI 在后处理阶段做（结果过滤）

observation_mode:
- forward: 前方（导航主视野）
- surround: 周边（环境变化）
- local: 局部（风险源 / 突发物）
"""

from typing import List, Dict, Any, Optional
import numpy as np


def filter_forward(objects: List[Dict[str, Any]], frame_shape: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    过滤前方视野（forward）
    
    只保留：
    - 中央区域 bbox
    - 靠近地面 / 行进方向的物体
    
    丢弃：
    - 远处广告
    - 高空无关物体
    
    Args:
        objects: YOLO 检测结果列表
        frame_shape: 图像尺寸 (height, width)，用于计算中央区域
    
    Returns:
        过滤后的 objects 列表
    """
    if not objects:
        return []
    
    filtered = []
    
    if frame_shape:
        height, width = frame_shape[:2]
        center_x = width / 2
        center_y = height / 2
        
        # 中央区域范围（占画面的 60%）
        center_region_width = width * 0.6
        center_region_height = height * 0.6
    else:
        # 如果没有 frame_shape，使用 bbox 中心点判断
        center_x = None
        center_y = None
        center_region_width = None
        center_region_height = None
    
    for obj in objects:
        bbox = obj.get("bbox", [])
        if not bbox or len(bbox) < 4:
            continue
        
        # 提取 bbox 坐标（假设格式为 [x1, y1, x2, y2]）
        x1, y1, x2, y2 = bbox[:4]
        bbox_center_x = (x1 + x2) / 2
        bbox_center_y = (y1 + y2) / 2
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        
        # 判断是否在中央区域
        if center_x is not None and center_y is not None:
            if (abs(bbox_center_x - center_x) > center_region_width / 2 or
                abs(bbox_center_y - center_y) > center_region_height / 2):
                continue
        
        # 判断是否靠近地面（bbox 底部在画面下半部分）
        if frame_shape:
            if y2 < height * 0.3:  # 物体太靠上，可能是高空物体
                continue
        
        # 判断 bbox 大小（太小可能是远处物体）
        if frame_shape:
            bbox_area_ratio = (bbox_width * bbox_height) / (width * height)
            if bbox_area_ratio < 0.01:  # 占画面小于 1%，可能是远处物体
                continue
        
        filtered.append(obj)
    
    return filtered


def filter_local(objects: List[Dict[str, Any]], frame_shape: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    过滤局部视野（local）
    
    只保留：
    - 最近 N 米（bbox 大、置信高）
    - 突然出现的物体（需要历史信息，这里先简化）
    
    Args:
        objects: YOLO 检测结果列表
        frame_shape: 图像尺寸 (height, width)，用于计算 bbox 大小
    
    Returns:
        过滤后的 objects 列表
    """
    if not objects:
        return []
    
    filtered = []
    
    if frame_shape:
        height, width = frame_shape[:2]
        frame_area = width * height
    else:
        frame_area = None
    
    for obj in objects:
        bbox = obj.get("bbox", [])
        if not bbox or len(bbox) < 4:
            continue
        
        # 提取 bbox 坐标
        x1, y1, x2, y2 = bbox[:4]
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        bbox_area = bbox_width * bbox_height
        
        # 判断 bbox 大小（大 bbox 表示近处物体）
        if frame_area:
            bbox_area_ratio = bbox_area / frame_area
            if bbox_area_ratio < 0.01:  # 占画面小于 1%，可能是远处物体
                continue
        
        # 判断置信度（高置信度优先）
        confidence = obj.get("confidence", 0.0)
        if confidence < 0.5:  # 置信度太低，可能是误检
            continue
        
        filtered.append(obj)
    
    # 按 bbox 大小排序（大的在前，表示更近）
    if frame_area:
        filtered.sort(
            key=lambda obj: (obj.get("bbox", [2])[2] - obj.get("bbox", [0])[0]) * 
                           (obj.get("bbox", [3])[3] - obj.get("bbox", [1])[1]),
            reverse=True
        )
        # 只保留前 5 个最大的（最近的）
        filtered = filtered[:5]
    
    return filtered


def filter_surround(objects: List[Dict[str, Any]], frame_shape: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    过滤周边视野（surround）
    
    保留全部（但仍可按置信度排序）
    
    Args:
        objects: YOLO 检测结果列表
        frame_shape: 图像尺寸（未使用，但保持接口一致）
    
    Returns:
        过滤后的 objects 列表（全部保留）
    """
    if not objects:
        return []
    
    # 按置信度排序（高的在前）
    filtered = sorted(objects, key=lambda obj: obj.get("confidence", 0.0), reverse=True)
    
    return filtered


def filter_objects_by_mode(
    objects: List[Dict[str, Any]],
    observation_mode: str,
    frame_shape: Optional[tuple] = None
) -> List[Dict[str, Any]]:
    """
    根据 observation_mode 过滤 objects
    
    Args:
        objects: YOLO 检测结果列表
        observation_mode: 观察模式（forward / surround / local）
        frame_shape: 图像尺寸 (height, width)
    
    Returns:
        过滤后的 objects 列表
    """
    if not objects:
        return []
    
    if observation_mode == "forward":
        return filter_forward(objects, frame_shape)
    elif observation_mode == "local":
        return filter_local(objects, frame_shape)
    elif observation_mode == "surround":
        return filter_surround(objects, frame_shape)
    else:
        # 未知模式，返回全部（降级处理）
        return objects

