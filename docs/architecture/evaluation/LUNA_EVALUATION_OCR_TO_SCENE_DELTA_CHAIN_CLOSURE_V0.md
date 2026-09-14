# Luna 评测 — OCR → Scene Delta Mock 链闭环归档 v0

**Phase**：`Phase-OCR-to-SceneDelta-Mock-Chain-Closure-001`  
**目标**：对 **OCR evidence → MidPlatform 只读候选 → 只读事件载荷 → Scene Delta write candidate stub → dry-run → executor trace stub → mock handshake → local_skeleton 合同 conformance** 做一次 **链级归档**，输出矩阵、血缘、无写边界、能力总结、非宣称与待办，并由 verifier 做静态收口检查。

## 约束（本 phase 禁止）

- 不运行 OCR、不调用 provider、不调用真实 Scene Delta executor  
- 不写 Scene Delta、不写数据库、不写 WAL、不写 MidPlatform fact、不写 WorldModel  
- 不调用 AI 解释、不改 OCR routing  

## 默认输入根（9）

| Phase ID | 默认 `_eval_out` 根 |
|----------|---------------------|
| OCR-Lightweight-Provider-Multi-ROI-Smoke-001 | `ocr_lightweight_provider_multi_roi_smoke_v0` |
| OCR-Evidence-Consumer-ReadOnly-Smoke-001 | `ocr_evidence_readonly_consumer_smoke_v0` |
| MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001 | `midplatform_ocr_evidence_readonly_ingest_candidate_smoke_v0` |
| OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001 | `ocr_ingest_readonly_bus_replay_smoke_v0` |
| MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001 | `scene_delta_write_candidate_from_ocr_ingest_stub_smoke_v0` |
| MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001 | `scene_delta_write_candidate_dryrun_verifier_smoke_v0` |
| MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001 | `scene_delta_executor_trace_stub_from_dryrun_smoke_v0` |
| MidPlatform-Scene-Delta-Executor-Mock-Handshake-001 | `scene_delta_executor_mock_handshake_smoke_v0` |
| MidPlatform-Scene-Delta-Executor-Contract-Conformance-001 | `scene_delta_executor_contract_conformance_smoke_v0` |

绝对路径默认值见 `capabilities/midplatform/ocr_to_scene_delta_chain_closure_v0.py` 中 `DEFAULT_CHAIN_ROOTS`；可通过 `--roots-json` 覆盖。

## 命令

```bash
python3 tools/evaluation/midplatform/run_ocr_to_scene_delta_chain_closure_v0.py \
  --output-root /ABS/PATH/_eval_out/ocr_to_scene_delta_chain_closure_smoke_v0

python3 tools/evaluation/midplatform/verify_ocr_to_scene_delta_chain_closure_v0.py \
  --smoke-root /ABS/PATH/_eval_out/ocr_to_scene_delta_chain_closure_smoke_v0
```

## 产物清单

与架构文档 `../midplatform/LUNA_OCR_TO_SCENE_DELTA_MOCK_CHAIN_CLOSURE_V0.md` 一致；verifier 报告文件名：`ocr_to_scene_delta_chain_closure_verifier_report.json`。

## 相关文档

- GO/NO_GO 语义：`LUNA_EVALUATION_OCR_TO_SCENE_DELTA_CHAIN_CLOSURE_GO_NO_GO_PACK_V0.md`  
- 中台叙事：`../midplatform/LUNA_OCR_TO_SCENE_DELTA_MOCK_CHAIN_CLOSURE_V0.md`
