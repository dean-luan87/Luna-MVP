# v1.8.5 Phase B 工程级测试指南

## 一、测试目标（边界明确）

### ❌ 这轮测试不做的事
- ❌ 不验证识别准不准
- ❌ 不评估模型效果
- ❌ 不引入新功能
- ❌ 不调参、不优化

### ✅ 这轮测试只验证 4 件事
1. **系统是否能完整跑通**（不崩溃是第一优先级）
2. **Pipeline 各阶段是否被正确调用**（LV1 → LV2 → LV3 → LV4 → WorldUpdate → SceneState）
3. **输入 / 输出是否结构正确**（NavigationResult / ModelingResult / WorldUpdate / SceneState）
4. **性能是否在可接受范围内**（不爆炸，单帧 < 1s，连续帧线性增长）

---

## 二、测试脚本位置

**文件路径**: `tests/test_phase_b_pipeline.py`

**测试脚本包含**:
- Layer 1: 系统冒烟测试（`test_pipeline_single_frame()`）
- Layer 2: Pipeline 链路测试（`test_pipeline_linkage()`）
- Layer 3: 性能 & 观测测试（`test_pipeline_multiple_frames()`）
- 降级路径测试（`test_degradation_paths()`）

---

## 三、运行测试

### 3.1 基本运行

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tests/test_phase_b_pipeline.py
```

### 3.2 测试图片准备

测试脚本会自动尝试加载以下路径的测试图片：
1. `tests/assets/test_frame.jpg`
2. `data/scene_images/test.jpg`
3. `营业执照.jpg`

如果找不到测试图片，脚本会自动创建一个随机测试帧（640x480 彩色噪声图像）。

### 3.3 预期输出

测试脚本会输出：
- ✅ 每个阶段的执行状态
- ✅ Pipeline 各阶段的调用情况
- ✅ NavigationResult / ModelingResult 的结构验证
- ✅ WorldUpdate → SceneState 的完整链路验证
- ✅ 性能统计（总耗时、平均耗时、最小/最大耗时）
- ✅ 性能恶化检测（如果存在）

---

## 四、测试重点观察项

### 4.1 是否有异常抛出（第一优先）

**需要关注的异常类型**:
- `TypeError`: 参数没迁移干净（例如：`build_state()` 仍在使用旧参数）
- `AttributeError`: 某层还在假设旧字段（例如：`NavigationResult` 缺少 `objects` 字段）
- `NoneType` 错误: 降级路径没兜住（例如：`pipeline_result` 为 `None`）

**检查方法**:
- 查看测试输出中的异常堆栈
- 确认异常发生在哪个阶段（LV2 / LV3 / LV4.1 / LV4.2 / WorldUpdate / SceneState）

### 4.2 Pipeline 是否真的"全跑了一遍"

**应该看到**:
- ✅ `LV2 Quality Gate: passed=True/False`
- ✅ `LV3 Semantic Router: route=navigation/non_navigation`
- ✅ `LV4.1 Navigation Executor: 已执行`（如果路由到 navigation）
- ✅ `LV4.2 Modeling Executor: 已执行`（应该总是执行）
- ✅ `WorldUpdate 构建成功`
- ✅ `SceneState 构建成功`

**如果某一步没跑**:
- 说明 Phase B 的假设有偏差
- 需要检查 `PipelineController.process_frame()` 的逻辑
- 需要检查路由逻辑是否正确

### 4.3 性能是否"指数恶化"

**正常情况**:
- 单帧 < 1s（哪怕 0.8s 也 OK）
- 连续帧时间线性增长（第一帧 0.3s，后续帧也接近 0.3s）

**异常情况**:
- 第一帧 0.3s，后面 2s、3s → 说明有缓存/状态泄漏
- 平均耗时 > 1s → 需要检查性能瓶颈

**检查方法**:
- 查看性能统计输出
- 检查是否有性能恶化警告

---

## 五、测试结果解读

### 5.1 所有测试 PASSED

**含义**:
- ✅ Phase B 迁移成功
- ✅ 系统可以正常运行
- ✅ Pipeline 链路完整
- ✅ 性能在可接受范围内

**下一步**:
- 可以进入 Phase C 或其他后续阶段

### 5.2 部分测试 FAILED

**需要关注**:
- 哪个测试失败了？
- 失败的原因是什么？
- 是结构问题还是性能问题？

**常见问题**:
1. **TypeError / AttributeError**: 说明迁移不完整，需要检查调用点
2. **NoneType 错误**: 说明降级路径有问题，需要检查空值处理
3. **性能恶化**: 说明有缓存/状态泄漏，需要检查状态管理

---

## 六、测试脚本结构说明

### 6.1 test_pipeline_single_frame()

**功能**: Layer 1 系统冒烟测试

**验证内容**:
- PipelineController 初始化
- SceneStateBuilder 初始化
- PipelineController.process_frame() 执行
- 返回结果结构验证
- NavigationResult / ModelingResult 结构验证
- WorldUpdate 构建
- SceneState 构建

### 6.2 test_pipeline_linkage()

**功能**: Layer 2 Pipeline 链路测试

**验证内容**:
- LV2 Quality Gate 是否被调用
- LV3 Semantic Router 是否被调用
- LV4.1 Navigation Executor 是否被调用（如果路由到 navigation）
- LV4.2 Modeling Executor 是否被调用
- WorldUpdate → SceneStateBuilder 链路是否完整

### 6.3 test_pipeline_multiple_frames()

**功能**: Layer 3 性能 & 观测测试

**验证内容**:
- 连续 N 帧的执行时间
- 是否有性能指数恶化
- 平均耗时是否在可接受范围内

### 6.4 test_degradation_paths()

**功能**: 降级路径测试

**验证内容**:
- 空的 WorldUpdate（objects 和 texts 都为空）
- 只有 objects 的 WorldUpdate
- 只有 texts 的 WorldUpdate

---

## 七、测试脚本使用建议

### 7.1 首次运行

**建议**:
1. 先运行单帧测试（`test_pipeline_single_frame()`）
2. 确认没有异常抛出
3. 再运行连续帧测试（`test_pipeline_multiple_frames()`）

### 7.2 调试模式

**如果需要详细日志**:
- 可以在测试脚本中添加 `logging.basicConfig(level=logging.DEBUG)`
- 或者修改 `PipelineController` 的日志级别

### 7.3 性能分析

**如果需要更详细的性能分析**:
- 可以在测试脚本中添加 `time.perf_counter()` 替代 `time.time()`
- 可以添加更细粒度的性能统计（每个阶段的耗时）

---

## 八、测试结果示例

### 8.1 成功输出示例

```
======================================================================
v1.8.5 Phase B Pipeline 工程级测试
======================================================================

=== Layer 1: 系统冒烟测试（能不能跑）===
[1/5] 初始化 PipelineController...
  ✅ PipelineController 初始化成功
[2/5] 初始化 SceneStateBuilder...
  ✅ SceneStateBuilder 初始化成功
[3/5] 准备测试帧...
  ✅ 加载测试图片: tests/assets/test_frame.jpg
[4/5] 执行 PipelineController.process_frame()...
  ✅ pipeline.process_frame() 完成，耗时: 0.523s
[5/5] 验证返回结果结构...
  ✅ pipeline_result 不为 None
  ✅ quality_result.passed = True
  ✅ route_result.route = navigation
  检查 NavigationResult...
    ✅ NavigationResult.objects: 3 个对象
  检查 ModelingResult...
    ✅ ModelingResult.content_candidates: 2 个候选
    提取的 texts: 1 个
    场景描述: 这是一个测试场景...
  构建 WorldUpdate...
    ✅ WorldUpdate 构建成功
      - objects: 3 个
      - texts: 1 个
      - confidence: 1.0
  构建 SceneState...
    ✅ SceneState 构建成功
      - scene_id: person_car_building
      - objects: 3 个
      - signs: 1 个
      - risk_level: low
      - stability: unstable

======================================================================
✅ Layer 1: 系统冒烟测试 PASSED
======================================================================
```

### 8.2 失败输出示例

```
======================================================================
❌ Layer 1: 系统冒烟测试 FAILED
错误: TypeError: build_state() got an unexpected keyword argument 'objects'
Traceback (most recent call last):
  File "tests/test_phase_b_pipeline.py", line 89, in test_pipeline_single_frame
    scene_state = scene_builder.build_state(
TypeError: build_state() got an unexpected keyword argument 'objects'
======================================================================
```

**解读**: 说明 `build_state()` 的调用点还没有完全迁移，需要检查调用代码。

---

## 九、测试完成后

### 9.1 如果所有测试 PASSED

**可以确认**:
- ✅ Phase B 迁移成功
- ✅ 系统可以正常运行
- ✅ 可以进入后续阶段

### 9.2 如果部分测试 FAILED

**需要**:
1. 记录失败的具体测试和错误信息
2. 分析失败原因
3. 修复问题后重新运行测试
4. 确认所有测试 PASSED 后再进入后续阶段

---

## 十、测试脚本维护

### 10.1 测试脚本更新

**当 Pipeline 结构发生变化时**:
- 需要同步更新测试脚本
- 确保测试脚本能够正确验证新的结构

### 10.2 测试数据准备

**建议**:
- 准备一些固定的测试图片
- 放在 `tests/assets/` 目录下
- 确保测试的可重复性

---

## 十一、总结

**这轮测试的目标**:
- 把"结构正确"变成"工程可信"
- 保护未来的每一次重构
- 确保系统能够稳定运行

**测试完成后**:
- 把测试结果（尤其是日志和耗时）记录下来
- 可以基于测试结果判断是否可以进入 Phase C
- 或者需要局部加固

---

## 十二、测试脚本位置

**文件**: `tests/test_phase_b_pipeline.py`

**运行命令**:
```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tests/test_phase_b_pipeline.py
```

---

**测试脚本已创建完成，可以直接运行验证 Phase B 迁移后的系统**


