"""
Grid Slicer (v1.3.0)

空间切片模块

将画面切分为 N×M 网格，分配检测对象，计算风险等级
支持参数化配置，可扩展到任意 N×M 网格
"""

import json
import os
import logging
import time
from typing import Dict, List, Tuple, Any, Optional

logger = logging.getLogger(__name__)


def load_grid_config(config_path: str = "config/grid_config.json") -> Dict[str, int]:
    """
    加载网格配置

    Args:
        config_path: 配置文件路径

    Returns:
        Dict[str, int]: 包含 rows 和 cols 的字典
    """
    default_config = {"rows": 5, "cols": 3}

    if not os.path.exists(config_path):
        logger.warning(f"配置文件不存在，使用默认配置: {default_config}")
        # 自动创建默认配置文件
        os.makedirs(os.path.dirname(config_path) or ".", exist_ok=True)
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
            logger.info(f"已创建默认配置文件: {config_path}")
        except Exception as e:
            logger.warning(f"创建默认配置文件失败: {e}")
        return default_config

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        rows = config.get("rows", 5)
        cols = config.get("cols", 3)
        
        logger.info(f"已加载网格配置: {rows}×{cols} (rows×cols)")
        return {"rows": rows, "cols": cols}
    
    except json.JSONDecodeError as e:
        logger.error(f"配置文件 JSON 格式错误: {e}，使用默认配置")
        return default_config
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}，使用默认配置")
        return default_config


def generate_grid(width: int, height: int, rows: int, cols: int) -> Dict[Tuple[int, int], List[int]]:
    """
    生成网格坐标

    将画面切分为 rows×cols 的网格，返回每个格子的边界框坐标

    Args:
        width: 画面宽度
        height: 画面高度
        rows: 行数
        cols: 列数

    Returns:
        Dict[Tuple[int, int], List[int]]: 网格字典，key 为 (row, col)，value 为 [x1, y1, x2, y2]
    """
    grid = {}

    cell_width = width // cols
    cell_height = height // rows

    for r in range(rows):
        for c in range(cols):
            x1 = c * cell_width
            y1 = r * cell_height
            x2 = (c + 1) * cell_width if c < cols - 1 else width
            y2 = (r + 1) * cell_height if r < rows - 1 else height

            grid[(r, c)] = [x1, y1, x2, y2]

    logger.debug(f"生成 {rows}×{cols} 网格，共 {len(grid)} 个格子")
    return grid


def assign_objects_to_grid(
    detections: List[Any],
    grid: Dict[Tuple[int, int], List[int]],
    rows: int,
    cols: int
) -> Dict[Tuple[int, int], Dict[str, Any]]:
    """
    将检测对象分配到网格

    Args:
        detections: 检测结果列表，每个元素应有 bbox 属性（[x1, y1, x2, y2]）和 cls 属性
        grid: 网格字典
        rows: 行数
        cols: 列数

    Returns:
        Dict[Tuple[int, int], Dict[str, Any]]: 网格单元数据，每个单元包含 objects, counts, risk
    """
    # 初始化网格单元
    grid_cells = {}
    for r in range(rows):
        for c in range(cols):
            grid_cells[(r, c)] = {
                "objects": [],
                "counts": {},
                "risk": 0.0,
            }

    # 分配对象到格子
    for det in detections:
        # 获取对象中心点
        if hasattr(det, 'center'):
            cx, cy = det.center()
        elif hasattr(det, 'bbox'):
            bbox = det.bbox
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2
        else:
            # 兼容不同格式
            bbox = det.get('bbox', []) if isinstance(det, dict) else []
            if len(bbox) >= 4:
                cx = (bbox[0] + bbox[2]) // 2
                cy = (bbox[1] + bbox[3]) // 2
            else:
                logger.warning(f"无法获取对象中心点，跳过: {det}")
                continue

        # 找到中心点所属的格子
        assigned = False
        for (r, c), cell_bbox in grid.items():
            x1, y1, x2, y2 = cell_bbox
            if x1 <= cx < x2 and y1 <= cy < y2:
                # 对象属于这个格子
                grid_cells[(r, c)]["objects"].append(det)
                
                # 统计类别数量
                cls_name = det.cls if hasattr(det, 'cls') else det.get('cls', 'unknown')
                grid_cells[(r, c)]["counts"][cls_name] = grid_cells[(r, c)]["counts"].get(cls_name, 0) + 1
                
                assigned = True
                break

        if not assigned:
            logger.debug(f"对象中心点 ({cx}, {cy}) 不在任何格子内")

    logger.debug(f"分配了 {len(detections)} 个对象到网格")
    return grid_cells


def compute_risk_for_cell(
    cell_data: Dict[str, Any],
    row: int,
    rows: int
) -> float:
    """
    计算网格单元的风险值

    风险与行号（距离层级）关联，而不是写死名称
    - 下方行（脚下）风险权重更高（row 值大）
    - 远处（行号小）风险权重更低

    Args:
        cell_data: 网格单元数据，包含 objects 和 counts
        row: 当前行号（0-based，0 为上方）
        rows: 总行数

    Returns:
        float: 风险值
    """
    risk = 0.0
    objects = cell_data.get("objects", [])
    counts = cell_data.get("counts", {})

    if not objects:
        return 0.0

    # 基于距离层级计算基础权重
    # row 越大（越靠近底部），权重越高
    # row 越小（越远离），权重越低
    base_weight = float(rows - row) / rows  # 归一化到 0-1

    # 遍历对象计算风险
    for obj in objects:
        cls_name = obj.cls if hasattr(obj, 'cls') else obj.get('cls', 'unknown')
        
        # 根据类别设置风险系数
        if cls_name in ["person", "bicycle", "motorcycle"]:
            # 人物、自行车、摩托车：中等风险
            risk += base_weight * 0.5
        elif cls_name in ["car", "truck", "bus"]:
            # 车辆：高风险
            risk += base_weight * 1.0
        elif cls_name in ["obstacle", "stair", "stairs"]:
            # 障碍物、楼梯：高风险
            risk += base_weight * 1.0
        else:
            # 其他对象：低风险
            risk += base_weight * 0.3

    return risk


def build_grid_snapshot(
    grid_cells: Dict[Tuple[int, int], Dict[str, Any]],
    rows: int,
    cols: int,
    timestamp: Optional[int] = None
) -> Dict[str, Any]:
    """
    构建网格快照

    Args:
        grid_cells: 网格单元数据
        rows: 行数
        cols: 列数
        timestamp: 时间戳（毫秒），如果为 None 则自动生成

    Returns:
        Dict[str, Any]: 网格快照，包含 cells, heatmap, safe_path_candidates 等
    """
    if timestamp is None:
        timestamp = int(time.time() * 1000)

    # 计算所有单元的风险
    for (r, c), cell_data in grid_cells.items():
        cell_data["risk"] = compute_risk_for_cell(cell_data, r, rows)

    # 构建风险热力图矩阵（N×M）
    heatmap = []
    for r in range(rows):
        row_risks = []
        for c in range(cols):
            risk = grid_cells[(r, c)].get("risk", 0.0)
            row_risks.append(risk)
        heatmap.append(row_risks)

    # 构建格子快照（结构化格式）
    cells_snapshot = {}
    for (r, c), cell_data in grid_cells.items():
        cells_snapshot[f"({r},{c})"] = {
            "row": r,
            "col": c,
            "object_count": len(cell_data.get("objects", [])),
            "counts": cell_data.get("counts", {}),
            "risk": cell_data.get("risk", 0.0),
        }

    # 寻找安全路径候选（简单版：找风险最低的列）
    safe_path_candidates = []
    if cols > 0:
        column_risks = []
        for c in range(cols):
            col_risk = sum(heatmap[r][c] for r in range(rows)) / rows if rows > 0 else 0.0
            column_risks.append((c, col_risk))
        
        # 按风险排序，选择风险最低的列
        column_risks.sort(key=lambda x: x[1])
        safe_path_candidates = [col for col, _ in column_risks[:min(3, cols)]]

    snapshot = {
        "timestamp": timestamp,
        "grid_size": {
            "rows": rows,
            "cols": cols,
        },
        "cells": cells_snapshot,
        "heatmap": heatmap,
        "safe_path_candidates": safe_path_candidates,
    }

    return snapshot


def save_grid_snapshot(snapshot: Dict[str, Any], output_dir: str = "logs/grid") -> str:
    """
    保存网格快照到文件

    Args:
        snapshot: 网格快照数据
        output_dir: 输出目录

    Returns:
        str: 保存的文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = snapshot.get("timestamp", int(time.time() * 1000))
    filename = f"grid_snapshot_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
        logger.info(f"网格快照已保存: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"保存网格快照失败: {e}")
        return ""









