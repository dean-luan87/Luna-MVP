"""
缓存管理路由 (v1.2.0)
统一管理所有缓存：图像 / TTS / 路径 / 临时文件
"""

from flask import Blueprint
from core.response import ok, error
from core.logger import logger, log_error
from config.error_codes import ERR
import shutil
import os

cache_bp = Blueprint("cache", __name__, url_prefix="/cache")


@cache_bp.route("/clear_all", methods=["POST"])
def clear_all():
    """统一清空所有缓存"""
    try:
        # 获取项目根目录
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        folders = [
            os.path.join(project_root, "tts_cache"),
            os.path.join(project_root, "cache", "tts"),
            os.path.join(project_root, "cache", "vision"),
            os.path.join(project_root, "cache", "temp"),
            os.path.join(project_root, "luna_backend", "tts_cache"),
        ]
        
        cleared_folders = []
        total_size = 0
        
        for folder in folders:
            if os.path.exists(folder):
                try:
                    # 计算文件夹大小
                    folder_size = sum(
                        os.path.getsize(os.path.join(dirpath, filename))
                        for dirpath, dirnames, filenames in os.walk(folder)
                        for filename in filenames
                    )
                    total_size += folder_size
                    
                    # 删除文件夹
                    shutil.rmtree(folder, ignore_errors=True)
                    cleared_folders.append(folder)
                    logger.info(f"已清空缓存目录: {folder}", module="System")
                except Exception as e:
                    logger.warn(f"清空缓存目录失败: {folder}", details={"error": str(e)}, module="System")
        
        # 记录日志
        from utils.logger import system_log
        system_log("CACHE_CLEAR_ALL", {
            "cleared_folders": cleared_folders,
            "total_size_mb": round(total_size / 1024 / 1024, 2)
        })
        
        return ok({
            "message": "所有缓存已清空",
            "cleared_folders": cleared_folders,
            "total_size_mb": round(total_size / 1024 / 1024, 2)
        })
        
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "清空缓存异常", {"exception": str(e)})
        return error(ERR.INTERNAL_ERROR, f"清空缓存失败: {str(e)}", http_status=500)


@cache_bp.route("/stats", methods=["GET"])
def cache_stats():
    """获取所有缓存统计信息"""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        stats = {}
        
        # TTS缓存统计
        try:
            from services.tts import get_tts_engine
            tts = get_tts_engine()
            if tts:
                stats["tts"] = tts.cache.get_stats()
        except:
            stats["tts"] = {"count": 0, "total_size_bytes": 0, "total_size_mb": 0}
        
        # 视觉缓存统计（预留）
        stats["vision"] = {"count": 0, "total_size_bytes": 0, "total_size_mb": 0}
        
        # 临时文件统计（预留）
        stats["temp"] = {"count": 0, "total_size_bytes": 0, "total_size_mb": 0}
        
        # 计算总计
        total_count = sum(s.get("count", 0) for s in stats.values())
        total_size_bytes = sum(s.get("total_size_bytes", 0) for s in stats.values())
        
        stats["total"] = {
            "count": total_count,
            "total_size_bytes": total_size_bytes,
            "total_size_mb": round(total_size_bytes / 1024 / 1024, 2)
        }
        
        return ok(stats)
        
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "获取缓存统计异常", {"exception": str(e)})
        return error(ERR.INTERNAL_ERROR, f"获取缓存统计失败: {str(e)}", http_status=500)


@cache_bp.route("/clear/<cache_type>", methods=["POST"])
def clear_cache_type(cache_type: str):
    """清空指定类型的缓存"""
    try:
        cleared = False
        
        if cache_type == "tts":
            # 清空TTS缓存
            try:
                from services.tts import get_tts_engine
                tts = get_tts_engine()
                if tts:
                    cache_dir = tts.cache.cache_dir
                    if os.path.exists(cache_dir):
                        shutil.rmtree(cache_dir, ignore_errors=True)
                        os.makedirs(cache_dir, exist_ok=True)
                        cleared = True
            except:
                pass
        
        elif cache_type == "vision":
            # 清空视觉缓存（预留）
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            vision_cache = os.path.join(project_root, "cache", "vision")
            if os.path.exists(vision_cache):
                shutil.rmtree(vision_cache, ignore_errors=True)
                cleared = True
        
        elif cache_type == "temp":
            # 清空临时文件（预留）
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            temp_cache = os.path.join(project_root, "cache", "temp")
            if os.path.exists(temp_cache):
                shutil.rmtree(temp_cache, ignore_errors=True)
                cleared = True
        
        else:
            return error(ERR.BAD_REQUEST, f"不支持的缓存类型: {cache_type}", http_status=400)
        
        if cleared:
            from utils.logger import system_log
            system_log("CACHE_CLEAR", {"cache_type": cache_type})
            return ok({"message": f"{cache_type}缓存已清空"})
        else:
            return ok({"message": f"{cache_type}缓存不存在或已为空"})
        
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "清空缓存异常", {"exception": str(e), "cache_type": cache_type})
        return error(ERR.INTERNAL_ERROR, f"清空缓存失败: {str(e)}", http_status=500)



