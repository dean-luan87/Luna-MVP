# 风险打断闭环 V1：最小旁路实现说明

## 实现了什么（V1）

已落地一个最小旁路模块：

- `capabilities/cross_domain/risk_interrupt_v1.py`

实现内容（严格按 V1 切片）：

1. 接收统一风险事件（`RiskInterruptEventV1`）
2. 最小裁决是否抢占（`high/critical` 才可抢占）
3. 打 `paused_by_risk` 标记（V1 仅标记，不做恢复）
4. 输出白盒字段（写入 `metadata["risk_interrupt_v1"]`）
5. 支持一键降级为只入白盒（不真正抢占）

## 默认怎么关（不污染主链）

该模块默认不被主链引用；即使被接入，也默认关闭：

- `LUNA_ENABLE_RISK_INTERRUPT_V1=0`（默认）

## 如何降级（只入白盒、不抢占）

开启总开关后，建议默认先跑白盒验证：

- `LUNA_ENABLE_RISK_INTERRUPT_V1=1`
- `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1`（默认 true）

当 `WHITEBOX_ONLY=1` 时：

- 不抢占
- 不打任务挂起
- 只输出白盒观测字段

## 怎么验证

最小验证脚本：

- `tools/test_risk_interrupt_v1.py`

覆盖用例：

- high 风险（允许抢占，非 whitebox-only）
- medium 风险（只留白盒）
- whitebox-only（即使 high 也只留白盒）

运行：

```bash
python3 tools/test_risk_interrupt_v1.py
```

## 还没做什么（V1 明确不做）

- 不做风险解除自动恢复
- 不做多风险合并/排队/恢复队列
- 不做轨迹预测
- 不做复杂裁决器/多模型融合
- 不做重规划/自动重算

