# LUNA Mainline Controlled Trial Order Policy v0

**Phase**：Phase-Mainline-GuardedTrial-001

---

## 1. 强制顺序（不得并发开启）

| Stage | Capability | 原因摘要 |
|-------|------------|----------|
| 1 | YOLO | 感知层，用户影响低，不触发语音输出链 |
| 2 | OCR | 文字层，不进入语义下游与输出链 |
| 3 | Qwen Voice | 输出链，用户影响风险最高，最后执行 |

---

## 2. 依赖规则

- Stage 2 **仅当** Stage 1 **GO**。  
- Stage 3 **仅当** Stage 1 **GO** 且 Stage 2 **GO**。  
- 任一 Stage **NO_GO** → 后续 Stage **不启动**（直至问题修复并重新 GO）。

---

## 3. 并发与 Kill

- **不允许**同时开启 YOLO + OCR + Qwen trial。  
- **Global kill switch**（`LUNA_DISABLE_ALL_GUARDED_TRIALS`）必须在运行手册中可达，用于紧急全关。
