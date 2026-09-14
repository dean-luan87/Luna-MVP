# 跨域旁路：统一主线编排入口最小实现计划（V1）

## 1. 目标

当前三条旁路能力（`risk_interrupt_v1` / `sidewalk_nav_v1` / `retail_find_item_v1`）都已完成 Level 1 / whitebox-only 的真实主线接入，并且最小编排规则已写死。  
但实现层仍是“**分散 hook**”：三条旁路分别在 `voice_final_text_dispatcher` 中以独立 helper 的方式被调用。

本计划的目标是：把“分散 hook”推进到“**统一主线旁路编排入口**”，形成一个最小 orchestrator（仍只服务 whitebox-only 阶段），从而：

- 固定顺序逻辑不再散落
- context 分发与 metadata 收集有统一位置
- 压制规则由 orchestrator 统一持有，避免每条旁路重复实现
- 为未来 `submit` 实链、speaking/runtime 接入、以及 Level 2 演进提供唯一生长点

本文件只做最小实现计划：**不直接改代码**，不扩功能、不做 Level 2、不做 speaking/runtime 接管、不重写全局裁决器。

---

## 2. 当前现状（简要）

### 2.1 当前接入点（事实）

- 三条旁路都在 `capabilities/voice/runtime/voice_final_text_dispatcher.py` 的真实主线分流路径中接入。
- 形式为 3 个独立 helper（示例命名）：
  - `_maybe_attach_risk_interrupt_v1_whitebox(...)`
  - `_maybe_attach_sidewalk_nav_v1_whitebox(...)`
  - `_maybe_attach_retail_find_item_v1_whitebox(...)`
- 顺序与压制逻辑虽已有规则文档，但在实现上仍以“多个 helper 串联”表达，存在持续增长风险。

### 2.2 已写死的规则（作为计划输入）

- 统一 `context/metadata` 规范：见《`LUNA_CROSS_DOMAIN_CONTEXT_METADATA_CONVENTION_V1.md`》
- 最小编排规则：见《`LUNA_CROSS_DOMAIN_MIN_ORCHESTRATION_V1.md`》

---

## 3. 统一入口的最小职责（V1 写死只做 4 件事）

第一版 orchestrator 只做：

1. **按固定顺序调用三条旁路**
   - `risk_interrupt_v1` → `sidewalk_nav_v1` → `retail_find_item_v1`
2. **传递统一 runtime context**
   - 输入：`VoiceRuntimeContext`（只读使用 `metadata` 中的摘要 key）
3. **收集三条旁路 metadata**
   - 输出：把三条旁路的白盒 key 并入 `VoiceFinalTextDispatchResult.metadata`
4. **应用最小压制规则（仅白盒层）**
   - 若高风险/抢占标记存在：后两条旁路强制只留白盒（`final_spoken_output=""` + `output_suppressed_by_risk=true`）

强调：第一版 orchestrator **不生成输出候选、不提交 SpeechRequest、不参与全局裁决**。

---

## 4. 建议代码落点（候选与推荐）

### 4.1 候选 A：在 `voice_final_text_dispatcher` 内提一个统一 helper（推荐）

做法：

- 在 `voice_final_text_dispatcher.py` 内新增单一入口函数，例如：
  - `_apply_cross_domain_bypasses_v1(res, event, runtime_context) -> res2`
- 将三条旁路的 helper 调用与顺序逻辑收敛到该函数中。

优点：

- 改动面最小（仍在同一文件/同一主线分流点）
- 易于保证“默认关闭零侵入”
- 便于回退：出现问题可快速恢复为原串联模式

缺点：

- orchestrator 仍与 voice dispatcher 同文件（但 V1 可接受）

### 4.2 候选 B：新增轻量 cross-domain orchestrator 模块（次选）

例如新增：

- `capabilities/cross_domain/orchestrator_v1.py`

由 `voice_final_text_dispatcher` 调用 orchestrator，得到合并后的 metadata。

优点：更清晰的模块边界  
缺点：引入新模块与 import 路径，V1 的“最小实现计划”阶段不一定必要。

### 4.3 当前推荐方案（写死）

推荐 **候选 A**：先在 `voice_final_text_dispatcher` 内提统一 helper（最小改动、最易回退）。  
当未来出现更多旁路、或需要跨 voice/vision 多入口复用时，再演进到候选 B。

---

## 5. 第一版不做项（写死）

- 不做跨旁路融合输出
- 不做全局打分
- 不做动态调度
- 不做 Level 2
- 不做 speaking/runtime 接管
- 不重写全局裁决器

---

## 6. 与现有三条旁路的边界（哪些留在旁路内，哪些上提）

### 6.1 仍保留在各旁路内部的逻辑（写死）

- 各自的 gating/场景判断（例如 retail 的 gating、sidewalk 的 scene 判定）
- 各自的白盒结构定义与字段填充
- 各自的开关读取（enable/whitebox-only）

### 6.2 必须上提到 orchestrator 的逻辑（写死）

- **调用顺序**：不再由多个 if/return 分散表达，应由统一入口持有
- **最小压制规则**（跨旁路共享部分）：
  - 统一读取 `risk_summary_v1`（及抢占标记），并形成“本轮压制信号”
  - 统一把压制信号传递给后两条旁路（或以统一约定的方式让后两条只白盒）

### 6.3 orchestrator 统一持有的字段/规则（V1）

- `risk_summary_v1` 的读取优先级（context 为主）
- “高风险/抢占标记”对非安全链的压制口径（只白盒、不外显）
- 三条白盒写入顺序（稳定、可对账）

---

## 7. 验证与回退（实现后怎么保证不改行为）

### 7.1 验证建议

第一版实现后，必须验证：

- 三条旁路各自的深接入验证脚本仍全部通过（行为不变）
- 默认关闭时仍零侵入（metadata 不出现旁路 key）
- 三条白盒 key 共存时不互相覆盖、字段结构不变

### 7.2 回退方式

若出现异常，回退策略应支持“秒级止血”：

- 直接回退到“分散 helper 串联调用”的旧实现（同文件内可回滚）
- 或通过总开关（各能力 enable=0）立即停用旁路（保持主线稳定）

---

## 一句话收束

先把三条旁路从“分散 hook 串联”收成“统一编排入口”的最小实现计划写清楚（仍只服务 Level 1 / whitebox-only），再进入后续真实代码收拢阶段，避免未来 Level 2/submit/speaking 接入时顺序与压制逻辑继续发散。

