# Perception Tool Layer Freeze Report V1

**Phase:** `Phase-P1-Midplatform-Perception-Tool-Layer-Freeze-And-Handoff-v1-001`  
**System ID:** `LunaMidplatformPerceptionToolLayerFreezeV1`  
**Status:** Frozen baseline — no further optimization in this layer

## 冻结目的

当前 Model Test Lens 感知链路已具备可运行、可审查、可复现的 **Perception Tool Layer** 基线。

本阶段**不继续修 SAM prompt、OCR 特例、Grounding/VLM 接入**。  
已知问题全部登记入 `schemas/perception_controller/perception_tool_layer_issue_registry_v1.json`，作为未来 **Luna Perception Controller** 的输入与验证数据。

## 冻结状态

```yaml
architecture_status: frozen
execution_status: available_in_test_only
optimization_status: paused
```

## 冻结版本：治理链

```
Image
  ↓
Observation Attention
  ↓
Task Candidate
  ↓
Runner Admission
  ↓
Controlled Execution
  ↓
Result Envelope
  ↓
Midplatform Processing
  ↓
Model Collaboration Candidate
```

## 已验证能力（测试环境）

| 能力 | 状态 | 备注 |
|------|------|------|
| MobileSAM 分割执行 | GO | Runner 8787 + envelope |
| OCR route candidate | GO | 受控链路，非 fact |
| Dual Route 对照 stub | GO | Route A/B + comparison |
| Scene-Task Model Activation stub | GO | 规则驱动激活计划 |
| Scene-Aware Prompt Policy | GO | 地铁/街景 prompt 修正 |
| Text-First Target Proposal | Planning GO | 未 Execution |

## 上游 GO 基线

- Scene-Task Model Activation Execution GO  
- Scene-Task Model Activation Planning GO  
- Text-First Target Proposal Validation Planning GO  
- Dual Route Perception Validation Execution GO  
- Scene-Aware Segmentation Prompt Policy Execution GO  
- MobileSAM Single Model Execution Integration GO  

## 已知问题（Problem 1–5）

### Problem 1：缺少中台认知控制模型

**当前：**

```
Image → Prompt / Rule → Model
```

**问题：** 模型由静态规则触发。缺少 Scene Understanding、Task Understanding、Attention Decision、Model Selection。

**未来：** Luna Perception Controller 位于模型之前，统一认知决策。

---

### Problem 2：Scene Profile Ownership 不清晰

**当前：** 部分 `scene_profile_candidate` 来自 Runner（如 `mobilesam_image_runner`）。

**问题：** 执行模型反向决定场景。店招图 `ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png` 在 Runner 输出 `unknown_scene`，浏览器侧因 envelope 已有 scene 而不再根据文件名纠正。

**目标：**

```
Image Evidence → Luna Perception Controller → Scene Candidate
```

Runner **不负责**场景判断。

---

### Problem 3：模型职责边界不足

**当前 SAM 承担过多：** 区域发现 + 视觉重点 + 类别暗示 → region proposal 与 semantic understanding 混淆。

**未来职责：**

| 模型 | 职责 |
|------|------|
| SAM | 空间边界 |
| OCR | 文字 |
| Detection | 目标发现 |
| SLAM | 空间连续理解 |
| VLM | 高级语义推理 |

---

### Problem 4：缺少 Model Activation Intelligence

**当前：** 已有 `model_activation_plan_candidate`，但是**规则驱动 stub**。

**未来 Perception Controller：**

```
场景 → 任务 → 观察目标 → 模型选择 → 区域分配
```

---

### Problem 5：主图表达仍偏模型视角

**当前用户感知：** 「模型在画框」— SAM box、region marker、candidate 堆叠。

**未来主图：** Luna 正在观察什么、为什么观察、下一步做什么。模型结果隐藏或降级为内部证据。

## 实证案例（店招图）

**Job:** `job_564f1aa93983`  
**文件:** `ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png`

| 字段 | 实际值 | 期望 |
|------|--------|------|
| scene_profile | `unknown_scene` | `shopfront_sign` |
| prompt_set | `scene_prompt_set_generic_v1` | text-first / shopfront |
| 框语义 | `P1 静态区域候选` ×5 | text_region_candidate |
| ocr_route_candidate | 全 false | OCR 优先激活 |

→ 登记为 `ISSUE_SHOP_SIGN_001`（见 issue registry）

## 本阶段冻结规则（禁止）

- 继续优化 MobileSAM prompt  
- 新增 SAM 场景 prompt  
- 新增 OCR 场景特例  
- 接入新的视觉模型  
- 修改 Runner Governance  
- 修改 Observation Attention Schema  

所有新问题 → `perception_tool_layer_issue_registry_v1.json`

## 下一阶段

**Phase-P1-Midplatform-Luna-Perception-Controller-Planning-v1-001**

讨论重点：

1. Luna Controller 是规则系统、小模型还是 VLM？  
2. 输入吃什么？  
3. 输出控制什么？  
4. 如何从 Observation Attention 演化？  
5. Human Correction 如何形成训练数据？  
6. 何时引入 Gemini/Qwen 作为辅助？  

---

*本报告为 Perception Tool Layer 冻结交付物，不代表生产就绪。*
