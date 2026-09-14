# LUNA OCR Bridge — Abort & Rollback Policy v0 (Phase-OCRBridge-Implementation-RFC-001)

## Abort 条件（任一满足即中止 forward / 事实层 / 下游消费）

1. **任一必填 `source_ref` 缺失**或 **`missing_fields` 非空**（实现阶段定义必填集）。  
2. **Pack validation failed**。  
3. **non-OCR evidence** 试图进入 **fact text layer**。  
4. **symbol / glyph** 被拼入 **事实文本** 或 `should_enter_raw_text` 违规。  
5. **`reading_order_uncertain`** 却生成 **global fact text**（或 `fact_text_layer_candidates` 非空且策略禁止）。  
6. **`quality_gate NO_GO`** 却进入 **eligible_text** 事实路径。  
7. **`runtime_integration`** 或 **`midplatform_invoked`** 等 **hard_audit** 意外为 true（仅 shadow 阶段应为 false）。  
8. **MidPlatform / SceneDelta / WorldContext** 被 **真实调用**（未授权）。  
9. **`world_write` / `hive_upload`** 被触发（未授权）。  
10. **trace / replay / audit 写入失败**（策略：fail-closed 或降级为仅 stderr，由实现 ADR 二选一，**默认 fail-closed**）。

---

## Rollback 动作（操作序；语义冻结）

1. 设置 **`LUNA_ENABLE_OCR_EVIDENCE_PACK_SHADOW_V1=false`**。  
2. 设置 **`LUNA_ENABLE_OCR_EVIDENCE_PACK_VALIDATE_V1=false`**。  
3. 强制 **`LUNA_DISABLE_OCR_BRIDGE_RUNTIME_V1=true`**。  
4. **保留已有日志**与已生成的 **shadow evidence 文件**（**不删除**，便于复盘；是否轮转由运维策略决定）。  
5. 输出 **rollback report**（路径与 schema 由实现 phase 定义）。

---

## 与 kill switch 的优先级

**全局 disable** 覆盖所有分项；rollback 第一步可为「直接全局 disable」以缩短故障窗口。
