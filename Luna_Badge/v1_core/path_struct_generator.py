#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
情绪地图图卡生成器
生成手绘风格的情绪地图，包含情绪标签、图标和方向线
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

class EmotionalMapCardGenerator:
    """情绪地图图卡生成器"""
    
    def __init__(self, 
                 memory_store_path: str = "data/memory_store.json",
                 output_dir: str = "data/map_cards",
                 icons_dir: str = "assets/icons"):
        """
        初始化情绪地图生成器
        
        Args:
            memory_store_path: 记忆存储文件路径
            output_dir: 输出目录
            icons_dir: 图标目录
        """
        self.memory_store_path = memory_store_path
        self.output_dir = output_dir
        self.icons_dir = icons_dir
        
        # 创建输出目录
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 情绪映射（使用字符符号替代emoji避免乱码）
        self.emotion_map = {
            "热闹": {"symbol": "*", "color": (255, 100, 100)},      # 红色
            "安静": {"symbol": "~", "color": (100, 150, 255)},      # 蓝色
            "推荐": {"symbol": "*", "color": (255, 200, 100)},      # 黄色
            "嘈杂": {"symbol": "!", "color": (255, 150, 100)},      # 橙色
            "温馨": {"symbol": "+", "color": (255, 180, 200)},      # 粉色
            "宽敞": {"symbol": "[]", "color": (150, 200, 255)},     # 淡蓝色
            "拥挤": {"symbol": "#", "color": (255, 150, 150)},      # 浅红色
            "明亮": {"symbol": "O", "color": (255, 255, 100)},      # 黄色
            "整洁": {"symbol": "=", "color": (150, 255, 150)},      # 绿色
            "等待": {"symbol": "...", "color": (200, 200, 200)},    # 灰色
        }
        
        # 手绘样式配置
        self.hand_drawn_style = {
            "paper_color": (249, 247, 238),  # 米黄色纸张
            "line_color": (50, 50, 50),      # 黑色线条
            "shadow_color": (200, 200, 200), # 灰色阴影
            "texture_alpha": 30,              # 纹理透明度
        }
        
        logger.info("🗺️ 情绪地图生成器初始化完成")
    
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
    
    def _apply_paper_texture(self, img: Image.Image) -> Image.Image:
        """应用纸张纹理效果"""
        width, height = img.size
        
        # 创建噪声纹理
        noise = np.random.randint(0, 50, (height, width), dtype=np.uint8)
        noise_img = Image.fromarray(noise, mode='L')
        
        # 应用高斯模糊
        noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=1.0))
        
        # 调整透明度
        noise_img = noise_img.point(lambda x: int(x * self.hand_drawn_style["texture_alpha"] / 255))
        
        # 叠加到原图
        result = img.copy()
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay.paste(noise_img, mask=noise_img)
        result = Image.alpha_composite(result.convert('RGBA'), overlay).convert('RGB')
        
        return result
    
    def _add_hand_drawn_noise(self, draw: ImageDraw.Draw) -> None:
        """添加手绘噪声效果"""
        width, height = draw.im.size
        
        # 添加一些随机小点
        for _ in range(50):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            radius = np.random.randint(1, 3)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(200, 200, 200, 20))
    
    def _draw_shaky_line(self, draw: ImageDraw.Draw, coords: List[Tuple[int, int]], 
                        color: Tuple[int, int, int], width: int = 3) -> None:
        """绘制抖动线条（手绘效果）"""
        for i in range(len(coords) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            
            # 添加抖动
            num_points = max(10, int(np.sqrt((x2-x1)**2 + (y2-y1)**2) / 5))
            for j in range(num_points):
                t = j / num_points
                x = int(x1 + (x2 - x1) * t)
                y = int(y1 + (y2 - y1) * t)
                
                # 随机偏移
                offset_x = np.random.randint(-2, 3)
                offset_y = np.random.randint(-2, 3)
                
                draw.ellipse([x+offset_x-width, y+offset_y-width, 
                             x+offset_x+width, y+offset_y+width], 
                            fill=color)
    
    def _render_node_icon(self, node_type: str, size: int = 48) -> Image.Image:
        """渲染节点图标"""
        # 创建图标
        icon = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(icon)
        
        # 根据节点类型绘制不同图标
        center = size // 2
        radius = size // 3
        
        if node_type in ["building", "hospital"]:
            # 建筑图标 - 简化版
            draw.rectangle([center-radius, center-radius, 
                           center+radius, center+radius], 
                          outline=(100, 100, 100), width=2)
            # 画一个简单的十字表示医院
            draw.line([center, center-radius, center, center+radius], 
                     fill=(100, 100, 100), width=2)
            draw.line([center-radius, center, center+radius, center], 
                     fill=(100, 100, 100), width=2)
        elif node_type == "toilet":
            # 卫生间图标
            draw.ellipse([center-radius, center-radius, 
                         center+radius, center+radius], 
                        outline=(100, 100, 100), width=2)
        elif node_type in ["elevator", "stairs"]:
            # 电梯/楼梯图标 - 简化版
            draw.rectangle([center-radius, center-radius, 
                           center+radius, center+radius], 
                          outline=(100, 100, 100), width=2)
            # 画几条横线表示楼梯
            for i in range(-2, 3):
                y = center + i * 5
                draw.line([center-radius+3, y, center+radius-3, y], 
                         fill=(100, 100, 100), width=1)
        else:
            # 默认圆形节点
            draw.ellipse([center-radius, center-radius, 
                         center+radius, center+radius], 
                        outline=(100, 100, 100), width=3, 
                        fill=(240, 240, 240))
        
        return icon
    
    def _render_emotion_tag(self, emotion: str, position: Tuple[int, int], 
                           img: Image.Image) -> None:
        """渲染情绪标签"""
        if emotion not in self.emotion_map:
            return
        
        emotion_data = self.emotion_map[emotion]
        symbol = emotion_data["symbol"]
        color = emotion_data["color"]
        
        draw = ImageDraw.Draw(img)
        
        # 绘制标签背景（彩色圆形）
        label_size = 45
        x, y = position
        
        # 绘制阴影
        draw.ellipse([x-label_size//2+3, y-label_size//2+3, 
                     x+label_size//2+3, y+label_size//2+3], 
                    fill=(150, 150, 150, 100))
        
        # 绘制主圆形
        draw.ellipse([x-label_size//2, y-label_size//2, 
                     x+label_size//2, y+label_size//2], 
                    fill=(*color, 255))
        
        # 绘制边框
        draw.ellipse([x-label_size//2, y-label_size//2, 
                     x+label_size//2, y+label_size//2], 
                    outline=(255, 255, 255), width=2)
        
        # 绘制符号
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
        # 计算文字位置（居中）
        bbox = draw.textbbox((0, 0), symbol, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.text((x - text_width//2, y - text_height//2), symbol, 
                 font=font, fill=(255, 255, 255))
    
    def generate_emotional_map(self, path_id: str, 
                              path_name: str = None,
                              nodes: List[Dict] = None) -> Optional[str]:
        """
        生成情绪地图图卡
        
        Args:
            path_id: 路径ID
            path_name: 路径名称（可选）
            nodes: 节点列表（可选，从memory_store加载）
            
        Returns:
            Optional[str]: 生成的文件路径
        """
        try:
            # 如果没有提供nodes，从memory_store加载
            if nodes is None:
                memory_data = self.load_memory_store()
                if "paths" not in memory_data:
                    logger.error("记忆存储中没有路径数据")
                    return None
                
                # 查找对应路径
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
            
            # 创建绘图对象
            draw = ImageDraw.Draw(img)
            
            # 绘制标题（使用英文避免中文乱码）
            if path_name:
                # 简化标题，避免中文乱码
                title_text = "Emotional Navigation Map"
                try:
                    title_font = ImageFont.truetype(
                        "/System/Library/Fonts/Supplemental/Arial.ttf", 36
                    )
                except:
                    title_font = ImageFont.load_default()
                draw.text((100, 80), title_text, 
                         font=title_font, fill=self.hand_drawn_style["line_color"])
                
                # 绘制路径ID（英文）
                subtitle_text = f"Path ID: {path_id}"
                draw.text((100, 125), subtitle_text, 
                         font=ImageFont.load_default(), 
                         fill=(120, 120, 120))
            
            # 计算节点位置（螺旋布局）
            center_x, center_y = width // 2, height // 2
            node_positions = []
            angle_step = 360 / len(nodes)
            
            for i, node in enumerate(nodes):
                angle = np.radians(i * angle_step)
                radius = 100 + i * 80
                x = int(center_x + radius * np.cos(angle))
                y = int(center_y + radius * np.sin(angle))
                node_positions.append((x, y))
            
            # 绘制路径线
            for i in range(len(nodes) - 1):
                start_pos = node_positions[i]
                end_pos = node_positions[i + 1]
                self._draw_shaky_line(draw, [start_pos, end_pos], 
                                     self.hand_drawn_style["line_color"], 
                                     width=3)
            
            # 绘制节点
            for i, (node, position) in enumerate(zip(nodes, node_positions)):
                x, y = position
                
                # 绘制节点图标
                node_type = node.get("type", "default")
                icon = self._render_node_icon(node_type, size=48)
                
                # 粘贴图标到主图
                icon_x = x - icon.size[0] // 2
                icon_y = y - icon.size[1] // 2
                img.paste(icon, (icon_x, icon_y), icon)
                
                # 绘制节点编号
                draw.ellipse([x-20, y-20, x+20, y+20], 
                           outline=self.hand_drawn_style["line_color"], 
                           width=2, fill=(255, 255, 255))
                draw.text((x-10, y-15), str(i+1), 
                         font=ImageFont.load_default(), 
                         fill=self.hand_drawn_style["line_color"])
                
                # 绘制节点标签（使用合适的字体大小和位置）
                # 使用节点类型或编号
                node_type = node.get("type", "default").upper()
                try:
                    label_font = ImageFont.truetype(
                        "/System/Library/Fonts/Supplemental/Arial.ttf", 14
                    )
                except:
                    label_font = ImageFont.load_default()
                # 计算文本宽度以便居中
                text_bbox = draw.textbbox((0, 0), node_type[:10], font=label_font)
                text_width = text_bbox[2] - text_bbox[0]
                draw.text((x - text_width//2, y + 35), node_type[:10], 
                         font=label_font, 
                         fill=self.hand_drawn_style["line_color"])
                
                # 绘制情绪标签
                emotion = node.get("emotion")
                if emotion:
                    # 支持emotion为列表的情况
                    if isinstance(emotion, list):
                        # 只显示第一个情绪标签
                        if emotion:
                            self._render_emotion_tag(emotion[0], (x-40, y-40), img)
                    else:
                        # emption是字符串
                        self._render_emotion_tag(emotion, (x-40, y-40), img)
            
            # 添加手绘噪声效果
            self._add_hand_drawn_noise(draw)
            
            # 保存图像
            output_path = os.path.join(self.output_dir, f"{path_id}_emotional.png")
            img.save(output_path)
            
            logger.info(f"✅ 情绪地图已生成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ 生成情绪地图失败: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """测试主函数"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    generator = EmotionalMapCardGenerator()
    
    # 测试生成
    test_path_id = "test_emotional_path"
    test_nodes = [
        {"type": "building", "label": "起点", "emotion": "推荐"},
        {"type": "toilet", "label": "卫生间", "emotion": "安静"},
        {"type": "elevator", "label": "电梯", "emotion": None},
        {"type": "hospital", "label": "目的地", "emotion": "温馨"},
    ]
    
    result = generator.generate_emotional_map(test_path_id, 
                                             path_name="测试情绪路径", 
                                             nodes=test_nodes)
    
    if result:
        print(f"✅ 情绪地图生成成功: {result}")
    else:
        print("❌ 情绪地图生成失败")

if __name__ == "__main__":
    main()

