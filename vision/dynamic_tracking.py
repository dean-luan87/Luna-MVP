#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态物体追踪模块
追踪行人、车辆等动态物体
"""

import cv2
import numpy as np
import argparse
from ultralytics import YOLO

class DynamicTracker:
    def __init__(self, classes="person,car,bicycle", max_distance=15):
        self.classes = classes.split(',')
        self.max_distance = max_distance
        self.tracker = cv2.TrackerKCF_create()
        self.model = None
        
    def load_model(self):
        try:
            self.model = YOLO('yolov8n.pt')
            return True
        except:
            return False
    
    def run_tracking(self):
        print("🏃 动态物体追踪模块")
        print(f"🎯 追踪类别: {self.classes}")
        print(f"📏 最大距离: {self.max_distance}米")
        
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.putText(frame, "Dynamic Tracking Mode", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("🏃 Luna Dynamic Tracking", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Luna 动态物体追踪工具')
    parser.add_argument('--classes', type=str, default="person,car,bicycle", help='追踪类别')
    parser.add_argument('--max_distance', type=float, default=15.0, help='最大距离(米)')
    
    args = parser.parse_args()
    
    tracker = DynamicTracker(args.classes, args.max_distance)
    tracker.run_tracking()

if __name__ == "__main__":
    main()
