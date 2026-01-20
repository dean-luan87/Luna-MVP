# B2 v0.5 自动化验收脚本总结

## ✅ 已完成

### 1. 验收脚本实现
- **文件**: `vision_pipeline/b2/v03/validation/b2_v05_validation.py`
- **功能**: 将 Step 1-7 的 Check List 转化为可执行的自动化验收脚本

### 2. 验收项目覆盖

#### Step 1: Gate
- ✅ Gate 是否是第一步执行
- ✅ Gate Mode 是否只存在 3 种
- ✅ Gate 输入是否结构化
- ✅ Gate 输出是否写入 trace
- ✅ Gate 规则是否严格

#### Step 2: Evidence Lifecycle
- ✅ 是否禁止瞬时判断
- ✅ Evidence 状态是否只用 4 种
- ✅ 每个 Evidence 是否包含必要字段

#### Step 3: Trigger
- ✅ Trigger 是否是显式步骤
- ✅ 不触发条件是否齐全
- ✅ Trigger 结果是否写 trace

#### Step 4: Impact Evaluation
- ✅ 判断问题是否唯一
- ✅ ActionImpact 是否只允许指定枚举
- ✅ ENV 是否永不直接产生 impact
- ✅ FORCE_ALERT 是否唯一干预路径

#### Step 5: B → C Contract
- ✅ B → C 是否只有一个出口
- ✅ 输出结构是否固定
- ✅ 是否遵守权限边界

#### Step 6: Runtime Trace
- ✅ 是否每一帧都有 trace
- ✅ Trace 是否包含完整字段
- ✅ Timeline 是否干净

#### Step 7: Web Visualization
- ✅ 是否能回放任意时间点
- ✅ 可视化是否只依赖 trace

#### 全局禁止项
- ⛔ 引入 OCR
- ⛔ 引入学习/自适应
- ⛔ 合并 B/C 职责
- ⛔ 输出 WORLD/SCENE 级语义
- ⛔ NO_OP 写入 timeline

#### 最终验收标准（三个问题）
1. 任意一帧，能不能说清楚：为什么 B 没工作/工作了？
2. 任意一条 timeline，能不能倒推出当时的视角状态？
3. 删掉 timeline，只看 trace，系统是否仍然完整可理解？

## 📊 使用方法

```bash
# 基本用法（只检查代码）
python vision_pipeline/b2/v03/validation/b2_v05_validation.py \
    vision_pipeline/b2/v03/b2_v03.py

# 完整验收（代码 + Trace 样本）
python vision_pipeline/b2/v03/validation/b2_v05_validation.py \
    vision_pipeline/b2/v03/b2_v03.py \
    traces/b2_runtime_trace_v05.jsonl
```

## 🎯 输出格式

验收脚本会输出：
- ✅ 通过的检查项
- ⚠️ 警告项
- ❌ 失败的检查项

**退出码**:
- 0: 所有检查项通过
- 1: 存在失败项

## 🔄 集成到 CI/CD

可以在 CI/CD 流程中自动运行验收脚本，确保每次代码变更都符合 v0.5 规范。

## 📝 下一步

1. 运行验收脚本检查当前代码
2. 根据验收结果修复不符合项
3. 集成到 CI/CD 流程
