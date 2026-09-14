## C 部分 Issue 模板（Immediate Safety & Veto Bring-Up）

C 阶段总目标一句话：  
在真实运行中，当系统不安全或不确定时，C 能即时 veto 行为（STOP / HOLD），并给出清晰、可播报、可回放的解释。  
C 只拦，不规划；只判定，不执行。

---

## C-1｜C 输入适配器（Snapshot → C）

目标  
把“即时危险事实”统一从 system_snapshot 提供给 C，杜绝旁路信号。

工作内容  
- 定义 C 只读的输入结构（从 snapshot 映射）  
- 明确哪些字段属于 即时危险事实

交付物  
- c/input_adapter.py  
- C 输入结构（最小集）：  
  - perception_health  
  - obstacle_distance  
  - device_state

验收标准  
- C 只从 snapshot 读取输入  
- 无模块向 C 直接传递“私有危险信号”  
- Snapshot 缺字段时有安全 fallback

---

## C-2｜即时危险规则 v0（最小可用）

目标  
在不引入复杂逻辑的情况下，证明 C 在真实运行中真的能拦。

工作内容  
- 实现最小规则集（可配置但先写死）：  
  - 感知失败 → HOLD  
  - 障碍过近 → STOP  
- 规则命中即返回决策

交付物  
- c/rules/basic_rules.py  
- CDecision 枚举（STOP / HOLD / PASS）

验收标准  
- 规则命中时，C 决策稳定、不抖动  
- 未命中规则时明确返回 PASS  
- 同一输入 → 同一决策（可预测）

---

## C-3｜C 决策接口与不变式

目标  
确保 C 的职责边界清晰、不可被绕过。

工作内容  
- 固定 C 决策接口：
```
def decide(c_input) -> CDecision
```
- 增加运行时断言（invariants）：  
  - C 不读 B  
  - C 不读 Risk / Authority  
  - C 不执行动作

交付物  
- c/controller.py  
- c/invariants.py

验收标准  
- 违反不变式立即抛错  
- C 输出不包含执行细节  
- C 决策只依赖输入事实

---

## C-4｜C → 执行层映射（Veto 生效）

目标  
让 C 的 STOP / HOLD 在真实系统中确实生效。

工作内容  
- 定义 C 决策到执行层的标准映射：  
  - STOP → 停止当前行为 + 播报  
  - HOLD → 暂停 / 等待 + 播报  
  - C 决策优先级高于 B

交付物  
- execution/c_veto_adapter.py  
- 执行回执结构（success / rejected / reason）

验收标准  
- C 决策发生时，B 的输出被中断或忽略  
- 执行层可明确区分 STOP / HOLD  
- 执行结果写入 Trace

---

## C-5｜C × B 协同裁决（最小矩阵）

目标  
明确 C 是 veto 层，B 不能绕过。

工作内容  
- 定义最小裁决规则：  
  - C = STOP → 最终 STOP  
  - C = HOLD → HOLD  
  - C = PASS → 交给 B  
- 不允许 B 覆盖 C

交付物  
- governance/bc_arbitration.py（或等价）  
- 最小协同矩阵

验收标准  
- 所有冲突场景裁决唯一  
- 无“双重执行”或“状态打架”  
- 裁决结果可在 Trace 中看到

---

## C-6｜C 决策解释（接入 B 的 Text Generator）

目标  
C 的拦截行为必须能被用户理解。

工作内容  
- 将 C 决策原因传递给 Text Generator  
- 为 STOP / HOLD 准备解释性文本模板

交付物  
- C 决策 reason code  
- 对应文本模板（由 B 提供）

验收标准  
- 每次 C 拦截都有语音解释  
- 解释内容与触发事实一致  
- 文案不使用“系统术语”

---

## C-7｜C 阶段闭环验证（真实运行）

目标  
验证 C 在真实运行中稳定、可解释、不误触。

工作内容  
- 制造至少 2 种危险场景：  
  1. 感知丢失  
  2. 障碍过近  
- 观察系统反应

交付物  
- 运行日志  
- Trace 样本

验收标准  
- C 能即时拦截  
- 系统无崩溃  
- Trace 可完整回放决策过程

---

## C 部分 Gate 验收 Checklist

任一项 NOT DONE → C 阶段失败 → 不允许进入 Task / OCR / 导航

---

### C-F｜功能正确性
- 感知失败 → HOLD 稳定生效  
- 障碍过近 → STOP 稳定生效  
- 无危险 → C 明确 PASS  
- 同一输入 → 同一决策

---

### C-A｜架构约束
- C 只读 system_snapshot  
- C 不读取 B / Risk / Authority  
- C 不执行动作  
- B 无法绕过 C

---

### C-S｜稳定性
- 启用 C 后系统可运行 ≥30 分钟  
- 无决策抖动（频繁 STOP/PASS 切换）  
- C 决策不阻塞主循环

---

### C-T｜可审计性
- 每次 C 决策写入 Trace  
- Trace 包含：  
  - 决策类型  
  - 触发事实  
  - 时间戳  
- 可回放“为什么停 / 等”

---

### C-U｜用户可理解性
- 每次 STOP / HOLD 都有语音解释  
- 文案能被非工程用户理解  
- 用户仅听语音可判断是否安全

---

### ❌ 禁止项（命中即 Fail）
- ❌ C 直接执行动作  
- ❌ C 读取 B 或模型输出  
- ❌ B 覆盖 C 决策  
- ❌ 危险发生无语音反馈  
- ❌ C 决策不可解释

---

## 🛑 C 阶段 Gate 判定
- C-F 全部 DONE  
- C-A 全部 DONE  
- C-S 全部 DONE  
- C-T 全部 DONE  
- C-U 全部 DONE  
- 未命中任何禁止项

➡ 全部勾选 → C = DONE，允许进入 Task / OCR / 导航
