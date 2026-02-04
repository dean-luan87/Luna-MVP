# Luna Badge v1.4.3 → 1.4.4 差分说明（DiffSpec）

**当前版本**: v1.4.3  
**目标版本**: v1.4.4  
**文档日期**: 2025-01-05

---

## 概述

本文档说明从 v1.4.3 到 v1.4.4 的预期变更，包括新增功能、接口变更、架构调整等。

---

## 需要新增（1.4.4）

### 1. 多模型调度器（Model Dispatcher v1）

#### 功能描述
实现多模型并行解析和结果合并机制。

#### 核心功能
- ✅ **模型注册**
  - 支持注册多个解析模型
  - 支持模型优先级配置
  - 支持模型健康检查

- ✅ **模型优先级**
  - 主模型（primary）
  - 备用模型（fallback）
  - 优先级排序机制

- ✅ **模型超时**
  - 单模型超时控制
  - 全局超时控制
  - 超时后自动切换

- ✅ **模型故障 fallback**
  - 模型失败检测
  - 自动切换到备用模型
  - 故障恢复机制

- ✅ **多模型结果合并**
  - 规则合并（不做智能，只做规则）
  - 投票机制
  - 结果置信度计算

#### 接口设计
```python
class ModelDispatcher:
    def register_model(self, model_id: str, model: Model, priority: int):
        """注册模型"""
        pass
    
    def parse_with_models(self, input_text: str, models: List[str] = None) -> ParsedIntent:
        """使用多个模型解析"""
        pass
    
    def get_model_health(self, model_id: str) -> Dict:
        """获取模型健康状态"""
        pass
```

#### 文件结构
```
scheduler/
├── dispatcher.py          # 模型调度器
├── model_registry.py      # 模型注册表
├── health_monitor.py      # 健康监控
└── router_rules.py        # 路由规则
```

---

### 2. 问询系统增强（Inquiry v2）

#### 功能描述
增强问询系统的解析能力和智能度。

#### 新增功能
- ✅ **多意图判断**
  - 识别复合意图
  - 意图优先级排序
  - 意图冲突处理

- ✅ **更复杂的回答解析**
  - 支持长句解析
  - 支持上下文理解
  - 支持隐含意图识别

- ✅ **识别"不确定"与"可能"**
  - 模糊度评分
  - 置信度计算
  - 不确定性处理

- ✅ **支持二期语义引擎接入**
  - 语义引擎接口预留
  - 语义引擎结果融合
  - 渐进式升级路径

#### 接口设计
```python
class InquiryParserV2:
    def parse_with_context(self, text: str, context: Dict) -> ParsedIntent:
        """带上下文的解析"""
        pass
    
    def parse_multiple_intents(self, text: str) -> List[ParsedIntent]:
        """多意图解析"""
        pass
    
    def calculate_confidence(self, intent: ParsedIntent) -> float:
        """计算置信度"""
        pass
```

---

### 3. 任务链升级（TaskChain v2）

#### 功能描述
增强任务链的管理能力和灵活性。

#### 新增功能
- ✅ **支持"高优先级任务抢占"**
  - 优先级定义
  - 抢占机制
  - 被抢占任务保存

- ✅ **支持"用户中断任务"**
  - 中断信号处理
  - 中断状态保存
  - 中断恢复机制

- ✅ **支持"取消子任务"**
  - 子任务取消
  - 取消后状态恢复
  - 取消确认机制

#### 接口设计
```python
class TaskChainManagerV2:
    def interrupt_task(self, task_id: str) -> Dict:
        """中断任务"""
        pass
    
    def cancel_subtask(self, subtask_id: str) -> Dict:
        """取消子任务"""
        pass
    
    def set_task_priority(self, task_id: str, priority: int) -> None:
        """设置任务优先级"""
        pass
```

---

### 4. 为二期提供接口预留

#### 语义引擎接口
```python
def semantic_engine_hook(intent: ParsedIntent, context: Dict) -> ParsedIntent:
    """
    语义引擎钩子函数
    
    用于二期语义引擎接入，对意图进行深度理解和增强。
    """
    pass
```

#### 接口位置
- `inquiry/semantic_hook.py` - 语义引擎钩子
- `decision/semantic_integration.py` - 语义集成点

---

## 架构变更

### 新增模块
```
scheduler/              # 新增：模型调度器模块
├── __init__.py
├── dispatcher.py
├── model_registry.py
├── health_monitor.py
└── router_rules.py

inquiry/
├── parser_v2.py        # 新增：增强版解析器
└── semantic_hook.py   # 新增：语义引擎钩子

taskchain/
└── manager_v2.py       # 新增：增强版管理器
```

### 接口变更
- ✅ 保持向后兼容
- ✅ 新增接口不影响现有功能
- ✅ 提供迁移指南

---

## 兼容性保证

### 向后兼容
- ✅ 所有 v1.4.3 的接口继续可用
- ✅ 现有代码无需修改即可运行
- ✅ 数据结构保持兼容

### 迁移路径
- ✅ 提供渐进式升级方案
- ✅ 提供迁移工具
- ✅ 提供迁移文档

---

## 测试要求

### 新增测试
- ✅ 多模型调度器测试
- ✅ 问询系统增强测试
- ✅ 任务链升级测试
- ✅ 语义引擎接口测试

### 回归测试
- ✅ 所有 v1.4.3 测试必须通过
- ✅ 新增功能测试覆盖
- ✅ 集成测试更新

---

## 开发计划

### 阶段 1：多模型调度器（优先级：高）
- 预计时间：2-3 周
- 依赖：无
- 风险：中

### 阶段 2：问询系统增强（优先级：中）
- 预计时间：1-2 周
- 依赖：阶段 1
- 风险：低

### 阶段 3：任务链升级（优先级：中）
- 预计时间：1-2 周
- 依赖：无
- 风险：低

### 阶段 4：接口预留（优先级：低）
- 预计时间：1 周
- 依赖：无
- 风险：低

---

## 风险评估

### 技术风险
- ⚠️ 多模型调度器复杂度较高
- ⚠️ 性能可能受影响
- ✅ 其他功能风险较低

### 兼容性风险
- ✅ 向后兼容性保证
- ✅ 迁移路径清晰
- ✅ 风险可控

---

## 总结

**v1.4.4 主要目标：**
1. ✅ 实现多模型调度器框架
2. ✅ 增强问询系统能力
3. ✅ 升级任务链管理
4. ✅ 为二期预留接口

**预期收益：**
- ✅ 提高解析准确率
- ✅ 增强系统可靠性
- ✅ 提升用户体验
- ✅ 为二期做好准备

---

**文档版本**: v1.0  
**最后更新**: 2025-01-05  
**维护者**: Luna Badge Team













