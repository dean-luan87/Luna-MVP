#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna 实体徽章 MVP - 快速启动脚本
"""

import sys
import os
import subprocess

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import cv2
        import numpy
        print("✓ OpenCV 和 NumPy 已安装")
        print(f"  - OpenCV版本: {cv2.__version__}")
        
        # 检查Mac特定的摄像头后端
        import platform
        if platform.system() == 'Darwin':
            if hasattr(cv2, 'CAP_AVFOUNDATION'):
                print("✓ AVFoundation后端可用（Mac推荐）")
            else:
                print("⚠ AVFoundation后端不可用，可能影响Mac摄像头兼容性")
        
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """主函数"""
    print("Luna 实体徽章 MVP - 启动检查")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查摄像头
    try:
        import cv2
        import platform
        
        print("检查摄像头可用性...")
        
        # 在Mac上优先尝试AVFoundation后端
        if platform.system() == 'Darwin':
            print("  - 尝试AVFoundation后端...")
            cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            if cap.isOpened():
                print("✓ AVFoundation后端摄像头可用")
                cap.release()
            else:
                cap.release()
                print("  - 尝试默认后端...")
                cap = cv2.VideoCapture(0)
                if cap.isOpened():
                    print("✓ 默认后端摄像头可用")
                    cap.release()
                else:
                    cap.release()
                    print("  - 尝试备用摄像头索引...")
                    cap = cv2.VideoCapture(1)
                    if cap.isOpened():
                        print("✓ 备用摄像头可用")
                        cap.release()
                    else:
                        cap.release()
                        print("✗ 所有摄像头都不可用")
                        print("请检查:")
                        print("1. 摄像头是否已连接")
                        print("2. 摄像头是否被其他程序占用")
                        print("3. 系统权限设置（Mac需要摄像头权限）")
                        sys.exit(1)
        else:
            # 非Mac系统使用默认方式
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✓ 摄像头可用")
                cap.release()
            else:
                cap.release()
                print("✗ 摄像头不可用，请检查摄像头连接")
                sys.exit(1)
                
    except Exception as e:
        print(f"✗ 摄像头检查失败: {e}")
        sys.exit(1)
    
    print("✓ 所有检查通过，启动主程序...")
    print("=" * 40)
    
    # 启动主程序
    try:
        subprocess.run([sys.executable, "main.py"] + sys.argv[1:])
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()
