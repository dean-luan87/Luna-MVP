# Luna Model Manager — Local Model Integration Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-Planning-v1-001`  
**Layer:** Model Manager → Local Runtime Provider  
**Mode:** Planning only — 验证不同运行形态的统一管理，非真正部署 InternVL/MiniCPM-V。

---

## 1. 战略定位

Qwen-VL DryRun 已验证 **External API Model**。本阶段验证 **Local Runtime Model**。

真正目标不是「接 InternVL」，而是：

> Luna Model Manager 能否管理不同运行形态的模型，且上层逻辑不变。

```
                Model Manager
                      |
        --------------------------------
        |                              |
 External Provider              Local Runtime Provider
        |                              |
     Qwen-VL                    InternVL / MiniCPM-V
        |                              |
    API Call                    Local Inference Runtime
        ↓                              ↓
          Evidence Candidate → Validation
```

---

## 2. 统一模型抽象（禁止两套逻辑）

Model Registry **不**按 `type: api` / `type: local` 分叉实现。

统一字段：

```json
{
  "model_id": "internvl2_5",
  "execution_mode": "local_runtime",
  "capabilities": ["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"],
  "provider_adapter": "local_vlm_adapter",
  "resource_profile_ref": "internvl2_5_resource_v1"
}
```

External 示例：

```json
{
  "model_id": "qwen_vl",
  "execution_mode": "external_api",
  "provider_adapter": "qwen_vl_provider_adapter"
}
```

Model Manager **不关心模型在哪里运行**，只关心：capability、lifecycle、resource availability、routing score。

---

## 3. Runtime Adapter 层

```
model_manager/runtime/
├── local_model_runtime_adapter_v1.py
├── runtime_health_checker_v1.py
├── runtime_resource_profile_v1.py
└── runtime_policy_v1.json
```

Local 模型链路：

```
Model Manager → Local Runtime Adapter → GPU/CPU Runtime → InternVL
```

---

## 4. Local Model 生命周期（扩展）

```
Model Discovery → Candidate → Environment Check → Runtime Compatibility
      → Benchmark → Admission → Active
```

失败路径 → `blocked`（非安装即用）。

检查项：CUDA available、VRAM sufficient、inference latency、capability benchmark。

---

## 5. Resource Profile

API 关注：cost、latency、quota  
Local 关注：GPU memory、CPU load、temperature、power、concurrent jobs

```json
{
  "model_id": "internvl2_5",
  "runtime": "local",
  "resource": {
    "gpu_memory_required_gb": 8,
    "inference_time_ms_avg": 2000,
    "concurrent_limit": 1
  }
}
```

---

## 6. Routing：能力 + 运行环境

```
capability_match + resource_availability → provider_selection_candidate
```

不一定选最高能力分——GPU busy 时可能 fallback 到 Qwen API（**provider fallback candidate**，非静默替换）。

---

## 7. Smoke Cases

- **A** Local model 正常接入：candidate → runtime check → benchmark → active → routing eligible
- **B** GPU 不足：not_available → provider fallback candidate（Qwen API）
- **C** Local vs External 竞争：quality + latency + cost + resource → selection
- **D** Local 版本升级：v1 active → v2 benchmark → v2 active → v1 deprecated

---

## 8. 本阶段不做

- 真正训练 / fine-tuning / 修改权重
- 自建大模型训练链

目标：**Luna 能管理任何模型**。

---

## 9. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-DryRun-v1-001`

完成后再接 Gemini、InternVL、MiniCPM-V 时，意义是扩展 Model OS，而非重新集成。
