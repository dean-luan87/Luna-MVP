# LUNA OCR Controlled Trial Plan v0（Stage 2）

**Phase**：Phase-Mainline-GuardedTrial-001  
**启动条件**：Stage 1 YOLO guarded trial = **GO**。

---

## 1. 目标

验证 OCR source policy / provider / fallback / raw_text / RequestTrace；**不**打开语义下游自动消费。

---

## 2. 允许 / 禁止

**允许**：读 frame/crop、走 source policy、在明确 flag 下调用 provider、fallback/not_available、写 raw text 候选、trace/replay/whitebox、RequestTrace stage。

**禁止**：`semantic_interpretation_enabled=true`、MidPlatform 下游自动消费、SceneTask/Fusion/Output、导航、播报、世界模型写入、蜂巢上传。

---

## 3. 建议窗口

- provider disabled precheck：**10 samples**  
- provider controlled trial：**30 samples**  
- extended OCR trial：**100 samples**（前一阶段 GO 后）

---

## 4. 验收（摘要）

source policy 选中率 100%、各类 provider/fallback/not_available 结果合法、raw_text schema 100%、`semantic_interpretation_enabled=false`、downstream=0、RequestTrace 100%、governance leakage=0。

---

## 5. Abort / Rollback（摘要）

Abort：source policy 缺失、provider 异常未被 fallback 接住、语义输出检出、downstream>0、navigation/TTS/world_write/trace/kill 等异常。

Rollback：关闭 `LUNA_ENABLE_OCR_GUARDED_TRIAL_V1`、强制 shadow_only/not_available、保留 raw 输出、生成 post_trial_report。
