# Luna Voice Stage-2.2 Changeset

## 1) 本轮目标

Stage-2.2 仅做本机真实执行验证，不做架构改造。  
核心是验证 Fish/Piper/provider fallback/legacy rollback/observation 的真实活性。

## 2) 新增文件

- `tools/validate_local_tts_runtime.py`
- `docs/architecture/voice/LUNA_VOICE_STAGE2_2_LOCAL_RUNTIME_SETUP.md`
- `docs/architecture/voice/LUNA_VOICE_STAGE2_2_RUNTIME_VALIDATION_REPORT.md`
- `docs/architecture/voice/LUNA_VOICE_STAGE2_2_CHANGESET.md`
- `capabilities/voice/models/piper/zh_CN-huayan-medium.onnx`
- `capabilities/voice/models/piper/zh_CN-huayan-medium.onnx.json`
- `logs/voice_stage22_validation_results.json`
- `logs/voice_stage22_observations.jsonl`

## 3) 修改文件

- `（已移除）`
  - 增加 `enabled/model_path` 最小运行配置支持
  - 保持失败结构化返回
- `capabilities/voice/providers/piper_tts_provider.py`
  - 增加 `enabled/model_path` 最小运行配置支持
  - 未配置模型路径时返回 `config_error`
- `capabilities/voice/output/tts_request_executor.py`
  - 增加 `local_runtime` 配置读取（executable/model_path）
- `capabilities/voice/runtime/tts_unified_entry.py`
  - 增加 `local_runtime` provider 实例化配置
  - 透出 `selection_observation`/`fallback_observation`
- `capabilities/voice/config/voice_tts_config.yaml`
  - 增加 `local_runtime` 最小本机运行字段

## 4) 本轮未改动（按边界保持）

- `main.py`（无新增主链重构）
- `core/audio_worker.py`（语义未改）
- `core/speech_gate.py`（语义未改）
- `modules/voice.py`（保留 legacy 底座）
- `modules/voice_to_text.py`（保留 legacy）

## 5) 真实验证结论摘要

- Fish provider 已移除；本阶段仅 Piper。
- Piper: 实机成功生成音频，满足“至少一方真实出音”。
- Fish->Piper fallback: 真实触发并成功。
- Provider chain->legacy rollback: 真实触发并成功。
- cutover 关闭->legacy 直通: 真实触发并成功。
- observation: selection/fallback/cutover/rollback 全部在实跑中可见。

## 6) 仍待解决问题

- Fish 本机 CLI 与模型链路仍需补齐，当前仅完成“可检测失败+可回退”。
- 目前听感记录为最小版本，后续可按 preset 维度补充细测。

## 7) 为什么本轮不继续扩展

- 本轮约束是“运行验证优先”，不是“能力增强优先”。
- 已满足 Stage-2.2 的关键验收闭环，不应在本轮引入 ASR/云端/主链重构等越界改动。

## 8) 主线—白盒—日志一致性检查

- A 主线：统一入口路径在实跑中可用，且 fallback/rollback 生效。
- B 白盒：四类观察对象均在真实路径中生成。
- C 日志：产物已落地到 `logs/` 与文档。
- D 最终判断：**主线通顺，白盒一致，日志已落地**。

