# Luna Voice：Legacy 降级与受控清理变更清单

> 目标：不删除影响主链运行的旧语音模块；先做“降级口径 + legacy 归属容器 + 可追踪清单”，停止旧语音继续扩散与被误认为正式主线能力。

## 1) 扫描了哪些模块（重点清单）

- 主链生效：
  - `main.py`（Voice 初始化与 `submit_tts` 调用）
  - `modules/voice.py`
  - `core/speech_gate.py`
  - `core/audio_worker.py`
- 原型/参考：
  - `modules/voice_to_text.py`（Vosk CLI）
  - `test_edge_tts.py`（edge-tts 实验脚本）
  - `luna_backend/services/tts/tts_engine.py`、`luna_backend/routes/tts_routes.py`
  - `luna_backend/services/speech/speech_router.py`
  - 历史测试：`luna_badge_tests/**/tts*`

## 2) 产出与标注

### 2.1 新增 legacy audit 文档
- `docs/architecture/voice/LUNA_VOICE_LEGACY_AUDIT.md`
  - 逐项标注：是否主链生效、建议状态、处理方式、风险与备注

### 2.2 新增 legacy 容器概念
- `legacy/voice/README.md`
  - 说明：什么是 legacy voice、为什么保留、哪些兜底、哪些准备移除、为什么现在不删

### 2.3 legacy 注释/归属声明（最小改动）
- `modules/voice.py`：明确降级为 **legacy fallback**，后续由 Fish+Piper 替换
- `modules/voice_to_text.py`：明确为 **原型/参考**，不进入主链
- `luna_backend/services/tts/tts_engine.py`：明确为 **后端侧过渡/参考**，非主链标准

## 3) 哪些标为 legacy（口径与状态）

- macOS `say`（`modules/voice.py`）：`legacy_keep_for_fallback`
- Vosk CLI（`modules/voice_to_text.py`）：`legacy_keep_for_reference`
- edge-tts 后端实现（`luna_backend/services/tts/*`）：`legacy_keep_for_reference`
- edge-tts 实验脚本（`test_edge_tts.py`）：`legacy_candidate_for_removal`

## 4) 哪些保留兜底

- `modules/voice.py` 作为当前主链播报兜底，保留到 Stage-2 cutover 完成。

## 5) 哪些未来移除/迁出

- `test_edge_tts.py` 与其它实验/历史测试：后续可迁入 `legacy/voice/` 或移除（在新链路稳定后）。

## 6) 哪些旧文件未动但已在文档中降级

- `main.py`：未改运行行为；在 audit 中明确其语音链路属于 legacy bridge required（后续再切换）
- `core/speech_gate.py` / `core/audio_worker.py`：未改语义；仅做归属说明（未来 Output Plane 可复用其语义）

## 7) 为什么本轮不直接删除

因为目标是“受控清理”：
- 删除/迁移可能破坏当前可运行性与回归对照
- 正确顺序是先降级主链地位，再由新 provider 链接管，最后再做可回滚精简

