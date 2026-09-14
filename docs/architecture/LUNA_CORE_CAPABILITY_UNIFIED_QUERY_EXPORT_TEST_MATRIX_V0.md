# Phase-CoreCapability-TRW-Unified-004
# Unified Query / Export Test Matrix v0

---

## A. 输入可读性

- A1：Phase-003 input root 可读

---

## B. Query 功能

- B1：capability filter 可用（yolo/ocr/voice/all）
- B2：stage_name filter 可用
- B3：missing_field filter 可用
- B4：hard_audit_only filter 可用（异常筛选）
- B5：request_id filter 可用
- B6：query 输出 json/jsonl/md 生成且非空（至少 summary）

---

## C. Export 功能

- C1：capability table 生成且包含 yolo/ocr/voice
- C2：stage table 非空
- C3：hard audit table 生成
- C4：missing fields table 生成
- C5：field-level mapping report 生成（字段级，不是结构统计）
- C6：export report md 生成

---

## D. 边界回归

- D1：不修改输入 root（只读）
- D2：不接 runtime，不执行真实 TTS，不执行导航动作

