#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频稳定模块
防抖处理，稳定视频画面
"""

import cv2
import numpy as np
import argparse

class VideoStabilizer:
    def __init__(self, input_source='live', output='stabilized', mode='light'):
        self.input_source = input_source
        self.output = output
        self.mode = mode
        self.prev_gray = None
        self.prev_keypoints = None
        
    def stabilize_frame(self, frame):
        """稳定视频帧"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.prev_gray is None:
            self.prev_gray = gray
            return frame
            
        # 特征点检测
        detector = cv2.SIFT_create()
        kp1, des1 = detector.detectAndCompute(gray, None)
        kp2, des2 = detector.detectAndCompute(self.prev_gray, None)
        
        if des1 is not None and des2 is not None:
            # 特征点匹配
            matcher = cv2.BFMatcher()
            matches = matcher.knnMatch(des1, des2, k=2)
            
            # 筛选好的匹配
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
            
            if len(good_matches) > 10:
                # 计算变换矩阵
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                M, mask = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC)
                
                if M is not None:
                    # 应用稳定变换
                    stabilized = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
                    self.prev_gray = gray
                    return stabilized
        
        self.prev_gray = gray
        return frame
    
    def run_stabilization(self):
        print("📹 视频稳定模式启动")
        print(f"📥 输入源: {self.input_source}")
        print(f"📤 输出模式: {self.output}")
        print(f"⚙️ 稳定模式: {self.mode}")
        
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # 稳定处理
            stabilized = self.stabilize_frame(frame)
            
            # 显示信息
            cv2.putText(stabilized, f"Video Stabilization - Mode: {self.mode}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(stabilized, "Press 'q' to quit", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("📹 Luna Video Stabilization", stabilized)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Luna 视频稳定工具')
    parser.add_argument('--input', type=str, default='live', help='输入源')
    parser.add_argument('--output', type=str, default='stabilized', help='输出模式')
    parser.add_argument('--mode', type=str, default='light', help='稳定模式')
    
    args = parser.parse_args()
    
    stabilizer = VideoStabilizer(args.input, args.output, args.mode)
    stabilizer.run_stabilization()

if __name__ == "__main__":
    main()
