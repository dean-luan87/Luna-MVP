#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SVG图标加载器
将SVG图标转换为OpenCV可用的图像格式
"""

import os
import re
import numpy as np
import cv2
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SVGIconLoader:
    """SVG图标加载器"""
    
    @staticmethod
    def svg_to_numpy(svg_path: str, size: int = 64, color: Tuple[int, int, int] = (255, 255, 255)) -> Optional[np.ndarray]:
        """
        将SVG转换为numpy数组
        
        Args:
            svg_path: SVG文件路径
            size: 输出图像大小
            color: SVG填充颜色 (R, G, B)
            
        Returns:
            Optional[np.ndarray]: 转换后的图像，失败返回None
        """
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            # 使用cairosvg如果有的话，否则使用简化方法
            try:
                import cairosvg
                # 将SVG转换为PNG
                png_data = cairosvg.svg2png(
                    bytestring=svg_content.encode('utf-8'),
                    output_width=size,
                    output_height=size
                )
                # 转换为numpy数组
                nparr = np.frombuffer(png_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
                return img
            except ImportError:
                # 如果没有cairosvg，使用简化方法绘制
                logger.warning("  ⚠️ 未安装cairosvg，将使用简化绘制")
                return SVGIconLoader._simple_svg_render(svg_content, size, color)
            
        except Exception as e:
            logger.error(f"  ❌ SVG加载失败: {e}")
            return None
    
    @staticmethod
    def _simple_svg_render(svg_content: str, size: int, color: Tuple[int, int, int]) -> np.ndarray:
        """
        简化的SVG渲染（仅绘制基本形状）
        
        Args:
            svg_content: SVG内容
            size: 输出大小
            color: 颜色
            
        Returns:
            np.ndarray: 渲染后的图像
        """
        # 创建空白图像
        img = np.zeros((size, size, 4), dtype=np.uint8)
        
        # 提取path数据
        paths = re.findall(r'<path[^>]*d="([^"]*)"', svg_content)
        circles = re.findall(r'<circle[^>]*r="([^"]*)"', svg_content)
        rects = re.findall(r'<rect[^>]*', svg_content)
        
        # 绘制路径
        for path_data in paths:
            try:
                # 简化的路径解析（仅绘制直线）
                coords = re.findall(r'([MLHV])([\d.-]+),?\s*([\d.-]+)?', path_data)
                points = []
                for cmd in coords:
                    if cmd[0] in ['M', 'L']:
                        x = float(cmd[1]) * size / 24  # Tabler图标通常是24x24
                        y = float(cmd[2]) * size / 24
                        points.append((int(x), int(y)))
                
                if len(points) >= 2:
                    pts = np.array(points, np.int32)
                    cv2.polylines(img, [pts], False, (*color, 255), 2)
            except:
                pass
        
        # 绘制圆形
        for circle_data in circles:
            try:
                radius = float(circle_data)
                center = (size // 2, size // 2)
                radius_px = int(radius * size / 24)
                cv2.circle(img, center, radius_px, (*color, 255), 2)
            except:
                pass
        
        # 绘制矩形
        for rect_data in rects:
            try:
                # 提取矩形属性
                x_match = re.search(r'x="([^"]*)"', rect_data)
                y_match = re.search(r'y="([^"]*)"', rect_data)
                w_match = re.search(r'width="([^"]*)"', rect_data)
                h_match = re.search(r'height="([^"]*)"', rect_data)
                
                if x_match and y_match and w_match and h_match:
                    x = int(float(x_match.group(1)) * size / 24)
                    y = int(float(y_match.group(1)) * size / 24)
                    w = int(float(w_match.group(1)) * size / 24)
                    h = int(float(h_match.group(1)) * size / 24)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (*color, 255), 2)
            except:
                pass
        
        return img
    
    @staticmethod
    def load_svg_icon(icon_path: str, size: int = 64) -> Optional[np.ndarray]:
        """
        加载SVG图标
        
        Args:
            icon_path: SVG文件路径
            size: 输出大小
            
        Returns:
            Optional[np.ndarray]: 加载的图像
        """
        if not os.path.exists(icon_path):
            return None
        
        # 尝试多种方法
        # 方法1: 尝试使用cairosvg
        try:
            return SVGIconLoader.svg_to_numpy(icon_path, size)
        except Exception as e:
            logger.warning(f"  ⚠️ SVG加载方法1失败: {e}")
        
        # 方法2: 使用简化渲染
        try:
            with open(icon_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            return SVGIconLoader._simple_svg_render(svg_content, size, (100, 100, 100))
        except Exception as e:
            logger.warning(f"  ⚠️ SVG加载方法2失败: {e}")
        
        return None


# 向后兼容的函数接口
def load_svg_icon(icon_path: str, size: int = 64) -> Optional[np.ndarray]:
    """加载SVG图标的便捷函数"""
    return SVGIconLoader.load_svg_icon(icon_path, size)


