# LUNA — Voice Output Priority / Expiry / Suppression Policy v0

## Phase

- **Phase-Voice-OutputGovernance-001**

## Purpose

把“输出优先级与抑制”扩展到语音输出治理：过期不播报、低置信不确定化、重复限频、静默合法。

本阶段只定义，不实现 runtime。

## Priority（v0）

从高到低：

- `critical`
- `high`
- `medium`
- `low`
- `silent`

## Expiry（Hard）

- `now >= expires_at` → 必须抑制/过期（不得播报）
- 过期的 high/critical 也不得播报

## Suppression（Hard）

- **Safety suppresses normal**：安全提醒压制普通导航/状态确认/闲聊输出
- **Repeat rate limit**：重复文本/模板必须限频
- **Low confidence**：低置信不得以确定语气输出（必须降级或静默）
- **Silence is valid**：无输出也是合法输出

## Governance invariants

- 不得出现 execute/release/retry/override 等放权语义
- 不得触发导航动作
- 不得把 provisional/uncertain 作为确定性指令播报

