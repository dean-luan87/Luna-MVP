# Luna 模型中台骨架 v1

> 定位：Luna 全部模型与外部能力的统一接入、治理、路由、评估中枢。  
> 约束边界与主权划分见同目录 `LUNA_MODEL_PLATFORM_CONSTITUTION_V1.md`。

## 一、中台定位

### 不负责

- 直接替代业务决策  
- 直接替代任务链  
- 直接替代记忆系统  
- 直接替代白盒  

### 负责

- 管模型  
- 管接口  
- 管版本  
- 管路由  
- 管降级  
- 管评估  
- 管监管  

---

## 二、中台四层骨架

### 1. 接入层

**职责**

- 统一接入本地模型、远程模型、自建服务、外部 API  
- 统一鉴权、超时、重试、熔断、限流  
- 统一 request / response adapter  

**产物**

- provider  
- client  
- adapter  
- endpoint config  
- timeout / retry policy  

**一句话**：解决「怎么接」。

---

### 2. 注册与路由层

**职责**

- 记录有哪些模型  
- 每个模型能做什么  
- 当前默认用谁  
- 主备关系是什么  
- 失败时降到谁  

**产物**

- model registry  
- capability tags  
- route selector  
- priority policy  
- fallback map  

**一句话**：解决「该用谁」。

---

### 3. 治理层

**职责**

- 输入裁剪  
- 输出校验  
- schema 验证  
- 安全约束  
- 成本约束  
- 越权阻断  
- fallback 执行  

**产物**

- validator  
- governance rules  
- policy gate  
- safety gate  
- schema guard  
- degradation rules  

**一句话**：解决「能不能放心用」。

---

### 4. 评估与优化层

**职责**

- 记录模型使用表现  
- 做质量评估  
- 做错误归因  
- 做模型对比  
- 提优化建议  

**产物**

- usage record  
- quality record  
- governance record  
- scorecard  
- optimization suggestion  

**一句话**：解决「用得怎么样，怎么优化」。

---

## 三、收束

中台骨架的核心就一句话：

**模型可以帮 Luna 做事，但不能绕过 Luna 的治理体系；模型可以生产、分析、建议，但不能自己审判自己、自己放行自己、自己替换自己。**

（宪法含第十三、十四条；全景见 `LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md`；其余专题见同目录 `LUNA_MODEL_PLATFORM_*.md`。）
