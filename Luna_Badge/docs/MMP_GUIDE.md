# Luna Badge 模块管理平台 (MMP) 使用指南

## 📋 概述

模块管理平台（Module Management Platform, MMP）是 Luna Badge 的核心控制系统，负责：
- ✅ 模块级状态管理（启动、挂起、重启、禁用）
- ✅ 系统健康状态监控
- ✅ 远程配置 & OTA管理（预留接口）
- ✅ 模块接口注册机制
- ✅ 调试与测试支持

## 🏗️ 架构设计

```
┌────────────────────────────┐
│      外部控制台/API         │ ← Web可视化控制入口 / 云平台 / App
└────────────┬─────────────┘
             ↓
┌────────────────────────────┐
│   🎯 模块管理中心 (mmp.py)   │ ← 控制调度 + 状态管理 + 模块路由
└────────────┬─────────────┘
             ↓
┌────────┬────────────┬────────┐
│ config │  logger     │  runtime│ ← 配置中心/日志管理/运行状态缓存
└────────┴────────────┴────────┘
             ↓
┌────────┬────────┬────────────┐
│ memory │ vision │ navigation │ ← 实际模块容器（封装好的模块）
└────────┴────────┴────────────┘
```

## 📦 模块状态模型

```
Registered (已注册)
    ↓
Active (运行中) ←→ Suspended (已挂起)
    ↓
Stopped (已停止)
```

## 🚀 快速开始

### 1. 创建自定义模块

```python
from core.base_module import BaseModule

class MyModule(BaseModule):
    def _initialize(self):
        """模块初始化逻辑"""
        # 执行初始化操作
        return True
    
    def _cleanup(self):
        """模块清理逻辑"""
        # 执行清理操作
        pass
```

### 2. 注册模块到MMP

```python
from core.mmp import get_mmp

mmp = get_mmp()
my_module = MyModule("my_module", "1.0.0")
mmp.register_module("my_module", my_module)
```

### 3. 启动模块

```python
# 启动单个模块
mmp.start_module("my_module")

# 启动所有模块
mmp.start_all_modules()
```

## 📖 API 参考

### 模块操作

#### 注册/注销模块

```python
# 注册模块
mmp.register_module("module_name", module_instance, dependencies=["dep1", "dep2"])

# 注销模块
mmp.unregister_module("module_name")

# 列出所有已注册模块
modules = mmp.list_registered()
```

#### 启动/停止模块

```python
# 启动模块
success = mmp.start_module("module_name")

# 停止模块
success = mmp.stop_module("module_name")

# 重启模块
success = mmp.restart_module("module_name")

# 挂起模块（暂停运行，保留状态）
success = mmp.suspend_module("module_name")

# 恢复模块（从挂起状态恢复）
success = mmp.resume_module("module_name")
```

#### 配置注入

```python
# 向模块注入动态配置
config = {
    "param1": "value1",
    "param2": 123
}
mmp.inject_config("module_name", config)
```

### 状态查询

#### 获取模块状态

```python
# 获取单个模块状态
status = mmp.get_module_status("module_name")
# 返回: {
#     "name": "module_name",
#     "state": "active",
#     "version": "1.0.0",
#     "health_score": 100.0,
#     ...
# }

# 获取所有模块状态
all_status = mmp.get_all_status()
```

#### 健康检查

```python
# 系统健康检查
health = mmp.health_check()
# 返回: {
#     "system_health": "healthy",
#     "total_modules": 5,
#     "active_modules": 4,
#     "error_modules": 0,
#     "average_health_score": 95.5
# }
```

#### 运行时状态

```python
# 获取运行时状态
runtime_state = mmp.get_runtime_state()
```

### 监控功能

```python
# 启动后台监控（自动保存状态、健康检查）
mmp.start_monitor()

# 停止监控
mmp.stop_monitor()
```

### 状态报告

```python
# 打印状态报告（控制台输出）
mmp.print_status_report()
```

## 💡 使用示例

### 示例1: 基本模块操作

```python
from core.mmp import get_mmp
from core.base_module import BaseModule

class MemoryModule(BaseModule):
    def _initialize(self):
        # 初始化记忆存储
        self.custom_info["memory_count"] = 0
        return True
    
    def _cleanup(self):
        # 清理资源
        pass

# 初始化MMP
mmp = get_mmp()

# 注册模块
memory = MemoryModule("memory_store", "1.0.0")
mmp.register_module("memory_store", memory)

# 启动模块
mmp.start_module("memory_store")

# 检查状态
status = mmp.get_module_status("memory_store")
print(f"模块状态: {status['state']}")

# 停止模块
mmp.stop_module("memory_store")
```

### 示例2: 模块依赖管理

```python
from core.mmp import get_mmp

mmp = get_mmp()

# 注册依赖模块
mmp.register_module("config_manager", config_module)
mmp.register_module("database", db_module)

# 注册需要依赖的模块
# navigation模块依赖config_manager和database
mmp.register_module(
    "navigation", 
    nav_module,
    dependencies=["config_manager", "database"]
)

# 启动navigation时，会自动先启动依赖模块
mmp.start_module("navigation")
```

### 示例3: 系统健康监控

```python
from core.mmp import get_mmp
import time

mmp = get_mmp()

# 启动所有模块
mmp.start_all_modules()

# 启动监控
mmp.start_monitor()

# 定期检查健康状态
while True:
    health = mmp.health_check()
    print(f"系统健康: {health['system_health']}")
    print(f"活跃模块: {health['active_modules']}/{health['total_modules']}")
    
    if health['system_health'] == 'critical':
        print("⚠️ 系统健康状态异常，需要检查")
    
    time.sleep(60)  # 每分钟检查一次
```

### 示例4: 动态配置更新

```python
from core.mmp import get_mmp

mmp = get_mmp()

# 动态更新模块配置
tts_config = {
    "speech_speed": 1.2,
    "voice_style": "cheerful"
}
mmp.inject_config("tts_manager", tts_config)

# 重启模块使配置生效
mmp.restart_module("tts_manager")
```

## 🔍 调试与测试

### 查看模块日志

每个模块有独立的日志记录，日志保存在 `logs/modules/` 目录：

```bash
# 查看特定模块日志
tail -f logs/modules/memory_store.log
```

### 模块自测

每个模块可以实现 `health_check()` 方法：

```python
class MyModule(BaseModule):
    def health_check(self):
        return {
            "healthy": True,
            "detail": "所有服务正常"
        }
```

### 运行时状态文件

运行时状态保存在 `core/runtime_state.json`：

```bash
# 查看运行时状态
cat core/runtime_state.json
```

## 📊 状态报告示例

```
================================================================================
📊 Luna Badge 模块管理平台状态报告 - 2025-10-28 15:11:09
================================================================================

🏥 系统健康: HEALTHY
   总模块数: 5
   活跃模块: 4
   错误模块: 0
   平均健康分数: 95.5

📦 模块状态:
   ✅ memory_store          active       健康分数: 100.0
   ✅ tts_manager           active       健康分数: 95.0
   ✅ path_evaluator        active       健康分数: 90.0
   ⏸️ vision_detector        suspended    健康分数: 100.0
   🛑 navigation            stopped      健康分数: 0.0

================================================================================
```

## 🔧 最佳实践

1. **模块初始化**: 在 `_initialize()` 中执行所有初始化操作
2. **错误处理**: 使用 try-except 捕获异常，更新错误计数
3. **资源清理**: 在 `_cleanup()` 中释放所有资源
4. **依赖管理**: 正确声明模块依赖，确保启动顺序
5. **状态更新**: 定期更新 `custom_info` 提供更多状态信息
6. **健康检查**: 实现 `health_check()` 方法进行自检

## 🚧 未来扩展 (v2.0)

- [ ] Web可视化控制台
- [ ] REST API接口
- [ ] OTA更新机制
- [ ] 模块插件系统
- [ ] 性能监控与统计
- [ ] 模块热更新
- [ ] 分布式模块管理

## 📚 相关文档

- [BaseModule API](../core/base_module.py)
- [ModuleRegistry API](../core/module_registry.py)
- [MMP API](../core/mmp.py)

---

**最后更新**: 2025-10-28  
**版本**: v1.0
