# PHASE_BRIEF

## Phase ID

`Phase-<Name>-v1-001`

## 目标（只做这些）

- 
- 

## 输入 roots（必须存在）

| intake_id | 路径 | 必读文件 |
|-----------|------|----------|
| | `_eval_out/.../` | `summary.json` |

## 输出（必须生成）

- capability: `capabilities/...`
- runner: `tools/evaluation/.../run_..._v1.py`
- verifier: `tools/evaluation/.../verify_..._v1.py`
- smoke: `_eval_out/<phase>_smoke_v0/`

## 边界（禁止）

- [ ] 不执行 human review / 不修改 protected assets
- [ ] 不移动/删除/合并文件
- [ ] 不 runtime / 不 stat-exists-open-read
- [ ] 不写 WorldModel / Memory / Fact / Library
- [ ] 其它：

## 验收标准

| 项 | 要求 |
|----|------|
| verifier | GO |
| min_checks | |
| final_decision | |
| recommended_next_phase | |
| 关键计数 | |

## 文档更新

- [ ] `docs/architecture/.../LUNA_*_V1.md`
- [ ] `docs/architecture/evaluation/LUNA_EVALUATION_*_V1.md`
- [ ] `LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`

## Non-Claims

- 
