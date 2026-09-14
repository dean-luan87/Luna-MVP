# LUNA YOLO Controlled Trial Plan v0（Stage 1）

**Phase**：Phase-Mainline-GuardedTrial-001  
**说明**：以下为 **计划定义**；执行另开 phase / 运行手册。

---

## 1. 目标

验证真实 frame / detector / RequestTrace 注入及与 shadow baseline 对比。

---

## 2. 允许 / 禁止

**允许**：读真实 frame、调用 YOLO detector、产出 detection、写 trace/replay/whitebox、写 RequestTrace stage、与 shadow 对比。

**禁止**：触发 OCR 自动链路、MidPlatform、SceneTask/Fusion/Output、导航、播报、世界模型写入、蜂巢上传。

---

## 3. 建议窗口

- dry-run precheck：**10 frames**  
- controlled local trial：**50 frames**  
- extended local trial：**200 frames**（仅当 50 frames 结果为 **GO**）

---

## 4. 验收（摘要）

detector 成功率 ≥95%、schema 100%、RequestTrace 发射率 100%、downstream=0、`navigation_action=null`、`real_tts_invoked=false`、`world_write_invoked=false`、abort 开关可用、p95 latency **仅记录**（本 phase 不定生产 SLA）。

---

## 5. Abort / Rollback（摘要）

Abort 包含：detector 连续异常≥2、schema 无效、downstream>0、navigation 非空、TTS/world_write 真、trace 缺失、global kill 触发等。

Rollback：关闭 `LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1`、必要时 `LUNA_DISABLE_ALL_GUARDED_TRIALS=true`、回 shadow/offline、保留日志、生成 post_trial_report。
