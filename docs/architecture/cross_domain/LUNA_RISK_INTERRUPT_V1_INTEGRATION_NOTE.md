# 风险打断闭环 V1：主线边缘集成验证说明

## 目标

验证 `risk_interrupt_v1` 能够在**不污染默认主链**的前提下，在主线边缘完成：

- 接收统一风险事件
- 最小裁决（是否抢占）
- 写入 `paused_by_risk` 标记
- 产出完整白盒字段
- 支持 whitebox-only 降级（只入白盒，不抢占）

## 验证产物

- 集成验证脚本：`tools/test_risk_interrupt_v1_integration.py`
- 旁路模块：`capabilities/cross_domain/risk_interrupt_v1.py`

## 验证覆盖的 4 类情况

1. **默认关闭**（`LUNA_ENABLE_RISK_INTERRUPT_V1=0`）
   - 预期：不挂载 `metadata["risk_interrupt_v1"]`；主链不受影响
2. **普通输出进行中 + critical**（`WHITEBOX_ONLY=0`）
   - 预期：`interrupt_applied=true`，`paused_by_risk=true`
3. **普通输出进行中 + medium**（`WHITEBOX_ONLY=0`）
   - 预期：不抢占，只留白盒（`interrupt_applied=false`）
4. **whitebox-only + critical**（`WHITEBOX_ONLY=1`）
   - 预期：不抢占、不挂起，只留白盒

## 运行方式

```bash
python3 tools/test_risk_interrupt_v1_integration.py
```

## 白盒字段检查清单（必须全有）

脚本会断言 `risk_interrupt_v1` 白盒字段至少包含：

- `event_timestamp`
- `risk_event_summary`
- `original_output`
- `interrupt_applied`
- `task_paused`
- `final_spoken_output`
- `interrupt_reason`

## 说明（为什么叫“主线边缘”）

本验证不修改主链代码，而是使用“主链最终会产生的结果载体”这一思路：

- 以 `metadata` 作为白盒字段承载位置
- 证明旁路模块在边缘能被接入、能产生可观测结果
- 并能在默认关闭/whitebox-only 时保持“零侵入”语义

