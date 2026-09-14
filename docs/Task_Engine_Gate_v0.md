✅ TASK-ENGINE-GATE v0

规则：任一 NOT DONE → Task Engine 未完成 → 不允许进入 OCR/导航复杂流程

---

## A. 自动化验收（必须）
- pytest -q tests/tasks 全部通过
- 所有任务状态流转覆盖：
  - PENDING → ACTIVE
  - ACTIVE → COMPLETED / FAILED / CANCELLED
  - BLOCKED 不崩溃
- Task Engine 在 task 结束后正确清空 active_task

---

## B. 架构约束（强制）
- Task 只读 system_snapshot（不拉外部依赖）
- Task 不直接调用 TTS（只产出 SAY 事件）
- Task 不做安全裁决（不产生 STOP/HOLD）
- Task 只通过事件输出意图：SAY / TASK_STATE / TASK_STATE_PATCH

---

## C. 文案与播报约束
- 所有 SAY 事件只包含 template_key + slots
- 所有播报文本可回溯 template_key
- 模板缺失时有兜底文案，不崩溃

---

## D. C 互锁约束（关键）
- C=STOP 时：
  - 只允许播报 c_stop
  - 禁止播报任何 Task 指令
- C=HOLD 时：
  - 优先播报 c_hold
  - v0 禁止播报“继续执行”类 Task 文案
- C=PASS 时：
  - Task 播报正常放行

---

## E. Trace & 可回放
- 每个 tick 记录：
  - C 决策
  - Task events
  - Speech intents
- 同一 trace 可重复回放，输出一致
- 不存在“当时说了什么但现在无法复现”的情况

---

## F. 禁止项（命中即 FAIL）
- ❌ Task 内部直接执行动作（调用执行层）
- ❌ Task 内部自行判定安全并越权继续
- ❌ Task 内部写 snapshot
- ❌ 文案硬编码在 Task 里
