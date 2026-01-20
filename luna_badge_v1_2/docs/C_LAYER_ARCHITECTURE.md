# C Layer Architecture (v1.4.8)

## 📋 C 板块总体目标

把"Luna 的灵魂（世界语义）"稳定地翻译成"不同身体/场景下用户能听懂的表达"，并且做到：
- **一期**：规则驱动、可控、低歧义、可稳定跑 Demo
- **二期**：情感引擎只影响"表达策略"，不直接产出语言
- **任意新模型/新硬件**：只要遵守契约，即可接入/替换

---

## 🏗️ C 板块分层（最终结构）

C = Cognitive Alignment Layer（认知对齐层），分为 5 层：

### C-1: Expression Contract（表达意图是什么）

**职责**：语义槽位标准

- 定义表达意图的数据结构
- 提供合约验证
- 支持导航、安全等不同类型的合约

**文件**：
- `expression/contracts/base_contract.py`
- `expression/contracts/navigation_contract.py`
- `expression/contracts/safety_contract.py`
- `expression/validators/contract_validator.py`

---

### C-2: Embodiment Context（我是谁/身体形态/单位体系）

**职责**：身体形态选择与单位体系映射

- 定义 EmbodimentProfile（blind / toy / default）
- 单位体系映射（米 vs 步）
- 方向参考系（身体相对 vs 世界相对）

**文件**：
- `expression/context/embodiment_profiles.py`
- `expression/context/embodiment_selector.py`

---

### C-2.5: Cognitive Calibrator（用什么认知协议说）

**职责**：专业/口语/共识词/引导的选择逻辑

- 根据 intent + embodiment + emotion_params 选择协议
- 一期：规则驱动
- 二期：情感引擎只影响参数，不直接产出语言

**文件**：
- `expression/calibrator/protocol.py`
- `expression/calibrator/calibrator_models.py`
- `expression/calibrator/calibrator_engine.py`
- `expression/calibrator/hooks_emotion_engine.py`（二期接口）

---

### C-3: Renderer Runtime（语言执行层）

**职责**：模板/短句/结构化文本，不做自由生成

- 同一 intent 不同协议不同句式
- 一期：模板化输出（不允许自由生成）
- 支持导航、安全等不同类型的模板

**文件**：
- `expression/renderer/render_models.py`
- `expression/renderer/render_engine.py`
- `expression/renderer/templates/nav_templates.py`
- `expression/renderer/templates/safety_templates.py`

---

### C-4: Output Adapter（输出通道映射）

**职责**：输出通道映射（voice/haptic/debug）

- 一期先支持 debug/voice_text
- 后续可接 TTS / 触觉反馈

**文件**：
- `expression/adapters/output_channel_models.py`
- `expression/adapters/output_router.py`

---

## 🔄 数据流

```
Intent (Contract)
    ↓
Embodiment Selector (C-2)
    ↓
Calibrator Engine (C-2.5)
    ↓
Renderer Engine (C-3)
    ↓
Output Router (C-4)
    ↓
Output Channel (DEBUG / VOICE_TEXT / HAPTIC)
```

---

## 📐 一期/二期边界

### 一期（当前阶段）

- ✅ 规则驱动的协议选择
- ✅ 模板化文本渲染
- ✅ 基础词库（内存版）
- ✅ Debug / Voice Text 输出

### 二期（未来扩展）

- 🔮 情感引擎接入（只影响 Calibrator 参数）
- 🔮 词库持久化
- 🔮 TTS 集成
- 🔮 触觉反馈

---

## 🎯 情感引擎接口位

**二期情感引擎的接口位**：只接入 C-2.5（Calibrator），通过参数影响协议/词库/冗余度。

**文件**：`expression/calibrator/hooks_emotion_engine.py`

**约束**：
- 情感引擎不得产生文本
- 只能通过 `adjust_calibration_params` 提供策略参数
- 不影响 C-1 / C-2 / C-3 / C-4 的实现

---

## 🚫 核心约束

1. **Renderer 不允许自由生成**，只允许模板渲染
2. **全部使用 Python 标准库**（dataclasses/enum/typing/time/logging）
3. **不引入第三方依赖**
4. **不接 TTS，不接真实硬件**（一期先用 debug/voice_text 输出）
5. **二期情感引擎只能通过 hooks_emotion_engine.py 提供策略参数，不得产生文本**

---

## 📚 相关文档

- `expression/contracts/` - C-1 合约定义
- `expression/context/` - C-2 身体形态配置
- `expression/calibrator/` - C-2.5 校准器
- `expression/renderer/` - C-3 渲染器
- `expression/adapters/` - C-4 输出适配器
- `expression/validators/` - 合约验证器

---

**文档版本**: v1.4.8 C Layer Skeleton  
**最后更新**: 2025-12-12






