# LUNA 主线 Guarded Trial 范围总定义 v0

**Phase**：Phase-Mainline-RuntimeReadiness-002  
**定位**：在 **R2_shadow_ready → R3_guarded_wiring_ready** 之前，将三条主线的 **trial 范围、开关、验收、回滚、TRW** 写成 **可冻结数据**；**不接 runtime、不改主链代码、不改默认 provider/env 语义**。

---

## 1. Trial 分轨（强制）

必须拆成 **三条互相独立** 的 trial，**禁止**单一总开关承载全部能力：

| 代号 | Trial | 入口 flag（默认 false） |
|------|--------|-------------------------|
| A | YOLO guarded trial | `LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1` |
| B | OCR guarded trial | `LUNA_ENABLE_OCR_GUARDED_TRIAL_V1` |
| C | Qwen Voice governed entry trial | `LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1` |

**Global kill switch**（与上表正交）：

- `LUNA_DISABLE_ALL_GUARDED_TRIALS`（默认 false；为 **true** 时 **禁止** 所有 A/B/C，即使分项为 true）

**优先级**：`global disable` > `capability entry flag` > `provider/mode 子闸`。

---

## 2. 统一 TRW / RequestTrace 策略（摘要）

若 `trace_id` / `session_id` 缺失：**不得伪造**；必须记入 `missing_fields`；**禁止**将 trial **升级到** `controlled_provider` 模式。

完整字段表见：`mainline_guarded_trial_trw_requirement_matrix.json`（生成路径见 Phase-002 `logs/`）。

---

## 3. Readiness 上限

任一 trial **验收通过** 后，允许宣称的最高级别仍为 **R3_guarded_wiring_ready**；**不得**在本 Phase 文档或产物中宣称 R4/R5。

---

## 4. 产物与工具

| 产物 | 说明 |
|------|------|
| `tools/run_mainline_guarded_trial_definition_v0.py` | 生成 JSON 矩阵 |
| `tools/verify_mainline_guarded_trial_definition_v0.py` | 校验产物完整性 |
| `logs/mainline_guarded_trial_definition_002_<timestamp>/` | 输出根目录 |

---

## 5. 分文档索引

- YOLO：`LUNA_YOLO_GUARDED_TRIAL_DEFINITION_V0.md`
- OCR：`LUNA_OCR_GUARDED_TRIAL_DEFINITION_V0.md`
- Qwen Voice：`LUNA_QWEN_VOICE_GUARDED_TRIAL_DEFINITION_V0.md`
- Env / kill switch：`LUNA_MAINLINE_GUARDED_TRIAL_ENV_FLAG_KILL_SWITCH_MATRIX_V0.md`
- Acceptance / rollback playbook：`LUNA_MAINLINE_GUARDED_TRIAL_ACCEPTANCE_AND_ROLLBACK_PLAYBOOK_V0.md`
- GO 包：`LUNA_MAINLINE_GUARDED_TRIAL_GO_NO_GO_PACK_V0.md`

---

**一句话**：001 说明当前只能到 R2；002 把「怎么安全升到 R3」写成 **可执行手册与 JSON**，但仍 **不真正接线**。
