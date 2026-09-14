# Luna Badge v1.8.1 测试脚本总集

**版本**: V1.8.1  
**创建日期**: 2025-12-29  
**目标**: 验证 v1.8.1 在新增 Observer Mode 能力的同时，始终满足：observer_mode=false ⇒ 行为 / 日志 / 副作用 100% 等价 v1.8

---

## 测试总原则（所有用例通用）

### 双重执行要求

**所有测试必须执行两次**：
1. ✅ `OBSERVER_MODE_ENABLED = true`
2. ✅ `OBSERVER_MODE_ENABLED = false`

### 硬门槛

- **第二次结果必须与 v1.8 完全一致**（这是硬门槛）
- **任一用例失败 ⇒ v1.8.1 不可进入灰度**

---

## 一、正常路径测试（Observer Mode 正向价值）

### TC-01: 导航中主动视角观察（基础）

**场景**: 用户在导航途中正常行走，无危险  
**目标**: 验证 Observer Mode 能进入 BACKGROUND 状态但不打扰

#### A. Given / When / Then

- **Given**: 导航状态 = active，observer_mode=true
- **When**: 前方路径清晰，无风险、无分叉
- **Then**:
  - `observer_mode.active = true`
  - `vision_output_state = BACKGROUND`
  - 不发生主动播报或仅低频提示

#### B. 人工 Checklist

- [ ] 启动导航
- [ ] 正常行走 10–20 秒
- [ ] 确认：
  - [ ] 没有被频繁打断
  - [ ] 若有播报，仅为"我在看着，前方通道正常"

#### C. observer_mode=false 对照

**期望**:
- 行为与 v1.8 完全一致
- 无任何 Observer Mode 相关提示或日志

#### 判定标准

- ✅ true 模式下安静、不干扰
- ✅ false 模式下 100% 等价 v1.8

---

### TC-02: 关键节点确认（CONFIRM）

**场景**: 到达入口 / 分叉点  
**目标**: 验证 CONFIRM 行为与确认逻辑

#### A. Given / When / Then

- **Given**: observer_mode=true，检测到分叉
- **When**: vision_output_state=CONFIRM
- **Then**:
  - 播报确认语句
  - 系统等待 yes/no
  - 不继续推进任务直到确认

#### B. 人工 Checklist

- [ ] 行走至分叉点
- [ ] 听到："你现在对着的是入口，对吗？"
- [ ] 回答"是 / 不是"
- [ ] 确认系统行为跟随选择变化

#### C. observer_mode=false 对照

**期望**:
- 无确认提问
- 行为与 v1.8 默认导航一致

#### 判定标准

- ✅ true 模式下正确确认
- ✅ false 模式下 100% 等价 v1.8

---

### TC-03: 危险场景打断（INTERVENE）

**场景**: 前方出现施工 / 马路  
**目标**: 验证强打断能力

#### A. Given / When / Then

- **Given**: observer_mode=true
- **When**: risk_level=HIGH
- **Then**:
  - `vision_output_state=INTERVENE`
  - 当前播报被中断
  - 输出强提示："停一下，前方是马路"

#### B. 人工 Checklist

- [ ] 模拟接近危险区域
- [ ] 确认系统立即打断
- [ ] 确认语气为"动作级提醒"

#### C. observer_mode=false 对照

**期望**:
- 无新增打断
- 与 v1.8 危险提示策略完全一致

#### 判定标准

- ✅ true 模式下正确打断
- ✅ false 模式下 100% 等价 v1.8

---

## 二、极端 / 边界场景测试

### TC-04: 连续 CONFIRM 失败

**场景**: 用户连续 2 次否认确认  
**目标**: 验证系统不进入异常状态

#### A. Given / When / Then

- **Given**: observer_mode=true
- **When**: 连续 2 次 CONFIRM → 用户回答"不是"
- **Then**:
  - 不崩溃
  - 不死循环
  - `observer_mode.confidence` 下降

#### B. 人工 Checklist

- [ ] 连续否认系统判断
- [ ] 确认系统仍可继续对话
- [ ] 不出现"我不知道了"之类失控输出

#### C. observer_mode=false 对照

**期望**:
- v1.8 无此逻辑
- 行为不变

#### 判定标准

- ✅ true 模式下不崩溃
- ✅ false 模式下 100% 等价 v1.8

---

### TC-05: 等待态安全行为

**场景**: 候诊 / 等待叫号  
**目标**: 验证 waiting_state 下只允许 INTERVENE

#### A. Given / When / Then

- **Given**: waiting_state=true，observer_mode=true
- **When**: 无风险
- **Then**:
  - 不输出 BACKGROUND
  - 不输出 CONFIRM

#### B. 人工 Checklist

- [ ] 进入等待态
- [ ] 确认系统安静
- [ ] 若出现危险 → 仍可打断

#### C. observer_mode=false 对照

**期望**:
- 与 v1.8 等待态完全一致

#### 判定标准

- ✅ true 模式下等待态安静
- ✅ false 模式下 100% 等价 v1.8

---

## 三、回滚等价性测试（最重要）

### TC-06: 全局回滚测试

**场景**: 关闭 Observer Mode  
**目标**: 验证系统完全退化为 v1.8

#### A. Given / When / Then

- **Given**: `OBSERVER_MODE_ENABLED=false`
- **When**: 执行完整导航 / 医院流程
- **Then**:
  - 所有 observer_mode 代码路径跳过
  - 无新增日志字段
  - 无新增播报

#### B. 人工 Checklist

- [ ] 明确关闭 Observer Mode
- [ ] 全流程走一遍
- [ ] 与 v1.8 行为逐项对比

#### C. 对照结果

**期望**: 100% 等价  
**任何差异 ⇒ FAIL**

#### 判定标准

- ✅ 所有行为与 v1.8 完全一致
- ✅ 无任何 Observer Mode 相关输出

---

### TC-07: 日志回滚测试

**场景**: observer_mode=false  
**目标**: 验证日志完全不污染

#### A. Given / When / Then

- **Given**: observer_mode=false
- **When**: 触发所有场景
- **Then**:
  - 日志中不存在 `observer_*` 字段

#### B. 人工 Checklist

- [ ] 检查日志文件 / 控制台
- [ ] 确认字段不存在

#### C. 对照结果

**必须与 v1.8 日志完全一致**

#### 判定标准

- ✅ 日志中无 `observer_*` 字段
- ✅ 日志格式与 v1.8 完全一致

---

## 四、人工求助专项测试（责任边界）

### TC-08: 人工求助触发

**场景**: 复杂环境 + 多次确认失败  
**目标**: 验证系统能主动建议求助

#### A. Given / When / Then

- **Given**: observer_mode=true
- **When**:
  - CONFIRM 连续失败 ≥ 2
  - confidence < threshold
- **Then**:
  - 输出人工求助建议
  - 不强制终止任务

#### B. 人工 Checklist

- [ ] 故意制造混乱场景
- [ ] 确认系统说：
  > "这个场景不太适合我继续指引，建议你向右前方的工作人员求助。"

#### C. observer_mode=false 对照

**期望**:
- v1.8 不会出现该建议

#### 判定标准

- ✅ true 模式下正确触发
- ✅ false 模式下 100% 等价 v1.8

---

### TC-09: 人工求助不越权

**场景**: 普通场景  
**目标**: 验证不会滥用人工求助

#### A. Given / When / Then

- **Given**: observer_mode=true
- **When**: 路径清晰
- **Then**:
  - 不触发人工求助

#### B. 人工 Checklist

- [ ] 正常走流程
- [ ] 确认无多余"找人"建议

#### C. observer_mode=false 对照

**行为一致**

#### 判定标准

- ✅ true 模式下不滥用
- ✅ false 模式下 100% 等价 v1.8

---

## 五、测试完成判定（Release Gate）

### v1.8.1 可以进入灰度 / 内测的必要条件

- ✅ **所有 TC 在 observer_mode=true 下通过**
- ✅ **所有 TC 在 observer_mode=false 下与 v1.8 完全一致**
- ❌ **任一回滚等价性失败 ⇒ 版本冻结**

### 测试执行记录

| 测试用例 | observer_mode=true | observer_mode=false | 状态 |
|---------|-------------------|---------------------|------|
| TC-01: 导航中主动视角观察 | ⬜ | ⬜ | ⬜ |
| TC-02: 关键节点确认 | ⬜ | ⬜ | ⬜ |
| TC-03: 危险场景打断 | ⬜ | ⬜ | ⬜ |
| TC-04: 连续 CONFIRM 失败 | ⬜ | ⬜ | ⬜ |
| TC-05: 等待态安全行为 | ⬜ | ⬜ | ⬜ |
| TC-06: 全局回滚测试 | ⬜ | ⬜ | ⬜ |
| TC-07: 日志回滚测试 | ⬜ | ⬜ | ⬜ |
| TC-08: 人工求助触发 | ⬜ | ⬜ | ⬜ |
| TC-09: 人工求助不越权 | ⬜ | ⬜ | ⬜ |

**状态说明**:
- ✅ PASS
- ❌ FAIL
- ⬜ 未执行

---

## 六、测试执行指南

### 前置条件

1. **环境准备**
   - 确保 v1.8 基线版本可用
   - 确保 v1.8.1 版本已部署
   - 准备测试场景（导航路径、医院场景等）

2. **配置准备**
   - 准备两个配置文件：
     - `config_v1.8.1_observer_on.yaml` (OBSERVER_MODE_ENABLED=true)
     - `config_v1.8.1_observer_off.yaml` (OBSERVER_MODE_ENABLED=false)

3. **日志准备**
   - 确保日志系统可访问
   - 准备日志对比工具

### 执行顺序

1. **第一阶段**: 执行所有 TC 的 observer_mode=true 场景
2. **第二阶段**: 执行所有 TC 的 observer_mode=false 场景
3. **第三阶段**: 对比验证回滚等价性

### 关键检查点

1. **行为对比**
   - 播报内容对比
   - 交互流程对比
   - 状态机行为对比

2. **日志对比**
   - 日志字段对比
   - 日志格式对比
   - 日志数量对比

3. **性能对比**
   - 响应时间对比
   - 资源占用对比

---

## 七、最终工程结论

**v1.8.1 是一个"可插拔、可回滚、可审计"的增强层版本。**  
**它不是一次冒险，而是一次结构性升级。**

### 核心价值

1. **可插拔**: 通过配置开关即可启用/关闭
2. **可回滚**: observer_mode=false 时 100% 等价 v1.8
3. **可审计**: 完整的日志和指标支持

### 质量保证

- ✅ 所有代码遵循 v1.8 冻结态原则
- ✅ 所有新增功能都有安全锚点
- ✅ 完整的测试覆盖和回滚验证

---

## 八、附录

### A. 测试环境要求

- Python 3.8+
- 完整的 Luna Badge 运行环境
- 测试场景数据（导航路径、医院场景等）

### B. 测试工具

- 日志分析工具
- 行为对比工具
- 性能监控工具

### C. 参考文档

- `docs/V1_8_1_LOGGING_METRICS.md` - 日志与指标文档
- `docs/V1_8_1_ENGINEERING_COMPLETE.md` - 工程完成报告
- `docs/V1_8_1_MODULE4_SAFETY_CHECK.md` - 模块 4 安全检查

---

**最后更新**: 2025-12-29  
**维护者**: V1.8.1 开发团队  
**状态**: ✅ 测试脚本就绪，等待执行


