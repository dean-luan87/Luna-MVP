#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试覆盖模块
显示FPS、物体数量、风险等级等调试信息
"""

import cv2
import numpy as np
import argparse
import time
from ultralytics import YOLO

class DebugOverlay:
    def __init__(self, show_fps=True, show_object_count=True, show_risk_level=True):
        self.show_fps = show_fps
        self.show_object_count = show_object_count
        self.show_risk_level = show_risk_level
        self.model = None
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
    def load_model(self):
        """加载YOLO模型"""
        try:
            self.model = YOLO('yolov8n.pt')
            return True
        except:
            return False
    
    def update_fps(self):
        """更新FPS计算"""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def detect_objects(self, frame):
        """检测物体"""
        if not self.model:
            return []
        
        try:
            results = self.model(frame)
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        confidence = float(box.conf[0].cpu().numpy())
                        
                        detections.append({
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'class_id': class_id,
                            'class_name': self.model.names[class_id],
                            'confidence': confidence
                        })
            
            return detections
            
        except:
            return []
    
    def calculate_risk_level(self, detections):
        """计算风险等级"""
        if not detections:
            return "Low"
        
        risk_objects = [d for d in detections if d['class_name'] in ['person', 'car', 'bicycle']]
        
        if len(risk_objects) >= 3:
            return "High"
        elif len(risk_objects) >= 1:
            return "Medium"
        else:
            return "Low"
    
    def draw_debug_overlay(self, frame, detections):
        """绘制调试覆盖层"""
        overlay = frame.copy()
        height, width = frame.shape[:2]
        
        # 计算风险等级
        risk_level = self.calculate_risk_level(detections)
        
        # 绘制半透明背景
        cv2.rectangle(overlay, (10, 10), (300, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        y_offset = 30
        
        # FPS信息
        if self.show_fps:
            cv2.putText(frame, f"FPS: {self.current_fps:.1f}", 
                       (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 25
        
        # 物体数量
        if self.show_object_count:
            cv2.putText(frame, f"Objects: {len(detections)}", 
                       (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            y_offset += 25
        
        # 风险等级
        if self.show_risk_level:
            risk_color = {
                'Low': (0, 255, 0),
                'Medium': (0, 255, 255),
                'High': (0, 0, 255)
            }
            color = risk_color.get(risk_level, (255, 255, 255))
            cv2.putText(frame, f"Risk: {risk_level}", 
                       (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            y_offset += 25
        
        # 系统状态
        cv2.putText(frame, "Debug Mode Active", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def run_debug_overlay(self):
        """运行调试覆盖模式"""
        if not self.load_model():
            print("❌ 模型加载失败，运行基础调试模式")
        
        print("🐛 调试覆盖模式启动")
        print(f"📊 显示FPS: {'开启' if self.show_fps else '关闭'}")
        print(f"🔢 显示物体数量: {'开启' if self.show_object_count else '关闭'}")
        print(f"⚠️ 显示风险等级: {'开启' if self.show_risk_level else '关闭'}")
        
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 更新FPS
            self.update_fps()
            
            # 检测物体
            detections = self.detect_objects(frame)
            
            # 绘制调试覆盖层
            frame = self.draw_debug_overlay(frame, detections)
            
            # 绘制检测框
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                class_name = detection['class_name']
                confidence = detection['confidence']
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(frame, f"{class_name}: {confidence:.2f}", 
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
            cv2.imshow("🐛 Luna Debug Overlay", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Luna 调试覆盖工具')
    parser.add_argument('--fps', action='store_true', help='显示FPS')
    parser.add_argument('--object_count', action='store_true', help='显示物体数量')
    parser.add_argument('--risk_level', action='store_true', help='显示风险等级')
    
    args = parser.parse_args()
    
    # 如果没有指定任何选项，默认显示所有
    if not any([args.fps, args.object_count, args.risk_level]):
        show_fps = show_object_count = show_risk_level = True
    else:
        show_fps = args.fps
        show_object_count = args.object_count
        show_risk_level = args.risk_level
    
    debug_overlay = DebugOverlay(show_fps, show_object_count, show_risk_level)
    debug_overlay.run_debug_overlay()

if __name__ == "__main__":
    main()
