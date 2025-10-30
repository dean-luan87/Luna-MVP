#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
情绪地图图卡生成器 v2.0
全面升级版本：支持中文、SVG图标、方向箭头、区域高亮
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path as MPath
import matplotlib.colors as mcolors

logger = logging.getLogger(__name__)

class EmotionalMapCardGeneratorV2:
    """情绪地图图卡生成器 v2.0"""
    
    def __init__(self, 
                 memory_store_path: str = "data/memory_store.json",
                 output_dir: str = "data/map_cards",
                 icons_dir: str = "assets/icons/tabler",
                 fonts_dir: str = "assets/fonts",
                 textures_dir: str = "assets/textures"):
        """
        初始化情绪地图生成器 v2.0
        
        Args:
            memory_store_path: 记忆存储文件路径
            output_dir: 输出目录
            icons_dir: 图标目录（Tabler SVG）
            fonts_dir: 字体目录
            textures_dir: 纹理目录
        """
        self.memory_store_path = memory_store_path
        self.output_dir = output_dir
        self.icons_dir = icons_dir
        self.fonts_dir = fonts_dir
        self.textures_dir = textures_dir
        
        # 创建输出目录
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 初始化SVG加载器
        try:
            from core.svg_icon_loader import SVGIconLoader
            self.svg_loader = SVGIconLoader
        except ImportError:
            self.svg_loader = None
            logger.warning("⚠️ SVG加载器不可用")
        
        # 加载中文字体
        self.chinese_font = self._load_chinese_font()
        
        # 情绪映射（emoji支持）
        self.emotion_map = {
            "热闹": {"emoji": "🎉", "color": (255, 100, 100), "text_color": (255, 255, 255)},
            "安静": {"emoji": "🤫", "color": (100, 150, 255), "text_color": (255, 255, 255)},
            "推荐": {"emoji": "⭐", "color": (255, 200, 100), "text_color": (255, 255, 255)},
            "嘈杂": {"emoji": "🔊", "color": (255, 150, 100), "text_color": (255, 255, 255)},
            "温馨": {"emoji": "💝", "color": (255, 180, 200), "text_color": (255, 255, 255)},
            "宽敞": {"emoji": "🏛️", "color": (150, 200, 255), "text_color": (255, 255, 255)},
            "拥挤": {"emoji": "👥", "color": (255, 150, 150), "text_color": (255, 255, 255)},
            "明亮": {"emoji": "💡", "color": (255, 255, 100), "text_color": (100, 100, 100)},
            "整洁": {"emoji": "✨", "color": (150, 255, 150), "text_color": (100, 100, 100)},
            "等待": {"emoji": "⏳", "color": (200, 200, 200), "text_color": (100, 100, 100)},
        }
        
        # 区域颜色映射
        self.zone_colors = {
            "医院一楼": {"color": (230, 240, 250, 100), "outline": (150, 200, 255)},
            "医院三楼": {"color": (240, 230, 250, 100), "outline": (200, 150, 255)},
            "候诊区": {"color": (255, 240, 250, 100), "outline": (255, 150, 200)},
            "挂号大厅": {"color": (250, 255, 240, 100), "outline": (200, 255, 150)},
            "电梯间": {"color": (240, 240, 240, 100), "outline": (150, 150, 150)},
        }
        
        # 手绘样式配置
        self.hand_drawn_style = {
            "paper_color": (249, 247, 238),
            "line_color": (50, 50, 50),
            "shadow_color": (200, 200, 200),
            "texture_alpha": 30,
            "dash_pattern": [8, 4],  # 虚线模式
        }
        
        logger.info("🗺️ 情绪地图生成器 v2.0 初始化完成")
    
    def _load_chinese_font(self) -> Optional[ImageFont.FreeTypeFont]:
        """加载中文字体"""
        # 尝试加载手写字体
        font_paths = [
            os.path.join(self.fonts_dir, "handwriting.ttf"),
            "/System/Library/Fonts/PingFang.ttc",  # macOS 苹方字体
            "/System/Library/Fonts/STHeiti Light.ttc",  # macOS 华文黑体
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # Linux 文泉驿
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, 20)
                    logger.info(f"✅ 加载中文字体: {font_path}")
                    return font
                except Exception as e:
                    logger.warning(f"字体加载失败: {font_path}")
                    continue
        
        logger.warning("⚠️ 未找到中文字体，将使用默认字体")
        return ImageFont.load_default()
    
    def _load_svg_icon(self, icon_name: str, size: int = 48) -> Optional[np.ndarray]:
        """加载SVG图标"""
        if not self.svg_loader:
            return None
        
        icon_path = os.path.join(self.icons_dir, f"{icon_name}.svg")
        if not os.path.exists(icon_path):
            return None
        
        try:
            return self.svg_loader.load_svg_icon(icon_path, size=size)
        except Exception as e:
            logger.warning(f"加载SVG图标失败: {icon_name} - {e}")
            return None
    
    def _render_hand_drawn_arrow(self, draw: ImageDraw.Draw, 
                                 from_pos: Tuple[int, int], 
                                 to_pos: Tuple[int, int],
                                 offset: int = 30) -> None:
        """绘制手绘风格箭头"""
        x1, y1 = from_pos
        x2, y2 = to_pos
        
        # 计算方向和距离
        dx = x2 - x1
        dy = y2 - y1
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance < 50:
            return  # 太近不画箭头
        
        # 箭头位置（前移一些）
        ratio = (distance - offset) / distance
        arrow_x = int(x1 + dx * ratio)
        arrow_y = int(y1 + dy * ratio)
        
        # 箭头角度
        angle = np.arctan2(dy, dx)
        
        # 箭头两边的角度
        arrow_angle = np.pi / 6  # 30度
        arrow_length = 15
        
        # 计算箭头顶点
        arrow_tip = (arrow_x, arrow_y)
        
        # 箭头左边点
        arrow_left = (
            int(arrow_x - arrow_length * np.cos(angle - arrow_angle)),
            int(arrow_y - arrow_length * np.sin(angle - arrow_angle))
        )
        
        # 箭头右边点
        arrow_right = (
            int(arrow_x - arrow_length * np.cos(angle + arrow_angle)),
            int(arrow_y - arrow_length * np.sin(angle + arrow_angle))
        )
        
        # 绘制箭头（带抖动）
        points = [arrow_tip, arrow_left, arrow_right]
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            # 添加抖动
            offset_x = np.random.randint(-1, 2)
            offset_y = np.random.randint(-1, 2)
            draw.line([x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y],
                     fill=self.hand_drawn_style["line_color"], width=2)
        
    def _render_zone_highlight(self, img: Image.Image, nodes: List[Dict], 
                               layout: Dict) -> None:
        """渲染区域高亮"""
        # 按层级分组节点
        zones = {}
        for i, node in enumerate(nodes):
            level = node.get("level", "未分类")
            if level in self.zone_colors:
                if level not in zones:
                    zones[level] = []
                # 假设layout中有节点位置信息
                # 这里需要从实际layout中获取位置
                zones[level].append(i)
        
        # 绘制区域
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        for zone_name, zone_color_info in self.zone_colors.items():
            # 获取该区域的所有节点位置
            zone_nodes = [i for i, node in enumerate(nodes) 
                         if zone_name in node.get("level", "")]
            
            if not zone_nodes:
                continue
            
            # 绘制区域椭圆（简化）
            for node_idx in zone_nodes:
                # 这里需要根据实际布局计算位置
                # 暂时使用简化的方式
                x = 400 + (node_idx * 200) % 1600
                y = 400 + (node_idx * 150) % 1200
                
                # 绘制半透明椭圆
                overlay_draw.ellipse([x-150, y-100, x+150, y+100],
                                   fill=zone_color_info["color"],
                                   outline=zone_color_info["outline"], 
                                   width=2)
        
        # 合成
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        return img
    
    def _render_emotion_tags(self, draw: ImageDraw.Draw, 
                            emotions: List[str], 
                            position: Tuple[int, int], 
                            img: Image.Image) -> None:
        """渲染情绪标签（支持emoji）"""
        x, y = position
        tag_spacing = 8
        
        for idx, emotion in enumerate(emotions[:3]):  # 最多3个标签
            if emotion not in self.emotion_map:
                continue
            
            emotion_data = self.emotion_map[emotion]
            emoji = emotion_data["emoji"]
            bg_color = emotion_data["color"]
            text_color = emotion_data["text_color"]
            
            # 绘制标签背景
            tag_size = 32
            tag_x = x - 10
            tag_y = y + idx * (tag_size + tag_spacing)
            
            # 圆角矩形背景
            draw.ellipse([tag_x, tag_y, tag_x + tag_size, tag_y + tag_size],
                        fill=bg_color)
            
            # 绘制emoji
            try:
                emoji_font = ImageFont.truetype(
                    "/System/Library/Fonts/Apple Color Emoji.ttc", 20
                )
                draw.text((tag_x + 6, tag_y + 6), emoji,
                         font=emoji_font)
            except:
                # fallback to text
                text = emotion[:2]
                draw.text((tag_x + 8, tag_y + 8), text,
                         font=ImageFont.load_default(),
                         fill=text_color)
    
    def _apply_paper_texture(self, img: Image.Image) -> Image.Image:
        """应用纸张纹理效果"""
        # 尝试加载纹理图片
        texture_path = os.path.join(self.textures_dir, "paper_background.png")
        if os.path.exists(texture_path):
            try:
                texture = Image.open(texture_path).convert('RGBA')
                texture = texture.resize(img.size)
                # 调整透明度
                texture.putalpha(30)
                img = Image.alpha_composite(img.convert('RGBA'), texture).convert('RGB')
                logger.info(f"✅ 加载纸张纹理: {texture_path}")
                return img
            except Exception as e:
                logger.warning(f"加载纹理失败: {e}")
        
        # 如果没有纹理文件，使用噪声纹理
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
        
        # 螺旋布局
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
        
        return {
            "positions": positions,
            "center": (center_x, center_y)
        }
    
    def generate_emotional_map(self, path_id: str) -> Optional[str]:
        """
        生成情绪地图图卡
        
        Args:
            path_id: 路径ID
            
        Returns:
            Optional[str]: 生成的文件路径
        """
        try:
            # 加载记忆存储
            memory_data = self.load_memory_store()
            if "paths" not in memory_data:
                logger.error("记忆存储中没有路径数据")
                return None
            
            # 查找路径
            path_data = None
            for path in memory_data["paths"]:
                if path.get("path_id") == path_id:
                    path_data = path
                    break
            
            if path_data is None:
                logger.error(f"未找到路径: {path_id}")
                return None
            
            path_name = path_data.get("path_name", path_id)
            nodes = path_data.get("nodes", [])
            
            if not nodes:
                logger.error(f"路径 {path_id} 没有节点数据")
                return None
            
            # 创建图像
            width, height = 2400, 1800
            img = Image.new('RGB', (width, height), 
                          self.hand_drawn_style["paper_color"])
            
            # 应用纸张纹理
            img = self._apply_paper_texture(img)
            
            # 计算布局
            layout = self._calculate_layout(nodes)
            positions = layout["positions"]
            
            # 创建绘图对象
            draw = ImageDraw.Draw(img)
            
            # 绘制标题（中文）
            title_text = f"情绪导航地图: {path_name}"
            try:
                title_font = ImageFont.truetype(
                    "/System/Library/Fonts/PingFang.ttc", 36
                )
            except:
                title_font = ImageFont.load_default()
            draw.text((100, 80), title_text, 
                     font=title_font, 
                     fill=self.hand_drawn_style["line_color"])
            
            # 绘制路径线（手绘风格）
            for i in range(len(nodes) - 1):
                from_pos = positions[i]
                to_pos = positions[i + 1]
                
                # 绘制虚线
                self._draw_dashed_line(draw, from_pos, to_pos,
                                      self.hand_drawn_style["line_color"],
                                      dash_pattern=self.hand_drawn_style["dash_pattern"],
                                      width=2)
                
                # 绘制箭头
                self._render_hand_drawn_arrow(draw, from_pos, to_pos)
            
            # 绘制节点
            for i, (node, position) in enumerate(zip(nodes, positions)):
                x, y = position
                
                # 绘制节点图标（SVG）
                node_type = node.get("type", "default")
                icon_name = node_type.lower()
                if icon_name in ["destination", "waypoint"]:
                    icon_name = "map-pin"
                elif icon_name == "entrance":
                    icon_name = "door-enter"
                
                icon_img = self._load_svg_icon(icon_name, size=48)
                if icon_img is not None:
                    # 转换为PIL Image
                    from PIL import Image as PILImage
                    if isinstance(icon_img, np.ndarray):
                        if icon_img.shape[2] == 4:  # RGBA
                            icon_pil = PILImage.fromarray(icon_img)
                            img.paste(icon_pil, (x-24, y-24), icon_pil)
                        else:  # RGB
                            icon_pil = PILImage.fromarray(icon_img)
                            img.paste(icon_pil, (x-24, y-24))
                
                # 绘制节点圆圈
                draw.ellipse([x-30, y-30, x+30, y+30],
                           outline=self.hand_drawn_style["line_color"],
                           width=3, fill=(255, 255, 255))
                
                # 绘制节点编号
                draw.text((x-8, y-12), str(i+1),
                         font=ImageFont.load_default(),
                         fill=self.hand_drawn_style["line_color"])
                
                # 绘制中文标签
                label = node.get("label", "")
                if label and self.chinese_font:
                    bbox = draw.textbbox((0, 0), label, font=self.chinese_font)
                    text_width = bbox[2] - bbox[0]
                    draw.text((x - text_width//2, y + 40), label,
                             font=self.chinese_font,
                             fill=self.hand_drawn_style["line_color"])
                
                # 绘制情绪标签
                emotions = node.get("emotion", [])
                if isinstance(emotions, str):
                    emotions = [emotions]
                if emotions:
                    self._render_emotion_tags(draw, emotions, (x+40, y), img)
            
            # 保存图像
            output_path = os.path.join(self.output_dir, f"{path_id}_emotional_v2.png")
            img.save(output_path)
            
            logger.info(f"✅ 情绪地图 v2.0 已生成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 生成情绪地图失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _draw_dashed_line(self, draw: ImageDraw.Draw, 
                         from_pos: Tuple[int, int], 
                         to_pos: Tuple[int, int],
                         color: Tuple[int, int, int],
                         dash_pattern: List[int] = [10, 5],
                         width: int = 2) -> None:
        """绘制虚线（带抖动效果）"""
        x1, y1 = from_pos
        x2, y2 = to_pos
        
        dx = x2 - x1
        dy = y2 - y1
        distance = np.sqrt(dx**2 + dy**2)
        
        dash_len, gap_len = dash_pattern
        total_pattern = dash_len + gap_len
        
        segments = int(distance / total_pattern)
        
        for i in range(segments):
            start_ratio = i * total_pattern / distance
            end_ratio = min((i * total_pattern + dash_len) / distance, 1.0)
            
            seg_x1 = int(x1 + dx * start_ratio)
            seg_y1 = int(y1 + dy * start_ratio)
            seg_x2 = int(x1 + dx * end_ratio)
            seg_y2 = int(y1 + dy * end_ratio)
            
            # 添加抖动
            offset = np.random.randint(-1, 2)
            draw.line([seg_x1 + offset, seg_y1 + offset, 
                      seg_x2 + offset, seg_y2 + offset],
                     fill=color, width=width)
    
    def load_memory_store(self) -> Dict:
        """加载记忆存储"""
        try:
            with open(self.memory_store_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"记忆存储文件不存在: {self.memory_store_path}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"记忆存储文件格式错误: {self.memory_store_path}")
            return {}

def main():
    """测试主函数"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    generator = EmotionalMapCardGeneratorV2()
    
    # 测试生成
    result = generator.generate_emotional_map("test_emotional_path")
    
    if result:
        print(f"✅ 情绪地图 v2.0 生成成功: {result}")
    else:
        print("❌ 情绪地图 v2.0 生成失败")

if __name__ == "__main__":
    main()

