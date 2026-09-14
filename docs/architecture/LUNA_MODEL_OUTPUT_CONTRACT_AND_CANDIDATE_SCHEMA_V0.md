# Phase-Model-001 — Model Output Contract And Candidate Schema v0（输出契约 + Schema 冻结）

**目的**：冻结模型输出 contract 与统一 candidate schema，确保模型只能输出可解析、可审计、可回放的候选信息，且绝不包含执行指令或放权意图。  
**性质**：contract/schema；不接入模型 runtime；不修改治理宪法。  

---

## 1) 允许输出类型（Allowed Output Kinds）

模型输出只允许落在以下集合：
- `candidate`
- `draft_explanation`
- `structured_suggestion`
- `confidence_hint`
- `comparison_hint`

---

## 2) 禁止输出类型（Forbidden Output Kinds，硬黑名单）

模型输出绝对禁止落在（任一出现即 no-go）：
- `execute_now`
- `open_release_window`
- `retry_now`
- `reopen_now`
- `enable_default_path`
- `override_governance`
- `grant_control`
- `long_running_enablement`

并且禁止在任何字段中以同义表达出现上述语义（即“禁止语义”，不只禁止字段名）。

---

## 3) 输出 contract（必须满足）

每次模型输出必须满足：
- **可解析**：必须是严格 JSON（UTF-8），不得夹杂自然语言前后缀
- **可审计**：必须包含 `model_id`、`model_version`、`policy_version`、`timestamp`、`request_id`
- **可回放**：必须包含 `input_hash`（或等价可复现指纹）与 `prompt_hash`（或等价）
- **可禁用**：输出必须可被系统丢弃而不影响基线
- **candidate-only**：输出不得携带任何“执行/放权/开窗”意图

---

## 4) 统一 Candidate Schema v0（写死）

```json
{
  "schema_version": "candidate_schema_v0",
  "policy_version": "phase_model_001_v0",
  "request_id": "string",
  "timestamp": "string",
  "model_id": "string",
  "model_version": "string",
  "input_hash": "string",
  "prompt_hash": "string",
  "output_kind": "candidate | draft_explanation | structured_suggestion | confidence_hint | comparison_hint",
  "candidates": [
    {
      "candidate_id": "string",
      "candidate_type": "string",
      "summary": "string",
      "structured_fields": { "any": "json" },
      "confidence": {
        "score": 0.0,
        "calibration_hint": "string"
      },
      "reason_codes": ["string"],
      "evidence_pointers": ["string"],
      "safety_notes": ["string"]
    }
  ],
  "comparisons": [
    {
      "lhs_candidate_id": "string",
      "rhs_candidate_id": "string",
      "preference": "lhs | rhs | tie | unknown",
      "score_delta_hint": 0.0,
      "reason_codes": ["string"]
    }
  ],
  "draft_explanation": {
    "text": "string",
    "structure": { "any": "json" }
  },
  "meta": {
    "parse_warnings": ["string"],
    "redaction_summary": "string"
  }
}
```

**约束说明（v0）**：
- `output_kind` 必须命中 allowlist
- `candidates[*].structured_fields` 允许扩展，但不得承载 forbidden 语义
- `confidence.score` 仅用于提示不确定性，不得被解释为执行阈值

---

## 5) 系统消费方式（写死：单向消费）

系统对模型输出的消费规则（v0）：
- 只能把输出作为“候选/草稿/比较提示”进入白盒日志与后续对比流程
- 不得将任何字段映射为 execute/retry/reopen/release 的直接触发条件
- 不得将输出映射为治理结论（go/no-go）的直接替代

---

## 6) 后续实现 no-go 条件（对 Phase-Model-002）

Phase-Model-002 只要出现任一，即必须 no-go：
- 输出含 forbidden 输出类型或禁止语义
- 输出不可稳定解析（非严格 JSON 或字段缺失导致不可消费）
- 输出不可审计（缺 request_id / model_id / hashes 等）
- 输出不可回放（缺 input_hash/prompt_hash 或等价复现指纹）
- 输出不可禁用（禁用后仍影响系统决策或执行）

---

## 7) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未接入真实模型 runtime  
- 本文件只冻结输出契约与 schema，不做实现  

