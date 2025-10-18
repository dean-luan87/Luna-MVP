#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
夜间增强模块
模拟夜视模式，增强亮度和降噪
"""

import cv2
import numpy as np
import argparse

class NightMode:
    def __init__(self, brightness_boost=2.0, denoise=True):
        self.brightness_boost = brightness_boost
        self.denoise = denoise
        
    def enhance_frame(self, frame):
        """增强夜间画面"""
        # 亮度增强
        enhanced = cv2.convertScaleAbs(frame, alpha=self.brightness_boost, beta=0)
        
        # 降噪处理
        if self.denoise:
            enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)
            
        return enhanced
    
    def run_night_mode(self):
        print("🌙 夜间增强模式启动")
        print(f"💡 亮度增强: {self.brightness_boost}x")
        print(f"🔇 降噪处理: {'开启' if self.denoise else '关闭'}")
        
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # 增强处理
            enhanced = self.enhance_frame(frame)
            
            # 显示信息
            cv2.putText(enhanced, f"Night Mode - Boost: {self.brightness_boost}x", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(enhanced, "Press 'q' to quit", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("🌙 Luna Night Mode", enhanced)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Luna 夜间增强工具')
    parser.add_argument('--brightness_boost', type=float, default=2.0, help='亮度增强倍数')
    parser.add_argument('--denoise', type=bool, default=True, help='是否启用降噪')
    
    args = parser.parse_args()
    
    night_mode = NightMode(args.brightness_boost, args.denoise)
    night_mode.run_night_mode()

if __name__ == "__main__":
    main()
