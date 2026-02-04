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
    
    # 判断是否为视频文件模式（--video 后跟有效路径则跳过摄像头检查）
    use_video = False
    if "--video" in sys.argv:
        try:
            idx = sys.argv.index("--video")
            if idx + 1 < len(sys.argv) and sys.argv[idx + 1].strip() and not sys.argv[idx + 1].startswith("-"):
                use_video = True
                print("✓ 使用视频文件模式，跳过摄像头检查")
        except (ValueError, IndexError):
            pass

    if not use_video:
        # 检查摄像头（显式索引，不允许 fallback）
        try:
            import cv2
            import platform

            print("检查摄像头可用性...")

            camera_index = int(os.environ.get("CAMERA_INDEX", "0"))
            if "--camera-index" in sys.argv:
                try:
                    idx = sys.argv.index("--camera-index")
                    if idx + 1 < len(sys.argv):
                        camera_index = int(sys.argv[idx + 1])
                except (ValueError, IndexError):
                    pass
            camera_backend = os.environ.get("CAMERA_BACKEND", "avfoundation" if platform.system() == "Darwin" else "default")

            if platform.system() == 'Darwin':
                backend_desc = "AVFoundation" if camera_backend == "avfoundation" else "默认后端"
                print(f"  - 使用{backend_desc}，索引={camera_index}...")
                if camera_backend == "avfoundation":
                    cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
                else:
                    cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    print("✓ 摄像头可用")
                    cap.release()
                else:
                    cap.release()
                    print("✗ 摄像头不可用")
                    print("请检查:")
                    print("1. 摄像头是否已连接")
                    print("2. 摄像头是否被其他程序占用")
                    print("3. 系统权限设置（Mac需要摄像头权限）")
                    print("4. CAMERA_INDEX / CAMERA_BACKEND 配置是否正确")
                    sys.exit(1)
            else:
                cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    print("✓ 摄像头可用")
                    cap.release()
                else:
                    cap.release()
                    print("✗ 摄像头不可用，请检查摄像头连接或 CAMERA_INDEX 配置")
                    sys.exit(1)

        except Exception as e:
            print(f"✗ 摄像头检查失败: {e}")
            sys.exit(1)
    
    print("✓ 所有检查通过，启动主程序...")
    print("=" * 40)
    
    # 保证在项目根目录运行 main.py，避免从其他目录执行时找不到 main.py 或相对路径视频
    project_root = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(project_root, "main.py")
    if not os.path.isfile(main_py):
        print(f"✗ 未找到主程序: {main_py}")
        sys.exit(1)
    # 若 --video 给的是相对路径，转为基于项目根的绝对路径，便于 cwd=project_root 时能找到
    argv = list(sys.argv[1:])
    if "--video" in argv:
        try:
            idx = argv.index("--video")
            if idx + 1 < len(argv) and argv[idx + 1].strip() and not argv[idx + 1].startswith("-"):
                v = argv[idx + 1]
                if not os.path.isabs(v) and not os.path.isfile(v):
                    abs_v = os.path.join(project_root, v)
                    if os.path.isfile(abs_v):
                        argv[idx + 1] = abs_v
        except (ValueError, IndexError):
            pass
    # 启动主程序（cwd=项目根，方便相对路径资源）
    try:
        subprocess.run([sys.executable, main_py] + argv, cwd=project_root)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()
