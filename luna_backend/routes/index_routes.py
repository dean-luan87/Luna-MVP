"""
首页和静态文件路由 (v1.2.0)
包含: /, /frontend/<path:filename>
"""

from flask import Blueprint, send_file, send_from_directory, render_template_string
import os

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def index():
    """首页 - 返回HTML模板"""
    # TODO: 从文件读取HTML模板，而不是硬编码
    # 暂时保持原逻辑，后续可以改为从文件读取
    html_template_path = os.path.join(os.path.dirname(__file__), "..", "..", "Luna_Badge", "web_test_server.py")
    
    # 如果HTML模板已提取到独立文件，使用：
    # frontend_html_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    # if os.path.exists(frontend_html_path):
    #     return send_file(frontend_html_path)
    
    # 临时方案：从web_test_server.py读取HTML_TEMPLATE
    # 后续应该将HTML_TEMPLATE提取到独立文件
    try:
        # 尝试从原文件读取（过渡期）
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "Luna_Badge"))
        from web_test_server import HTML_TEMPLATE
        return render_template_string(HTML_TEMPLATE)
    except:
        # 如果读取失败，返回简单提示
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Luna Backend</title></head>
        <body>
            <h1>Luna Backend v1.2.0</h1>
            <p>请将HTML模板迁移到 frontend/index.html</p>
        </body>
        </html>
        """


@index_bp.route("/frontend/<path:filename>")
def frontend_static(filename):
    """提供前端静态文件"""
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "Luna_Badge", "frontend")
    file_path = os.path.join(frontend_dir, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return f"File not found: {filename}", 404



