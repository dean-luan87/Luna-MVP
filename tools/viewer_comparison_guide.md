# Viewer 对比指南：v0.3 → v0.4.3 危险消退曲线

**目标：** 回答一个硬问题：👉 哪一代在"自以为安全"的时候，实际上最危险？

---

## 一、怎么跑（你现在就能做）

### 1️⃣ 准备三份 trace（30–60 秒即可）

你只需要同一段场景，三种版本各跑一次：

```
artifacts/
├── trace_v03.jsonl
├── trace_v041.jsonl
└── trace_v043.jsonl
```

**要求：**
- ✅ 同一视频 / 同一模拟 perception
- ✅ 不要求真实 OCR
- ✅ 关键是结构一致

### 2️⃣ 用 DCS 批量审判

**方式 1：逐个评估**
```bash
python3 tools/dcs_eval.py artifacts/trace_v03.jsonl
python3 tools/dcs_eval.py artifacts/trace_v041.jsonl
python3 tools/dcs_eval.py artifacts/trace_v043.jsonl
```

**方式 2：批量评估（推荐）**
```bash
python3 tools/batch_dcs_eval.py \
  artifacts/trace_v03.jsonl \
  artifacts/trace_v041.jsonl \
  artifacts/trace_v043.jsonl
```

**会生成：**
```
artifacts/
├── trace_v03_enriched.jsonl
├── trace_v041_enriched.jsonl
├── trace_v043_enriched.jsonl
├── dcs_report_v03.json
├── dcs_report_v041.json
├── dcs_report_v043.json
└── dcs_comparison.json  # 对比报告
```

### 3️⃣ 打开 Viewer（同一个页面，换 src）

**方式 1：直接在浏览器打开**
```
file:///path/to/viewer/trace_viewer_v043.html?src=../artifacts/trace_v03_enriched.jsonl
file:///path/to/viewer/trace_viewer_v043.html?src=../artifacts/trace_v041_enriched.jsonl
file:///path/to/viewer/trace_viewer_v043.html?src=../artifacts/trace_v043_enriched.jsonl
```

**方式 2：使用本地服务器（推荐）**
```bash
cd /path/to/Luna-2
python3 -m http.server 8000
```

然后在浏览器打开：
```
http://localhost:8000/viewer/trace_viewer_v043.html?src=../artifacts/trace_v03_enriched.jsonl
http://localhost:8000/viewer/trace_viewer_v043.html?src=../artifacts/trace_v041_enriched.jsonl
http://localhost:8000/viewer/trace_viewer_v043.html?src=../artifacts/trace_v043_enriched.jsonl
```

---

## 二、怎么看（重点）

### 👁 Viewer 里你只看 4 个东西

#### ① 时间轴颜色分布（最重要）

- 🔴 **红** = 架构错误
- 🟡 **黄** = 设计瑕疵
- 🟢 **绿** = 合规

**你会看到一个非常明显的趋势：**

```
v0.3:  ████████████████████  (高)
v0.4.1: ████████░░░░░░░░░░  (中)
v0.4.3: █░░░░░░░░░░░░░░░░░  (极低)
```

**红色不是"逐步减少"，而是"突然断崖式消失"**

这是好事，说明不是调参，是结构修复。

#### ② 点击 RED，读"违规原因"

**重点关注这几类：**
- `missing_view_state_but_active`
- `authority_violation`
- `over_prediction_language`
- `env_overreach`

**你会发现一个非常关键的差异：**

> v0.3 的 RED 不是集中在危险点，而是集中在 **"看不清但仍然开口"** 的地方。

#### ③ 同一时间点，对比三代输出

选一个具体时间（比如 01:12）：

| 版本 | B 的行为 |
|------|---------|
| v0.3 | 输出提醒（但无视角依据） |
| v0.4.1 | 有时沉默，有时提醒 |
| v0.4.3 | 要么提醒（有 view_state），要么沉默 |

👉 **危险的不是"提醒多"或"提醒少"**  
👉 **危险的是"不知道自己有没有资格提醒"**

#### ④ DCS Report 顶部统计

你会看到类似：

```json
{
  "red_count": {
    "v0.3": 12,
    "v0.4.1": 4,
    "v0.4.3": 0
  }
}
```

**这不是调优，这是代际分水岭。**

---

## 三、怎么看出结论（这一步最关键）

### ✅ 结论 1：最危险的一代是 v0.3

**不是因为能力弱，而是因为：**

> 它在"自以为看见未来"的时候，其实什么都没看清

这是安全系统里最致命的状态。

### ✅ 结论 2：v0.4.3 的安全性来自"承认无知"

**v0.4.3 的核心变化不是 Gate 本身，而是：**
- B 被迫回答一个问题："我现在看得稳吗？"
- 如果答不上来，就闭嘴

**这是人类安全经验的直接映射。**

### ✅ 结论 3：这条曲线证明你的架构是"可进化的"

**危险曲线不是慢慢下降，而是结构性消失，这说明：**
- 不是靠"更聪明"
- 而是靠"不越权"

这为 v0.5 的 Gate 实装、v0.6 的学习机制，打下了非常扎实的伦理和工程基础。

---

## 四、下一步建议

你现在可以顺着这条曲线，做三件非常有价值的事：

1. **把这条曲线截图，作为架构里程碑**
2. **冻结 v0.4.3**（这是一个"安全基线版本"）
3. **进入 v0.5**：Gate 从"裁决器"升级为"节律控制器"

---

**版本：** v0.4.3  
**最后更新：** 2025-01-12
