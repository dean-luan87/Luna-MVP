#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摄像头权限检查和诊断工具
"""

import cv2
import platform
import subprocess
import sys

def check_camera_permissions():
    """检查Mac摄像头权限"""
    if platform.system() != 'Darwin':
        return True, "非Mac系统，跳过权限检查"
    
    try:
        # 检查摄像头权限
        result = subprocess.run([
            'system_profiler', 'SPCameraDataType'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            return True, "检测到摄像头设备"
        else:
            return False, "未检测到摄像头设备"
            
    except Exception as e:
        return False, f"权限检查失败: {e}"

def test_camera_access():
    """测试摄像头访问"""
    print("测试摄像头访问...")
    
    # 测试不同的后端和索引
    test_configs = [
        (0, cv2.CAP_AVFOUNDATION, "AVFoundation后端，索引0"),
        (0, cv2.CAP_ANY, "默认后端，索引0"),
        (1, cv2.CAP_AVFOUNDATION, "AVFoundation后端，索引1"),
        (1, cv2.CAP_ANY, "默认后端，索引1"),
    ]
    
    for index, backend, description in test_configs:
        print(f"  测试: {description}")
        try:
            cap = cv2.VideoCapture(index, backend)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"  ✓ 成功: {description}")
                    cap.release()
                    return True, description
                else:
                    print(f"  ✗ 无法读取帧: {description}")
            else:
                print(f"  ✗ 无法打开: {description}")
            cap.release()
        except Exception as e:
            print(f"  ✗ 异常: {description} - {e}")
    
    return False, "所有测试都失败"

def main():
    """主函数"""
    print("Luna 实体徽章 MVP - 摄像头诊断工具")
    print("=" * 50)
    
    # 检查系统信息
    print(f"操作系统: {platform.system()}")
    print(f"OpenCV版本: {cv2.__version__}")
    
    # 检查权限
    has_permission, permission_msg = check_camera_permissions()
    print(f"权限检查: {permission_msg}")
    
    if not has_permission:
        print("\n⚠️ 摄像头权限问题:")
        print("1. 打开 系统偏好设置 > 安全性与隐私 > 隐私")
        print("2. 选择 摄像头 选项")
        print("3. 确保 Terminal 或 Python 应用有摄像头权限")
        print("4. 重启终端后再次运行")
        return False
    
    # 测试摄像头访问
    success, working_config = test_camera_access()
    
    if success:
        print(f"\n✓ 摄像头工作正常: {working_config}")
        print("可以运行主程序了！")
        return True
    else:
        print("\n✗ 摄像头访问失败")
        print("\n可能的解决方案:")
        print("1. 确保摄像头没有被其他应用占用")
        print("2. 重启电脑")
        print("3. 检查摄像头硬件连接")
        print("4. 更新OpenCV: pip install --upgrade opencv-python")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

