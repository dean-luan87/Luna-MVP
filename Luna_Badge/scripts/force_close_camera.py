#!/usr/bin/env python3
"""
强制关闭摄像头脚本
用于紧急情况下关闭所有摄像头资源
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def force_close_all_cameras():
    """强制关闭所有摄像头"""
    try:
        # 尝试关闭所有OpenCV窗口
        cv2.destroyAllWindows()
        logger.info("✅ OpenCV窗口已关闭")
        
        # 尝试释放摄像头（最多尝试10个设备号）
        for i in range(10):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    cap.release()
                    logger.info(f"✅ 摄像头设备 {i} 已释放")
            except Exception as e:
                pass
        
        # 尝试使用摄像头管理器关闭
        try:
            from core.camera_manager import get_camera_manager
            camera_manager = get_camera_manager()
            if camera_manager.state.is_open:
                camera_manager.close_camera()
                logger.info("✅ 摄像头管理器已关闭摄像头")
        except Exception as e:
            logger.debug(f"摄像头管理器关闭失败: {e}")
        
        logger.info("🎉 所有摄像头资源清理完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 关闭摄像头失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("🛑 强制关闭摄像头")
    print("=" * 70)
    
    success = force_close_all_cameras()
    
    if success:
        print("✅ 摄像头关闭成功")
    else:
        print("❌ 摄像头关闭失败")
    
    print("=" * 70)

