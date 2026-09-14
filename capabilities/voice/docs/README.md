# Voice docs（Stage-1）

本目录用于存放 Voice 板块内部说明（实现前置约束、对象约定、接线策略等）。

Stage-1 以 `docs/architecture/voice/` 下的正式文档为准；本目录仅用于工程侧补充说明。

## Voice 主线总基线（System Status Map）

- **统一入口**（V1 / V2 / V3 冻结面、硬约束、验证脚本总表）：`docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  
- 分阶段 freeze 文档与脚本仍按下文各小节索引；改主线相关代码时请对照总基线文档中的验证入口重跑。
- 上位治理约束（冲突治理宪法 v0）：`docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`

## V1（基础语音交互可用版）规划入口

- `docs/architecture/voice/LUNA_VOICE_V1_PLAN.md`
- 单一闭环锚点（代码事实）：`docs/architecture/voice/LUNA_VOICE_V1_MINIMAL_FLOW.md`
- 最小闭环验证脚本（session_wake + reject，不扩说话范围）：`tools/verify_voice_v1_minimal_flow.py`
- V1 最小会话状态锚（设计）：`docs/architecture/voice/LUNA_VOICE_V1_SESSION_STATE.md`

## V2（语义转换器接口契约）

- 语义归一化层接口与边界（不接模型）：`docs/architecture/voice/LUNA_VOICE_V2_SEMANTIC_CONVERTER_INTERFACE.md`

## V2（Assisted Routing v0 设计）

- 仅控制类的受控语义辅助路由（设计 + 最小接入准备，不改主链行为）：`docs/architecture/voice/LUNA_VOICE_V2_ASSISTED_ROUTING_V0.md`

## V2（Control Assisted Routing v0 Baseline）

- 控制类辅助信号消费基线（仅 stop/cancel，冻结面 + 验证入口索引）：`docs/architecture/voice/LUNA_VOICE_V2_CONTROL_ASSISTED_ROUTING_V0_BASELINE.md`
- 验证入口（改相关链路必须重跑）：
  - `tools/verify_semantic_converter_v2_shadow_consume.py`
  - `tools/verify_semantic_converter_v2_assist_stop_candidate.py`
  - `tools/verify_semantic_converter_v2_assist_stop_consumption.py`
  - `tools/verify_semantic_converter_v2_assist_cancel_consumption.py`
  - `tools/verify_voice_v1_minimal_flow.py`

## V2（Assisted Consumption Interface v0，已冻结）

- 受控消费接口面（stop/cancel 的 candidate+consumption 统一结构与准入口径）：  
  `docs/architecture/voice/LUNA_VOICE_V2_ASSISTED_CONSUMPTION_INTERFACE_V0.md`

## V3（准备阶段：视角—语义桥接接口 v0）

- 视角摘要如何进入语义层（接口与边界，不接真实视觉模型）：`docs/architecture/voice/LUNA_VOICE_V3_VISION_SEMANTIC_BRIDGE_INTERFACE.md`

## V3（Vision Shadow Read Baseline / Freeze）

- V3 输入承载 + V2 只读影子消费冻结面（不扩视觉解释、不做 provenance/白盒）：`docs/architecture/voice/LUNA_VOICE_V3_VISION_SHADOW_READ_BASELINE.md`
- 验证入口（改相关链路必须重跑）：
  - `tools/verify_vision_semantic_input_pack_v0.py`
  - `tools/verify_semantic_converter_v2_vision_shadow_read.py`
  - `tools/verify_voice_v1_minimal_flow.py`

## Topic 04（继续请求：固定确认响应，已冻结）

- 设计：`docs/architecture/voice/LUNA_CONFLICT_TOPIC_04_CONTINUE_REQUEST_HANDLING_V0.md`  
- Baseline（响应型 submit vs 执行型 submit、验证入口）：`docs/architecture/voice/LUNA_CONTINUE_REQUEST_CONFIRMATION_RESPONSE_V0_BASELINE.md`  
- 验证：`tools/verify_continue_request_response_v0.py`（另须与 `verify_voice_v1_minimal_flow.py`、`verify_voice_confirmation_gate_v0.py` 一并回归）

## Response Submit Template v0（响应型 submit 统一接口，已冻结）

- Baseline：`docs/architecture/voice/LUNA_RESPONSE_SUBMIT_TEMPLATE_V0_BASELINE.md`  
- 验证：`tools/verify_response_submit_template_v0.py`（另须与 `verify_continue_request_response_v0.py`、`verify_voice_v1_minimal_flow.py` 一并回归）

