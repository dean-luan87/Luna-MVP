#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna 识路测试服务器启动脚本
"""

import os
import sys
import subprocess

def check_dependencies():
    """检查依赖"""
    required = ['flask', 'flask-cors']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print(f"请运行: pip install {' '.join(missing)}")
        return False
    
    return True

def get_local_ip():
    """获取本机IP地址"""
    import socket
    try:
        # 连接到一个远程地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    print("=" * 60)
    print("🌟 Luna 识路测试服务器")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 获取IP地址
    local_ip = get_local_ip()
    port = 5000
    
    print(f"\n📱 手机访问地址: http://{local_ip}:{port}")
    print(f"💻 本地访问地址: http://localhost:{port}")
    print("\n⚠️  确保手机和Mac在同一WiFi网络下")
    print("\n按 Ctrl+C 停止服务器\n")
    
    # 切换到Luna_Badge目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 启动服务器
    try:
        subprocess.run([sys.executable, 'web_test_server.py'])
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")

if __name__ == '__main__':
    main()

