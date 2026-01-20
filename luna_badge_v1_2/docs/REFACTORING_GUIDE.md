# Luna Badge 重构指南

## 🎯 重构目标

本次重构实现了：
1. ✅ **测试系统独立化** - 测试代码完全独立，不耦合主系统
2. ✅ **统一日志系统** - 全局日志接口，支持异步写入、按天切割、全局开关
3. 🔄 **代码结构规范化** - 为未来扩展做好准备

## 📚 使用新系统

### 1. 使用统一日志系统

#### 基本用法

```python
from core.logging import get_logger

# 获取日志器（按模块名）
log = get_logger("vision")
log = get_logger("navigation")
log = get_logger("audio")

# 记录日志
log.debug("调试信息")
log.info("一般信息")
log.warning("警告信息")
log.error("错误信息")
log.exception("异常信息", exc_info=True)
```

#### 测试模式

```python
# 测试模式下，日志会写入 logs/tests/
log = get_logger("test_vision", test_mode=True)
```

#### 配置日志

创建 `config/logging.yaml`:

```yaml
enabled: true
level: INFO  # DEBUG, INFO, WARNING, ERROR
log_dir: logs/system
test_log_dir: logs/tests
async_write: true
rotate_daily: true
max_file_size_mb: 100
backup_count: 30
```

### 2. 使用测试工具

#### 基本用法

```python
from tests.utils.test_helpers import (
    load_frame,
    mock_camera,
    mock_yolo_output,
    mock_navigation_state,
    mock_audio_response,
    create_test_config
)

# 加载测试图像
frame = load_frame()  # 随机图像
frame = load_frame("path/to/image.jpg")  # 指定图像

# 模拟摄像头
camera = mock_camera(width=640, height=480)

# 模拟 YOLO 输出
detections = mock_yolo_output(num_objects=5)

# 模拟导航状态
nav_state = mock_navigation_state(
    current_position=(0, 0),
    target_position=(10, 10)
)

# 创建测试配置
config = create_test_config(model="yolo11_tiny", device="cpu")
```

#### 运行测试

```bash
# 运行所有测试
python tests/run_all_tests.py

# 运行视觉测试
python tests/run_vision_tests.py

# 运行导航测试
python tests/run_nav_tests.py
```

## 📁 新目录结构

### 测试系统

```
tests/
├── unit_tests/          # 单元测试
├── integration_tests/   # 集成测试
├── vision_tests/        # 视觉相关测试
├── navigation_tests/    # 导航相关测试
├── mock_data/           # Mock 数据
│   ├── sample_frames/   # 测试图像
│   ├── sample_ocr/      # OCR 测试数据
│   └── sample_yolo/     # YOLO 测试数据
└── utils/
    └── test_helpers.py  # 测试工具
```

### 日志系统

```
core/logging/
├── __init__.py          # 导出接口
├── logger.py            # 统一日志接口
├── log_config.py        # 日志配置
├── log_writer.py        # 日志写入器
└── log_rotator.py       # 日志轮转
```

### 新项目结构（框架已创建）

```
src/
├── core/
│   ├── config/          # 统一配置中心
│   ├── logging/         # ✅ 日志系统
│   ├── utils/           # 工具函数
│   ├── state_machine/   # 状态机（预留）
│   ├── event_bus/       # 事件总线
│   └── async_runner/    # 异步运行器
├── vision/
│   ├── models/          # 视觉模型
│   ├── pipeline/        # 处理流水线
│   ├── fusion/          # 融合逻辑
│   └── perception_graph/ # 感知图谱（预留）
├── navigation/
│   ├── planner/         # 路径规划
│   ├── path_eval/       # 路径评估
│   └── map_builder/     # 地图构建
├── audio/
│   ├── asr/             # 语音识别
│   ├── tts/             # 语音合成
│   └── audio_router/    # 音频路由
└── tasks/
    ├── task_chain/      # 任务链
    └── task_manager/    # 任务管理
```

## 🔄 迁移旧代码到新系统

### 替换旧日志

**旧代码：**
```python
print("Processing frame...")
print(f"Error: {error}")
```

**新代码：**
```python
from core.logging import get_logger
log = get_logger("vision")

log.info("Processing frame...")
log.error(f"Error: {error}")
```

### 迁移测试代码

**旧代码：**
```python
# test_xxx.py 在根目录
import sys
sys.path.insert(0, ".")
from core.vision import Detector
```

**新代码：**
```python
# tests/unit_tests/test_xxx.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.utils.test_helpers import mock_yolo_output
from core.vision import Detector
```

## ⚠️ 注意事项

1. **日志系统已可用** - 可以立即开始使用新日志系统
2. **测试系统已可用** - 测试工具和目录已就绪
3. **模块迁移需谨慎** - 大规模文件移动建议分批次执行
4. **保持兼容性** - 重构过程中保持系统可运行

## 📝 下一步

1. **测试新日志系统** - 在现有代码中试用新日志接口
2. **逐步迁移模块** - 一次迁移一个模块，确保功能正常
3. **更新导入路径** - 移动文件后更新所有导入语句
4. **运行测试** - 每次迁移后运行测试确保无误

## 📚 相关文档

- `REFACTORING_PLAN.md` - 详细重构计划
- `REFACTORING_STATUS.md` - 当前执行状态
















