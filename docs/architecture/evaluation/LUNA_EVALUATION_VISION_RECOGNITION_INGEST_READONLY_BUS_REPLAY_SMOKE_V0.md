# Luna 评测 — Vision Recognition Ingest ReadOnly Bus Replay Smoke v0

**Phase**：`Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001`  
**Runner**：`tools/evaluation/midplatform/run_vision_recognition_ingest_readonly_bus_replay_smoke_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_vision_recognition_ingest_readonly_bus_replay_smoke_v0.py`

## 输入（MidPlatform Vision ingest candidate 根目录）

须为 **绝对路径**，且包含：

- `midplatform_vision_recognition_ingest_candidate.json`  
- `midplatform_vision_recognition_ingest_matrix.json`  
- `midplatform_vision_recognition_ingest_source_chain_summary.json`  
- `midplatform_vision_recognition_ingest_audit_report.json`  

## CLI

```bash
python3 tools/evaluation/midplatform/run_vision_recognition_ingest_readonly_bus_replay_smoke_v0.py \
  --ingest-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/midplatform_vision_recognition_evidence_readonly_ingest_candidate_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_ingest_readonly_bus_replay_smoke_v0
```

Verifier：

```bash
python3 tools/evaluation/midplatform/verify_vision_recognition_ingest_readonly_bus_replay_smoke_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_recognition_ingest_readonly_bus_replay_smoke_v0
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `vision_recognition_ingest_readonly_bus_replay_summary.json` | 回放摘要 |
| `vision_recognition_ingest_readonly_event_payload.json` | 只读事件载荷 |
| `vision_recognition_ingest_readonly_replay_log.jsonl` | 回放阶段日志 |
| `vision_recognition_ingest_readonly_replay_consumer_view.json` | replay consumer 视图 |
| `vision_recognition_ingest_readonly_replay_audit_report.json` | audit |
| `vision_recognition_ingest_readonly_bus_replay_notes.md` | 短说明 |
| `vision_recognition_ingest_readonly_bus_replay_verifier_report.json` | verifier 输出 |

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_RECOGNITION_INGEST_READONLY_BUS_REPLAY_SMOKE_GO_NO_GO_PACK_V0.md`。
