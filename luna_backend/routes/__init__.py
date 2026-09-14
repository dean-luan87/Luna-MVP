"""
Luna Backend 路由模块
统一注册所有Blueprint
"""

from flask import Flask
from . import index_routes, visual_routes, navigation_routes, tts_routes, system_routes, cache_routes

def register_routes(app: Flask):
    """注册所有路由Blueprint"""
    # 首页和静态文件
    app.register_blueprint(index_routes.index_bp)
    
    # 视觉路由 (/visual/*)
    app.register_blueprint(visual_routes.visual_bp)
    
    # 导航路由 (/navigation/*) - 旧版路由
    app.register_blueprint(navigation_routes.nav_bp)
    
    # 导航路由 (/api/navigation/*) - 新版路由（v2.0）
    try:
        from .navigation_routes_v2 import navigation_bp as nav_bp_v2
        app.register_blueprint(nav_bp_v2)
    except ImportError:
        pass
    
    # 导航路由 (/nav/*) - 策略引擎集成版（v3.0）
    try:
        from .navigation_routes_v3 import nav_bp as nav_bp_v3
        app.register_blueprint(nav_bp_v3)
    except ImportError:
        pass
    
    # 导航路由 (/api/navigation/*) - 从web_test_server拆分版（v4.0）
    try:
        from .navigation_routes_v4 import nav_bp as nav_bp_v4
        app.register_blueprint(nav_bp_v4)
    except ImportError:
        pass
    
    # 地图路由 (/api/map/*)
    try:
        from .map_routes import map_bp
        app.register_blueprint(map_bp)
    except ImportError:
        pass
    
    # 医院路由 (/api/hospital/*)
    try:
        from .hospital_routes import hospital_bp
        app.register_blueprint(hospital_bp)
    except ImportError:
        pass
    
    # 如果以上都不存在，使用旧版
    try:
        from .navigation_routes import navigation_bp
        app.register_blueprint(navigation_bp)
    except ImportError:
        pass
    
    # TTS路由 (/tts/*)
    app.register_blueprint(tts_routes.tts_bp)
    
    # 系统路由 (/system/*) - 包含健康检查、性能指标、错误日志、SSL证书
    app.register_blueprint(system_routes.system_bp)
    
    # 缓存路由 (/cache/*) - 缓存管理
    app.register_blueprint(cache_routes.cache_bp)
