# unified env 最小接线资格评审（V1）

## 1. 评审目标

在 unified env 已完成：

- shadow 进入主线（默认关闭，不驱动行为）
- 真实 snapshot JSONL 可落盘
- analyzer 可对照统计与导出样本
- mismatch pattern 已归因
- generation audit 已坐实“机制问题”
- family guardrail 已做最小收紧并产出修前/修后对比

的基础上，正式回答：

- **是否具备进入“最小接线实验”的资格**
- **若具备，允许的边界只能是什么**
- **若不具备，还缺什么证据/条件**

本评审不做实现，不改变任何主线决策。

---

## 2. 证据回顾（按时间线）

### 2.1 首个 shadow 窗口（V1）

- 归档：`docs/architecture/cross_domain/LUNA_UNIFIED_ENV_SHADOW_WINDOW_REVIEW_V1.md`
- 结论要点：candidate 稳（1.0）、family 不稳（0.8），出现 P0 字符串诱导错配；具备补缺潜力但证据不稳定。

### 2.2 第二窗口（真实 snapshot，V2）

- 归档：`docs/architecture/cross_domain/LUNA_UNIFIED_ENV_SHADOW_WINDOW_REVIEW_V2.md`
- 修前：`scene_family_match_rate=0.8`，错配集中在 P0，可解释且重复出现。
- 修后（family 护栏最小收紧 + 同窗口重跑）：
  - `scene_family_match_rate: 0.8 → 1.0`
  - `family_mismatch_count: 1 → 0`
  - `scene_candidate_match_rate: 1.0 → 1.0（保持）`

### 2.3 mismatch pattern 清单

- 文档：`docs/architecture/cross_domain/LUNA_UNIFIED_ENV_SHADOW_MISMATCH_PATTERNS_V1.md`
- 结论：错配模式收敛为 P0 为主（字符串诱导跨域错配），非随机噪声。

### 2.4 generation audit（机制审计）

- 文档：`docs/architecture/cross_domain/LUNA_UNIFIED_ENV_GENERATION_AUDIT_V1.md`
- 结论：根因更像 **生成机制过宽**（candidate→family 绑定过紧、强判定过宽挤压 unknown），而非数据不足。

### 2.5 family guardrail 最小修正结果

证据：同窗口修前/修后对比（见 V2 归档中“修前/修后产物与指标”）。

---

## 3. 最小接线资格判断（满足/部分满足/未满足）

### 3.1 已满足（可进入最小接线实验的必要条件）

- **观测证据面闭环已成立**：shadow + snapshot + analyzer + 窗口归档可重复跑。
- **关键错配模式可被机制护栏命中并消除**：P0 在同窗口修后已降为 0。
- **candidate 层未受影响**：`scene_candidate_match_rate` 保持 1.0。
- **仍保持“不驱动行为”默认态**：unified 目前仍是参考/观察层。

### 3.2 部分满足（需要扩大窗口确认稳定性）

- **长期稳定性**：当前提升是在“同一窗口”上验证，仍需更大真实窗口确认不会引入新错配类型。
- **补缺价值**：`unified_helpful_fill_count` 在 V2 为 0，说明补缺收益尚未被真实窗口稳定证明（但这不阻塞“资格评审通过”，只影响接线边界的保守程度）。

### 3.3 未满足（本轮不要求，但决定了不可扩边界）

以下能力/证据 **不具备**，因此不允许进入更宽接线：

- unified 作为**主线决策输入**的安全性证据（无）
- unified **覆盖/替代**垂直 summary 的可靠性证据（无）
- unified 单独驱动分流/路由的长期回归与观测保障（无）

---

## 4. 若允许进入“最小接线实验”，边界必须是什么（写死）

### 4.1 接线定位

**仅允许：只读参考 / 补缺型接线（shadow+观测的“下一小步”）。**

### 4.2 明确禁止（硬约束）

- **禁止** unified 直接参与任何主线决策（分流、gating、orchestrator 顺序、真实输出）。
- **禁止** unified 覆盖或替代 `sidewalk_env_summary_v1` / `retail_env_summary_v1`。
- **禁止** unified 改写或融合 `risk_summary_v1` / `find_item_intent_summary_v1` / `ocr_summary_v1`。
- **禁止** 以 unified 单独决定 `scene_family` 分流或能力开关。

### 4.3 允许的最小接线形态（建议）

只允许在“垂直 summary 缺字段/弱字段”的情况下：

- **补齐观测字段**（例如补 `summary_freshness`、`age_ms` 等）到一个**独立 debug/whitebox 键**（而不是回写垂直键）。
- 或在垂直模块内部做“仅供日志的参考对照”，不影响输出。

> 注：本评审不落实现；这里只固定边界。

---

## 5. 单选结论

**具备进入“最小接线实验”资格。**

但该“最小接线实验”必须严格限定为：

- **只读参考 / 补缺**
- **不覆盖垂直真源**
- **不驱动主线决策**

不允许任何更宽边界的接线。

---

## 一句话收束

unified env 已完成从“纯观察”到“可进入最小接线实验评审”的证据闭环；可以启动**极保守**的最小接线实验（只读参考/补缺），但仍不具备决策输入层资格。

