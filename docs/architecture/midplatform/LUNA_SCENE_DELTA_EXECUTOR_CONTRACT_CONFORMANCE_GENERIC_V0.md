# Luna MidPlatform — Scene Delta Executor Contract Conformance Generic v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-Generic-001`

## 目的

对 **generic mock request / ACK**（`scene_delta_mock_executor_*_generic_v0`）做 **本地 skeleton** 静态合同对齐：生成 **contract skeleton**、request/ACK **conformance matrix**、**gap report**、**no-write contract report** 与 **audit**。支持 **`ocr_evidence`** 与 **`vision_recognition_evidence`**。

## 边界

- **`contract_reference_mode=local_skeleton`** — **不得**声称已对齐生产 executor OpenAPI / proto。  
- **禁止**：真实 executor、Scene Delta 写入、数据库、WAL、rehearsal log、事实层 / WorldModel、AI / 导航 / provider。

## 与 OCR 专用 conformance 的关系

- **保留**：`run_scene_delta_executor_contract_conformance_v0.py`（消费 OCR 专用 mock request/ACK）。  
- **新增**：本 phase 消费 **generic** mock handshake 产物；新链路默认走 generic。

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_GENERIC_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_GENERIC_V0.md)。

## 与上一 phase 的关系

输入来自 [LUNA_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_V0.md](./LUNA_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_V0.md)。

## 建议下一跳

**Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001**：聚合 OCR + Vision generic 四层产物做闭环归档，见 [LUNA_SCENE_DELTA_GENERIC_CHAIN_CLOSURE_V0.md](./LUNA_SCENE_DELTA_GENERIC_CHAIN_CLOSURE_V0.md)。
