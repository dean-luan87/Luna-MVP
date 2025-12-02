"""
性能指标路由 (v1.2.0)
包含: /api/performance/metrics 等
"""

from flask import Blueprint, jsonify
from core.response import api_success, api_error, api_exception
from core.logger import logger, log_error
from config.error_codes import ERR

metrics_bp = Blueprint("metrics", __name__)


def get_performance_metrics():
    """获取性能指标字典"""
    from flask import current_app
    return current_app.extensions.get("performance_metrics", {})


def get_graceful_degrader():
    """获取优雅降级器实例"""
    from flask import current_app
    return current_app.extensions.get("graceful_degrader")


@metrics_bp.route("/api/performance/metrics", methods=["GET"])
def get_performance_metrics_route():
    """获取性能指标"""
    try:
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
        except:
            memory_mb = 0
        
        # 计算延迟统计
        performance_metrics = get_performance_metrics()
        vision_latencies = performance_metrics.get("vision_latency", [])
        audio_latencies = performance_metrics.get("audio_latency", [])
        
        def calc_stats(latencies):
            if not latencies:
                return {"avg": 0, "p95": 0, "p99": 0, "min": 0, "max": 0, "count": 0}
            
            sorted_latencies = sorted(latencies[-100:])  # 最近100次
            count = len(sorted_latencies)
            avg = sum(sorted_latencies) / count if count > 0 else 0
            p95_index = int(count * 0.95)
            p99_index = int(count * 0.99)
            
            return {
                "avg": round(avg, 2),
                "p95": round(sorted_latencies[p95_index] if p95_index < count else 0, 2),
                "p99": round(sorted_latencies[p99_index] if p99_index < count else 0, 2),
                "min": round(sorted_latencies[0] if count > 0 else 0, 2),
                "max": round(sorted_latencies[-1] if count > 0 else 0, 2),
                "count": count
            }
        
        vision_stats = calc_stats(vision_latencies)
        audio_stats = calc_stats(audio_latencies)
        
        # 计算FPS
        fps_history = performance_metrics.get("fps", [])
        current_fps = fps_history[-1] if fps_history else 0
        avg_fps = sum(fps_history[-30:]) / len(fps_history[-30:]) if fps_history else 0
        
        graceful_degrader = get_graceful_degrader()
        degrade_level = graceful_degrader.current_level.value if graceful_degrader else "normal"
        
        return jsonify({
            "success": True,
            "metrics": {
                "memory_mb": round(memory_mb, 2),
                "vision": vision_stats,
                "audio": audio_stats,
                "fps": {
                    "current": round(current_fps, 1),
                    "average": round(avg_fps, 1)
                },
                "degrade_level": degrade_level
            }
        })
    except Exception as e:
        log_error(logger, ERR.PERF_STATS_ERROR, "获取性能指标失败", {"exception": str(e)})
        return api_exception(e, ERR.PERF_STATS_ERROR)



