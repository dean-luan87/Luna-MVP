#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险碰撞提醒模块
检测路径遮挡、行人靠近、车辆快速接近等风险
"""

import cv2
import numpy as np
import argparse
import time
from ultralytics import YOLO

class RiskAlert:
    def __init__(self, alert_level='medium', voice_alert=True):
        self.alert_level = alert_level
        self.voice_alert = voice_alert
        self.model = None
        self.last_alert_time = 0
        self.alert_cooldown = 2  # 秒
        
        # 风险等级设置
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.5,
            'high': 0.7
        }
    
    def load_model(self):
        """加载YOLO模型"""
        try:
            self.model = YOLO('yolov8n.pt')
            print("✅ 风险检测模型加载成功")
            return True
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            return False
    
    def calculate_risk(self, detections):
        """计算风险等级"""
        risk_score = 0.0
        risk_factors = []
        
        for detection in detections:
            class_name = detection['class_name']
            distance = detection['distance']
            confidence = detection['confidence']
            
            # 根据物体类型和距离计算风险
            if class_name == 'person':
                if distance < 2.0:  # 2米内有人
                    risk_score += 0.4
                    risk_factors.append(f"行人接近 ({distance:.1f}m)")
            elif class_name == 'car':
                if distance < 5.0:  # 5米内有车辆
                    risk_score += 0.3
                    risk_factors.append(f"车辆接近 ({distance:.1f}m)")
            elif class_name == 'bicycle':
                if distance < 3.0:  # 3米内有自行车
                    risk_score += 0.2
                    risk_factors.append(f"自行车接近 ({distance:.1f}m)")
        
        return min(1.0, risk_score), risk_factors
    
    def trigger_alert(self, risk_score, risk_factors):
        """触发警报"""
        current_time = time.time()
        if current_time - self.last_alert_time < self.alert_cooldown:
            return
        
        threshold = self.risk_thresholds[self.alert_level]
        
        if risk_score >= threshold:
            alert_msg = f"⚠️ 风险警报! 风险等级: {risk_score:.2f}"
            print(alert_msg)
            
            for factor in risk_factors:
                print(f"  - {factor}")
            
            if self.voice_alert:
                print("🔊 语音警报: 请注意安全!")
            
            self.last_alert_time = current_time
    
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
                        
                        # 估算距离
                        box_height = y2 - y1
                        distance = (frame.shape[0] * 0.3) / (box_height + 1)
                        distance = max(0.1, min(20.0, distance))
                        
                        detections.append({
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'class_id': class_id,
                            'class_name': self.model.names[class_id],
                            'confidence': confidence,
                            'distance': distance
                        })
            
            return detections
            
        except Exception as e:
            print(f"❌ 检测错误: {e}")
            return []
    
    def run_risk_alert(self):
        """运行风险警报系统"""
        if not self.load_model():
            return
        
        print("⚠️ 风险碰撞提醒系统启动")
        print(f"📊 警报等级: {self.alert_level}")
        print(f"🔊 语音警报: {'开启' if self.voice_alert else '关闭'}")
        
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 检测物体
            detections = self.detect_objects(frame)
            
            # 计算风险等级
            risk_score, risk_factors = self.calculate_risk(detections)
            
            # 触发警报
            self.trigger_alert(risk_score, risk_factors)
            
            # 绘制检测结果
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                class_name = detection['class_name']
                distance = detection['distance']
                
                # 根据距离设置颜色
                if distance < 3.0:
                    color = (0, 0, 255)  # 红色 - 高风险
                elif distance < 5.0:
                    color = (0, 255, 255)  # 黄色 - 中风险
                else:
                    color = (0, 255, 0)  # 绿色 - 低风险
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{class_name} ({distance:.1f}m)", 
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # 显示风险信息
            risk_color = (0, 0, 255) if risk_score >= self.risk_thresholds[self.alert_level] else (0, 255, 0)
            cv2.putText(frame, f"Risk Level: {risk_score:.2f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, risk_color, 2)
            cv2.putText(frame, f"Alert Level: {self.alert_level}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow("⚠️ Luna Risk Alert", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Luna 风险碰撞提醒工具')
    parser.add_argument('--alert_level', type=str, default='medium', help='警报等级 (low/medium/high)')
    parser.add_argument('--voice_alert', type=bool, default=True, help='是否启用语音警报')
    
    args = parser.parse_args()
    
    risk_alert = RiskAlert(args.alert_level, args.voice_alert)
    risk_alert.run_risk_alert()

if __name__ == "__main__":
    main()
