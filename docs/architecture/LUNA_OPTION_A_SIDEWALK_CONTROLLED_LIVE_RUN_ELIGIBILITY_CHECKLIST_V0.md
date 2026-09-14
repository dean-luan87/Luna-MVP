---
phase: Phase-RealSceneReview-003
title: Option A Sidewalk Controlled Live Run Eligibility Checklist v0
status: CHECKLIST
version: v0
last_updated: 2026-04-24
scope: eligibility_only
---

## 0. 目的

定义：是否允许进入下一次 **Option A 人行道短距离 controlled live run** 的资格清单。

本清单只用于“进入资格判断”，不触发 run、不扩 scope。

## 1. 复审输入（本轮依据）

- Mac live archive_root: `logs/device_env_003_archive_20260424_135440`
- Validator: `validate_controlled_live_evidence_collection_execution_v0.py` summary.recommendation=`go`

## 2. Eligibility Checklist（必须逐项打勾）

### A) Evidence Chain（证据链）

- [ ] **A1**：Mac live archive validator=`go`
- [ ] **A2**：required_files complete（run_evidence/trace/replay/whitebox/model/output/notes/risk/summary/manifest）
- [ ] **A3**：manifest pass（missing_files=0, hash_mismatch=0, integrity_status=pass）
- [ ] **A4**：trace/replay/whitebox present 且可解析
- [ ] **A5**：存在“摄像头失败不造假”验证证据（verifier 或等价检查）

### B) Safety Boundary（安全边界）

- [ ] **B1**：default_path_disabled=true（whitebox/断言口径）
- [ ] **B2**：no execute leakage（断言为 true + trace 中无执行语义）
- [ ] **B3**：no default-on（断言为 true）
- [ ] **B4**：no side effects expansion（断言为 true）
- [ ] **B5**：candidate-only（allows_execute_now=false；模型无执行权）

### C) Scope（范围）

- [ ] **C1**：仍为 Option A only（不扩 B/C/D）
- [ ] **C2**：不进入 full controlled trial
- [ ] **C3**：不开放真实用户测试
- [ ] **C4**：环境约束写死（无高风险过街/夜间/雨天/高拥挤）
- [ ] **C5**：人员三角色齐备（operator/safety_observer/record_owner）

### D) Run Control（运行控制与可回退）

- [ ] **D1**：timebox 已配置且上限明确
- [ ] **D2**：abort 方法就绪（可立即停止）
- [ ] **D3**：archive_root 路径规划明确且空目录校验启用
- [ ] **D4**：validator 可用且可在 run 后立即执行
- [ ] **D5**：post-run review 必做（先 review 再扩大）

## 3. 允许进入的判定规则（写死）

- 若 A/B/C/D 全部满足：**eligible = true**
- 若存在任一 hard blocker（validator 非 go、required_files 缺失、manifest fail、安全断言失败、造假风险）：**eligible = false**
- 若仅存在 soft follow-up（例如 frame_ref 可追溯性不足、whitebox 字段较少）：**eligible = true（但必须记录并在 run 中提升证据质量）**

