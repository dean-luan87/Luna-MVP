#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摄像头初始化模块
支持多种分辨率和帧率设置
"""

import cv2
import argparse
import sys
import time

class CameraInitializer:
    def __init__(self, source=0, resolution="1280x720", fps=30):
        """
        初始化摄像头
        
        Args:
            source: 摄像头源 (0为默认摄像头)
            resolution: 分辨率字符串，格式如 "1280x720"
            fps: 帧率
        """
        self.source = source
        self.resolution = resolution
        self.fps = fps
        self.cap = None
        self.width, self.height = self._parse_resolution(resolution)
        
    def _parse_resolution(self, resolution_str):
        """解析分辨率字符串"""
        try:
            width, height = map(int, resolution_str.split('x'))
            return width, height
        except ValueError:
            print(f"❌ 错误的分辨率格式: {resolution_str}")
            print("✅ 使用默认分辨率 1280x720")
            return 1280, 720
    
    def initialize(self):
        """初始化摄像头"""
        print(f"🎥 正在初始化摄像头...")
        print(f"📹 源: {self.source}")
        print(f"📐 分辨率: {self.width}x{self.height}")
        print(f"🎬 帧率: {self.fps}")
        
        # 创建摄像头对象
        self.cap = cv2.VideoCapture(self.source)
        
        if not self.cap.isOpened():
            print("❌ 无法打开摄像头")
            return False
        
        # 设置分辨率
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        # 验证设置
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        print(f"✅ 摄像头初始化成功")
        print(f"📊 实际分辨率: {actual_width}x{actual_height}")
        print(f"📊 实际帧率: {actual_fps}")
        
        return True
    
    def test_camera(self, duration=5):
        """测试摄像头功能"""
        if not self.cap:
            print("❌ 摄像头未初始化")
            return False
        
        print(f"🧪 开始摄像头测试 ({duration}秒)")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ 无法读取摄像头画面")
                return False
            
            # 显示测试信息
            cv2.putText(frame, f"Luna Camera Test - {self.width}x{self.height}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            cv2.imshow("🎥 Luna Camera Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
        print("✅ 摄像头测试完成")
        return True
    
    def release(self):
        """释放摄像头资源"""
        if self.cap:
            self.cap.release()
            print("🧹 摄像头资源已释放")

def main():
    parser = argparse.ArgumentParser(description='Luna 摄像头初始化工具')
    parser.add_argument('--source', type=int, default=0, help='摄像头源编号 (默认: 0)')
    parser.add_argument('--resolution', type=str, default='1280x720', help='分辨率 (默认: 1280x720)')
    parser.add_argument('--fps', type=int, default=30, help='帧率 (默认: 30)')
    parser.add_argument('--test', action='store_true', help='运行摄像头测试')
    parser.add_argument('--duration', type=int, default=5, help='测试持续时间(秒)')
    
    args = parser.parse_args()
    
    # 创建摄像头初始化器
    camera = CameraInitializer(args.source, args.resolution, args.fps)
    
    try:
        # 初始化摄像头
        if not camera.initialize():
            sys.exit(1)
        
        # 如果指定了测试模式
        if args.test:
            camera.test_camera(args.duration)
        
        print("✅ 摄像头初始化完成，可以开始使用")
        
    except KeyboardInterrupt:
        print("\n⚠️ 程序被用户中断")
    except Exception as e:
        print(f"❌ 程序出现错误: {e}")
    finally:
        camera.release()

if __name__ == "__main__":
    main()
