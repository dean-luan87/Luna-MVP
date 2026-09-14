"""
系统级路由 (v1.2.0)
性能监控 / 健康检查 / 错误码拉取
包含：/system/performance, /system/health, /system/errors
"""

from flask import Blueprint
from core.response import ok, error
from core.logger import logger, log_error
from config.error_codes import ERR
from utils.logger import system_log
import os
import json

system_bp = Blueprint("system", __name__, url_prefix="/system")


@system_bp.route("/performance", methods=["GET"])
def performance():
    """性能指标"""
    try:
        try:
            import psutil
            process = psutil.Process()
            mem_mb = round(process.memory_info().rss / 1024 / 1024, 2)
            cpu_percent = round(process.cpu_percent(interval=0.1), 2)
        except ImportError:
            mem_mb = 0
            cpu_percent = 0
        
        # 获取各模块性能指标
        metrics = {
            "memory_mb": mem_mb,
            "cpu_percent": cpu_percent
        }
        
        # 视觉模块指标
        try:
            from services.vision import get_vision_engine
            vision = get_vision_engine()
            if vision:
                vision_metrics = vision.get_metrics()
                metrics["vision"] = vision_metrics
        except:
            pass
        
        # TTS缓存统计
        try:
            from services.tts import get_tts_engine
            tts = get_tts_engine()
            if tts:
                metrics["tts_cache"] = tts.cache.get_stats()
        except:
            pass
        
        # 后期可加入 FPS / 延迟统计（此处预留接口）
        return ok(metrics)
        
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "获取性能指标异常", {"exception": str(e)})
        return error(ERR.INTERNAL_ERROR, f"获取性能指标失败: {str(e)}", http_status=500)


@system_bp.route("/health", methods=["GET"])
def health():
    """系统健康检查"""
    try:
        # 检查各个模块状态
        modules_status = {}
        
        # 视觉模块
        try:
            from services.vision import get_vision_engine
            vision = get_vision_engine()
            modules_status["vision"] = vision.is_ready() if vision else False
        except:
            modules_status["vision"] = False
        
        # TTS模块
        try:
            from services.tts import get_tts_engine
            tts = get_tts_engine()
            modules_status["tts"] = tts is not None
        except:
            modules_status["tts"] = False
        
        # 导航模块
        try:
            from services.navigation import get_navigation_manager
            nav = get_navigation_manager()
            modules_status["navigation"] = nav.manager is not None if nav else False
        except:
            modules_status["navigation"] = False
        
        # OCR模块（通过视觉引擎）
        modules_status["ocr"] = modules_status.get("vision", False)
        
        # 危险检测模块
        try:
            from services.navigation import get_hazard_detector
            hazard = get_hazard_detector()
            modules_status["hazard"] = hazard.detector is not None if hazard else False
        except:
            modules_status["hazard"] = False
        
        all_ready = all(modules_status.values())
        
        return ok({
            "status": "healthy" if all_ready else "degraded",
            "modules": modules_status,
            "version": "1.2.0"
        })
        
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "健康检查异常", {"exception": str(e)})
        return error(ERR.INTERNAL_ERROR, f"健康检查失败: {str(e)}", http_status=500)


@system_bp.route("/errors", methods=["GET"])
def list_errors():
    """展示最近的错误日志"""
    try:
        from utils.logger import ERROR_LOG_PATH
        
        log_path = ERROR_LOG_PATH
        
        if not os.path.exists(log_path):
            return ok({"errors": [], "message": "暂无错误日志"})
        
        # 读取最近200条错误日志
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-200:]
        
        logs = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                log_entry = json.loads(line)
                # 只返回错误相关的日志
                if log_entry.get("error_code") is not None:
                    logs.append(log_entry)
            except:
                pass
        
        # 按时间戳倒序排列（最新的在前）
        logs.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        
        return ok({
            "errors": logs[:100],  # 最多返回100条
            "total": len(logs),
            "log_file": log_path
        })
        
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "获取错误日志异常", {"exception": str(e)})
        return error(ERR.INTERNAL_ERROR, f"获取错误日志失败: {str(e)}", http_status=500)


@system_bp.route("/ssl/cert.pem", methods=["GET"])
def download_cert():
    """下载SSL证书文件"""
    try:
        cert_path = os.path.join(os.path.dirname(__file__), "..", "ssl", "cert.pem")
        if os.path.exists(cert_path):
            from flask import send_file
            return send_file(
                cert_path,
                mimetype="application/x-x509-ca-cert",
                as_attachment=True,
                download_name="luna-cert.pem"
            )
        else:
            return error(ERR.SYS_SSL_LOAD_FAILED, "证书文件不存在", http_status=404)
    except Exception as e:
        log_error(logger, ERR.SYS_SSL_LOAD_FAILED, "下载证书异常", {"exception": str(e)})
        return error(ERR.SYS_SSL_LOAD_FAILED, f"下载证书失败: {str(e)}", http_status=500)


# ==================== 向后兼容的路由 ====================

@system_bp.route("/api/health", methods=["GET"])
def health_legacy():
    """健康检查（向后兼容）"""
    return health()


@system_bp.route("/api/performance/metrics", methods=["GET"])
def performance_legacy():
    """性能指标（向后兼容）"""
    return performance()
