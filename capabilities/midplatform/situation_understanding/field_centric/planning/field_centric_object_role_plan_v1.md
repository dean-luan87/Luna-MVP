# Luna — Field-Centric Object Role Planning v1

**Phase:** `Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-Planning-v1-001`  
**Principle:** Luna 的核心不是识别物体，而是理解「场」。  
**Mode:** Planning only — deterministic fixture。

---

## 核心原则（冻结）

不是先问「这是什么物体？」，而是先问：

1. 我现在处在什么场？
2. 这个场里通常有哪些角色、物体、规则、风险和任务？
3. 眼前这个东西在这个场里可能承担什么功能？

**不是识别世界，而是在场中理解世界。**

---

## L1 架构（更新）

```
L1 Situation Understanding
    ↓
Field Understanding              ← 本阶段核心
    ↓
Role / Object / Behavior Expectation
    ↓
Attention Allocation
    ↓
Region Intelligence
    ↓
Interaction Graph
    ↓
Object Role Inference
    ↓
Model Manager / Tool OS
```

---

## 场决定四件事

1. **什么东西可能出现** — Unknown Object 候选空间被场约束
2. **什么行为合理** — 行为意义 = 动作 + 场 + 作用对象 + 结果
3. **什么信息有价值** — Attention 从 Field + Goal 继承，非视觉显著性
4. **什么风险需关注** — 安全理解 Field-first

---

## 管线

```
Field Understanding
    ↓
Expected Entity / Behavior / Information / Risk Profile
    ↓
Interaction Graph
    ↓
Object Role Candidate
    ↓
Unresolved Object Memory
```

---

## 下一阶段

`Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001`
