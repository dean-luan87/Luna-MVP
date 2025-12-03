# Luna Badge 项目结构与开发规范 v1.0

**版本**: 1.0  
**生效日期**: 2025-12-03  
**适用范围**: 1.3.x → 1.4.0 → 1.6.0 → 2.0 全系列版本  
**文档状态**: 正式版（工程版、可执行版、长期适用版）

---

## 📋 目录

- [第一章 总体架构原则](#第一章-总体架构原则)
- [第二章 目录结构规范（强制）](#第二章-目录结构规范强制)
- [第三章 模型规范（Model Spec v1.0）](#第三章-模型规范model-spec-v10)
- [第四章 感知图谱（Perception Graph）规范](#第四章-感知图谱perception-graph规范)
- [第五章 日志规范（Log System v1.0）](#第五章-日志规范log-system-v10)
- [第六章 测试规范（Testing Spec v1.0）](#第六章-测试规范testing-spec-v10)
- [第七章 代码风格规范](#第七章-代码风格规范)
- [第八章 启动规范（Entry Point）](#第八章-启动规范entry-point)
- [第九章 Cursor 执行规则](#第九章-cursor-执行规则)
- [第十章 长期演进（为 2.0 预留）](#第十章-长期演进为-20-预留)
- [附录：Cursor 指令模板](#附录cursor-指令模板)

---

## 第一章 总体架构原则

Luna Badge 项目必须遵循以下设计理念：

### 1.1 分层架构（Layered Architecture）

- **核心层（Core Layer）**：系统底座，提供基础服务
- **功能层（Feature Layer）**：视觉、导航、音频、任务等业务模块
- **系统层（System Layer）**：硬件抽象、设备管理
- **应用层（Application Layer）**：主入口、任务编排

**原则**：上层可以调用下层，下层不得调用上层。

### 1.2 模块独立（No Cross-Layer Imports）

- 禁止跨层直接调用
- 禁止循环依赖
- 模块间通过事件总线或接口通信

**示例**：
```python
# ✅ 正确：vision 通过接口调用 navigation
vision → navigation (通过接口)

# ❌ 错误：vision 直接导入 navigation 内部实现
from navigation.planner import PathPlanner  # 禁止
```

### 1.3 可扩展（Model Plug-in / Hot Swap）

- 所有模型必须实现统一接口
- 支持运行时模型切换
- 支持模型热插拔
- 通过模型注册表管理

### 1.4 可调度（统一模型注册 + 状态机）

- 所有模型必须注册到 `model_registry`
- 通过状态机管理模型生命周期
- 支持模型降级和恢复

### 1.5 可测试（测试分离 + Mock 体系）

- 测试代码完全独立
- 所有 I/O 使用 Mock
- 测试日志独立存储

### 1.6 可观察（独立日志系统 + 调试工具）

- 统一日志系统
- 日志分类存储
- 支持调试模式

### 1.7 可演进（未来世界模型兼容）

- 结构预留扩展点
- 接口设计考虑未来需求
- 支持多模态融合

---

## 第二章 目录结构规范（强制）

项目必须严格使用以下结构：

```
/src
    /core                  # 系统底座
        /config            # 所有配置文件（模型/系统/参数）
        /logging           # 新日志系统（独立）
        /utils             # 通用工具 / 时间 / ID / 数学
        /state_machine     # 视觉/任务状态机
        /event_bus         # 全局事件总线
        /async_runner      # 统一异步执行器

    /vision                # 视觉主系统
        /models            # YOLO / Seg / Depth / CLIP / OCR / Free-space
        /pipeline          # 摄像头输入 → 多模型并行 → 输出
        /fusion            # 多模型融合（V-Level → S-Level）
        /perception_graph  # 感知图谱（多线程任务树）
        /model_registry    # 模型注册、调度、生命周期

    /navigation            # 导航主系统
        /planner           # 路径规划
        /path_eval         # 路径评分 / 偏航处理
        /map_builder       # 微地图构建（未来 1.6+）
        /obstacle_handler  # 障碍物处理

    /audio                 # 音频系统
        /asr               # Whisper / ASR
        /tts               # TTS / Real Voice
        /audio_router      # 语音控制逻辑

    /tasks                 # 任务链系统
        /task_chain        # 主任务链
        /task_manager      # 任务调度
        /task_cache        # 任务恢复与缓存

    /system                # 硬件系统
        /device            # 电源、状态、序列号、版本
        /camera            # 摄像头管理
        /sensors           # 环境传感器
        /recovery          # 故障恢复 / failsafe
```

### 2.1 目录创建规则

1. **所有新功能必须按该结构创建模块**
2. **不允许在 `src` 根目录写散乱文件**
3. **每个目录必须包含 `__init__.py`**
4. **模块命名使用小写字母和下划线**

### 2.2 文件命名规范

- **模块文件**：`snake_case.py`
- **类文件**：`snake_case.py`（类名使用 `PascalCase`）
- **测试文件**：`test_snake_case.py`
- **配置文件**：`snake_case.yaml` 或 `snake_case.json`

---

## 第三章 模型规范（Model Spec v1.0）

### 3.1 统一模型接口

所有模型（YOLO、Seg、Depth、OCR）必须实现统一接口：

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import numpy as np

class VisionModel(ABC):
    """视觉模型统一接口"""
    
    @abstractmethod
    def load(self) -> bool:
        """加载模型"""
        pass
    
    @abstractmethod
    def warmup(self, num_iterations: int = 3) -> None:
        """模型预热"""
        pass
    
    @abstractmethod
    def predict(self, frame: np.ndarray) -> Dict[str, Any]:
        """模型推理"""
        pass
    
    @abstractmethod
    def unload(self) -> None:
        """卸载模型"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """模型名称"""
        pass
    
    @property
    @abstractmethod
    def model_type(self) -> str:
        """模型类型：object_detection / segmentation / depth / ocr"""
        pass
```

### 3.2 统一输出格式（V-Level）

模型输出必须遵循统一 V-Level 结构：

```python
{
    "model": "yolo_v11",
    "type": "object_detection",  # object / region / free_space / depth
    "label": "person",
    "score": 0.93,
    "bbox": [x1, y1, x2, y2],
    "mask": [...],  # 可选，用于分割模型
    "depth": 1.5,  # 可选，深度值
    "motion": {"vx": 0.1, "vy": 0.2},  # 可选，运动向量
    "timestamp": 1234567890.123,
    "metadata": {
        "input_size": [640, 640],
        "inference_time_ms": 12.5
    }
}
```

### 3.3 模型注册规范

所有模型必须通过 `model_registry` 注册：

```python
from src.vision.model_registry import ModelRegistry

registry = ModelRegistry()

registry.register(
    name="yolo_v11_tiny",
    type="object_detection",
    input="rgb",
    output="bbox",
    cost="medium",  # low / medium / high
    latency_ms=40,
    memory_mb=150,
    framework="pytorch",
    path="models/nav/yolo11_tiny.pt",
    input_size=[640, 640],
    threshold=0.5
)
```

### 3.4 模型调用规范

**禁止**：模型直接互相调用

```python
# ❌ 错误示例
class YOLODetector:
    def detect(self, frame):
        # 直接调用其他模型
        depth = depth_model.predict(frame)  # 禁止
```

**正确**：通过 pipeline / fusion / graph 调度

```python
# ✅ 正确示例
class VisionPipeline:
    def process(self, frame):
        # 通过 pipeline 调度多个模型
        yolo_result = self.yolo_model.predict(frame)
        depth_result = self.depth_model.predict(frame)
        # 融合结果
        return self.fusion.merge(yolo_result, depth_result)
```

---

## 第四章 感知图谱（Perception Graph）规范

### 4.1 感知图谱职责

感知图谱是多模型并行任务树，其职责是：

1. **管理子模型线程**：并行执行多个模型
2. **组合导航/识别/场景模型**：协调不同模型
3. **生成 S-Level（语义输出）**：将 V-Level 转换为语义级输出
4. **作为视觉的"状态流动器"**：管理视觉状态流转

### 4.2 统一输出结构（S-Level）

感知图谱必须输出统一结构（供任务链 / 语音使用）：

```python
{
    "scene_type": "indoor_corridor",  # indoor / outdoor / stairs / elevator
    "walkable": {
        "forward": 0.8,  # 可通行性评分 0-1
        "right": 0.6,
        "left": 0.4
    },
    "obstacles": [
        {
            "type": "person",
            "position": [320, 240],
            "distance": 2.5,
            "risk": "low"
        }
    ],
    "entrances": [
        {
            "type": "door",
            "position": [100, 200],
            "direction": "forward"
        }
    ],
    "risk": "low",  # low / medium / high
    "nav_suggestion": "turn_right",
    "confidence": 0.85,
    "timestamp": 1234567890.123
}
```

### 4.3 状态机绑定

状态机必须与感知图谱绑定，完成：

- **模型切换**：根据场景切换模型
- **模型降级**：性能不足时降级到轻量模型
- **异常恢复**：模型失败时自动恢复
- **场景识别 → 状态变化**：场景变化触发状态机转换
- **多模型结果融合**：融合多个模型输出

### 4.4 感知图谱实现示例

```python
class PerceptionGraph:
    """感知图谱"""
    
    def __init__(self):
        self.models = {}
        self.state_machine = VisionStateMachine()
        self.fusion = FusionEngine()
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """处理一帧，返回 S-Level 输出"""
        # 1. 根据状态机选择模型
        active_models = self.state_machine.get_active_models()
        
        # 2. 并行执行模型
        results = self.run_models_parallel(frame, active_models)
        
        # 3. 融合结果
        fused_result = self.fusion.merge(results)
        
        # 4. 生成 S-Level 输出
        s_level = self.generate_s_level(fused_result)
        
        # 5. 更新状态机
        self.state_machine.update(s_level)
        
        return s_level
```

---

## 第五章 日志规范（Log System v1.0）

### 5.1 日志系统要求

日志必须由 `/core/logging/` 模块统一管理。

**要求**：

1. **异步写入**：不能阻塞视觉线程
2. **每日文件切割**：按日期自动分割日志文件
3. **统一格式**：JSON 行格式（JSONL）
4. **可关闭/降级**：生产环境必须可调
5. **调试日志与系统日志分离**：不同用途的日志分开存储

### 5.2 日志分类

```
/logs
    /system/          # 系统运行日志
    /tests/           # 测试日志
    /vision/          # 视觉模块日志
    /navigation/      # 导航模块日志
    /audio/           # 音频模块日志
    /tasks/           # 任务链日志
```

### 5.3 日志使用规范

**禁止使用 `print()`**：

```python
# ❌ 错误
print("Processing frame...")
print(f"Detected {len(objects)} objects")
```

**必须使用统一 logger**：

```python
# ✅ 正确
from core.logging import get_logger

log = get_logger("vision")

log.debug("Processing frame...")
log.info(f"Detected {len(objects)} objects")
log.warning("Low confidence detection")
log.error("Model inference failed")
log.exception("Exception occurred")
```

### 5.4 日志级别

- **DEBUG**：详细调试信息
- **INFO**：一般信息
- **WARNING**：警告信息
- **ERROR**：错误信息
- **CRITICAL**：严重错误

### 5.5 日志格式

日志文件使用 JSONL 格式：

```json
{"timestamp": "2025-12-03T11:00:00.123Z", "level": "INFO", "module": "vision", "message": "Processing frame", "frame_id": 12345}
{"timestamp": "2025-12-03T11:00:00.125Z", "level": "DEBUG", "module": "vision", "message": "YOLO inference", "latency_ms": 12.5}
```

---

## 第六章 测试规范（Testing Spec v1.0）

### 6.1 测试目录结构

测试必须完全独立于主系统：

```
/tests
    /unit_tests          # 单元测试
    /integration_tests    # 集成测试
    /vision_tests        # 视觉模块测试
    /navigation_tests     # 导航模块测试
    /mock_data           # Mock 数据
        /sample_frames/  # 测试用图像
        /sample_ocr/     # 测试用 OCR 数据
        /sample_yolo/    # 测试用 YOLO 输出
    /utils
        /test_helpers.py # 测试工具函数
```

### 6.2 测试要求

测试必须：

1. **不得影响主系统**：测试代码与主代码完全隔离
2. **所有 I/O 必须使用 mock**：不依赖真实硬件或文件系统
3. **所有视觉测试必须用离线 sample frame**：使用预定义的测试图像
4. **测试日志写到 `/logs/tests/`**：测试日志独立存储

### 6.3 测试文件命名

- 单元测试：`test_module_name.py`
- 集成测试：`test_integration_feature.py`
- Mock 数据：`mock_data/type_name/sample_*.json`

### 6.4 测试示例

```python
import unittest
from tests.utils.test_helpers import load_frame, mock_yolo_output
from src.vision.models.yolo import YoloDetector

class TestYOLODetector(unittest.TestCase):
    def setUp(self):
        self.detector = YoloDetector()
        self.test_frame = load_frame("sample_frames/test_image.jpg")
    
    def test_detection(self):
        result = self.detector.detect(self.test_frame)
        self.assertIsNotNone(result)
        self.assertGreater(len(result.boxes), 0)
```

---

## 第七章 代码风格规范

### 7.1 格式化工具

1. **强制使用 Black 格式化**：
   ```bash
   black src/ tests/
   ```

2. **import 必须使用 isort**：
   ```bash
   isort src/ tests/
   ```

### 7.2 代码质量要求

1. **禁止循环引用**：模块间不得形成循环依赖
2. **禁止跨层调用**：核心规则，必须严格遵守
3. **所有配置放在 `/core/config`**：统一配置管理
4. **所有异常归类至 `/core/errors.py`**：统一异常处理
5. **删除所有未使用的代码、变量、文件、import**：保持代码整洁

### 7.3 Import 顺序规范

```python
# 1. 标准库
import os
import sys
from typing import Dict, List

# 2. 第三方库
import numpy as np
import cv2

# 3. 本地模块
from core.logging import get_logger
from src.vision.models.yolo import YoloDetector
```

### 7.4 代码检查

使用以下工具检查代码质量：

```bash
# 格式化检查
black --check src/ tests/

# Import 检查
isort --check src/ tests/

# 代码质量检查（可选）
flake8 src/ tests/ --max-line-length=100
```

---

## 第八章 启动规范（Entry Point）

### 8.1 主入口文件

主入口固定为：

```
main.py
```

### 8.2 主入口职责

主入口只做三件事：

1. **启动设备**（camera / sensors）
2. **启动视觉 pipeline**
3. **启动任务链系统**

**不允许进行业务逻辑**。

### 8.3 主入口示例

```python
#!/usr/bin/env python3
"""
Luna Badge 主入口
只负责启动系统，不包含业务逻辑
"""
from core.logging import get_logger
from system.camera import CameraManager
from system.sensors import SensorManager
from vision.pipeline import VisionPipeline
from tasks.task_manager import TaskManager

log = get_logger("main")

def main():
    """主函数"""
    log.info("Luna Badge 启动")
    
    # 1. 启动设备
    camera = CameraManager()
    sensors = SensorManager()
    camera.start()
    sensors.start()
    
    # 2. 启动视觉 pipeline
    vision = VisionPipeline()
    vision.start()
    
    # 3. 启动任务链系统
    task_manager = TaskManager()
    task_manager.start()
    
    try:
        # 主循环
        while True:
            # 业务逻辑在其他模块中
            pass
    except KeyboardInterrupt:
        log.info("收到停止信号")
    finally:
        # 清理资源
        task_manager.stop()
        vision.stop()
        sensors.stop()
        camera.stop()

if __name__ == "__main__":
    main()
```

---

## 第九章 Cursor 执行规则

当 Cursor 需要重构代码结构时，必须遵守以下规则：

### 9.1 不允许破坏目录规范

- 如不确定，先询问，但不能随意创建新模块
- 所有新模块必须符合第二章的目录结构规范

### 9.2 每个模块必须创建 `__init__.py`

- 保证可被 import
- `__init__.py` 可以导出主要接口

### 9.3 所有新文件必须加入日志（logger）

- 验证可用性
- 确保日志系统正常工作

### 9.4 所有修改前必须生成 Diff 预览

- 让你先确认
- 避免意外修改

### 9.5 重构必须分步骤执行

- 不允许一次性全局修改
- 避免破坏运行环境
- 每步完成后进行测试

### 9.6 Cursor 工作流程

1. **分析需求**：理解要做什么
2. **生成计划**：列出步骤
3. **生成 Diff 预览**：显示将要修改的内容
4. **等待确认**：用户确认后再执行
5. **执行修改**：按步骤执行
6. **运行测试**：验证修改正确性
7. **提交更改**：确认无误后提交

---

## 第十章 长期演进（为 2.0 预留）

### 10.1 预留扩展点

结构必须预留未来接入：

- **多模型调度（v1.6）**：支持动态模型切换
- **视觉状态机（v1.6–1.7）**：状态驱动的视觉处理
- **世界模型（v2.0）**：3D 场景理解
- **三摄结构（v2.0+）**：多摄像头融合
- **帧融合（v2.0）**：时序信息融合
- **语音 × 视觉 × 任务链三模态融合（1.7）**：多模态协同

### 10.2 接口设计原则

- **接口优先**：先定义接口，再实现
- **向后兼容**：新版本保持旧接口可用
- **扩展性**：接口设计考虑未来需求

### 10.3 版本兼容性

- **主版本号（Major）**：不兼容的 API 变更
- **次版本号（Minor）**：向后兼容的功能新增
- **修订号（Patch）**：向后兼容的问题修复

---

## 附录：Cursor 指令模板

### A.1 标准 Cursor 指令

```
请从现在开始严格遵循《Luna Badge 项目结构与开发规范 v1.0》的所有内容进行开发与重构。任何新增模块、重构、目录调整、文件清理，都必须按规范执行。

第一步任务：
按规范拆分测试系统（/tests）与日志系统（/core/logging）。

第二步任务：
按规范重构项目整体目录结构。

第三步任务：
执行代码格式化、无用代码删除、import 清理。

所有执行必须分步骤进行，每一步都要输出 diff 预览并等待确认。
```

### A.2 模块创建指令模板

```
请按照《Luna Badge 项目结构与开发规范 v1.0》在 [模块路径] 创建新模块 [模块名]。

要求：
1. 创建 __init__.py 并导出主要接口
2. 实现统一模型接口（如果是模型）
3. 添加日志系统
4. 创建对应的测试文件
5. 生成 diff 预览供确认
```

### A.3 重构指令模板

```
请按照《Luna Badge 项目结构与开发规范 v1.0》重构 [目标模块/文件]。

要求：
1. 检查是否符合目录结构规范
2. 替换所有 print 为 logger
3. 检查并修复循环依赖
4. 执行代码格式化
5. 生成 diff 预览供确认
6. 分步骤执行，每步完成后测试
```

---

## 文档维护

### 版本历史

- **v1.0** (2025-12-03)：初始版本，适用于 1.3.x → 2.0

### 更新原则

- 规范变更需要团队讨论
- 重大变更需要更新版本号
- 所有变更需要记录在版本历史中

---

## 联系与反馈

如有疑问或建议，请通过以下方式反馈：

- 项目 Issue 跟踪
- 团队内部讨论
- 代码审查流程

---

**本文档是 Luna Badge 项目的官方工程规范第一版（v1.0），所有开发工作必须严格遵循本规范。**

