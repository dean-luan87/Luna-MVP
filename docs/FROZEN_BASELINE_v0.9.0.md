# FROZEN BASELINE v0.9.0

**状态：** ✅ FROZEN（只读）

## 冻结时间
- 2026-01-19

## 冻结范围
- Risk Phase-1 / Phase-2（含 VO 风险投影）
- RA-View v1.2（事件/诊断/根因候选）
- DebugView schema（append-only）
- Authority × Ability Matrix
- Freeze 测试套件（`tests/freeze/*`）

## 冻结基线验证
- `pytest tests/freeze -v` 全绿

## 冻结原则
- 不裁决、不写回、不锁死
- 只读、可回放、可对比
- 结构性退化必须被 CI 拦截

## 备注
- 本冻结仅记录工程基线，不等同于发布版本号。
