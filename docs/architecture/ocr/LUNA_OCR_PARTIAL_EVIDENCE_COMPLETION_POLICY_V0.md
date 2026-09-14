# LUNA OCR Partial Evidence Completion Policy v0

**建议阶段命名**：`Phase-OCR-Partial-Evidence-Completion-Policy-001`  
**阶段判定（当前）**：**DESIGN_RECORDED / FIELD_RESERVED** — 策略文档与 merge stub 字段预留已完成；补全候选生成、用户确认状态机、记忆/搜索/STCM 联动与高风险闸门 **未**在本 phase 实现；**不**建议宣称 GO，除非建立独立 verifier 与闸门产物。

**术语（强制）**：**Partial Evidence Completion / 局部证据补全候选** — **不得**称为「补全事实」「补全识别结果」。

## 定位

半张图、截断 tile、低置信 OCR 等产生的 **partial evidence** 可以进入中台；中台可基于其它渠道生成 **completion candidates（补全候选）**。候选 **≠** OCR 直接读出内容，**≠** 已确认事实，**≠** 默认可驱动高风险行动。

## 补全渠道（设计枚举，实现可分期接入）

1. **记忆补全**：历史相似场景 / 店铺 / 标牌 / 物品（需来源归因与衰减）。  
2. **人机互动补全**：向用户确认缺失片段。  
3. **词语联想 / 搜索补全**：基于已识别片段推测词组（受隐私、网络、来源可信度、时效约束）。  
4. **周边上下文补全**：地点、任务、对象、历史路径、Scene Delta 等（与 MidPlatform / WorldModel 读路径严格隔离默认写入）。  
5. **后续重新采样补全**：用户靠近、重拍、**异步 tile 补齐**（与 STCM 衔接）。

## 证据分层（目标 JSON 形状，实现阶段填充）

```json
{
  "direct_observed_text": "句句治愈",
  "partial_scope": "partial_image",
  "completion_candidates": [
    {
      "text": "句句治愈，句句自愈",
      "source": "memory | user_confirmation | lexical_association | search | context_inference",
      "confidence": "low | medium | high",
      "requires_confirmation": true,
      "can_drive_action": false
    }
  ],
  "user_disclosure_required": true
}
```

## 对用户播报的披露义务（原则）

- **禁止**：「我看到完整内容是……」  
- **必须**：区分「直接看见」与「推测/补全」，并明确后者需确认。示例话术见需求文档（可配置为简短版）。

## 核心规则（10 条）

1. partial tile / partial image evidence **允许**进入中台。  
2. 中台 **可以** 生成 completion candidates（在策略允许且审计链完整时）。  
3. 每个 candidate **必须** `source` 归因。  
4. 每个 candidate **必须** 标记不确定性（`confidence` + `requires_confirmation`）。  
5. completion **默认不得**直接写入 WorldModel。  
6. **未确认**补全不得驱动安全、导航、医疗、支付等高风险行动（`can_drive_action` 默认 false）。  
7. 用户可 **确认 / 否定 / 修正**。  
8. 用户确认后才可升级为 **confirmed evidence** 或 **memory candidate**（升级路径由后续阶段定义）。  
9. 播报必须披露 **看见 vs 推测** 分层。  
10. 搜索/联想补全受 **时效、隐私、网络、来源可信度** 约束（与 STCM / 策略引擎对齐）。

## 与上下游的关系（逻辑链）

```text
partial evidence
  → completion candidate
  → user confirmation / memory / search / resample
  → confirmed evidence 或 rejected candidate
  → OCR Bridge / MidPlatform（仅确认后路径）
```

## 与当前实现的关系

- **`Phase-OCR-Tile-Evidence-Merge-Stub-001`** 已在 merge 输出中挂载 **`partial_evidence_completion`** 占位对象（`ocr_partial_evidence_completion_policy_stub_v0`），字段包括：  
  `completion_allowed`、`completion_required`、`completion_candidates`（空数组）、`completion_source_policy`、`user_disclosure_required`、`direct_observed_text`、`partial_scope`、`direct_observed_vs_inferred_split` 及 **风险闸门** 布尔说明。  
- **本阶段不执行**任何真实补全、不写 WorldModel、不接 MidPlatform 语义回路。

## 一句话

**可以补全，但必须把「看见的」和「推测的」拆开，并强制对用户披露；补全永远不能伪装成 OCR 事实。**
