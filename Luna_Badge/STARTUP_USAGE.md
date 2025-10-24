# 🚀 Luna Badge 启动流程使用说明

## 📋 概述

本文档详细说明如何在Luna Badge项目中使用启动流程封装，实现从设备上电到开始识别循环的完整启动流程。

## 🎯 启动流程特性

### ✅ 核心功能

- **完整启动序列**: 8个启动阶段，覆盖从设备上电到开始识别循环
- **状态播报**: 实时播报启动状态和进度
- **个性化欢迎语**: 根据人格风格定制欢迎语
- **错误处理**: 完善的异常处理和恢复机制
- **配置管理**: 灵活的启动配置选项
- **状态监控**: 实时监控启动状态变化

### 🎛️ 启动阶段

1. **设备上电** - 系统启动
2. **系统初始化** - 基础系统准备
3. **模块初始化** - AI导航、语音引擎、视觉识别、路径预测
4. **硬件检查** - 摄像头、麦克风、扬声器、传感器
5. **网络检查** - WiFi、互联网、API访问
6. **欢迎语播报** - 个性化用户问候
7. **准备就绪** - 系统准备完成
8. **开始识别循环** - 进入工作状态

## 🔧 使用方法

### 1. 基本使用

```python
from core.startup_manager import StartupManager

# 创建启动管理器
startup_manager = StartupManager(hardware_interface, voice_interface)

# 执行完整启动序列
success = await startup_manager.full_startup_sequence()
```

### 2. 快速启动

```python
from core.startup_manager import quick_startup

# 快速启动
success = await quick_startup(hardware_interface, voice_interface, config)
```

### 3. 自定义配置

```python
# 设置启动配置
config = {
    "enable_voice_feedback": True,      # 启用语音反馈
    "enable_status_broadcast": True,    # 启用状态播报
    "welcome_message": "Luna Badge 启动完成，准备为您服务",
    "personality_style": "friendly",    # 人格风格: friendly/professional
    "check_intervals": {
        "hardware_check": 2.0,          # 硬件检查间隔
        "network_check": 3.0,           # 网络检查间隔
        "module_init": 1.0              # 模块初始化间隔
    }
}
startup_manager.set_config(config)
```

### 4. 状态监控

```python
# 添加状态回调
def on_status_change(status):
    print(f"启动状态: {status.stage.value} - {status.success}")

startup_manager.add_status_callback(on_status_change)
```

## 📱 集成示例

### 完整集成示例

```python
async def main():
    # 初始化组件
    hardware_interface = MacHAL()
    voice_interface = hardware_interface.tts
    
    # 创建启动管理器
    startup_manager = StartupManager(hardware_interface, voice_interface)
    
    # 设置配置
    config = {
        "enable_voice_feedback": True,
        "personality_style": "friendly"
    }
    startup_manager.set_config(config)
    
    # 执行启动序列
    success = await startup_manager.full_startup_sequence()
    
    if success:
        print("🎉 Luna Badge启动成功！")
    else:
        print("❌ Luna Badge启动失败！")
```

### 主程序集成

```python
class LunaBadgeMain:
    def __init__(self):
        self.startup_manager = None
        self.startup_complete = False
    
    async def run_startup_sequence(self):
        """运行启动序列"""
        # 创建启动管理器
        self.startup_manager = StartupManager(
            hardware_interface=self.hardware_interface,
            voice_interface=self.voice_interface
        )
        
        # 设置配置和回调
        self.startup_manager.set_config(config)
        self.startup_manager.add_status_callback(self.on_startup_status_change)
        
        # 执行启动序列
        success = await self.startup_manager.full_startup_sequence()
        
        if success:
            self.startup_complete = True
            logger.info("🎉 启动完成！")
        
        return success
    
    def on_startup_status_change(self, status):
        """启动状态变化回调"""
        if status.stage == StartupStage.START_RECOGNITION and status.success:
            self.startup_complete = True
            logger.info("🔄 开始识别循环，系统进入工作状态")
```

## 🎛️ 配置选项

### 启动配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enable_voice_feedback` | bool | True | 启用语音反馈 |
| `enable_status_broadcast` | bool | True | 启用状态播报 |
| `welcome_message` | str | "Luna Badge 启动完成，准备为您服务" | 欢迎语消息 |
| `personality_style` | str | "friendly" | 人格风格 (friendly/professional) |
| `check_intervals` | dict | {...} | 检查间隔配置 |

### 人格风格配置

- **friendly**: 友好风格
  - 欢迎语: "你好！我是Luna，很高兴为您服务！"
- **professional**: 专业风格
  - 欢迎语: "Luna Badge 系统已就绪，开始为您提供导航服务。"

### 检查间隔配置

```python
"check_intervals": {
    "hardware_check": 2.0,    # 硬件检查间隔（秒）
    "network_check": 3.0,     # 网络检查间隔（秒）
    "module_init": 1.0        # 模块初始化间隔（秒）
}
```

## 📊 状态监控

### 启动状态回调

```python
def status_callback(status: StartupStatus):
    """启动状态变化回调"""
    print(f"阶段: {status.stage.value}")
    print(f"成功: {status.success}")
    print(f"消息: {status.message}")
    print(f"时间戳: {status.timestamp}")
    print(f"详情: {status.details}")

startup_manager.add_status_callback(status_callback)
```

### 启动总结

```python
summary = startup_manager.get_startup_summary()
print(f"启动完成: {summary['startup_complete']}")
print(f"成功率: {summary['success_rate']:.2%}")
print(f"启动耗时: {summary['startup_duration']:.2f}秒")
```

## 🧪 测试和验证

### 运行测试

```bash
# 测试启动流程
python3 test_startup_flow.py

# 运行演示
python3 startup_demo.py

# 运行主程序
python3 main_with_startup.py
```

### 测试覆盖

- ✅ 启动管理器基本功能
- ✅ 快速启动函数
- ✅ 各个启动阶段
- ✅ 状态播报功能
- ✅ 错误处理机制
- ✅ 配置管理

## 🎯 最佳实践

### 1. 启动配置

- 根据设备性能调整检查间隔
- 根据用户偏好设置人格风格
- 启用状态播报提升用户体验

### 2. 错误处理

- 实现状态回调函数处理启动异常
- 设置合理的超时时间
- 提供详细的错误信息

### 3. 性能优化

- 并行执行独立的启动阶段
- 缓存初始化结果
- 优化硬件检查频率

## 🔧 扩展功能

### 1. 自定义启动阶段

```python
async def custom_stage(self) -> bool:
    """自定义启动阶段"""
    # 实现自定义逻辑
    return True

# 添加到启动序列
startup_stages.append((self.custom_stage, "自定义阶段"))
```

### 2. 启动进度显示

```python
def progress_callback(progress: float):
    """启动进度回调"""
    print(f"启动进度: {progress:.1%}")

startup_manager.add_progress_callback(progress_callback)
```

### 3. 启动日志记录

```python
# 启用详细日志记录
logging.getLogger('core.startup_manager').setLevel(logging.DEBUG)
```

## 📋 故障排除

### 常见问题

1. **启动失败**
   - 检查硬件接口是否正确初始化
   - 验证语音接口是否可用
   - 查看日志获取详细错误信息

2. **状态播报失败**
   - 确认语音接口已正确配置
   - 检查网络连接状态
   - 验证TTS服务是否正常

3. **配置不生效**
   - 确认配置在启动前设置
   - 检查配置格式是否正确
   - 验证配置参数是否有效

### 调试技巧

```python
# 启用调试日志
logging.basicConfig(level=logging.DEBUG)

# 添加详细状态回调
def debug_callback(status):
    print(f"DEBUG: {status.stage.value} - {status.success} - {status.message}")

startup_manager.add_status_callback(debug_callback)
```

## 📚 相关文档

- [启动流程架构指南](STARTUP_FLOW_GUIDE.md)
- [系统架构文档](docs/Luna_Badge_Architecture_v1_Summary.md)
- [API参考文档](docs/Luna_Badge_System_v2_Todo_List.md)

## 🎉 总结

Luna Badge的启动流程封装提供了：

- ✅ **完整的启动序列**: 从设备上电到开始识别循环
- ✅ **状态播报功能**: 实时播报启动状态和进度
- ✅ **个性化欢迎语**: 根据人格风格定制欢迎语
- ✅ **错误处理机制**: 完善的异常处理和恢复
- ✅ **配置管理**: 灵活的启动配置选项
- ✅ **状态监控**: 实时监控启动状态变化

通过这个启动流程封装，Luna Badge能够提供清晰顺滑的启动体验，确保用户能够清楚地了解系统状态，并获得个性化的欢迎体验。

---

**文档版本**: v1.0  
**更新时间**: 2025年10月24日  
**维护者**: AI Assistant
