# Luna 模型中台落地路线图 v1

> **代码现状**：`mid_platform/model_governance/` 已实现 **P0 + P1 + P2 占位**（见 `LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1.md`）。P2 **仅为** schema + 样例 + 单测，**无**自动评分/提炼/消费执行。  
> **历史叙事**：`../model_platform/LUNA_MODEL_PLATFORM_DOC_AND_OBJECT_ROLLOUT_V1.md`。

---

## 1. 阶段定义

| 阶段 | 含义 |
|------|------|
| **P0** | 登记、任务卡、留痕落盘 |
| **P1** | 静态选路、fallback 解析、主链预检 |
| **P2** | 蜂巢/图书馆/建议 **对象壳**（占位） |

---

## 2. 当前仓库进度

| 阶段 | 文档 | 代码 |
|------|------|------|
| **P0** | 具备 | **已有** |
| **P1** | 具备 | **已有**（骨架） |
| **P2** | 具备 | **已有占位**（`hive/`、`library/`、intake/decision record） |
| **P2+ 运行时** | 部分在 spec | **未做**（引擎、编排、外部 API） |

---

## 3. 建议下一步

蜂巢服务、图书馆流水线、建议四阶段消费、多 provider 接入 — **单独排期**；进仓前先更新 `OBJECT_MAP` 与路线图。

---

## 4. 验收与汇报

- `../model_platform/LUNA_MODEL_MID_PLATFORM_ACCEPTANCE_CHECKLIST_V1.md`  
- `../model_platform/LUNA_MODEL_MID_PLATFORM_REPORT_TEMPLATE_V1.md`  
