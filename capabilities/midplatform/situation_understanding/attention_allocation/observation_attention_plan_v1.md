# Luna — Observation Attention & Value Assessment Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Allocation-Planning-v1-001`  
**Layer:** L1 Situation Understanding → Attention Allocation  
**Mode:** Planning only — Active Perception（主动感知）— 决定「现在有没有必要理解」，非识别细节。

---

## 1. 核心问题

Ownership 解决「信息属于谁」，Attention 解决「现在有没有必要理解它」。

人类进入商场不会 OCR 所有广告、分割所有人物。分层观察：

```
Image Stream
      ↓
L0 快速环境扫描 (Observation Scan)
      ↓
Situation Understanding — 环境价值判断
      ↓
Attention Allocation — 观察资源投入
      ↓
Region Intelligence (仅高价值区域)
      ↓
Deep Understanding
```

---

## 2. L1 内部结构

```
L1 Situation Understanding
    ├── Scene Understanding
    ├── Attention Allocation          ← 本阶段
    ├── Region Intelligence (下游)
    └── Evidence Completeness
```

---

## 3. 三层机制

### 第一层：快速观察（低成本）

输出：`scene_profile_candidate`, `environment_summary_candidate`, `attention_priority_candidate`

**禁止：** OCR、Qwen、复杂模型

### 第二层：价值判断

同样是文字，不同处理：

| 区域 | 任务 find_exit | 价值 |
|------|----------------|------|
| 开往嘉会湖 | 导航相关 | high |
| 夏季饮料优惠 | 任务无关 | low |

### 第三层：Observation Budget Manager

任务 `find_subway_exit`：

- Direction signs: 80%
- Exit symbol: 15%
- Advertisement: 5%

---

## 4. 与 Model Manager

```
Situation: 我需要知道什么？
Attention: 哪里值得看？
Model Manager: 需要什么能力？
Collaboration: 怎么组合？
```

**不是：** 看到图片 → 调用模型

---

## 5. 解决 SAM 式「全部分割」问题

```
快速观察 → 导视 priority very high → 仅导视深入 Ownership+Channels
广告 priority low → 不触发 Region Intelligence
```

---

## 6. 下一阶段

`Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Allocation-DryRun-v1-001`
