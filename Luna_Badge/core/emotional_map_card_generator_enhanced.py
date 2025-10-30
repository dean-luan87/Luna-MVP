#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
情绪地图生成器增强版 v1.1
生成具备方向感、中文表达、区域划分和情绪标签的高质量地图图卡
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches
from matplotlib.bezier import BezierSegment

logger = logging.getLogger(__name__)

class EmotionalMapCardGeneratorEnhanced:
    """情绪地图生成器增强版 v1.1"""
    
    def __init__(self, 
                 memory_store_path: str = "data/memory_store.json",
                 output_dir: str = "data/map_cards",
                 icons_dir: str = "assets/icons/tabler",
                 fonts_dir: str = "assets/fonts",
                 textures_dir: str = "assets/textures"):
        """初始化增强版生成器"""
        self.memory_store_path = memory_store_path
        self.output_dir = output_dir
        self.icons_dir = icons_dir
        self.fonts_dir = fonts_dir
        self.textures_dir = textures_dir
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 初始化SVG加载器
        try:
            from core.svg_icon_loader import SVGIconLoader
            self.svg_loader = SVGIconLoader
        except ImportError:
            self.svg_loader = None
        
        # 加载中文字体
        self.chinese_font_small = self._load_chinese_font(size=16)
        self.chinese_font_large = self._load_chinese_font(size=24)
        
        # 情绪标签颜色映射
        self.emotion_colors = {
            "推荐": {"bg": (255, 182, 193), "text": (255, 255, 255)},  # 粉红色
            "安静": {"bg": (144, 238, 144), "text": (0, 100, 0)},      # 绿色
            "担忧": {"bg": (255, 165, 0), "text": (255, 255, 255)},     # 橙色
            "嘈杂": {"bg": (169, 169, 169), "text": (255, 255, 255)},   # 灰色
        }
        
        # 区域颜色映射
        self.zone_colors = {
            "候诊区": {"color": (255, 240, 245, 60), "outline": (255, 182, 193)},
            "三楼病区": {"color": (240, 255, 255, 60), "outline": (173, 216, 230)},
            "挂号大厅": {"color": (255, 250, 240, 60), "outline": (255, 215, 0)},
            "电梯间": {"color": (240, 240, 240, 60), "outline": (150, 150, 150)},
        }
        
        # 样式配置
        self.style = {
            "paper_color": (249, 247, 238),
            "line_color": (50, 50, 50),
            "node_size": 48,
            "node_thickness": 3,
            "arrow_size": 20,
        }
        
        logger.info("🎨 情绪地图生成器增强版 v1.1 初始化完成")
    
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
    
    def _load_svg_icon(self, icon_name: str, size: int = 48) -> Optional[Image.Image]:
        """加载SVG图标"""
        if not self.svg_loader:
            return None
        
        icon_path = os.path.join(self.icons_dir, f"{icon_name}.svg")
        if os.path.exists(icon_path):
            try:
                icon_np = self.svg_loader.load_svg_icon(icon_path, size=size)
                if icon_np is not None:
                    return Image.fromarray(icon_np)
            except:
                pass
        
        return None
    
    def _render_zone_background(self, img: Image.Image, nodes: List[Dict], 
                                layout: Dict) -> Image.Image:
        """渲染区域背景"""
        # 按区域分组节点
        zones = {}
        for i, node in enumerate(nodes):
            level = node.get("level", "")
            if level in self.zone_colors:
                if level not in zones:
                    zones[level] = []
                zones[level].append(i)
        
        if not zones:
            return img
        
        # 绘制区域
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        positions = layout.get("positions", [])
        
        for zone_name, zone_color_info in self.zone_colors.items():
            if zone_name not in zones:
                continue
            
            zone_indices = zones[zone_name]
            
            # 计算区域边界（简化：椭圆包围）
            if zone_indices:
                xs = [positions[i][0] for i in zone_indices]
                ys = [positions[i][1] for i in zone_indices]
                
                min_x, max_x = min(xs) - 100, max(xs) + 100
                min_y, max_y = min(ys) - 100, max(ys) + 100
                
                center_x = (min_x + max_x) // 2
                center_y = (min_y + max_y) // 2
                radius_x = (max_x - min_x) // 2
                radius_y = (max_y - min_y) // 2
                
                # 绘制椭圆背景
                overlay_draw.ellipse(
                    [center_x - radius_x, center_y - radius_y,
                     center_x + radius_x, center_y + radius_y],
                    fill=zone_color_info["color"],
                    outline=zone_color_info["outline"],
                    width=2
                )
                
                # 绘制区域标签
                if self.chinese_font_small:
                    bbox = overlay_draw.textbbox(
                        (0, 0), zone_name, font=self.chinese_font_small)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    overlay_draw.text(
                        (center_x - text_width//2, center_y - radius_y - text_height - 10),
                        zone_name,
                        font=self.chinese_font_small,
                        fill=(50, 50, 50))
        
        # 合成
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        return img
    
    def _draw_bezier_arrow(self, draw: ImageDraw.Draw,
                          from_pos: Tuple[int, int],
                          to_pos: Tuple[int, int],
                          color: Tuple[int, int, int],
                          width: int = 2) -> None:
        """使用贝塞尔曲线绘制箭头"""
        x1, y1 = from_pos
        x2, y2 = to_pos
        
        # 创建控制点（使曲线更自然）
        dx, dy = x2 - x1, y2 - y1
        mid_x = x1 + dx * 0.5
        mid_y = y1 + dy * 0.5
        
        # 垂直偏移创建曲线
        perp = np.array([-dy, dx])
        perp_norm = perp / np.linalg.norm(perp)
        offset = perp_norm * 30
        
        ctrl_x = int(mid_x + offset[0])
        ctrl_y = int(mid_y + offset[1])
        
        # 绘制贝塞尔曲线（简化：分段绘制）
        num_points = 20
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            x = int((1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2)
            y = int((1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2)
            points.append((x, y))
        
        # 绘制曲线（带抖动）
        for i in range(len(points) - 1):
            x1_pt, y1_pt = points[i]
            x2_pt, y2_pt = points[i + 1]
            
            jitter_x = np.random.randint(-1, 2)
            jitter_y = np.random.randint(-1, 2)
            
            draw.line([x1_pt + jitter_x, y1_pt + jitter_y,
                      x2_pt + jitter_x, y2_pt + jitter_y],
                     fill=color, width=width)
        
        # 绘制箭头
        arrow_x, arrow_y = to_pos
        angle = np.arctan2(dy, dx)
        arrow_len = 25
        arrow_angle = np.pi / 6
        
        # 箭头顶点
        arrow_left = (
            int(arrow_x - arrow_len * np.cos(angle - arrow_angle)),
            int(arrow_y - arrow_len * np.sin(angle - arrow_angle))
        )
        arrow_right = (
            int(arrow_x - arrow_len * np.cos(angle + arrow_angle)),
            int(arrow_y - arrow_len * np.sin(angle + arrow_angle))
        )
        
        # 绘制箭头
        draw.polygon([arrow_x, arrow_y, arrow_left[0], arrow_left[1],
                     arrow_right[0], arrow_right[1]],
                    fill=color, outline=color)
    
    def _render_emotion_tags(self, draw: ImageDraw.Draw,
                            emotions: List[str],
                            position: Tuple[int, int]) -> None:
        """渲染情绪标签气泡"""
        x, y = position
        
        for idx, emotion in enumerate(emotions[:2]):  # 最多2个
            if emotion not in self.emotion_colors:
                continue
            
            color_info = self.emotion_colors[emotion]
            
            # 圆角矩形背景
            tag_width = 50
            tag_height = 30
            tag_x = x + idx * (tag_width + 5)
            tag_y = y
            
            # 绘制圆角矩形
            draw.rounded_rectangle(
                [tag_x, tag_y, tag_x + tag_width, tag_y + tag_height],
                radius=8,
                fill=color_info["bg"],
                outline=color_info["bg"]
            )
            
            # 绘制文字
            if self.chinese_font_small:
                bbox = draw.textbbox((0, 0), emotion, font=self.chinese_font_small)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                draw.text(
                    (tag_x + (tag_width - text_width) // 2,
                     tag_y + (tag_height - text_height) // 2),
                    emotion,
                    font=self.chinese_font_small,
                    fill=color_info["text"])
    
    def _draw_compass(self, draw: ImageDraw.Draw, position: Tuple[int, int]) -> None:
        """绘制指南针"""
        x, y = position
        size = 80
        
        # 绘制外圆
        draw.ellipse([x - size, y - size, x + size, y + size],
                    outline=self.style["line_color"],
                    width=2)
        
        # 绘制方向标记
        directions = [
            ("北", (x, y - size + 15), (255, 0, 0)),  # 红色北
            ("东", (x + size - 15, y), (0, 255, 0)),  # 绿色东
            ("南", (x, y + size - 15), (0, 0, 255)),  # 蓝色南
            ("西", (x - size + 15, y), (255, 165, 0)),  # 橙色西
        ]
        
        for text, (tx, ty), color in directions:
            if self.chinese_font_small:
                bbox = draw.textbbox((0, 0), text, font=self.chinese_font_small)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                draw.text((tx - text_width//2, ty - text_height//2),
                         text,
                         font=self.chinese_font_small,
                         fill=color)
        
        # 绘制指北针
        draw.line([x, y - size + 10, x, y + size - 10],
                 fill=(255, 0, 0), width=2)
    
    def _apply_paper_texture(self, img: Image.Image) -> Image.Image:
        """应用纸张纹理"""
        texture_path = os.path.join(self.textures_dir, "paper_background.png")
        
        if os.path.exists(texture_path):
            try:
                texture = Image.open(texture_path).convert('RGBA')
                texture = texture.resize(img.size)
                texture.putalpha(30)
                img = Image.alpha_composite(img.convert('RGBA'), texture).convert('RGB')
                return img
            except:
                pass
        
        # Fallback: 噪声纹理
        width, height = img.size
        noise = np.random.randint(0, 50, (height, width), dtype=np.uint8)
        noise_img = Image.fromarray(noise, mode='L')
        noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=1.0))
        noise_img = noise_img.point(lambda x: int(x * 30 / 255))
        
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay.paste(noise_img, mask=noise_img)
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        return img
    
    def _calculate_layout(self, nodes: List[Dict]) -> Dict:
        """计算节点布局"""
        num_nodes = len(nodes)
        width = 2400
        height = 1800
        
        center_x, center_y = width // 2, height // 2
        angle_step = 360 / num_nodes
        radius_base = 150
        
        positions = []
        for i in range(num_nodes):
            angle = np.radians(i * angle_step)
            radius = radius_base + i * 100
            x = int(center_x + radius * np.cos(angle))
            y = int(center_y + radius * np.sin(angle))
            positions.append((x, y))
        
        return {"positions": positions, "center": (center_x, center_y)}
    
    def generate_emotional_map(self, path_id: str) -> Optional[str]:
        """
        生成情绪地图
        
        Args:
            path_id: 路径ID
            
        Returns:
            Optional[str]: 生成的文件路径
        """
        try:
            # 加载数据
            memory_data = self._load_memory_store()
            if "paths" not in memory_data:
                logger.error("无路径数据")
                return None
            
            path_data = None
            for path in memory_data["paths"]:
                if path.get("path_id") == path_id:
                    path_data = path
                    break
            
            if not path_data:
                logger.error(f"路径不存在: {path_id}")
                return None
            
            path_name = path_data.get("path_name", path_id)
            nodes = path_data.get("nodes", [])
            
            if not nodes:
                logger.error("无节点数据")
                return None
            
            # 创建图像
            width, height = 2400, 1800
            img = Image.new('RGB', (width, height), self.style["paper_color"])
            img = self._apply_paper_texture(img)
            
            # 计算布局
            layout = self._calculate_layout(nodes)
            positions = layout["positions"]
            
            # 绘制区域背景
            img = self._render_zone_background(img, nodes, layout)
            
            # 创建绘图对象
            draw = ImageDraw.Draw(img)
            
            # 绘制标题
            title = f"情绪导航地图: {path_name}"
            if self.chinese_font_large:
                draw.text((100, 80), title,
                         font=self.chinese_font_large,
                         fill=self.style["line_color"])
            
            # 绘制路径（贝塞尔曲线+箭头）
            for i in range(len(nodes) - 1):
                from_pos = positions[i]
                to_pos = positions[i + 1]
                
                self._draw_bezier_arrow(draw, from_pos, to_pos,
                                       self.style["line_color"], width=2)
                
                # 标注距离（如果有）
                distance = nodes[i].get("distance", 0)
                if distance > 0:
                    mid_x = (from_pos[0] + to_pos[0]) // 2
                    mid_y = (from_pos[1] + to_pos[1]) // 2
                    
                    distance_text = f"{distance}米"
                    if self.chinese_font_small:
                        draw.text((mid_x - 20, mid_y - 10),
                                 distance_text,
                                 font=self.chinese_font_small,
                                 fill=(100, 100, 100))
            
            # 绘制节点
            for i, (node, position) in enumerate(zip(nodes, positions)):
                x, y = position
                
                # 绘制节点图标（SVG）
                node_type = node.get("type", "default")
                icon_name_map = {
                    "destination": "map-pin",
                    "waypoint": "map-pin",
                    "entrance": "door-enter",
                    "toilet": "toilet",
                    "elevator": "elevator",
                    "stairs": "stairs",
                    "building": "building",
                }
                icon_name = icon_name_map.get(node_type.lower(), "map-pin")
                
                icon_img = self._load_svg_icon(icon_name, size=self.style["node_size"])
                if icon_img:
                    if icon_img.mode == 'RGBA':
                        img.paste(icon_img, (x - 24, y - 24), icon_img)
                    else:
                        img.paste(icon_img, (x - 24, y - 24))
                
                # 绘制节点外圆（加粗）
                draw.ellipse([x - 30, y - 30, x + 30, y + 30],
                           outline=self.style["line_color"],
                           width=self.style["node_thickness"],
                           fill=(255, 255, 255))
                
                # 绘制节点编号
                draw.text((x - 6, y - 10), str(i + 1),
                         font=ImageFont.load_default(),
                         fill=self.style["line_color"])
                
                # 绘制中文标签
                label = node.get("label", "")
                if label and self.chinese_font_small:
                    bbox = draw.textbbox((0, 0), label, font=self.chinese_font_small)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    draw.text((x - text_width // 2, y + 45),
                             label,
                             font=self.chinese_font_small,
                             fill=self.style["line_color"])
                
                # 绘制情绪标签
                emotions = node.get("emotion", [])
                if isinstance(emotions, str):
                    emotions = [emotions]
                elif emotions is None:
                    emotions = []
                
                if emotions:
                    self._render_emotion_tags(draw, emotions, (x - 50, y + 70))
            
            # 绘制指南针
            self._draw_compass(draw, (width - 150, 150))
            
            # 保存图像
            output_path = os.path.join(self.output_dir, f"{path_id}_emotional.png")
            img.save(output_path)
            
            # 生成元信息
            meta_info = self._generate_meta_info(path_data, nodes, layout)
            meta_path = os.path.join(self.output_dir, f"{path_id}_emotional.meta.json")
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta_info, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 情绪地图已生成: {output_path}")
            logger.info(f"✅ 元信息已生成: {meta_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 生成失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generate_meta_info(self, path_data: Dict, nodes: List[Dict],
                           layout: Dict) -> Dict:
        """生成元信息"""
        # 提取区域
        regions = set()
        for node in nodes:
            level = node.get("level", "")
            if level and level in self.zone_colors:
                regions.add(level)
        
        # 计算总距离
        total_distance = sum(node.get("distance", 0) for node in nodes)
        
        return {
            "path_id": path_data.get("path_id"),
            "path_name": path_data.get("path_name"),
            "map_direction_reference": "上 = 北",
            "compass_added": True,
            "regions_detected": sorted(list(regions)),
            "node_count": len(nodes),
            "total_distance": f"{total_distance}米",
            "generation_timestamp": __import__("datetime").datetime.now().isoformat(),
        }
    
    def _load_memory_store(self) -> Dict:
        """加载记忆存储"""
        try:
            with open(self.memory_store_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载失败: {e}")
            return {}

def main():
    """测试主函数"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    generator = EmotionalMapCardGeneratorEnhanced()
    result = generator.generate_emotional_map("test_emotional_path")
    
    if result:
        print(f"✅ 生成成功: {result}")

if __name__ == "__main__":
    main()

