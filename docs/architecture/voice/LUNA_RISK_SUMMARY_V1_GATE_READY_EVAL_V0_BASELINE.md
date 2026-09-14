# risk_summary_v1 Gate-Ready Eval v0 — Baseline / Freeze（冻结）

**文件**：`docs/architecture/voice/LUNA_RISK_SUMMARY_V1_GATE_READY_EVAL_V0_BASELINE.md`  
**性质**：Topic 03（Risk Gate）下当前**唯一已落地**的“只读 gate-ready 评估层”冻结面（不是 Risk Gate）。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  
- `docs/architecture/voice/LUNA_CONFLICT_TOPIC_03_RISK_GATE_V0.md`  
- `docs/architecture/voice/LUNA_RISK_SUMMARY_V1_GATE_READY_CONTRACT.md`  
- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`

---

## A. 当前基线范围

当前只批准一个 Topic 03 下的只读评估层：

- **`risk_summary_v1 Gate-Ready Eval v0`**

当前只做：
- 字段完整性检查  
- 口径合法性检查  
- gate-ready 可用性评估（是否满足契约最小要求）

当前未做：
- Risk Gate 拦截  
- 风险准入裁决  
- 用户协商策略  
- 文本 vs 视角冲突处理  
- 白盒 / provenance / 审批流实现

---

## B. 当前系统定位（写死）

- 这是一个**只读 gate-ready 评估层**。  
- 它只输出“是否满足未来 gate-ready 契约”的评估结果。  
- 它**不是 Risk Gate**。  
- 它不决定是否进入 submit。  
- 它不改 `dispatch_type`。  
- 它不改 `bridge_decision.route`。  
- 它不改 `proposal.device_action`。  
- 它不改现有 **Resource / Information** 两个 gate 的行为（见 `LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`）。

---

## C. 当前唯一输入来源（写死）

### C1. 输入对象

- **只读** `risk_summary_v1`

### C2. 读取口径

- 优先使用当前 dispatcher 的统一读取方式：  
  `voice_final_text_dispatcher._risk_summary_v1_for_orchestrator_observation(...)`  
  （优先 `runtime_context.metadata["risk_summary_v1"]`，缺失回退 `event.metadata["risk_summary_v1"]`）

### C3. 明确不读取（写死）

当前不读取以下任何键（它们都不是 gate-ready 评估输入）：
- `sidewalk_env_summary_v1`  
- `retail_env_summary_v1`  
- `vision_shadow`  
- `semantic_v2_shadow`  
- `semantic_v2_assist_*`

---

## D. 当前评估内容（写死）

当前只评估这些字段（严格按契约最小集合，不扩展）：
- `risk_level`  
- `risk_type`  
- `risk_reason`  
- `confidence`  
- `source`  
- `is_gate_ready`

并且口径写死：
- `risk_level` 合法值仅：`none | warning | high`  
- `confidence` 必须为数值  
- `is_gate_ready` 必须为布尔值

---

## E. 当前输出结构（冻结）

输出位置固定为：
- `result.metadata["risk_summary_v1_gate_ready_eval_v0"]`

### E1. 通过（示例形态）

```json
{
  "gate_ready_passed": true,
  "eval_scope": "risk_summary_v1_gate_ready_v0",
  "risk_level_seen": "high",
  "source_seen": "xxx"
}
```

### E2. 不通过（示例形态）

```json
{
  "gate_ready_passed": false,
  "eval_scope": "risk_summary_v1_gate_ready_v0",
  "missing_fields": ["risk_reason", "source"],
  "invalid_fields": ["confidence"]
}
```

### E3. 不存在（示例形态）

```json
{
  "gate_ready_passed": false,
  "eval_scope": "risk_summary_v1_gate_ready_v0",
  "not_present": true
}
```

并明确写死：
- 当前不加时间戳、位置、坐标等字段  
- 当前评估结果只用于观察，不用于拦截

---

## F. 当前明确禁止项（写死）

- 不允许把 `gate_ready_passed == true` 解释成“现在就该拦截”  
- 不允许把 `risk_level == high` 自动升格成 Risk Gate 条件  
- 不允许在本 baseline 上顺手实现 Risk Gate  
- 不允许用视觉摘要/语义影子补齐缺失字段  
- 不允许 voice 本地生成风险事实（No Fabrication）

---

## G. 当前验证入口（冻结）

当前阶段最小验证入口为：
- `tools/verify_risk_summary_v1_gate_ready_eval_v0.py`  
- `tools/verify_voice_v1_minimal_flow.py`

写死要求：
- 改到评估字段、读取方式、metadata 结构、落点时，必须重跑以上两个脚本。  
- 这两个脚本构成当前阶段最小回归入口（不足则在后续专项补齐，但不得在本 baseline 内扩成框架）。

---

## H. 与 Admission Layer 的关系（写死）

- 当前 admission layer 只正式包含（冻结）：  
  - Resource Sufficiency Gate v0  
  - Information Confirmation Gate v0  
  （见 `LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`）
- `risk_summary_v1` eval 层目前**不属于 gate**。  
- 它只是未来 Risk Gate 的**前置观察层**。  
- 后续若要进入真正 Risk Gate，必须单开专项，并以本 baseline + contract 为前置。

---

## I. 下一阶段前置条件（写死）

- 在实现 Risk Gate 前，必须保持本评估层冻结（不得“先改评估、再顺手拦截”）。  
- 若后续要改变 `risk_level` 分层、字段集合、来源口径，必须专项评审。  
- 后续 Risk Gate 只能消费满足 contract 且经评估可用的 `risk_summary_v1`。  
- 但不得跳过额外设计直接把 eval 结果当拦截条件（Topic 03 仍需单独实现与冻结）。

