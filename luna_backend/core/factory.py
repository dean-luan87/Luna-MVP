"""
应用工厂 (Application Factory) v1.2.0
创建Flask应用，注册所有蓝图
"""

from flask import Flask
from bootstrap import init_all_modules

# 延迟导入蓝图以避免循环依赖
def _register_blueprints(app: Flask):
    """注册所有蓝图"""
    try:
        from routes.ui_routes import ui_bp
        app.register_blueprint(ui_bp)
    except ImportError as e:
        print(f"⚠️ 无法导入ui_routes: {e}")
    
    try:
        from routes.visual_routes import visual_bp
        app.register_blueprint(visual_bp, url_prefix="/api")
    except ImportError as e:
        print(f"⚠️ 无法导入visual_routes: {e}")
    
    try:
        from routes.navigation_routes import nav_bp
        app.register_blueprint(nav_bp, url_prefix="/api/navigation")
    except ImportError as e:
        print(f"⚠️ 无法导入navigation_routes: {e}")
    
    # 导航路由v4（从web_test_server拆分）
    try:
        from routes.navigation_routes_v4 import nav_bp as nav_bp_v4
        app.register_blueprint(nav_bp_v4, url_prefix="/api/navigation")
    except ImportError as e:
        print(f"⚠️ 无法导入navigation_routes_v4: {e}")
    
    try:
        from routes.voice_routes import voice_bp
        app.register_blueprint(voice_bp, url_prefix="/api")
    except ImportError as e:
        print(f"⚠️ 无法导入voice_routes: {e}")
    
    try:
        from routes.map_routes import map_bp
        app.register_blueprint(map_bp, url_prefix="/api")
    except ImportError as e:
        print(f"⚠️ 无法导入map_routes: {e}")
    
    try:
        from routes.system_routes import system_bp
        app.register_blueprint(system_bp, url_prefix="/api")
    except ImportError as e:
        print(f"⚠️ 无法导入system_routes: {e}")
    
    try:
        from routes.hospital_routes import hospital_bp
        app.register_blueprint(hospital_bp, url_prefix="/api/hospital")
    except ImportError as e:
        print(f"⚠️ 无法导入hospital_routes: {e}")
    
    # 测试路由（测试中心）
    try:
        from routes.test_routes import test_bp
        app.register_blueprint(test_bp)  # url_prefix已在test_routes.py中定义
    except ImportError as e:
        print(f"⚠️ 无法导入test_routes: {e}")
    
    # 视觉路由（backend版本）
    try:
        from backend.routes.vision_routes import bp_vision, init_vision_routes
        # 注意：init_vision_routes需要在有detector实例后调用
        app.register_blueprint(bp_vision)
    except ImportError as e:
        print(f"⚠️ 无法导入backend.routes.vision_routes: {e}")


def create_app() -> Flask:
    """
    创建Flask应用
    
    Returns:
        Flask应用实例
    """
    app = Flask(__name__)
    
    # 初始化所有模块（vision_engine等）
    init_result = init_all_modules()
    app.config['INIT_RESULT'] = init_result
    
    # 注册蓝图
    _register_blueprints(app)
    
    return app

