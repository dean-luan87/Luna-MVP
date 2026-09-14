"""
Luna Backend 主应用入口 (v1.2.0)
从web_test_server.py拆分出来的主启动文件
"""

import os
import socket
import logging
from core.factory import create_app

logger = logging.getLogger(__name__)

# 创建Flask应用
app = create_app()


@app.route("/ssl/cert.pem")
def download_cert():
    """下载证书文件"""
    from flask import send_file
    
    cert_path = os.path.join(os.path.dirname(__file__), 'ssl', 'cert.pem')
    if os.path.exists(cert_path):
        return send_file(
            cert_path,
            mimetype='application/x-x509-ca-cert',
            as_attachment=True,
            download_name='luna-cert.pem'
        )
    else:
        return "证书文件不存在", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9001))
    
    ssl_cert_path = os.path.join(os.path.dirname(__file__), 'ssl', 'cert.pem')
    ssl_key_path = os.path.join(os.path.dirname(__file__), 'ssl', 'key.pem')
    use_https = os.path.exists(ssl_cert_path) and os.path.exists(ssl_key_path)
    
    # 获取本机IP地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "localhost"
    
    logger.info("🚀 Luna 完整功能测试服务器启动中...")
    
    if use_https:
        logger.info(f"🔒 HTTPS模式已启用")
        logger.info(f"📱 手机访问地址: https://{local_ip}:{port}")
        logger.info(f"💻 本地访问地址: https://localhost:{port}")
        app.run(host='0.0.0.0', port=port, debug=False,
                ssl_context=(ssl_cert_path, ssl_key_path))
    else:
        logger.info(f"📱 手机访问地址: http://{local_ip}:{port}")
        logger.info(f"💻 本地访问地址: http://localhost:{port}")
        logger.warning("⚠️ HTTP模式：Safari浏览器无法使用摄像头/麦克风")
        app.run(host='0.0.0.0', port=port, debug=False)
