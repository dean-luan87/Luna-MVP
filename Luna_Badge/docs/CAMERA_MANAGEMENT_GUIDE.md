# Luna Badge 摄像头管理指南

## 📋 概述

本文档介绍 Luna Badge 系统中的摄像头管理机制，包括多种关闭方式和安全保障措施。

## 🔧 摄像头关闭方式

### 1. 语音关闭

通过语音命令关闭摄像头，支持以下关键词：
- "关闭摄像头"
- "关闭相机"
- "关闭镜头"
- "摄像头关闭"
- "停止录制"

**使用示例**:
```python
from core.camera_manager import get_camera_manager

manager = get_camera_manager()
manager.handle_voice_command("关闭摄像头")
```

### 2. 硬件双击关闭

通过硬件按键双击（0.5秒内两次点击）关闭摄像头。

**使用示例**:
```python
from core.camera_manager import get_camera_manager

manager = get_camera_manager()
# 检测硬件双击事件
manager.handle_hardware_double_click()
```

### 3. 任务完成后问询关闭

任务完成后自动询问用户是否关闭摄像头。

**使用示例**:
```python
from core.camera_manager import get_camera_manager

manager = get_camera_manager()
# 任务完成后问询关闭
manager.handle_task_complete(ask_before_close=True)
```

### 4. 空闲超时自动关闭

摄像头空闲超过3分钟（可配置）自动关闭。

**配置方式**:
```python
from core.camera_manager import CameraManager

# 设置超时时间为180秒（3分钟）
manager = CameraManager(idle_timeout=180)
```

## 📷 摄像头管理器API

### 初始化

```python
from core.camera_manager import get_camera_manager

# 获取全局摄像头管理器实例
manager = get_camera_manager(camera_interface=hal, idle_timeout=180)
```

### 打开摄像头

```python
# 打开摄像头
success = manager.open_camera()
if success:
    print("摄像头已打开")
else:
    print("摄像头打开失败")
```

### 关闭摄像头

```python
from core.camera_manager import CameraCloseReason

# 手动关闭
manager.close_camera(CameraCloseReason.MANUAL)

# 语音关闭
manager.close_camera(CameraCloseReason.VOICE_COMMAND)

# 空闲超时关闭
manager.close_camera(CameraCloseReason.IDLE_TIMEOUT)
```

### 更新活动时间

在摄像头使用时调用，用于重置空闲计时器：

```python
# 摄像头有活动时调用
manager.update_activity()
```

### 检查空闲超时

手动检查是否超时：

```python
# 检查是否超时
timeout = manager.check_idle_timeout()
if timeout:
    print("摄像头已因超时关闭")
```

### 获取摄像头状态

```python
# 获取状态
state = manager.get_state()
print(f"摄像头状态: {state}")
# 输出示例:
# {
#     "is_open": True,
#     "is_recording": False,
#     "last_activity_time": 1698576000.0,
#     "open_count": 1,
#     "close_reason": None,
#     "idle_duration": 120.5
# }
```

### 设置关闭回调

当摄像头关闭时执行自定义回调：

```python
def on_camera_close(reason):
    print(f"摄像头已关闭，原因: {reason}")

manager.set_close_callback(on_camera_close)
```

## 🔒 关闭原因类型

| 原因 | 说明 |
|------|------|
| `VOICE_COMMAND` | 语音命令关闭 |
| `HARDWARE_DOUBLE_CLICK` | 硬件双击关闭 |
| `TASK_COMPLETE` | 任务完成关闭 |
| `IDLE_TIMEOUT` | 空闲超时关闭 |
| `MANUAL` | 手动关闭 |
| `PRIVACY_LOCK` | 隐私锁定关闭 |
| `ERROR` | 错误关闭 |

## 🛡️ 安全机制

### 1. 自动清理

摄像头管理器析构时自动关闭摄像头：

```python
manager = CameraManager()
# ... 使用摄像头 ...
# 当对象销毁时，自动关闭摄像头
del manager
```

### 2. 隐私锁定检查

打开摄像头前自动检查隐私锁定状态：

```python
# 如果摄像头被隐私锁定，无法打开
from core.privacy_protection import is_camera_locked

if is_camera_locked():
    print("摄像头被隐私锁定，无法打开")
```

### 3. 监控线程

自动监控摄像头空闲状态，超时自动关闭：

```python
# 监控线程自动运行，无需手动调用
manager.open_camera()  # 自动启动监控
```

## 🔧 集成示例

### 与AI导航模块集成

```python
from core.ai_navigation import AINavigator
from core.camera_manager import get_camera_manager

# 初始化AI导航
navigator = AINavigator()

# 获取摄像头管理器
manager = get_camera_manager(navigator.hal_interface)

# 开始YOLO检测
navigator.start_yolo_detection(duration=10)

# 检测过程中更新活动时间
manager.update_activity()

# 检测完成后关闭
manager.close_camera(CameraCloseReason.TASK_COMPLETE)
```

### 与系统控制模块集成

```python
from core.system_control import LunaCore
from core.camera_manager import get_camera_manager

# 初始化系统
luna = LunaCore()

# 获取摄像头管理器
manager = get_camera_manager(luna.hal_interface)

# 系统启动时打开摄像头
manager.open_camera()

# 系统关闭时关闭摄像头
manager.close_camera(CameraCloseReason.MANUAL)
```

## 🚨 故障处理

### 摄像头无法关闭

如果摄像头无法正常关闭，可以使用强制关闭脚本：

```bash
# 强制关闭所有摄像头资源
python3 scripts/force_close_camera.py
```

### 摄像头进程残留

检查是否有残留的摄像头进程：

```bash
# Mac系统
lsof | grep -i video

# 或检查OpenCV相关进程
ps aux | grep -i "cv2\|opencv\|camera"
```

## 📝 最佳实践

1. **及时关闭**: 任务完成后立即关闭摄像头，节省资源
2. **活动更新**: 在摄像头使用过程中定期调用 `update_activity()`
3. **异常处理**: 使用 try-finally 确保摄像头关闭
4. **监控超时**: 根据实际需求调整空闲超时时间

### 示例：安全的摄像头使用

```python
from core.camera_manager import get_camera_manager, CameraCloseReason

manager = get_camera_manager(camera_interface=hal)

try:
    # 打开摄像头
    if manager.open_camera():
        # 使用摄像头
        frame = manager.camera_interface.camera.capture_frame()
        
        # 更新活动时间
        manager.update_activity()
        
        # ... 处理帧 ...
        
except Exception as e:
    print(f"错误: {e}")
finally:
    # 确保关闭摄像头
    manager.close_camera(CameraCloseReason.MANUAL)
```

## 🔍 调试技巧

### 查看摄像头状态

```python
from core.camera_manager import get_camera_manager

manager = get_camera_manager()
state = manager.get_state()
print(f"摄像头状态: {state}")

# 检查是否打开
if manager.state.is_open:
    print("摄像头正在运行")
else:
    print("摄像头已关闭")
```

### 日志监控

```python
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 查看摄像头管理器的详细日志
from core.camera_manager import CameraManager
manager = CameraManager()
```

## 📚 相关文档

- [系统控制指南](SYSTEM_CONTROL_GUIDE.md)
- [隐私保护指南](PRIVACY_PROTECTION_SUMMARY.md)
- [AI导航指南](AI_NAVIGATION_GUIDE.md)

---

**最后更新**: 2025-10-28  
**版本**: v1.0

