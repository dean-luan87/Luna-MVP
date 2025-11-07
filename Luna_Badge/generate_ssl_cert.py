#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成SSL证书脚本
用于启用HTTPS支持，让Safari浏览器可以访问摄像头和麦克风
"""

import os
import subprocess
import sys

def generate_ssl_cert():
    """生成自签名SSL证书"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ssl_dir = os.path.join(script_dir, 'ssl')
    
    # 创建ssl目录
    os.makedirs(ssl_dir, exist_ok=True)
    
    cert_path = os.path.join(ssl_dir, 'cert.pem')
    key_path = os.path.join(ssl_dir, 'key.pem')
    
    # 获取本机IP地址
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "192.168.3.213"
    
    print("=" * 60)
    print("🔒 生成SSL证书")
    print("=" * 60)
    print(f"📱 本机IP地址: {local_ip}")
    print(f"📁 证书保存位置: {ssl_dir}")
    print()
    
    # 检查是否已存在证书
    if os.path.exists(cert_path) and os.path.exists(key_path):
        response = input("证书已存在，是否重新生成？(y/N): ")
        if response.lower() != 'y':
            print("✅ 使用现有证书")
            return
    
    # 生成证书
    print("正在生成SSL证书...")
    try:
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
            '-nodes', '-out', cert_path, '-keyout', key_path,
            '-days', '365',
            '-subj', f'/C=CN/ST=State/L=City/O=Luna/CN={local_ip}'
        ], check=True, capture_output=True)
        
        print("✅ SSL证书生成成功！")
        print()
        print("=" * 60)
        print("📱 在iPhone上信任证书的步骤：")
        print("=" * 60)
        print("1. 在Safari中访问: https://" + local_ip + ":5001")
        print("2. 点击地址栏的锁图标")
        print("3. 点击'显示详细信息'")
        print("4. 点击'访问此网站'")
        print("5. 在设置 > 通用 > 关于本机 > 证书信任设置中")
        print("   找到并信任 'Luna' 证书")
        print("=" * 60)
        print()
        print("✅ 现在可以重启服务器使用HTTPS了")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 证书生成失败: {e}")
        print("请确保已安装OpenSSL: brew install openssl")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 未找到openssl命令")
        print("请安装OpenSSL:")
        print("  macOS: brew install openssl")
        print("  Linux: sudo apt-get install openssl")
        sys.exit(1)

if __name__ == '__main__':
    generate_ssl_cert()

