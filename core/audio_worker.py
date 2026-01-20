# -*- coding: utf-8 -*-
"""
音频播放工作线程（Audio Worker）

目标：音频播放必须彻底脱离主循环线程
策略：主循环永远不能等音频

关键原则：
- 允许漏播（队列满时丢弃）
- 允许延迟（异步播放）
- ❌ 不允许卡顿（不阻塞主循环）
- ❌ 不允许杂音（单一播放线程）
- ❌ 不允许重建风暴（不重初始化）
"""

import threading
import queue
import logging
import time

logger = logging.getLogger(__name__)

# 音频播放队列（最大容量 1，测试期策略：宁可漏播，不可积压）
audio_queue = queue.Queue(maxsize=1)

# 音频工作线程状态
_audio_worker_running = False
_audio_worker_thread = None
_audio_worker_lock = threading.Lock()


def audio_worker_loop():
    """
    音频工作线程主循环
    
    从队列中取出音频任务并播放
    阻塞 OK，但只阻塞这个独立线程，不影响主循环
    """
    global _audio_worker_running
    
    logger.info("[AudioWorker] 音频工作线程已启动")
    _audio_worker_running = True
    
    while _audio_worker_running:
        try:
            # 从队列中获取任务（阻塞等待，但只阻塞这个线程）
            item = audio_queue.get(timeout=1.0)
            if item is None:  # 停止信号
                break
            
            text, tts_engine = item
            
            try:
                logger.debug(f"[AudioWorker] 开始播放: {text[:50]}...")
                # 阻塞 OK，但只阻塞这里，不影响主循环
                success = tts_engine.speak(text)
                if success:
                    logger.debug(f"[AudioWorker] 播放已启动: {text[:50]}...")
                else:
                    logger.debug(f"[AudioWorker] 播放启动失败（已忽略）")
            except Exception as e:
                # 播放失败，只记录，不重初始化，不抛异常
                logger.debug(f"[AudioWorker] 播放异常（已忽略）: {e}")
            finally:
                audio_queue.task_done()
                
        except queue.Empty:
            # 超时，继续循环
            continue
        except Exception as e:
            logger.error(f"[AudioWorker] 工作线程异常: {e}", exc_info=True)
            time.sleep(0.1)  # 避免异常风暴
    
    logger.info("[AudioWorker] 音频工作线程已停止")
    _audio_worker_running = False


def start_audio_worker():
    """启动音频工作线程"""
    global _audio_worker_thread, _audio_worker_running
    
    with _audio_worker_lock:
        if _audio_worker_thread is not None and _audio_worker_thread.is_alive():
            logger.debug("[AudioWorker] 音频工作线程已在运行")
            return
        
        _audio_worker_thread = threading.Thread(
            target=audio_worker_loop,
            name="AudioWorker",
            daemon=True  # 守护线程，主程序退出时自动退出
        )
        _audio_worker_thread.start()
        logger.info("[AudioWorker] 音频工作线程已启动")


def stop_audio_worker():
    """停止音频工作线程"""
    global _audio_worker_running, _audio_worker_thread
    
    with _audio_worker_lock:
        if not _audio_worker_running:
            return
        
        _audio_worker_running = False
        
        # 发送停止信号
        try:
            audio_queue.put_nowait(None)
        except queue.Full:
            pass  # 队列满，直接停止
        
        if _audio_worker_thread is not None:
            _audio_worker_thread.join(timeout=2.0)
            logger.info("[AudioWorker] 音频工作线程已停止")


def submit_tts(text: str, tts_engine) -> bool:
    """
    投递 TTS 播放任务到音频工作线程
    
    关键原则：
    - 不等待
    - 不阻塞
    - 不判断 is_speaking
    - 不重建 TTS
    - 队列满时直接丢弃（测试期允许漏播）
    
    Args:
        text: 要播放的文本
        tts_engine: TTS 引擎实例（Voice 对象）
    
    Returns:
        bool: 是否成功投递（False 表示队列满，已丢弃）
    """
    if not text or not text.strip():
        return False
    
    if tts_engine is None:
        logger.debug("[AudioWorker] TTS 引擎未初始化，跳过")
        return False
    
    # 确保工作线程已启动
    if not _audio_worker_running:
        start_audio_worker()
    
    try:
        # 非阻塞投递
        audio_queue.put_nowait((text, tts_engine))
        logger.debug(f"[AudioWorker] 已投递播放任务: {text[:30]}...")
        return True
    except queue.Full:
        # 队列满，直接丢弃（测试期策略：宁可漏播，不可积压）
        logger.debug(f"[AudioWorker] 队列已满，丢弃播放任务: {text[:30]}...")
        return False
    except Exception as e:
        logger.debug(f"[AudioWorker] 投递失败（已忽略）: {e}")
        return False


def is_audio_worker_running() -> bool:
    """检查音频工作线程是否在运行"""
    return _audio_worker_running


def get_queue_size() -> int:
    """获取队列当前大小（用于调试）"""
    return audio_queue.qsize()


