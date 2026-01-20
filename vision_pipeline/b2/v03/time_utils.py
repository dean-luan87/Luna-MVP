# vision_pipeline/b2/v03/time_utils.py
from __future__ import annotations

def format_video_time(seconds: float) -> str:
    """
    将视频时间（秒，float）格式化为 mm:ss.xx
    用于日志、人类对照、截图命名
    """
    if seconds is None:
        seconds = 0.0
    if seconds < 0:
        seconds = 0.0

    minutes = int(seconds // 60)
    remain = seconds - minutes * 60
    return f"{minutes:02d}:{remain:05.2f}"


def clamp(v: float, lo: float, hi: float) -> float:
    """
    通用裁剪工具，防止时间/分数越界
    """
    return max(lo, min(hi, v))


def frame_to_video_time(frame_idx: int, fps: float) -> float:
    """
    B2 内部标准时间定义：
        t_video = frame_idx / fps
    """
    if fps <= 0:
        return 0.0
    return frame_idx / fps


def window_range(
    now_t: float,
    start_offset: float = 1.0,
    end_offset: float = 8.0,
) -> tuple[float, float]:
    """
    B2 v0.3 默认验证窗口定义：
        [now + 1s , now + 8s]

    注意：这是"未来窗口"，不是"8 秒之后"
    """
    start = now_t + start_offset
    end = now_t + end_offset
    if end < start:
        end = start
    return start, end

