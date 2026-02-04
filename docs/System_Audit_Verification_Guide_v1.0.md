# System Audit & Verification Guide v1.0
# （Explain / Risk / Authority 非越权审计流程）

本文档描述 Luna 系统在 冻结版本前 的人工 + 自动审计流程，
目标是验证：
观测、解释、风险评估模块不参与、不污染、不反向影响任何裁决逻辑。

---

## 一、审计目标（What we are verifying）

在任何 release 版本中，系统必须满足以下事实：
1. Risk Layer 不影响决策
2. Explain Layer 不影响决策
3. Debug / Observe 层仅用于回放与分析
4. Authority / C / BC 的裁决路径不可被旁路读取或修改

本审计流程只验证 结构正确性与越权隔离，
不评估“决策是否聪明”或“模型是否准确”。

---

## 二、审计输入：Freeze Fixtures（世界状态样本）

### 1️⃣ 什么是 Freeze Fixture

Freeze Fixture 是一个 世界状态快照（World State Snapshot），仅包含：
- 世界事实（障碍、速度、位置等）
- 系统事实（perception_state / gate / hardware）
- 上下文信息

严格禁止包含：
- decision / reason / selected_result
- authority / abilities
- risk / explain / evaluation 输出

路径示例：

tests/freeze/fixtures/
├── F-01_clear_safe_world.json
├── F-02_static_obstacle_approaching.json
├── F-03_dynamic_crossing.json
├── F-04_perception_unstable.json
└── F-05_hardware_failure.json

这些文件是长期资产，不可随意修改。

---

## 三、自动校验流程（必须全部通过）

### Step 1：不变式校验（Invariant Tests）

python3 -m pytest tests/invariants -v

验证内容：
- B / C / BC / Risk / Explain 不读取禁止字段
- 输出字段集合被严格约束

---

### Step 2：Explain Layer 无害性校验

python3 -m pytest tests/explain_layer -v

验证内容：
- Explain 只读 Risk Phase-3 输出
- 不读取 decision / authority / c_decision
- 输出为纯描述性标签

---

### Step 3：Risk → 决策隔离校验

python3 -m pytest tests/test_risk_bc_integration.py -v

验证内容：
- risk 字段不影响 decision / reason
- 裁决路径与 risk 解耦

---

### Step 4：Freeze Fixture 回放一致性

python3 -m pytest tests/freeze -v

验证内容：
- 固定世界状态 → 行为稳定
- 不因 Explain / Risk 接入产生结构变化

---

### Step 5：RA-View 后视性验证（只读）

python3 -m pytest tests/observe -v

验证内容：
- Risk × Authority 只读关联
- 不存在裁决字段泄露

---

## 四、人工审计流程（冻结前必做）

### Step 6：DebugView 回放（人工）

#### 1️⃣ 从 Freeze Fixture 生成运行记录

python3 tools/run_from_fixtures.py \
  --fixtures tests/freeze/fixtures/F-02_static_obstacle_approaching.json \
  --enable-debug-view \
  --out runs/debug_sample.jsonl

#### 2️⃣ 导出 DebugView

python3 tools/debug/dump_debug_view.py runs/debug_sample.jsonl

#### 3️⃣ 人工检查要点
DebugView 输出中 必须满足：
- timeline 非空
- 不包含以下字段：
  - decision
  - reason
  - selected_result
  - abilities
  - risk / authority / envelope 为描述性状态

---

## 五、Freeze Gate（Release Only）

在 main 分支 push 时，系统会自动触发：

.github/workflows/freeze-gate.yml

该 Gate 会执行：

pytest tests/freeze -v

失败即拒绝 release。

Freeze Gate 不在 PR 阶段触发，
只作为最终版本冻结前的安全闸门。

---

## 六、重要原则（必须遵守）
- Debug / Explain / Observe 永远是 旁路系统
- 所有解释均为 事后描述
- 任何“更聪明”的解释能力，必须等情感引擎阶段统一设计
- 如果一个模块需要“知道为什么系统这么做”
  → 它 不应该存在于裁决链路中

---

## 七、版本状态
- Explain Layer：explain.v1.frozen
- DebugView：debugview.v1
- Risk Phase-3：risk.phase3.v1
- RA-View：risk_authority_view.v1.2

本审计流程适用于以上冻结版本。

---

✅ 总结一句话

系统不是因为“很聪明”才值得信任，
而是因为它在任何时候都能被验证“没有越权”。
