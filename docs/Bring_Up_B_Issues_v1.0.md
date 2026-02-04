# B 部分 Issue 模板（Language Output Bring-Up）

B 阶段总目标一句话：  
系统可以把任意“决策 / 状态 / 任务”转换为人性化但可控的文本，并通过 TTS 真实播报。  
不是聊天，是系统发声能力。

---

## B-1｜文本生成模块骨架（Text Generator v0）

目标  
建立“决策 / 状态 → 文本”的统一生成入口，替代所有固定文案。

工作内容  
- 建立 Text Generator 模块  
- 定义统一入口：generate_text(context)  
- 明确：所有语音输出必须经由此模块

交付物  
- language/text_generator/  
  - __init__.py  
  - generator.py（主入口）
- 最小接口定义：
```
def generate_text(context: dict) -> str
```

验收标准  
- 可输入任意 context，输出字符串  
- 系统中不存在“直接写死字符串再播报”的路径  
- Text Generator 可被独立调用测试

---

## B-2｜文本模板体系（Template + Slot）

目标  
用模板保证“人性化 + 可控”，避免传统导航腔。

工作内容  
- 建立模板注册表  
- 模板支持 slot 填充（变量替换）  
- 至少支持 3 类模板：  
  1. 状态反馈  
  2. 决策解释  
  3. 任务指令

交付物  
- language/text_generator/templates.py  
- 示例模板（不少于 5 条）

验收标准  
- 不同 context 会命中不同模板  
- 同一模板可复用不同 slot 值  
- 模板修改不影响系统其他模块

---

## B-3｜文本生成策略（什么时候说 / 什么时候不说）

目标  
防止系统“话太多”或“该说不说”。

工作内容  
- 定义最小输出策略：  
  - 哪些事件必须说  
  - 哪些事件可沉默  
- 策略独立于模板

交付物  
- language/text_generator/policy.py

验收标准  
- 在空运行时不会疯狂播报  
- 在关键事件（任务开始 / 危险 / 完成）必然有输出  
- 策略逻辑可被 trace 记录

---

## B-4｜Text Generator → Trace 接通

目标  
所有生成过的文本必须可回放、可审计。

工作内容  
- Text Generator 输出写入 trace  
- Trace 中记录：  
  - 文本内容  
  - 文本类型（状态/解释/指令）  
  - 触发来源

交付物  
- Trace 中新增 language_output 字段

验收标准  
- 每一次播报在 trace 中都有对应文本  
- 可从 trace 重放系统“说过什么”

---

## B-5｜TTS 执行器骨架（Dynamic Text）

目标  
系统可播报任意文本，而非固定文案。

工作内容  
- 建立 TTS Executor  
- 接收字符串输入  
- 支持至少一种播放策略：  
  - 顺序播放 或  
  - 打断当前播放

交付物  
- runtime_adapters/tts_executor.py

验收标准  
- 播报内容来自 Text Generator  
- 不存在“固定文案播放路径”  
- 播报行为写入 trace

---

## B-6｜TTS 播放策略（Queue / Interrupt）

目标  
避免语音混乱、抢话。

工作内容  
- 明确播放策略：  
  - 是否允许打断  
  - 是否排队  
- 策略独立于 TTS 引擎

交付物  
- runtime_adapters/tts_policy.py

验收标准  
- 连续触发多次播报时行为可预测  
- 危险类播报可优先级更高（哪怕只是规则）

---

## B-7｜系统最小发声闭环验证

目标  
验证 B 阶段在真实运行中可用。

工作内容  
- 在 main loop 中制造一个测试事件  
- 事件 → Text Generator → TTS → Trace

交付物  
- 一个最小 demo（不依赖 OCR / 任务 / 危险）

验收标准  
- 系统运行时能主动说一句完整的话  
- 说的内容来自模板  
- Trace 可回放这次播报

---

## B 阶段完成 Gate（必须全部满足）

- 系统不再使用任何固定语音文案  
- 所有语音输出统一经 Text Generator  
- Text Generator 输出可回放  
- TTS 可播报任意文本  
- 连续运行 ≥30 分钟语音行为稳定

满足 → 才允许进入 C（任务 / 危险 / OCR）

---

## B 阶段执行顺序建议（直接照着排）
1. B-1 文本生成骨架  
2. B-2 模板体系  
3. B-3 输出策略  
4. B-5 TTS Executor  
5. B-6 播放策略  
6. B-4 Trace 接通  
7. B-7 闭环验证
