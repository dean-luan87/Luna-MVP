# Luna Evaluation — Scene Delta Executor Contract Conformance Smoke v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001`

## 目的

验证 **mock request / ACK** 与本地 **`scene_delta_executor_contract_skeleton_v0`** 的 **静态 conformance** 与 **no-write 合同**；产出 skeleton、请求/ACK 矩阵、gap、no-write 报告与 audit。**不**调用真实 executor，**无** DB/WAL/事实写入。

## 前置

- `Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-001` = GO  
- `Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001` = GO  

**默认输入 mock handshake 根目录**：`_eval_out/scene_delta_executor_mock_handshake_smoke_v0/`

## 命令

```bash
python3 tools/evaluation/midplatform/run_scene_delta_executor_contract_conformance_v0.py \
  --output-root /ABS/PATH/_eval_out/scene_delta_executor_contract_conformance_smoke_v0

python3 tools/evaluation/midplatform/verify_scene_delta_executor_contract_conformance_v0.py \
  --smoke-root /ABS/PATH/_eval_out/scene_delta_executor_contract_conformance_smoke_v0
```

## 产物

| 文件 | 说明 |
|------|------|
| `scene_delta_executor_contract_skeleton_v0.json` | 本地合同骨架（`local_skeleton`）。 |
| `scene_delta_executor_contract_conformance_summary.json` | 摘要、`contract_reference_mode`、输入路径。 |
| `scene_delta_executor_request_conformance_matrix.json` | Mock request 字段检查。 |
| `scene_delta_executor_ack_conformance_matrix.json` | Mock ACK 字段检查。 |
| `scene_delta_executor_contract_gap_report.json` | 缺失/额外字段与 `conformance_level`。 |
| `scene_delta_executor_no_write_contract_report.json` | No-write 合同检查。 |
| `scene_delta_executor_contract_conformance_audit_report.json` | Conformance audit。 |
| `scene_delta_executor_contract_conformance_notes.md` | 短说明。 |
| `scene_delta_executor_contract_conformance_verifier_report.json` | Verifier 报告。 |

## Verifier 退出码

- **GO**：**0**；**NO_GO**：**2**。
