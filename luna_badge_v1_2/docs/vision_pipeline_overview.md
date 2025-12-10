# Vision → Scene → TaskChain Pipeline 概览（Pro-1）

本模块实现从视觉输入到任务自动触发的最小可用链路：

1. 视觉底层产生 `VisionEvent(ocr_lines, objects, ...)`
2. `SceneObserver` 使用 `SceneClassifier` 对场景进行识别
3. `SceneContext` 记录当前场景与历史轨迹
4. `SceneTaskBinder` 根据 `scene/tag` 给出推荐的 `task_meta`
5. 上层可以使用 `TaskChainManager.register_task(task_meta)` 触发 AskChain + TaskChain
6. 如需自动触发，可通过 `VisionTaskOrchestrator` 直接将视觉事件转为任务执行

## 相关文件

### 核心模块
- `task_engine/vision/vision_event.py` - 视觉事件数据模型
- `task_engine/vision/scene_observer.py` - 视觉到场景的观察者
- `task_engine/vision/vision_scene_bridge.py` - 视觉到场景到任务的桥接器
- `task_engine/scene/scene_task_binder.py` - 场景到任务建议的绑定器
- `task_engine/vision/vision_task_orchestrator.py` - 视觉任务编排器

### Bootstrap
- `bootstrap/vision_pipeline.py` - 统一构建 Vision Pipeline 的工厂函数

### Demo 脚本
- `scripts/demo_vision_scene_task.py` - 本地命令行 demo
- `scripts/vision_api_demo.py` - HTTP + WebSocket API demo 服务

## 快速验证

### 本地 demo

```bash
python scripts/demo_vision_scene_task.py
```

### HTTP + WebSocket demo 服务

```bash
# 安装依赖
pip install fastapi uvicorn pydantic

# 启动服务
python scripts/vision_api_demo.py
```

然后可以：

- **HTTP POST**: `http://localhost:8081/api/vision/event`
  ```json
  {
    "ocr_lines": ["静安寺地铁站"],
    "objects": ["gate"],
    "source": "camera_front"
  }
  ```

- **WebSocket**: `ws://localhost:8081/ws/vision`
  ```json
  {
    "ocr_lines": ["虹口医院门诊部"],
    "objects": [],
    "source": "camera_front"
  }
  ```

## 使用示例

### 基础用法

```python
from task_engine.vision.vision_event import VisionEvent
from task_engine.vision.scene_observer import SceneObserver
from task_engine.vision.vision_scene_bridge import VisionSceneTaskBridge
from task_engine.scene.scene_classifier import SceneClassifier
from task_engine.scene.scene_context import SceneContext
from task_engine.scene.scene_task_binder import create_default_scene_task_binder

# 1. 创建组件
ctx = SceneContext()
classifier = SceneClassifier()  # 或使用自定义分类器
observer = SceneObserver(classifier=classifier, context=ctx)
binder = create_default_scene_task_binder()
bridge = VisionSceneTaskBridge(observer=observer, binder=binder)

# 2. 处理视觉事件
event = VisionEvent(
    ocr_lines=["静安寺地铁站"],
    objects=["gate"],
)
result = bridge.handle_vision_event(event)

# 3. 检查任务建议
if result.suggested_task_meta:
    # 上层可以决定是否启动任务
    # task_manager.register_task(task_meta=result.suggested_task_meta)
    print(f"推荐任务: {result.suggested_task_meta}")
```

### 使用 Bootstrap

```python
from bootstrap.vision_pipeline import create_vision_pipeline
from task_chain.task_chain_manager import TaskChainManager
from core.flow_engine.runtime import FlowRuntime

# 创建 TaskChainManager（可选）
runtime = FlowRuntime()
task_manager = TaskChainManager(runtime)

# 一行创建完整 pipeline
pipeline = create_vision_pipeline(task_manager=task_manager)

# 使用 pipeline
event = VisionEvent(ocr_lines=["地铁站"], objects=["gate"])
result = pipeline.bridge.handle_vision_event(event)

# 或使用 orchestrator（如果传入了 task_manager）
if pipeline.orchestrator:
    task_meta = pipeline.orchestrator.suggest_task_from_vision(event)
    if task_meta:
        # 根据 task_meta 创建 FlowInstance 并注册任务
        pass
```

## 架构设计

### 非侵入式设计

- 不修改 TaskChainManager / AskChain 的核心逻辑
- 只提供任务建议，由上层决定是否启动任务
- 可随时接入或移除

### 完整的数据流

```
VisionEvent 
  → SceneObserver 
  → SceneContext 更新
  → SceneTaskBinder 
  → 任务建议 (task_meta)
  → (可选) VisionTaskOrchestrator 
  → TaskChainManager
```

### 可扩展性

- SceneTaskBinder 支持自定义映射规则
- 未来可从 scene_pack.json 读取配置
- 支持精确匹配（scene, tag）和回退匹配（scene, None）

## 注意事项

1. **VisionTaskOrchestrator** 只返回任务建议，不直接创建 FlowInstance
   - 上层需要根据 `task_meta` 通过 `FlowPlanner` 创建 `FlowInstance` 后再调用 `register_task`

2. **SceneObserver** 有两个版本：
   - `task_engine/vision/scene_observer.py` - 用于 Vision Pipeline，会更新 SceneContext
   - `task_engine/scene/scene_observer.py` - 用于 Scene Integration，只做数据转换

3. **默认分类器** 使用规则匹配，生产环境应替换为真实模型

