# NT Coordination Review M0

**文件**：`docs/NT_COORDINATION_REVIEW_M0.md`  
**依据**：`docs/NARRATIVE_TRACE_SUPPORT_HEURISTIC_TIGHTENING_M0.md`、`docs/REAL_SCENARIO_PACK_M1_8_DELIVERY.md`、`logs/real_scenario_pack_m18.json`、`logs/benchmark_triage_board_m18.json`、`logs/nt_coordination_m18_analysis.json`

## 一、文档定位

1. 本轮**不是**功能开发。  
2. 本轮**不是**启发式修改。  
3. 本轮是对 `nt` 协同表现的复盘（只读分析）。  
4. 本文回答：
   - 为什么 `nt` 已经能亮，但在 `pc/lg` 有张力时仍常为 `none`
   - 这是缺陷还是保守设计边界
   - 当前 `nt` 是否达到 M1.x 阶段“可接受”水平

---

## 二、核心事实（M1.8）

来源：`logs/nt_coordination_m18_analysis.json`

- 总样本：`106`
- `nt` 分布：`none=79`、`low=13`、`medium=13`、`unknown=1`
- `nt` 命中（low/medium）总数：`26`
- `nt` 命中原因分布：
  - `thin_key_anchors_for_long_narrative(key=9,types=9)`：`13`
  - `slightly_thin_key_anchors_for_long_narrative(key=10,types=10)`：`13`

交叉关系：

- `pc_high + nt_none = 71`
- `pc_high + nt_hit = 7`
- `lg_high + nt_none = 18`
- `lg_medium + nt_hit = 13`
- `advisory_hit + nt_none = 12`
- `advisory_hit + nt_hit = 0`

---

## 三、必须回答的问题

### 1) `nt` 当前命中了什么样的样本

**结论**：命中样本主要集中在“长叙事 + key anchors 偏薄（9/10 档）”，与 tightening 设计目标一致。

代表（A 类）：

- `R101_long_narrative_sparse_key_anchors_should_raise_nt_real`：`nt=low`
- `R106_entry_summary_smooth_but_key_support_thin_review_only_real`：`nt=low`
- `R1_container_real`、`R2_occlusion_real`：`nt=medium`

说明：`nt` 已从“全 none”走到“可解释的薄证据信号”，且 reason 文本可读、稳定。

### 2) 为什么 `pc/lg` 有张力时 `nt` 仍常为 `none`

**主因是职责分工，不是单点坏掉**：

1. `nt` 关注“叙事是否被关键证据支撑”，不是“总体风险高低”；`pc/lg` 关注的是 phase/closure 错位与局部-全局推进张力。  
2. 当前 `nt` 判定使用 key anchors 阈值（9/10 命中，11+ 回落）；许多 `pc/lg` 高张力样本仍有足够锚点，所以 `nt=none` 是规则内结果。  
3. `advisory_hit + nt_none = 12` 表明：SF-1′ 与 `nt` 不是同一任务维度，`nt` 不该替代 advisory。

### 3) 当前保守性是合理还是偏过头

**判断**：当前保守性**总体合理**，但协同能力仍有“可改进空间”。

- 应保持 `none` 的场景（正确边界）：
  - 健康复杂且支撑充分：`R102`、`R105`、`R97`
  - advisory 强但证据锚点并不薄：`R104`
- 理论上“可协同点亮但没亮”的场景：
  - `R103`（`pc=high`、`lg=medium`、`nt=none`）
  - 以及大量 `pc_high_nt_none`（71）中的部分样本，可能存在“风险高但叙事锚点仍够”的情况

这不是“`nt` 错了”，而是 `nt` 的当前定义偏“证据薄弱探测器”，天然不会跟所有高风险维同步。

---

## 四、样本复盘（正/反/近邻）

### A. `nt` 命中样本（正样本）

- `R101`、`R106`：`nt=low`，符合“长叙事 + 锚点偏薄”  
- `R1`、`R2`：`nt=medium`，同样落在薄锚点阈值

### B. `pc/lg` 高张力但 `nt=none`（协同弱样本）

- `R103`：`pc=high`、`lg=medium`、`nt=none`（本轮指定样本）  
- `R104`：`pc=high`、`lg=high`、`advisory_hit=true`，但 `nt=none`（说明 `nt` 并非总风险裁判）

### C. 健康复杂对照

- `R102`、`R105`、`R97`：`nt` 保持 `none`，未见误伤升级

---

## 五、分析维度结论

### A. `nt` 命中分布

- 命中数 `26/106`，并非泛滥。
- 命中理由几乎都落在“薄锚点”两档（9/10），符合目标。

### B. 与 `pc/lg` 交叉

- `pc` 高样本里，`nt` 大多不亮（71 vs 7）  
- `lg` 高样本中也存在较多 `nt=none`（18）  
- 说明当前 `nt` 与 `pc/lg` 并非强绑定，属于“分工式协同”

### C. 健康样本误伤

- 健康复杂样本总体维持 `none/low`，未出现明显误伤扩散。

### D. 协同缺口

- 当前 `nt` 不应与 `pc/lg` 强绑定是**设计成立**的一面。  
- 但若目标是“在部分高风险场景更积极协同提示”，仍缺“跨维协同触发”的观察逻辑（当前无此层）。

---

## 六、职责与边界（必须写清）

### 1) `nt` 当前主要职责

`nt` 是**薄证据叙事观察器**，不是总体风险裁判器，不负责替代 `pc/lg`、severity 或 advisory。

### 2) 当前合理边界

- `pc/lg` 高但证据锚点充分时，`nt=none` 是合理结果。  
- 若要让 `nt` 在更多高风险场景“协同亮”，那是下一层“跨维协同观察”设计，不应把当前 `nt` 判定为失败。

### 3) 是否继续 `nt` 专项（明确结论）

**结论：可以阶段收口（M0）。**

理由：

- `nt` 已从失敏变成可用弱信号（26 个命中且可解释）；  
- 未出现明显误伤爆炸；  
- 协同偏弱更多是“职责边界”而非当前缺陷。

### 4) 若继续做，优先级建议

若后续要继续，不建议再拧 `nt` 单维阈值；优先级应是：

1. 设计“跨维协同观察层”（例如 `pc_high` 且 `nt_none` 的人工审阅提示，不改 fail）  
2. 再考虑 key anchors 定义细化（语义锚点而非数量锚点）

---

## 七、阶段判断

- 当前 `nt` 达到 M1.x 阶段“够用”标准：**是**。  
- 下一步更合适回到扩包观察（M1.9 或后续批次），验证协同稳定性，而非立即再开 `nt` 单维 tightening 专项。

---

## 八、本轮是否适合作为 `nt` 协同复盘文档

**适合。**  
已覆盖命中结构、交叉统计、正反样本、职责边界与明确决策（收口/继续）。

---

## 九、本轮是否通过

**通过。**

---

## 主线—白盒—日志 串联检查

- **A 主线**：本轮仅复盘，不改主链。  
- **B 白盒**：`nt/pc/lg/advisory` 同帧交叉分析，分工边界清晰。  
- **C 日志**：`logs/real_scenario_pack_m18.json`、`logs/benchmark_triage_board_m18.json`、`logs/nt_coordination_m18_analysis.json` 已落地。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。

