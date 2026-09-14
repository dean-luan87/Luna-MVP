# LUNA OCR Guarded Trial 定义 v0

**Phase**：Phase-Mainline-RuntimeReadiness-002  
**Trial id**：`ocr_guarded_trial_v1`  
**入口**：`LUNA_ENABLE_OCR_GUARDED_TRIAL_V1`（默认 **false**）

---

## 目标

只验证 **OCR provider / source policy / fallback / not_available / RequestTrace 注入**，**不**进入语义下游。

---

## 允许

- 读取 frame / crop  
- 调用 OCR source policy  
- 仅在子闸允许时调用 provider  
- fallback / not_available  
- 写 raw text candidate  
- 写 trace / replay / whitebox  
- 生成 RequestTrace stage  

---

## 禁止

- `semantic_interpretation_enabled=true`  
- 任意下游业务调用  
- 导航动作  
- TTS / 播报  
- 写世界模型  
- SceneTask / Fusion / Output  
- 上传蜂巢  

---

## 建议 env（与生成矩阵一致）

| Flag | 典型默认值 | 说明 |
|------|------------|------|
| `LUNA_DISABLE_ALL_GUARDED_TRIALS` | false | Global kill |
| `LUNA_ENABLE_OCR_GUARDED_TRIAL_V1` | false | Trial 总入口 |
| `LUNA_OCR_TRIAL_MODE` | shadow_only | `shadow_only` \| `guarded_provider` |
| `LUNA_OCR_TRIAL_PROVIDER_POLICY` | ocr_default_offline_raw_text_source_policy_v0 | policy 标识冻结 |
| `LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION` | false | 真实 provider 闸 |
| `LUNA_OCR_TRIAL_ABORT_ON_GOVERNANCE_LEAKAGE` | true | 泄漏即 abort |
| `LUNA_OCR_TRIAL_WRITE_REQUEST_TRACE` | true | 关闭则不作为验收 |

---

## Acceptance（摘要）

- source policy 已选择并记录  
- provider / fallback / not_available 路径合法  
- raw_text schema 合法  
- **semantic_interpretation_enabled=false**  
- **downstream_invocation_count＝0**  
- **governance_leakage＝0**  
- RequestTrace stage 已发出  

---

## Abort（摘要）

- source policy 缺失  
- provider 异常  
- schema 非法  
- 检测到语义输出  
- 检测到下游调用  
- `real_tts_invoked=true`（非法进入语音链）  

---

## Rollback（摘要）

- 关闭 `LUNA_ENABLE_OCR_GUARDED_TRIAL_V1`  
- 强制 not_available 或 shadow-only  
- **保留** raw 输出与日志  

机器可读完整表：`mainline_guarded_trial_matrix.json`（capability=`ocr`）。
