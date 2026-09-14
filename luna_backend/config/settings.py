"""
Luna Badge 配置管理 (v1.2.0)
"""

import os
from typing import Optional

class Settings:
    """应用配置"""
    
    # Flask配置
    DEBUG = os.getenv('LUNA_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('LUNA_HOST', '0.0.0.0')
    PORT = int(os.getenv('LUNA_PORT', '9001'))
    
    # SSL配置
    SSL_CERT_PATH = os.path.join(os.path.dirname(__file__), '..', 'ssl', 'cert.pem')
    SSL_KEY_PATH = os.path.join(os.path.dirname(__file__), '..', 'ssl', 'key.pem')
    USE_HTTPS = os.path.exists(SSL_CERT_PATH) and os.path.exists(SSL_KEY_PATH)
    
    # 静态文件配置
    STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static')
    FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'Luna_Badge', 'frontend')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LUNA_LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_local_ip(cls) -> str:
        """获取本机IP地址"""
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"

# 全局配置实例
settings = Settings()



