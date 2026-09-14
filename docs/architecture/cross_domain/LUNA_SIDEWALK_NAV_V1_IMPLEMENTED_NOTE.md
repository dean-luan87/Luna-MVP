# Sidewalk Nav V1：实现说明

## 实现了什么

- 旁路模块：`capabilities/cross_domain/sidewalk_nav_v1/`
  - `evaluate_sidewalk_nav_v1(...)`：环境初判（规则占位）、风险摘要只读、高风险或 `risk_interrupt_preempt` 时压下普通导航提示、白盒 `metadata["sidewalk_nav_v1"]`
- 最小通行建议：仅在 `scene_type=outdoor_walkway` 且未被压制时生成一条固定短句（V1 不做路径规划）
- 验证脚本：`tools/test_sidewalk_nav_v1.py`
- 主线边缘集成验证：`tools/test_sidewalk_nav_v1_integration.py`（说明见《`LUNA_SIDEWALK_NAV_V1_INTEGRATION_NOTE.md`》）

## 默认怎么关

- `LUNA_ENABLE_SIDEWALK_NAV_V1` 未设置或 `0`：**不写入** `metadata["sidewalk_nav_v1"]`，主链零侵入（旁路未被上层调用时同样不生效）

## 怎么验证

```bash
python3 tools/test_sidewalk_nav_v1.py
python3 tools/test_sidewalk_nav_v1_integration.py
```

覆盖：默认关闭、开启+人行道+低风险、开启+高风险压制、whitebox-only 不外显、`risk_interrupt_preempt` 压制；集成脚本额外验证向主链式 `metadata` 合并时的字段与零侵入。

## 与 risk_interrupt_v1 的关系

- **不** import `risk_interrupt_v1`；由上层在适当时机传入 `risk_interrupt_preempt=True`（例如已调用 `handle_risk_interrupt_v1` 且本轮需抢占时）
- 风险摘要中 `risk_level` 为 `high` / `critical` 时，本模块自行将 `output_suppressed_by_risk=true`，不产出普通导航提示
- 播报裁决仍应由统一上层完成：本模块只提供 `final_spoken_output` 候选与白盒

## 哪些还没做

- 不接真实视觉/地图管线；环境初判为规则占位
- 无 OCR、无交叉路口、无多模型协同
- 未接入主链调用点（需上层显式集成）
