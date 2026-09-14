# LUNA YOLO Guarded Trial 定义 v0

**Phase**：Phase-Mainline-RuntimeReadiness-002  
**Trial id**：`yolo_guarded_trial_v1`  
**入口**：`LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1`（默认 **false**）

---

## 目标

只验证 **真实 frame / detector / RequestTrace 注入**，**不**进入任务执行链。

---

## 允许

- 读取真实 frame  
- 调用 YOLO detector  
- 生成 detection result  
- 写 trace / replay / whitebox  
- 生成 RequestTrace stage  
- 与 shadow 输出对比  

---

## 禁止

- 进入 SceneTask / Fusion / Output  
- 执行导航动作  
- 触发播报或 TTS  
- 写世界模型  
- 上传蜂巢  
- 自动影响任务链  
- 下游语义消费调用  

---

## 建议 env（与生成矩阵一致）

| Flag | 典型默认值 | 说明 |
|------|------------|------|
| `LUNA_DISABLE_ALL_GUARDED_TRIALS` | false | Global kill；true 时本 trial 不得运行 |
| `LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1` | false | Trial 总入口 |
| `LUNA_YOLO_TRIAL_MODE` | shadow_only | `shadow_only` \| `guarded_local` |
| `LUNA_YOLO_TRIAL_MAX_FRAMES` | 0 | 0＝内置默认上限（接线 PR 冻结数值） |
| `LUNA_YOLO_TRIAL_ABORT_ON_DETECTOR_ERROR` | true | 异常即 abort tick |
| `LUNA_YOLO_TRIAL_WRITE_REQUEST_TRACE` | true | 关闭则不作为 trial 验收 |

---

## Acceptance（摘要）

- detector 调用成功率 ≥ 配置阈值  
- `frame_id` / `timestamp` / `request_id` / `trace_id` 注入完备  
- detection result schema 合法  
- **下游调用数为 0**  
- RequestTrace stage 已发出  
- abort 路径经验证（注入故障）  

---

## Abort（摘要）

- detector 异常  
- 缺失 `frame_id`  
- schema 非法  
- 延迟超过 trial budget  
- 置信度坍塌（按策略）  
- 检测到下游调用  

---

## Rollback（摘要）

- 关闭 `LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1`  
- 回到 offline / shadow-only  
- **保留** trial 日志（按 `trial_id`）  

机器可读完整表：`mainline_guarded_trial_matrix.json`（capability=`yolo`）。
