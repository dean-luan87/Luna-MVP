"""
摄像头资源泄漏修复方案
问题分析：
1. AI导航模块直接使用cv2.VideoCapture(0)打开摄像头
2. 主程序关闭时，AI导航模块的摄像头资源没有被正确清理
3. 即使调用了cleanup()，OpenCV的摄像头资源仍然可以被访问

解决方案：
1. 确保AI导航模块的摄像头资源在系统关闭时被正确释放
2. 添加强制摄像头释放机制
3. 在系统关闭时检查并清理所有摄像头资源
"""

import cv2
import time
import threading
import subprocess
import os
import signal
from typing import List, Optional

class CameraResourceManager:
    """摄像头资源管理器"""
    
    def __init__(self):
        self.active_cameras: List[cv2.VideoCapture] = []
        self.camera_threads: List[threading.Thread] = []
        self.cleanup_lock = threading.Lock()
    
    def register_camera(self, camera: cv2.VideoCapture):
        """注册摄像头资源"""
        with self.cleanup_lock:
            self.active_cameras.append(camera)
    
    def unregister_camera(self, camera: cv2.VideoCapture):
        """注销摄像头资源"""
        with self.cleanup_lock:
            if camera in self.active_cameras:
                self.active_cameras.remove(camera)
    
    def force_cleanup_all(self):
        """强制清理所有摄像头资源"""
        print("🔧 强制清理所有摄像头资源...")
        
        with self.cleanup_lock:
            # 1. 释放所有注册的摄像头
            for camera in self.active_cameras[:]:
                try:
                    if camera and camera.isOpened():
                        camera.release()
                        print(f"   ✅ 释放摄像头: {id(camera)}")
                except Exception as e:
                    print(f"   ⚠️ 释放摄像头失败: {e}")
                finally:
                    self.active_cameras.remove(camera)
            
            # 2. 销毁所有OpenCV窗口
            try:
                cv2.destroyAllWindows()
                print("   ✅ 销毁所有OpenCV窗口")
            except Exception as e:
                print(f"   ⚠️ 销毁窗口失败: {e}")
            
            # 3. 等待一小段时间让资源释放
            time.sleep(0.1)
            
            # 4. 强制垃圾回收
            import gc
            gc.collect()
            print("   ✅ 执行垃圾回收")
    
    def check_camera_status(self) -> bool:
        """检查摄像头是否仍可访问"""
        try:
            test_camera = cv2.VideoCapture(0)
            if test_camera.isOpened():
                test_camera.release()
                return True
            return False
        except Exception:
            return False
    
    def kill_camera_processes(self):
        """终止摄像头相关进程"""
        print("🔧 终止摄像头相关进程...")
        
        try:
            # 查找Python摄像头进程
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            camera_processes = []
            for line in lines:
                if 'python' in line and any(keyword in line.lower() for keyword in ['camera', 'opencv', 'cv2', 'main_mac']):
                    camera_processes.append(line)
            
            if camera_processes:
                print(f"   发现 {len(camera_processes)} 个摄像头相关进程")
                for proc in camera_processes:
                    parts = proc.split()
                    if len(parts) > 1:
                        try:
                            pid = int(parts[1])
                            os.kill(pid, signal.SIGTERM)
                            print(f"   ✅ 终止进程 {pid}")
                        except Exception as e:
                            print(f"   ⚠️ 终止进程失败: {e}")
            else:
                print("   ✅ 没有发现摄像头相关进程")
                
        except Exception as e:
            print(f"   ❌ 进程终止失败: {e}")


# 全局摄像头资源管理器
_global_camera_manager = CameraResourceManager()


def get_camera_resource_manager() -> CameraResourceManager:
    """获取全局摄像头资源管理器"""
    return _global_camera_manager


def force_close_all_cameras():
    """强制关闭所有摄像头"""
    manager = get_camera_resource_manager()
    
    print("📹 开始强制关闭所有摄像头...")
    print("=" * 40)
    
    # 1. 强制清理资源
    manager.force_cleanup_all()
    
    # 2. 检查状态
    if manager.check_camera_status():
        print("⚠️ 摄像头仍然可访问，尝试终止进程...")
        manager.kill_camera_processes()
        
        # 再次检查
        time.sleep(1)
        if manager.check_camera_status():
            print("❌ 摄像头仍无法完全关闭")
            return False
        else:
            print("✅ 摄像头已成功关闭")
            return True
    else:
        print("✅ 摄像头已成功关闭")
        return True


if __name__ == "__main__":
    print("🔧 摄像头资源泄漏修复工具")
    print("=" * 50)
    
    # 测试摄像头资源管理器
    manager = get_camera_resource_manager()
    
    # 模拟注册摄像头
    print("1. 模拟注册摄像头...")
    camera = cv2.VideoCapture(0)
    if camera.isOpened():
        manager.register_camera(camera)
        print("   ✅ 摄像头注册成功")
        
        # 强制清理
        print("2. 强制清理摄像头...")
        success = force_close_all_cameras()
        
        if success:
            print("🎉 摄像头资源泄漏修复成功！")
        else:
            print("❌ 摄像头资源泄漏修复失败")
    else:
        print("❌ 无法打开摄像头进行测试")
    
    print("=" * 50)

