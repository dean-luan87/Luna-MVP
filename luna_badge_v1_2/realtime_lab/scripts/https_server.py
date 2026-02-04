#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTPS 静态文件服务器（用于前端）

支持 iOS Safari 摄像头访问
"""

import http.server
import ssl
import sys
import os
from pathlib import Path

def run_https_server(port=8081, cert_file=None, key_file=None):
    """启动 HTTPS 静态文件服务器"""
    
    script_dir = Path(__file__).parent
    frontend_dir = script_dir.parent / "frontend"
    
    if not frontend_dir.exists():
        print(f"❌ 前端目录不存在: {frontend_dir}")
        return
    
    os.chdir(frontend_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    
    httpd = http.server.HTTPServer(("0.0.0.0", port), handler)
    
    if cert_file and key_file:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"[HTTPS] 启动 HTTPS 服务器: https://0.0.0.0:{port}")
    else:
        print(f"[HTTP] 启动 HTTP 服务器: http://0.0.0.0:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] 服务器已停止")
        httpd.shutdown()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    
    # 查找 SSL 证书
    script_dir = Path(__file__).parent
    ssl_dir = script_dir.parent / "ssl_certs"
    cert_file = ssl_dir / "cert.pem"
    key_file = ssl_dir / "key.pem"
    
    if cert_file.exists() and key_file.exists():
        run_https_server(port=port, cert_file=str(cert_file), key_file=str(key_file))
    else:
        print(f"[WARN] 未找到 SSL 证书，使用 HTTP 模式")
        print(f"[WARN] 运行 'bash scripts/generate_ssl_cert.sh' 生成证书")
        run_https_server(port=port)

