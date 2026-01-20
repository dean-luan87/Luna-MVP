# Luna Badge v1.4.3 - Inquiry System（问询系统）完整版设计

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 设计文档  
**标准级别**: 最高工程标准

---

## 📋 概述

建立一个弱语义 + 可控规则 + 可升级到二期情感引擎的问询系统，用于：
- 路线/任务节点确认
- 插入任务确认
- 用户回答解析
- 指令识别
- 闭环决策

---

## 1. 模块总体架构

### 1.1 目录结构

```
inquiry_system/
    __init__.py
    inquiry_manager.py       # 问询调度器
    inquiry_parser.py        # 回答解析器（含规则/同义词/指令解析）
    inquiry_templates.json   # 问句模板库
```

### 1.2 三层结构

#### (1) InquiryManager

**职责**:
- 构建问句
- 调用 TTS 播报
- 接收用户回答
- 调用解析器解析答案
- 返回结构化意图给决策层

#### (2) InquiryParser

**职责**: 将用户文本转成结构化意图

**包含三个解析层级**:
1. 选项匹配（option match）
2. 同义词匹配（synonym match）
3. 指令解析（special intent detect）

**特殊处理**: 如果触发指令 → 标记 `need_confirm=True`，开启二次确认机制。

#### (3) InquiryTemplates

**职责**: 所有问句配置化、可扩展、可替换。

---

## 2. Template 结构规范（inquiry_templates.json）

### 2.1 完整格式

```json
{
  "enter_hospital_flow": {
    "question": "我们已经到医院门口了，需要我带你进去吗？",
    "options": ["是", "否"],
    "synonyms": {
      "是": ["是", "好", "行", "可以", "带我进去", "进去吧"],
      "否": ["否", "不用", "不需要", "先不用", "暂时不要"]
    },
    "map": {
      "是": "CONFIRM",
      "否": "REJECT"
    }
  },
  "resume_main_task": {
    "question": "插入任务已经完成，要继续原来的任务吗？",
    "options": ["继续", "不继续"],
    "synonyms": {
      "继续": ["继续", "好", "行", "可以", "继续往前走", "继续吧"],
      "不继续": ["不继续", "停一下", "不用", "算了", "不走了"]
    },
    "map": {
      "继续": "RESUME",
      "不继续": "ABORT"
    }
  },
  "confirm_new_intent": {
    "question": "你希望我执行：{intent_desc}，对吗？",
    "options": ["是", "否"],
    "synonyms": {
      "是": ["是", "对", "可以", "没错", "确认"],
      "否": ["否", "不要", "不对", "先不用"]
    },
    "map": {
      "是": "CONFIRM",
      "否": "REJECT"
    }
  },
  "subtask_failed": {
    "question": "子任务执行失败，是否继续主任务？",
    "options": ["继续", "不继续"],
    "synonyms": {
      "继续": ["继续", "好", "行", "可以"],
      "不继续": ["不继续", "停一下", "不用"]
    },
    "map": {
      "继续": "RESUME",
      "不继续": "ABORT"
    }
  }
}
```

### 2.2 字段说明

- **question**: 主问句（支持变量替换，如 `{intent_desc}`）
- **options**: 可选项列表
- **synonyms**: 同义词扩展（key 为选项，value 为同义词列表）
- **map**: 回答 → 意图映射（key 为选项，value 为意图类型）

---

## 3. InquiryManager（问询管理器）完整版

### 3.1 完整实现

```python
# -*- coding: utf-8 -*-
"""
问询管理器
"""

import json
import os
from typing import Dict, Any, Optional
from .inquiry_parser import InquiryParser


class InquiryManager:
    """问询管理器"""
    
    def __init__(self, template_path: Optional[str] = None):
        """
        初始化问询管理器
        
        Args:
            template_path: 模板文件路径，默认使用 inquiry_templates.json
        """
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(__file__),
                "inquiry_templates.json"
            )
        
        self.template_path = template_path
        self.templates = self._load_templates()
        self.parser = InquiryParser()
    
    def _load_templates(self) -> Dict[str, Any]:
        """加载问询模板"""
        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load templates: {e}")
            return {}
    
    def build_question(
        self,
        question_type: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        构建问句
        
        Args:
            question_type: 问题类型
            context: 上下文信息（用于变量替换）
            
        Returns:
            dict: 问询结构
        """
        if context is None:
            context = {}
        
        tpl = self.templates.get(question_type)
        
        if not tpl:
            return {
                "type": "inquiry",
                "question": "请再说一遍，我没有听清。",
                "options": ["是", "否"],
                "internal_type": "fallback"
            }
        
        question = tpl["question"]
        
        # 动态填充问句（如 intent_desc）
        if "{intent_desc}" in question and "intent_desc" in context:
            question = question.replace("{intent_desc}", context["intent_desc"])
        
        return {
            "type": "inquiry",
            "question": question,
            "options": tpl["options"],
            "internal_type": question_type,
            "context": context
        }
    
    def handle_user_response(
        self,
        question_type: str,
        user_text: str
    ) -> Dict[str, Any]:
        """
        处理用户回答
        
        Args:
            question_type: 问题类型
            user_text: 用户回答文本
            
        Returns:
            dict: 解析后的意图
        """
        tpl = self.templates.get(question_type, {})
        parsed = self.parser.parse(user_text, tpl)
        return parsed
    
    def ask(
        self,
        question_type: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        构建并返回问询（兼容旧接口）
        
        Args:
            question_type: 问题类型
            context: 上下文信息
            
        Returns:
            dict: 问询结构
        """
        return self.build_question(question_type, context)
```

---

## 4. InquiryParser（解析器）完整版

### 4.1 完整实现

```python
# -*- coding: utf-8 -*-
"""
问询解析器
"""

from typing import Dict, Any, Optional, List


class InquiryParser:
    """问询解析器"""
    
    def __init__(self):
        """初始化解析器"""
        # 指令关键词映射（可扩展）
        self.special_intent_keywords = {
            "INSERT_TASK_TOILET": ["厕所", "洗手间", "卫生间", "去厕所"],
            "CHANGE_DESTINATION": ["换", "改", "改变", "换地方", "改路线"],
            "INSERT_TASK_BUY": ["买", "购买", "买东西", "去商店"],
            "CANCEL_TASK": ["停", "取消", "不要", "算了", "不走了"],
        }
    
    def parse(
        self,
        text: str,
        tpl: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        解析用户回答
        
        Args:
            text: 用户回答文本
            tpl: 问询模板
            
        Returns:
            dict: 解析后的意图
        """
        normalized = text.strip().lower()
        
        # 1. 同义词匹配（优先级最高）
        synonyms = tpl.get("synonyms", {})
        for key, syns in synonyms.items():
            for s in syns:
                if s in normalized:
                    return {
                        "intent_type": tpl["map"][key],
                        "raw": text,
                        "need_confirm": False
                    }
        
        # 2. 精确选项匹配（兜底）
        for opt in tpl.get("options", []):
            if opt in normalized:
                return {
                    "intent_type": tpl["map"][opt],
                    "raw": text,
                    "need_confirm": False
                }
        
        # 3. 指令解析（插入任务/更改目标等）
        intent = self._parse_special_intents(normalized)
        if intent:
            intent["raw"] = text
            intent["need_confirm"] = True  # 二次确认
            return intent
        
        # 4. 无法识别
        return {
            "intent_type": "UNKNOWN",
            "raw": text,
            "need_confirm": False
        }
    
    def _parse_special_intents(
        self,
        text: str
    ) -> Optional[Dict[str, Any]]:
        """
        解析特殊指令
        
        Args:
            text: 用户文本
            
        Returns:
            dict: 解析后的意图或 None
        """
        for intent_type, keywords in self.special_intent_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return {
                        "intent_type": intent_type,
                        "matched_keyword": keyword
                    }
        return None
    
    def parse_response(
        self,
        user_text: str
    ) -> Dict[str, Any]:
        """
        解析用户回答（兼容旧接口，使用默认模板）
        
        Args:
            user_text: 用户回答文本
            
        Returns:
            dict: 解析后的意图
        """
        # 使用默认模板
        default_tpl = {
            "options": ["是", "否"],
            "synonyms": {
                "是": ["是", "好", "行", "可以", "ok", "yes"],
                "否": ["否", "不用", "不需要", "no"]
            },
            "map": {
                "是": "CONFIRM",
                "否": "REJECT"
            }
        }
        return self.parse(user_text, default_tpl)
```

---

## 5. 指令确认机制（正式写入系统契约）

### 5.1 确认流程

当解析器返回：

```python
{
    "intent_type": "INSERT_TASK_TOILET",
    "need_confirm": True
}
```

**DecisionCore 必须**:

1. 输出 `DecisionAction.ASK_USER`
2. 使用问句类型 `confirm_new_intent`
3. context 中传递描述：

```python
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="need_confirm_special_intent",
    params={
        "question_type": "confirm_new_intent",
        "context": {
            "intent_desc": "前往厕所",
            "original_intent": "INSERT_TASK_TOILET"
        }
    }
)
```

**用户确认后才允许执行任务变更**

### 5.2 确认后的处理

用户确认后：

```python
# 用户回答"是"
parsed = {
    "intent_type": "CONFIRM",
    "need_confirm": False
}

# DecisionCore 处理确认
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_confirmed_insert_task",
    params={
        "main_task_id": "...",
        "insert_task_spec": {
            "type": "go_to_toilet",
            "target": {"poi_type": "toilet"}
        },
        "resume_strategy": "auto"
    }
)
```

---

## 6. 决策层与 Inquiry System 联动标准

### 6.1 问询闭环

```
ASK_USER → build_question → 播报 → 用户回答
→ InquiryParser → 结构意图
→ DecisionCore → 决策输出
→ TaskChain 执行
```

### 6.2 完整流程示例

**步骤 1: DecisionCore 输出 ASK_USER**
```python
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="node_requires_confirmation",
    params={
        "question_type": "enter_hospital_flow",
        "context": {...}
    }
)
```

**步骤 2: InquiryManager 构建问句**
```python
inquiry = inquiry_manager.build_question(
    question_type="enter_hospital_flow",
    context={...}
)
# inquiry = {
#     "type": "inquiry",
#     "question": "我们已经到医院门口了，需要我带你进去吗？",
#     "options": ["是", "否"],
#     ...
# }
```

**步骤 3: TTS 播报**
```python
voice.speak(inquiry["question"])
```

**步骤 4: 用户回答**
```python
user_text = "带我进去"
```

**步骤 5: InquiryParser 解析**
```python
parsed = inquiry_manager.handle_user_response(
    question_type="enter_hospital_flow",
    user_text=user_text
)
# parsed = {
#     "intent_type": "CONFIRM",
#     "raw": "带我进去",
#     "need_confirm": False
# }
```

**步骤 6: 生成 USER_INTENT 事件**
```python
DecisionInput(
    event_type=EventType.USER_INTENT,
    event_payload={
        "parsed_intent": parsed
    },
    ...
)
```

**步骤 7: DecisionCore 再次决策**
```python
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_confirmed",
    params={...}
)
```

---

## 7. TaskChain 联动规则（与 A 模块完全兼容）

### 7.1 用户答"继续/不继续"

**直接 → DecisionCore → TaskChain resume/abort**

```python
# 用户回答"继续"
parsed = {
    "intent_type": "RESUME",
    "need_confirm": False
}

# DecisionCore 处理
DecisionOutput(
    action=DecisionAction.CONTINUE_TASK,
    reason="user_confirmed_resume",
    params={
        "task_id": "nav_to_hospital_1"
    }
)

# TaskChainManager 恢复主任务
task_chain_manager._resume_main_task()
```

### 7.2 用户答新指令

**解析 → need_confirm=True → 二次确认 → 确认后 → DecisionCore → INSERT_TASK / REPLACE_TASK 注入 TaskChain**

```python
# 用户回答"先去厕所"
parsed = {
    "intent_type": "INSERT_TASK_TOILET",
    "need_confirm": True
}

# DecisionCore 二次确认
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="need_confirm_special_intent",
    params={
        "question_type": "confirm_new_intent",
        "context": {
            "intent_desc": "前往厕所"
        }
    }
)

# 用户确认后
DecisionOutput(
    action=DecisionAction.INSERT_TASK,
    reason="user_confirmed_insert_task",
    params={...}
)
```

### 7.3 用户答未知语句

**DecisionCore → 再问一次（fallback）**

```python
# 用户回答无法识别
parsed = {
    "intent_type": "UNKNOWN",
    "need_confirm": False
}

# DecisionCore 处理
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="unknown_response",
    params={
        "question_type": "fallback",  # 使用 fallback 模板
        "context": {
            "original_question_type": "enter_hospital_flow"
        }
    }
)
```

---

## 8. 错误处理机制（稳定性保证）

### 8.1 模板缺失

**fallback 为默认问句**

```python
def build_question(self, question_type: str, context: Dict = None):
    tpl = self.templates.get(question_type)
    
    if not tpl:
        return {
            "type": "inquiry",
            "question": "请再说一遍，我没有听清。",
            "options": ["是", "否"],
            "internal_type": "fallback"
        }
    # ...
```

### 8.2 内容识别失败

**intent_type="UNKNOWN" → DecisionCore 再问**

```python
# 解析失败
parsed = {
    "intent_type": "UNKNOWN",
    "raw": "用户说的内容",
    "need_confirm": False
}

# DecisionCore 处理
DecisionOutput(
    action=DecisionAction.ASK_USER,
    reason="unknown_response",
    params={
        "question_type": "fallback",
        "context": {...}
    }
)
```

### 8.3 指令识别冲突

**优先级顺序为**:
1. 同义词匹配（最高优先级）
2. 精确选项匹配
3. 指令识别
4. fallback（最低优先级）

**示例**:
```python
# 用户回答"好"（既是同义词，也可能触发指令）
# 优先匹配同义词
synonyms = {
    "是": ["是", "好", "行", "可以"]
}
# 匹配到"好" → 返回 "CONFIRM"
```

---

## 9. 扩展与升级路径（为二期情感引擎预留能力）

### 9.1 一期结构已为二期设计好升级点

#### 9.1.1 InquiryParser 可扩展为 LLM 意图分类器

```python
# 当前：规则匹配
class InquiryParser:
    def _parse_special_intents(self, text: str):
        # 规则匹配
        ...

# 二期：LLM 分类
class InquiryParser:
    def _parse_special_intents(self, text: str):
        # LLM 意图分类
        return llm_classifier.classify(text)
```

#### 9.1.2 Template 可扩展多风格问句

```json
{
  "enter_hospital_flow": {
    "question": "我们已经到医院门口了，需要我带你进去吗？",
    "question_style": {
      "formal": "我们已经到医院门口了，需要我带你进去吗？",
      "casual": "到啦！要进去吗？",
      "empathetic": "我们已经到医院门口了，你准备好了吗？需要我带你进去吗？"
    }
  }
}
```

#### 9.1.3 need_confirm=True 可支持情绪判断

```python
# 当前：固定 need_confirm=True
if intent:
    intent["need_confirm"] = True

# 二期：根据情绪判断
if intent:
    emotion = emotion_detector.detect(text)
    intent["need_confirm"] = emotion.needs_confirmation()
```

#### 9.1.4 指令识别可升级为 semantic parser

```python
# 当前：关键词匹配
if "厕所" in text:
    return {"intent_type": "INSERT_TASK_TOILET"}

# 二期：语义解析
semantic_result = semantic_parser.parse(text)
return {
    "intent_type": semantic_result.intent,
    "entities": semantic_result.entities
}
```

### 9.2 结构无需改动

- 接口保持不变
- 数据结构向后兼容
- 升级只需替换内部实现

---

## 10. 完整接口定义

### 10.1 InquiryManager 公共接口

```python
class InquiryManager:
    def __init__(self, template_path: Optional[str] = None)
    def build_question(self, question_type: str, context: Dict = None) -> Dict
    def handle_user_response(self, question_type: str, user_text: str) -> Dict
    def ask(self, question_type: str, context: Dict = None) -> Dict
```

### 10.2 InquiryParser 公共接口

```python
class InquiryParser:
    def __init__(self)
    def parse(self, text: str, tpl: Dict) -> Dict
    def parse_response(self, user_text: str) -> Dict
    def _parse_special_intents(self, text: str) -> Optional[Dict]
```

---

## 11. 数据结构定义

### 11.1 问询结构

```python
{
    "type": "inquiry",
    "question": str,
    "options": List[str],
    "internal_type": str,
    "context": Dict
}
```

### 11.2 解析结果结构

```python
{
    "intent_type": str,  # CONFIRM / REJECT / INSERT_TASK_TOILET / UNKNOWN
    "raw": str,
    "need_confirm": bool,
    "matched_keyword": Optional[str]  # 如果是指令识别
}
```

---

## 12. 设计原则总结

### 12.1 核心原则

1. **弱语义处理** - 规则匹配 + 同义词扩展
2. **可控规则** - 所有规则可配置
3. **可升级性** - 为二期 LLM 预留接口
4. **错误容错** - 所有错误都有 fallback
5. **二次确认** - 指令需要确认

### 12.2 工程标准

1. **接口统一** - 所有方法返回统一格式
2. **配置化** - 模板可配置、可扩展
3. **可测试性** - 所有方法都可以独立测试
4. **向后兼容** - 升级不影响现有接口

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**标准级别**: 最高工程标准  
**最后更新**: 2025-12-05













