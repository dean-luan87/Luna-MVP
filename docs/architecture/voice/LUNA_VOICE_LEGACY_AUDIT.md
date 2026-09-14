# Luna Voice：Legacy 资产盘点（受控清理 Stage-Legacy）

> 目标：不粗暴删除、不破坏可运行性；先剥夺旧语音模块“正式主链能力”地位，将其降级为 **Legacy / fallback / reference / 待迁移资产**，为后续 provider + Piper provider 链让路。

## 枚举（硬约束）

### 建议状态（枚举）
- `legacy_keep_for_fallback`
- `legacy_keep_for_reference`
- `legacy_candidate_for_removal`
- `legacy_bridge_required`

### 处理方式（枚举）
- `annotate_only`
- `move_to_legacy`
- `mark_do_not_extend`
- `bridge_temporarily`
- `keep_until_stage2_cutover`

## 盘点表（必须）

| 路径 | 当前职责 | 当前是否主链生效 | 建议状态 | 处理方式 | 风险 | 备注 |
|---|---|---:|---|---|---|---|
| `modules/voice.py` | macOS `say` TTS 播放实现（当前主链播报依赖） | 是 | `legacy_keep_for_fallback` | `keep_until_stage2_cutover` | high | **必须保留可运行性**；明确后续由 Fish 主链替换，当前仅兜底/过渡 |
| `core/audio_worker.py` | 播放工作线程（异步，不阻塞） | 是 | `legacy_bridge_required` | `annotate_only` | medium | 不是“legacy语音模块”，但属于旧播报执行层；Stage-2 新链路未来可复用其“执行语义”但本轮不改语义 |
| `core/speech_gate.py` | 发言权 gate（去重/冷却/占用） | 是 | `legacy_bridge_required` | `annotate_only` | medium | 同上：治理层 gate，Stage-2 未来可复用但本轮不改语义 |
| `main.py`（语音调用段） | 旧播报链路编排（初始化 Voice + submit_tts） | 是 | `legacy_bridge_required` | `annotate_only` | high | 本轮禁止大改；只在文档中降级“macOS say 为 legacy fallback”并保留现状 |
| `modules/voice_to_text.py` | Vosk ASR CLI 原型 | 否 | `legacy_keep_for_reference` | `mark_do_not_extend` | low | 明确为“原型资产/参考”，不是正式输入系统 |
| `test_edge_tts.py` | edge-tts 实验脚本 | 否 | `legacy_candidate_for_removal` | `mark_do_not_extend` | low | 可保留为实验参考，但不进入正式方案；后续可迁入 `legacy/voice/` |
| `luna_backend/services/tts/tts_engine.py` | 后端服务侧 edge-tts TTSEngine | 否（非 main.py 主链） | `legacy_keep_for_reference` | `mark_do_not_extend` | medium | 明确：过渡/参考实现，不是未来主链标准 |
| `luna_backend/routes/tts_routes.py` | 后端 TTS API 路由 | 否（非 main.py 主链） | `legacy_keep_for_reference` | `mark_do_not_extend` | low | 同上 |
| `luna_backend/services/speech/speech_router.py` | 后端侧 speech 路由（TTS/真人音库占位） | 否（非 main.py 主链） | `legacy_keep_for_reference` | `mark_do_not_extend` | medium | TODO 播放路径未落地；明确不作为主链输出面 |
| `core/speech_policy_engine.py` | 旧播报去重策略（v1.8.2） | 取决于主链是否调用 | `legacy_keep_for_reference` | `mark_do_not_extend` | low | 若主链未使用则仅参考；若使用也应逐步归位到 Output Plane policy（后续阶段） |
| `core/speech_deduplicator.py` | 文本去重器 | 取决于主链是否调用 | `legacy_keep_for_reference` | `mark_do_not_extend` | low | 同上 |
| `luna_badge_tests/**/tts*` | 历史 TTS 测试资产 | 否（不影响主链） | `legacy_keep_for_reference` | `mark_do_not_extend` | low | 可保留为回归对照，但不作为新链路标准测试 |

## 结论与保留/退出项（必须）

### 暂时保留（不删，保障可运行性）
- `modules/voice.py`（当前播报兜底）：**保留到 Stage-2 cutover**
- `core/speech_gate.py`、`core/audio_worker.py`：治理/执行语义保持不变

### 准备退出正式主线（降级为 legacy）
- macOS `say` 的“主方案地位”（改为 legacy/fallback）
- 分散的 speak 调用风格（后续统一进入 Output Plane）
- `modules/voice_to_text.py`（明确为原型资产）
- 后端 edge-tts 作为“主链标准”的任何暗示（统一降级为参考/过渡）

