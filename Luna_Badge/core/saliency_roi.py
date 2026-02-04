"""
显著性ROI提取模块（借鉴STAViS）
用于快速定位图像中的关键区域，提高检测速度
"""

import cv2
import numpy as np
import logging
from typing import List, Dict, Tuple, Optional, Any

logger = logging.getLogger(__name__)

class SaliencyROI:
    """基于显著性的ROI提取（借鉴STAViS的音视频显著性网络）"""
    
    def __init__(self, saliency_threshold: float = 0.7, min_roi_size: int = 50):
        """
        初始化显著性ROI提取器
        
        Args:
            saliency_threshold: 显著性阈值（0-1）
            min_roi_size: 最小ROI尺寸（像素）
        """
        self.saliency_threshold = saliency_threshold
        self.min_roi_size = min_roi_size
        self.logger = logging.getLogger(__name__)
        self.logger.info("✅ 显著性ROI提取器初始化完成")
    
    def compute_saliency(self, image: np.ndarray) -> np.ndarray:
        """
        计算视觉显著性图（借鉴STAViS的视觉显著性计算）
        
        Args:
            image: 输入图像（BGR格式）
        
        Returns:
            显著性图（0-255）
        """
        # 方法1：基于梯度的显著性（快速）
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Sobel算子计算梯度（边缘=显著性）
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        # 方法2：基于颜色对比度（补充）
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        color_contrast = cv2.Laplacian(l_channel, cv2.CV_64F)
        color_contrast = np.abs(color_contrast)
        
        # 融合两种方法
        saliency = (gradient_magnitude * 0.6 + color_contrast * 0.4)
        
        # 归一化到0-255
        saliency = cv2.normalize(saliency, None, 0, 255, cv2.NORM_MINMAX)
        saliency = saliency.astype(np.uint8)
        
        return saliency
    
    def extract_roi(self, image: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        提取高显著性区域（ROI）
        
        Args:
            image: 输入图像
            top_k: 返回前k个ROI
        
        Returns:
            List[Dict]: ROI区域列表，每个包含bbox和score
        """
        # 1. 计算显著性图
        saliency_map = self.compute_saliency(image)
        
        # 2. 二值化
        threshold_value = int(self.saliency_threshold * 255)
        _, binary = cv2.threshold(saliency_map, threshold_value, 255, cv2.THRESH_BINARY)
        
        # 3. 形态学操作（去除噪声）
        kernel = np.ones((5, 5), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # 4. 提取连通区域
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 5. 计算每个区域的显著性得分
        roi_regions = []
        h, w = image.shape[:2]
        
        for contour in contours:
            # 计算边界框
            x, y, w_roi, h_roi = cv2.boundingRect(contour)
            
            # 过滤太小的区域
            if w_roi < self.min_roi_size or h_roi < self.min_roi_size:
                continue
            
            # 计算该区域的显著性得分
            mask = np.zeros(saliency_map.shape, dtype=np.uint8)
            cv2.fillPoly(mask, [contour], 255)
            
            roi_saliency = saliency_map[mask > 0]
            score = np.mean(roi_saliency) / 255.0  # 归一化到0-1
            
            # 计算区域面积占比
            area_ratio = cv2.contourArea(contour) / (w * h)
            
            roi_regions.append({
                'bbox': (x, y, w_roi, h_roi),
                'score': score,
                'area_ratio': area_ratio,
                'center': (x + w_roi // 2, y + h_roi // 2)
            })
        
        # 6. 按得分排序，返回top_k
        roi_regions.sort(key=lambda x: x['score'], reverse=True)
        
        return roi_regions[:top_k]
    
    def detect_in_roi(self, image: np.ndarray, roi_regions: List[Dict[str, Any]], 
                      detector_func: callable) -> List[Any]:
        """
        只在ROI区域进行检测（提高速度）
        
        Args:
            image: 原始图像
            roi_regions: ROI区域列表
            detector_func: 检测函数，接收图像返回检测结果
        
        Returns:
            检测结果列表
        """
        all_results = []
        
        for roi in roi_regions:
            x, y, w, h = roi['bbox']
            
            # 提取ROI图像
            roi_image = image[y:y+h, x:x+w]
            
            if roi_image.size == 0:
                continue
            
            # 在ROI区域进行检测
            try:
                results = detector_func(roi_image)
                
                # 调整坐标（从ROI坐标转换到原图坐标）
                if isinstance(results, list):
                    for result in results:
                        if isinstance(result, dict) and 'bbox' in result:
                            orig_x, orig_y, orig_w, orig_h = result['bbox']
                            result['bbox'] = (orig_x + x, orig_y + y, orig_w, orig_h)
                        all_results.append(result)
                else:
                    all_results.append(results)
            except Exception as e:
                self.logger.warning(f"ROI检测失败: {e}")
        
        return all_results
    
    def fuse_audio_saliency(self, visual_saliency: np.ndarray, 
                           audio_direction: Optional[float] = None) -> np.ndarray:
        """
        融合音频显著性（如果可用）
        
        Args:
            visual_saliency: 视觉显著性图
            audio_direction: 音频方向（角度，0-360度）
        
        Returns:
            融合后的显著性图
        """
        if audio_direction is None:
            return visual_saliency
        
        h, w = visual_saliency.shape
        
        # 根据音频方向创建音频显著性图
        audio_saliency = np.zeros((h, w), dtype=np.float32)
        
        # 假设音频方向对应图像中的某个区域
        # 这里简化处理：在对应方向区域增加显著性
        center_x, center_y = w // 2, h // 2
        
        # 根据角度计算位置
        angle_rad = np.radians(audio_direction)
        target_x = int(center_x + np.cos(angle_rad) * w * 0.3)
        target_y = int(center_y + np.sin(angle_rad) * h * 0.3)
        
        # 在该位置创建高斯分布
        y_coords, x_coords = np.ogrid[:h, :w]
        dist_sq = (x_coords - target_x)**2 + (y_coords - target_y)**2
        sigma = min(w, h) * 0.1
        audio_saliency = np.exp(-dist_sq / (2 * sigma**2)) * 255
        
        # 融合视觉和音频显著性
        fused_saliency = (visual_saliency * 0.7 + audio_saliency * 0.3).astype(np.uint8)
        
        return fused_saliency

