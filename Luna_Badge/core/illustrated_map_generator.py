#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 插图化地图生成器 v3.0
基于参考地图的手绘插画风格实现

核心特性:
- 丰富的插图元素（建筑物、场景、装饰）
- 多层次信息表达
- 手绘风格的视觉表现
- 实用信息标注
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random

logger = logging.getLogger(__name__)


class IllustratedMapGenerator:
    """插图化地图生成器 v3.0"""
    
    def __init__(self,
                 output_dir: str = "data/map_cards",
                 icons_dir: str = "assets/icons/tabler",
                 fonts_dir: str = "assets/fonts",
                 textures_dir: str = "assets/textures"):
        """初始化生成器"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.icons_dir = icons_dir
        self.fonts_dir = fonts_dir
        self.textures_dir = textures_dir
        
        # 加载字体
        self.font_heading = self._load_chinese_font(size=32)  # 标题大字
        self.font_label = self._load_chinese_font(size=18)    # 标签
        self.font_hint = self._load_chinese_font(size=14)     # 提示小字
        
        # 插图化配色方案（参考地图风格 - 增强版）
        self.colors = {
            "bg": (251, 248, 240),           # 米黄色背景
            "path": (80, 100, 120),          # 路径蓝灰色（更深）
            "node": (40, 40, 40),            # 节点深灰
            "region_light": (220, 235, 250), # 浅蓝区域（更亮）
            "region_warm": (255, 248, 230),  # 暖黄区域（更暖）
            "highlight": (255, 80, 80),      # 高亮红
            "text_dark": (20, 20, 20),       # 深色文字
            "text_medium": (80, 80, 80),     # 中等文字
            "shadow": (200, 200, 200),       # 阴影色
            "accent": (100, 150, 200),       # 强调色
        }
        
        # 插图元素配置
        self.illustration_config = {
            "node_decor": True,              # 节点装饰
            "building_outline": True,        # 建筑轮廓
            "scene_bg": True,                # 场景背景
            "decorative_lines": True,        # 装饰线条
            "info_badges": True,             # 信息徽章
            "shadows": True,                 # 阴影效果
            "gradients": True,               # 渐变填充
            "scene_icons": True,             # 场景图标
        }
        
        logger.info("🎨 插图化地图生成器 v3.0 初始化完成")
    
    def _load_chinese_font(self, size: int = 16) -> Optional[ImageFont.FreeTypeFont]:
        """加载中文字体"""
        font_paths = [
            os.path.join(self.fonts_dir, "handwriting.ttf"),
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        return ImageFont.load_default()
    
    def _draw_node_icon(self, draw: ImageDraw.Draw, x: int, y: int, node_type: str) -> None:
        """绘制节点图标（替代建筑物轮廓）"""
        if not self.illustration_config["building_outline"]:
            return
        
        # 根据节点类型绘制不同的图标
        if "hospital" in node_type.lower() or "destination" in node_type.lower() or "clinic" in node_type.lower():
            # 医院/诊室图标：红十字符号
            cross_size = 15
            # 十字横线
            draw.line([x - cross_size, y, x + cross_size, y],
                     fill=(220, 50, 50), width=4)
            # 十字竖线
            draw.line([x, y - cross_size, x, y + cross_size],
                     fill=(220, 50, 50), width=4)
            
        elif "building" in node_type.lower():
            # 建筑图标：简化建筑
            # 小房子图标
            # 屋顶（三角形）
            roof_points = [
                (x - 12, y - 5),
                (x, y - 15),
                (x + 12, y - 5),
            ]
            draw.polygon(roof_points, fill=(100, 120, 140), outline=(60, 80, 100), width=2)
            # 墙面
            draw.rectangle([x - 10, y - 5, x + 10, y + 10],
                         fill=(180, 200, 220), outline=(100, 120, 140), width=2)
            # 门
            draw.rectangle([x - 3, y, x + 3, y + 10],
                         fill=(100, 80, 60), outline=(60, 40, 20), width=1)
        
        elif "entrance" in node_type.lower():
            # 入口图标：打开的门
            # 门框左柱
            draw.rectangle([x - 8, y - 12, x - 5, y + 8],
                         fill=(140, 120, 100), outline=(100, 80, 60), width=1)
            # 门（打开状态）
            door_points = [
                (x - 5, y - 12),
                (x + 5, y - 8),
                (x + 5, y + 8),
                (x - 5, y + 8),
            ]
            draw.polygon(door_points, fill=(120, 100, 80), outline=(80, 60, 40), width=1)
            # 门把手
            draw.ellipse([x + 2, y, x + 4, y + 2],
                        fill=(60, 60, 60), outline=(40, 40, 40), width=1)
        
        elif "registration" in node_type.lower() or "reception" in node_type.lower():
            # 挂号处/接待处：服务台图标
            # 服务台台面
            draw.rectangle([x - 15, y - 8, x + 15, y - 3],
                         fill=(120, 140, 160), outline=(80, 100, 120), width=2)
            # 服务台支撑
            draw.rectangle([x - 12, y - 3, x + 12, y + 8],
                         fill=(180, 200, 220), outline=(140, 160, 180), width=2)
            # 台面标记
            draw.ellipse([x - 8, y - 6, x + 8, y - 1], 
                        fill=(200, 200, 200), outline=(150, 150, 150), width=1)
        
        elif "elevator" in node_type.lower():
            # 电梯图标：简化立方体
            # 前面
            draw.rectangle([x - 12, y - 18, x + 12, y + 5],
                         fill=(200, 200, 200), outline=(140, 140, 140), width=2)
            # 顶部
            top_points = [
                (x - 12, y - 18),
                (x - 8, y - 22),
                (x + 8, y - 22),
                (x + 12, y - 18),
            ]
            draw.polygon(top_points, fill=(220, 220, 220), outline=(160, 160, 160), width=2)
            # 按钮
            draw.ellipse([x - 3, y - 8, x + 3, y - 2], 
                        fill=(100, 100, 100), outline=(60, 60, 60), width=1)
        
        elif "toilet" in node_type.lower():
            # 卫生间图标：马桶符号
            # 马桶座圈
            draw.ellipse([x - 10, y - 8, x + 10, y + 8],
                        fill=(220, 220, 220), outline=(140, 140, 140), width=2)
            # 马桶水箱
            draw.rectangle([x - 6, y - 15, x + 6, y - 8],
                         fill=(200, 200, 200), outline=(120, 120, 120), width=1)
            # 马桶盖前端开口
            draw.arc([x - 8, y - 5, x + 8, y + 15],
                    start=0, end=180, fill=(255, 255, 255), width=0)
        
        elif "waiting" in node_type.lower() or "room" in node_type.lower():
            # 候诊区/房间：椅子图标
            # 椅子背
            draw.rectangle([x - 3, y - 15, x + 3, y - 5],
                         fill=(120, 100, 80), outline=(80, 60, 40), width=1)
            # 椅子座
            draw.rectangle([x - 10, y - 5, x + 10, y + 2],
                         fill=(140, 120, 100), outline=(100, 80, 60), width=1)
            # 椅子扶手
            draw.rectangle([x - 12, y - 5, x - 10, y + 2],
                         fill=(100, 80, 60), outline=(60, 40, 20), width=1)
            draw.rectangle([x + 10, y - 5, x + 12, y + 2],
                         fill=(100, 80, 60), outline=(60, 40, 20), width=1)
        
        elif "bus" in node_type.lower() or "stop" in node_type.lower():
            # 公交站：站牌图标
            # 站牌柱
            draw.rectangle([x - 2, y, x + 2, y + 12],
                         fill=(100, 100, 100), outline=(60, 60, 60), width=1)
            # 站牌
            draw.rectangle([x - 12, y - 8, x + 12, y],
                         fill=(250, 200, 50), outline=(180, 140, 30), width=2)
            # 站牌数字标识
            draw.rectangle([x - 8, y - 6, x + 8, y - 2],
                         fill=(255, 255, 255), outline=(200, 200, 200), width=1)
        
        elif "stairs" in node_type.lower():
            # 楼梯：台阶图标
            for i in range(3):
                step_y = y - 5 + i * 4
                draw.rectangle([x - 10, step_y, x + 10, step_y + 3],
                             fill=(180, 180, 180), outline=(120, 120, 120), width=1)
    
    def _draw_decorative_elements(self, draw: ImageDraw.Draw, x: int, y: int) -> None:
        """绘制装饰元素（光线、装饰线条等）"""
        if not self.illustration_config["decorative_lines"]:
            return
        
        # 随机添加一些装饰性短线
        for _ in range(3):
            dx = random.randint(-20, 20)
            dy = random.randint(-20, 20)
            draw.line([x + dx, y + dy, x + dx + random.randint(5, 15), y + dy],
                     fill=(200, 200, 200), width=1)
    
    def _draw_info_badge(self, draw: ImageDraw.Draw, text: str, position: Tuple[int, int], 
                        color: Tuple[int, int, int], icon: Optional[str] = None) -> None:
        """绘制信息徽章（距离、时间等 - 优化版）"""
        if not self.illustration_config["info_badges"]:
            return
        
        x, y = position
        
        # 背景圆角矩形（更大更醒目）
        padding = 10
        bbox = draw.textbbox((0, 0), text, font=self.font_label)
        w = bbox[2] - bbox[0] + padding * 2 + 20  # 留空间给图标
        h = bbox[3] - bbox[1] + padding
        
        # 带阴影的背景
        draw.rounded_rectangle([x - w//2 + 2, y + 2, x + w//2 + 2, y + h + 2],
                             radius=6, fill=(200, 200, 200, 150))
        
        # 主背景
        draw.rounded_rectangle([x - w//2, y, x + w//2, y + h],
                             radius=6, fill=(255, 255, 255), 
                             outline=color, width=3)
        
        # 如果有点图标，绘制一下
        if icon:
            icon_x = x - w//2 + 12
            icon_y = y + h//2
            # 简化的图标绘制（小圆点表示）
            draw.ellipse([icon_x - 5, icon_y - 5, icon_x + 5, icon_y + 5],
                       fill=color, outline=color)
        
        # 文字（更大）
        draw.text((x - w//2 + padding + 15, y + padding//2 + 2), text,
                 font=self.font_label, fill=self.colors["text_dark"])
    
    def _draw_handdrawn_path(self, draw: ImageDraw.Draw, points: List[Tuple[int, int]],
                            color: Tuple[int, int, int], width: int = 3) -> None:
        """绘制手绘风格路径（增强版 - 方向指示）"""
        if len(points) < 2:
            return
        
        # 添加轻微抖动
        jitter_points = []
        for x, y in points:
            jx = x + random.randint(-1, 1)
            jy = y + random.randint(-1, 1)
            jitter_points.append((jx, jy))
        
        # 绘制路径（虚线效果）
        segment_len = 8
        gap_len = 4
        total_len = 0
        
        for i in range(len(jitter_points) - 1):
            x1, y1 = jitter_points[i]
            x2, y2 = jitter_points[i + 1]
            dx, dy = x2 - x1, y2 - y1
            dist = np.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                unit_x, unit_y = dx/dist, dy/dist
                
                # 绘制虚线
                current_pos = 0
                while current_pos < dist:
                    seg_start = (int(x1 + unit_x * current_pos), int(y1 + unit_y * current_pos))
                    seg_end_pos = min(current_pos + segment_len, dist)
                    seg_end = (int(x1 + unit_x * seg_end_pos), int(y1 + unit_y * seg_end_pos))
                    
                    draw.line([seg_start, seg_end], fill=color, width=width)
                    current_pos += segment_len + gap_len
        
        # 添加多个箭头指示方向
        if len(jitter_points) >= 2:
            x1, y1 = jitter_points[-2]
            x2, y2 = jitter_points[-1]
            dx, dy = x2 - x1, y2 - y1
            
            # 主箭头（大）
            arrow_len = 15
            angle = np.arctan2(dy, dx)
            arrow_x1 = int(x2 - arrow_len * np.cos(angle - np.pi / 6))
            arrow_y1 = int(y2 - arrow_len * np.sin(angle - np.pi / 6))
            arrow_x2 = int(x2 - arrow_len * np.cos(angle + np.pi / 6))
            arrow_y2 = int(y2 - arrow_len * np.sin(angle + np.pi / 6))
            
            # 箭头填充
            draw.polygon([(x2, y2), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                        fill=color, outline=color, width=2)
            
            # 箭头边框突出
            draw.polygon([(x2, y2), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                        fill=None, outline=(255, 255, 255), width=1)
    
    def _apply_handdrawn_filter(self, img: Image.Image) -> Image.Image:
        """应用手绘风格滤镜"""
        # 轻微的模糊模拟手绘感
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # 增强对比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        # 轻微的不规则处理
        width, height = img.size
        noise = np.random.randint(-3, 4, (height, width, 3), dtype=np.int16)
        img_array = np.array(img, dtype=np.int16)
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def _draw_background_grid(self, draw: ImageDraw.Draw, width: int, height: int) -> None:
        """绘制背景网格"""
        grid_color = (240, 235, 230)
        grid_spacing = 50
        
        # 垂直线
        for x in range(0, width, grid_spacing):
            draw.line([x, 0, x, height], fill=grid_color, width=1)
        
        # 水平线
        for y in range(0, height, grid_spacing):
            draw.line([0, y, width, y], fill=grid_color, width=1)
    
    def generate_illustrated_map(self, path_data: Dict, output_name: str) -> Optional[str]:
        """
        生成插图化风格地图
        
        Args:
            path_data: 路径数据
            output_name: 输出文件名
            
        Returns:
            生成的文件路径
        """
        try:
            # 创建画布
            width, height = 2400, 1800
            img = Image.new('RGB', (width, height), self.colors["bg"])
            draw = ImageDraw.Draw(img)
            
            # 绘制背景网格
            self._draw_background_grid(draw, width, height)
            
            nodes = path_data.get("nodes", [])
            if not nodes:
                logger.error("无节点数据")
                return None
            
            # 计算节点位置
            positions = self._calculate_positions(nodes, width, height)
            
            # 绘制区域背景（先绘制，在其他元素下方）
            self._draw_regions(draw, nodes, positions, width, height)
            
            # 绘制路径（在节点下方）
            self._draw_paths(draw, nodes, positions)
            
            # 绘制节点和装饰（最后绘制，在最上层）
            for i, (node, pos) in enumerate(zip(nodes, positions)):
                self._draw_node_with_illustration(draw, node, pos, i + 1)
            
            # 绘制标题
            title = path_data.get("path_name", "导航地图")
            if self.font_heading:
                # 标题背景
                bbox = draw.textbbox((0, 0), title, font=self.font_heading)
                title_w = bbox[2] - bbox[0]
                draw.rounded_rectangle([90, 40, 110 + title_w, 110],
                                     radius=8, fill=(255, 255, 255, 240),
                                     outline=self.colors["accent"], width=3)
                # 标题文字
                draw.text((100, 60), title, font=self.font_heading,
                         fill=self.colors["text_dark"])
            
            # 绘制指南针
            self._draw_compass(draw, width - 120, 120)
            
            # 应用手绘滤镜
            img = self._apply_handdrawn_filter(img)
            
            # 保存
            output_path = self.output_dir / f"{output_name}_illustrated.png"
            img.save(output_path)
            
            logger.info(f"✅ 插图化地图已生成: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ 生成失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _calculate_positions(self, nodes: List[Dict], width: int, height: int) -> List[Tuple[int, int]]:
        """计算节点位置"""
        num_nodes = len(nodes)
        center_x, center_y = width // 2, height // 2
        radius = 300
        angle_step = 360 / num_nodes if num_nodes > 0 else 0
        
        positions = []
        for i in range(num_nodes):
            angle = np.radians(i * angle_step)
            x = int(center_x + radius * np.cos(angle))
            y = int(center_y + radius * np.sin(angle))
            positions.append((x, y))
        
        return positions
    
    def _draw_regions(self, draw: ImageDraw.Draw, nodes: List[Dict], 
                     positions: List[Tuple[int, int]], width: int, height: int) -> None:
        """绘制区域背景"""
        # 简化的区域绘制
        for i, node in enumerate(nodes):
            level = node.get("level", "")
            if level and i < len(positions):
                x, y = positions[i]
                # 绘制圆形区域
                draw.ellipse([x - 150, y - 150, x + 150, y + 150],
                           fill=self.colors["region_light"], 
                           outline=(180, 190, 200), width=2)
    
    def _draw_paths(self, draw: ImageDraw.Draw, nodes: List[Dict], 
                   positions: List[Tuple[int, int]]) -> None:
        """绘制路径（增强版 - 带运动方式图标）"""
        for i in range(len(nodes) - 1):
            from_pos = positions[i]
            to_pos = positions[i + 1]
            
            # 使用手绘路径
            self._draw_handdrawn_path(draw, [from_pos, to_pos], 
                                     self.colors["path"], width=5)  # 更粗
            
            # 添加距离标注（带运动方式图标）
            distance = nodes[i].get("distance", 0)
            movement_type = nodes[i].get("movement", "walking")  # walking, elevator, stairs
            
            if distance > 0:
                mid_x = (from_pos[0] + to_pos[0]) // 2
                mid_y = (from_pos[1] + to_pos[1]) // 2
                
                # 确定运动方式图标
                movement_icon = None
                if "elevator" in movement_type.lower():
                    movement_icon = "🚪"
                elif "stairs" in movement_type.lower() or "楼梯" in movement_type:
                    movement_icon = "🪜"
                else:
                    movement_icon = "👣"
                
                # 绘制带图标的信息徽章
                self._draw_info_badge(draw, f"{distance}米", 
                                     (mid_x, mid_y - 25),
                                     self.colors["path"],
                                     icon=movement_icon)
    
    def _draw_node_with_illustration(self, draw: ImageDraw.Draw, node: Dict, 
                                    position: Tuple[int, int], index: int) -> None:
        """绘制带插图的节点（增强版 - 地标优先）"""
        x, y = position
        node_type = node.get("type", "").lower()
        label = node.get("label", "")
        
        # 绘制阴影（增加层次感）
        if self.illustration_config["shadows"]:
            draw.ellipse([x - 38, y - 38, x + 42, y + 42],
                       fill=(220, 220, 220), 
                       outline=None)
        
        # 绘制节点图标（作为主要地标icon）
        self._draw_node_icon(draw, x, y, node_type)
        
        # 绘制节点圆圈（很小，作为数字背景）
        # 外圈
        draw.ellipse([x - 20, y - 20, x + 20, y + 20],
                   fill=(240, 240, 250), 
                   outline=(180, 180, 200), width=1)
        # 内圈
        draw.ellipse([x - 17, y - 17, x + 17, y + 17],
                   fill=(255, 255, 255), 
                   outline=self.colors["node"], width=2)
        
        # 绘制编号（很小，不遮挡地标）
        draw.text((x - 4, y - 6), str(index),
                 font=self.font_hint, fill=self.colors["node"])
        
        # 绘制标签（更大更醒目，带装饰）
        if label and self.font_label:
            bbox = draw.textbbox((0, 0), label, font=self.font_label)
            text_width = bbox[2] - bbox[0]
            
            # 标签阴影
            draw.rounded_rectangle(
                [x - text_width//2 - 8, y + 62,
                 x + text_width//2 + 12, y + 88],
                radius=8,
                fill=(220, 220, 220)
            )
            
            # 标签背景（带装饰边框）
            draw.rounded_rectangle(
                [x - text_width//2 - 10, y + 60,
                 x + text_width//2 + 10, y + 85],
                radius=6,
                fill=(255, 255, 255, 250),
                outline=self.colors["accent"],
                width=3
            )
            
            # 标签文字
            draw.text((x - text_width//2, y + 70),
                     label,
                     font=self.font_label,
                     fill=self.colors["text_dark"])
        
        # 绘制装饰元素
        self._draw_decorative_elements(draw, x, y)
        
        # 绘制情绪标签
        emotions = node.get("emotion", [])
        if emotions and isinstance(emotions, list):
            for idx, emotion in enumerate(emotions[:2]):
                self._draw_emotion_badge(draw, emotion, 
                                       (x + 70 + idx * 60, y - 10))
    
    def _draw_emotion_badge(self, draw: ImageDraw.Draw, emotion: str, 
                           position: Tuple[int, int]) -> None:
        """绘制情绪徽章"""
        x, y = position
        
        # 情绪配色
        emotion_colors = {
            "推荐": (255, 182, 193),
            "安静": (144, 238, 144),
            "担忧": (255, 165, 0),
            "嘈杂": (169, 169, 169),
        }
        
        color = emotion_colors.get(emotion, (200, 200, 200))
        
        # 绘制徽章
        draw.ellipse([x - 20, y - 20, x + 20, y + 20],
                   fill=color, outline=(220, 220, 220), width=2)
        
        # 文字
        if self.font_hint:
            bbox = draw.textbbox((0, 0), emotion, font=self.font_hint)
            text_x = x - (bbox[2] - bbox[0]) // 2
            text_y = y - (bbox[3] - bbox[1]) // 2
            draw.text((text_x, text_y), emotion,
                     font=self.font_hint, fill=(255, 255, 255))
    
    def _draw_compass(self, draw: ImageDraw.Draw, x: int, y: int) -> None:
        """绘制指南针"""
        size = 60
        
        # 外圆
        draw.ellipse([x - size, y - size, x + size, y + size],
                   outline=(100, 100, 100), width=2)
        
        # 方向标记
        for direction, offset, color in [
            ("N", (0, -size + 10), (255, 0, 0)),
            ("S", (0, size - 10), (0, 0, 255)),
            ("E", (size - 10, 0), (0, 255, 0)),
            ("W", (-size + 10, 0), (255, 165, 0)),
        ]:
            px, py = x + offset[0], y + offset[1]
            if self.font_hint:
                bbox = draw.textbbox((0, 0), direction, font=self.font_hint)
                text_x = px - (bbox[2] - bbox[0]) // 2
                text_y = py - (bbox[3] - bbox[1]) // 2
                draw.text((text_x, text_y), direction,
                         font=self.font_hint, fill=color)


def main():
    """测试函数"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 测试数据（增强版 - 添加运动方式）
    test_path = {
        "path_id": "hospital_test",
        "path_name": "医院导航路径",
        "nodes": [
            {"type": "entrance", "label": "医院入口", "emotion": ["明亮"], "distance": 20, "movement": "walking"},
            {"type": "registration", "label": "挂号处", "emotion": ["推荐", "明亮"], "distance": 15, "movement": "walking"},
            {"type": "elevator", "label": "电梯", "emotion": ["嘈杂", "推荐"], "distance": 15, "movement": "elevator"},
            {"type": "waiting_room", "label": "候诊区", "emotion": ["安静"], "distance": 20, "movement": "walking"},
            {"type": "toilet", "label": "卫生间", "emotion": ["安静", "推荐"], "distance": 10, "movement": "walking"},
            {"type": "destination", "label": "诊室", "emotion": ["推荐"], "distance": 5, "movement": "walking"},
        ]
    }
    
    generator = IllustratedMapGenerator()
    result = generator.generate_illustrated_map(test_path, "test_illustrated")
    
    if result:
        print(f"✅ 生成成功: {result}")


if __name__ == "__main__":
    main()
