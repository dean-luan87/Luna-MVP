# 📋 D&E 模块修复指令（给 Cursor）

## ✅ Cursor 专用 · D&E 修复指令（一次性修复版）

---

## 📌 [Cursor 指令]：修复 D&E 模块整体结构，不拆碎、不重写全局，只做定向增强

接下来请你对 Luna Badge 的 D/E 模块（方向检测 DirectionEvaluator 与环境检测 EnvironmentScanner）执行结构化修复，要求如下：

---

## 【核心目标】

1. 保持当前项目结构，不重新拆碎文件；
2. 合并冗余逻辑，统一为一个可复用的"场景节点感知层 SceneNodeLayer"；
3. 加强 D（方向判断）与 E（场景理解）之间的协同；
4. 为未来"场景智能 / 小范围地图 / 多节点补全"预留接口；
5. 保留现有的视觉/YOLO/OCR 调用方式。

---

## 【必须完成的修复项】

### ① DirectionEvaluator（D 模块）

- 新增统一输入结构 FrameContext（包含方向向量、光流、历史方向、相机角度）
- 修复偏航判断逻辑：避免因噪声反复触发
- 增加"方向置信度 direction_confidence"
- 加入"方向意图推理"接口（不实现，只预留）

### ② EnvironmentScanner（E 模块）

- 将所有场景元素（人群、道路、标识牌、障碍物、服务台等）统一输出成 SceneNode
- 新增 SceneNodeLayer：可登记节点类型、位置、标签、可信度
- 支持多帧融合（3~5 帧）避免抖动导致节点消失
- 场景节点全走同一种数据结构，不再多个地方重复判断

### ③ D + E 协同

- 新增 DirectionEvaluator.sync_env(scene_nodes)
- 新增 方向纠错策略：视觉节点支持方向修正（如转角、走廊、斑马线）
- 增加"场景驱动的方向优先级"表（不实现表内容，只写接口）

### ④ 预留未来"场景地图绘制"能力

- 新增接口 SceneMapIntegrator（不实现）
- 支持注册关键场景节点（如入口、电梯、楼梯、窗口）

---

## 【文件需修改/创建】

需要你修改或新增以下文件：

```
core/navigation/direction_evaluator.py        ← 新文件（基于 direction_estimator.py 增强）
core/navigation/environment_scanner.py       ← 新文件（整合现有环境检测逻辑）
core/navigation/scene_node.py               ← 新文件（统一场景节点数据结构）
core/navigation/scene_node_layer.py         ← 新文件（场景节点感知层）
core/navigation/scene_context.py            ← 新文件（FrameContext 统一输入结构）
```

修改时请遵循：
- 不拆碎文件
- 不引入额外依赖
- 所有新模块必须有注释
- 暂不写单元测试

---

## 【现有模块参考】

参考以下现有模块的实现风格：
- `core/direction_estimator.py`（方向估算器）
- `core/path_evaluator.py`（路径判断引擎）
- `core/flow_direction_analyzer.py`（人流方向分析）
- `core/hazard_detector.py`（危险检测器）

保持与现有代码风格一致，使用 dataclass、类型注解、logging。

---

## 【实施步骤】

1. **先创建目录结构**（如果不存在）：
   ```bash
   mkdir -p core/navigation
   ```

2. **创建基础数据结构文件**（按顺序）：
   - `scene_context.py` - FrameContext 统一输入结构
   - `scene_node.py` - SceneNode 统一场景节点数据结构
   - `scene_node_layer.py` - SceneNodeLayer 场景节点感知层

3. **创建核心功能模块**：
   - `direction_evaluator.py` - DirectionEvaluator 方向检测器
   - `environment_scanner.py` - EnvironmentScanner 环境扫描器

4. **集成到现有系统**：
   - 在 `web_test_server.py` 中导入新模块
   - 保持向后兼容，不破坏现有调用

---

## 【代码风格要求】

- 使用 Python 3.9+ 类型注解
- 使用 `@dataclass` 定义数据结构
- 使用 `logging.getLogger(__name__)` 进行日志记录
- 所有公共方法必须有文档字符串
- 遵循 PEP 8 代码规范

---

## 【注意事项】

- 不要删除或修改现有的 `direction_estimator.py` 和 `path_evaluator.py`
- 新模块应该是增强版本，可以与旧模块共存
- 所有接口设计要考虑未来扩展性
- 保持代码简洁，避免过度设计

---

请在修改前先输出完整的差异规划（diff plan），确认后再执行代码变更。

