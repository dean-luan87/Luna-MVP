# Luna Model Manager — Foundation Planning v1

**Phase:** Phase-P1-Midplatform-Luna-Model-Manager-Foundation-Planning-v1-001  
**Layer:** Model Manager（L2.5 之后，Tool OS / Teacher System 之上）  
**Status:** Foundation planning only — 收拢已有 Teacher 能力，不碎片化 Manager

## 1. 核心定位

模型是 Luna 的**工具**，不是约束者。Model Manager 统一：

- Teacher Registry / Routing / Evaluation / Provider Adapter
- 未来 OCR / Detection / SLAM / Depth / Speech / Memory 等

**禁止碎片化：**

```
Teacher Manager + OCR Manager + Vision Manager + Speech Manager ...
```

**目标统一框架：**

```
                 Luna Model Manager
                         |
    ------------------------------------------------
    |              |              |                |
Model Registry  Capability     Routing        Evaluation
               Registry       Engine          Engine
                         |
              Admission / Sandbox / Lifecycle
```

## 2. 架构位置

```
L1 Situation Understanding
        ↓
L2 Agent Planning
        ↓
L2.5 Decision Validation
        ↓
Model Manager                    ← 本层
        ├──────────────┬──────────────┐
        ↓              ↓              ↓
    Tool OS      Teacher System   (future models)
    OCR/SLAM     Qwen/Gemini/GPT
```

## 3. 前置成果（冻结引用）

| 模块 | 状态 |
|------|------|
| Teacher Adapter | 前置验证成果 → 纳入 Model Registry |
| Teacher Routing | 升级为 Model Routing Engine |
| Teacher Performance Evaluation | 升级为 Model Evaluation Engine |
| Qwen-VL Real Provider | 首个 external_teacher 条目 |

## 4. 六大组件

### 4.1 Model Registry
「Luna 有哪些能力提供者可以调用？」

### 4.2 Capability Registry
「谁提供 `unknown_scene_reasoning`？」— 能力优先，非模型优先。

### 4.3 Routing Engine
统一评分与选择 Tool / Model。

### 4.4 Evaluation Engine
统一评价 OCR_v1、Qwen、Gemini、SAM 等。

### 4.5 Admission Policy
Model Candidate → Security → Capability → Benchmark → Admission。

### 4.6 Model Lifecycle
candidate → sandbox → admitted → active → deprecated。

## 5. 核心原则

- Luna 想的是「我要什么能力」，不是「我要调 Qwen」
- Routing 输出 `routing_candidate`，不自动执行
- Evaluation 输出 `evaluation_candidate`，不自动改 policy
- Admission 门控后才进入 Available Pool

## 6. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Foundation-DryRun-v1-001`
