"""
TTS API 完整拆分版 (v1.2.0)
负责：/tts/generate, /tts/cache/stats
自动错误码上报，调用 services 层的 TTSEngine
"""

from flask import Blueprint, request
from core.response import ok, error
from core.logger import logger, log_error
from config.error_codes import ERR
from services.tts import get_tts_engine
from utils.logger import log_tts

tts_bp = Blueprint("tts", __name__, url_prefix="/tts")

# 初始化TTS引擎
tts_engine = get_tts_engine()


@tts_bp.route("/generate", methods=["POST"])
def generate_tts():
    """语音合成"""
    try:
        data = request.get_json() or {}
        text = data.get("text")
        style = data.get("style", "cheerful")
        voice = data.get("voice")  # 可选，覆盖style
        rate = data.get("rate")    # 可选，覆盖style
        
        if not text or not isinstance(text, str):
            return error(ERR.BAD_REQUEST, "text 字段缺失或格式错误", http_status=400)
        
        if not text.strip():
            return error(ERR.TTS_TEXT_EMPTY, "文本不能为空", http_status=400)
        
        try:
            # 使用TTS引擎合成
            audio_b64 = tts_engine.synthesize(
                text=text,
                style=style,
                voice=voice,
                rate=rate
            )
            
            # 记录成功日志
            log_tts("GENERATE_SUCCESS", {
                "text_len": len(text),
                "style": style,
                "voice": voice or "default",
                "rate": rate or "default"
            })
            
            return ok({
                "audio": audio_b64,
                "cached": False,  # TTSEngine内部会处理缓存
                "text_length": len(text),
                "style": style
            })
            
        except ValueError as e:
            return error(ERR.BAD_REQUEST, str(e), http_status=400)
        except ImportError as e:
            log_error(logger, ERR.TTS_ENGINE_ERROR, "TTS引擎未安装", {"exception": str(e)})
            return error(ERR.TTS_ENGINE_ERROR, "TTS引擎未安装", http_status=500)
        except Exception as e:
            log_error(logger, ERR.TTS_SYNTH_FAIL, "TTS合成失败", {"exception": str(e)})
            return error(ERR.TTS_SYNTH_FAIL, f"TTS合成失败: {str(e)}", http_status=500)
            
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "TTS生成异常", {"exception": str(e)})
        return error(ERR.INTERNAL_ERROR, f"服务器异常: {str(e)}", http_status=500)


@tts_bp.route("/cache/stats", methods=["GET"])
def cache_stats():
    """获取TTS缓存统计信息"""
    try:
        stats = tts_engine.cache.get_stats()
        return ok({"cache": stats})
    except Exception as e:
        log_error(logger, ERR.INTERNAL_ERROR, "获取缓存统计异常", {"exception": str(e)})
        return error(ERR.INTERNAL_ERROR, f"获取缓存失败: {str(e)}", http_status=500)


# ==================== 向后兼容的路由 ====================

@tts_bp.route("/api/tts", methods=["POST"])
def generate_tts_legacy():
    """语音合成（向后兼容）"""
    return generate_tts()


@tts_bp.route("/api/tts/cache/stats", methods=["GET"])
def cache_stats_legacy():
    """获取缓存统计（向后兼容）"""
    return cache_stats()
