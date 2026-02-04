# main.py 播报链核心代码（供 v1.8.4 集成参考）

## 一、process_frame() 中的决策调用（第 460-462 行）

```python
# 5. v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD）
decision = self._handle_speech_decision(result)
self._execute_speech_decision(result, decision)
```

---

## 二、_handle_speech_decision() 函数（第 485-530 行）

```python
def _handle_speech_decision(self, result: dict) -> dict:
    """
    v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD）
    
    这是唯一允许调用 TTS 的地方，禁止任何模块绕过决策层直呼 TTS
    """
    if not result:
        return {"action": "WAIT", "reason": "no_result"}
    
    # v1.8.3: 构建场景状态（把瞬时识别结果变成可判断的状态）
    scene_state = self.scene_state_builder.build_state(
        objects=result.get("objects", []),
        texts=result.get("texts", []),
        risk_level=None  # 自动判断
    )
    
    # 构建语音播报文本
    voice_text = self._build_voice_text(result)
    
    if not OUTPUT_CONFIG['play_audio'] or not voice_text:
        return {"action": "WAIT", "reason": "audio_disabled_or_no_text"}
    
    # v1.8.3a 阶段 C: 使用决策控制器（只做三态判断，不调用 TTS）
    # v1.8.3: 从 result 中获取 motion_state（禁止凭空创建）
    motion_state = result.get('motion_state')  # 允许为 None
    decision_result = decide(
        scene_state=scene_state,
        speech_gate=self.speech_gate,
        user_state=self.user_state,
        motion_state=motion_state
    )
    
    return decision_result
```

---

## 三、_execute_speech_decision() 函数（第 532-589 行）

```python
def _execute_speech_decision(self, result: dict, decision: dict):
    """
    v1.8.3a 阶段 C: 执行决策结果
    v1.8.3: 支持 RISK_LV1 动作（强制插队）
    
    主循环必须明确消费决策结果，没有 default，没有 else
    """
    action = decision.get("action")
    
    # v1.8.3: Debug 输出威胁语义（只读，不驱动行为）
    threat = decision.get("threat")
    if threat:
        self.logger.debug(
            f"[Threat] level={threat.level.value} type={threat.risk_type} reason={threat.reason}"
        )
    
    # v1.8.3: LV1 风险评估（最高优先级）
    if action == "RISK_LV1":
        # LV1: 强制插队，必须发声
        self._handle_immediate_risk(decision.get("risk_result"))
        return
    
    if action == "SPEAK":
        # 可以且应该说 → 调用 TTS
        scene_state = self.scene_state_builder.build_state(
            objects=result.get("objects", []),
            texts=result.get("texts", []),
            risk_level=None
        )
        voice_text = self._build_voice_text(result)
        if voice_text:
            self._speak_safely(voice_text, scene_hash=scene_state.scene_hash)
        
        # 兼容原有的描述播报（如果配置启用且与 voice_text 不同）
        if OUTPUT_CONFIG['play_audio'] and result.get('description'):
            description = result['description']
            if description != voice_text:
                # 对描述单独决策
                desc_decision = self._handle_speech_decision({"description": description, "objects": result.get("objects", []), "texts": result.get("texts", [])})
                if desc_decision["action"] == "SPEAK":
                    self._speak_safely(description, scene_hash=scene_state.scene_hash)
    
    elif action == "WAIT":
        # 不能说，但系统继续运行 → 不播报（明确：系统在运行，只是不说话）
        self.logger.debug(f"Decision=WAIT reason={decision['reason']}")
        pass
    
    elif decision["action"] == "YIELD":
        # 用户优先 → 主动让位（明确：用户优先，系统让位）
        self.logger.debug(f"Decision=YIELD reason={decision['reason']}")
        pass
    
    # 硬规则：不要 else，不要兜底说一句，WAIT/YIELD 都不播报
```

---

## 四、_handle_immediate_risk() 函数（第 220-240 行）

```python
def _handle_immediate_risk(self, risk_result):
    """
    v1.8.3: 处理立即风险（LV1）
    
    LV1 行为特性：
    - ✅ 可以打断自动播报
    - ❌ 不打断用户正在说的话（由 can_speak 检查）
    - ✅ 用户说话结束后立即补播
    - ✅ 不可被去重
    - ✅ 不可被冷却抑制
    """
    if not risk_result:
        return
    
    # 生成警告文本
    warning = self._generate_risk_warning(risk_result)
    
    if warning:
        # LV1 强制获取 speech_gate（绕过冷却和去重）
        if self.speech_gate.force_acquire(owner="RISK_LV1", source="RISK"):
            try:
                # 直接调用 TTS，不经过 _speak_safely（因为已经强制获取了锁）
                if self.voice and self.voice.is_available:
                    from core.audio_worker import submit_tts
                    submit_tts(warning, self.voice)
            finally:
                # 释放锁（LV1 不设置冷却，因为已经强制清除了）
                self.speech_gate.release()
```

---

## 五、_speak_safely() 函数（第 149-232 行）

```python
def _speak_safely(self, text: str, scene_hash: Optional[str] = None):
    """
    安全的语音播报方法（v1.8.3a: 通过语音总闸统一入口）
    
    关键原则：
    - 必须通过 speech_gate.can_speak() 检查
    - 必须通过 speech_gate.acquire() 获取锁
    - 播报完成后必须 release()
    """
    if not text or not text.strip():
        return
    
    if not self.voice or not self.voice.is_available:
        self.logger.debug("[Speech] 语音模块不可用，跳过播报")
        return
    
    # 检查 speech_gate
    can_speak, gate_reason = self.speech_gate.can_speak(
        scene_hash=scene_hash,
        user_speaking=self.user_state.is_speaking
    )
    
    if not can_speak:
        self.logger.debug(f"[Speech] 语音总闸拒绝: {gate_reason}")
        return
    
    # 获取锁
    if not self.speech_gate.acquire(owner="normal_speech"):
        self.logger.debug("[Speech] 无法获取语音总闸锁")
        return
    
    try:
        # 投递到音频工作线程
        from core.audio_worker import submit_tts
        success = submit_tts(text, self.voice)
        
        if success:
            self.logger.info(f"[Speech] 已投递播报: {text[:50]}...")
        else:
            self.logger.debug(f"[Speech] 播报投递失败: {text[:50]}...")
    finally:
        # 释放锁（设置冷却）
        self.speech_gate.release(
            scene_hash=scene_hash,
            cooldown=self.speech_gate.cooldown_seconds
        )
```

---

## 六、当前优先级顺序

1. **RISK_LV1**（最高优先级）：立即风险，强制插队
2. **YIELD**：用户正在说话，系统让位
3. **WAIT**：speech_gate 拒绝或 LV2 风险
4. **SPEAK**：正常播报

---

## 七、关键数据结构

### decision 字典结构
```python
{
    "action": "SPEAK" | "WAIT" | "YIELD" | "RISK_LV1" | "ADVISORY",  # v1.8.4 新增
    "reason": str,  # 决策原因
    "risk_result": RiskResult,  # v1.8.3 风险评估结果（可选）
    "threat": ThreatAssessment,  # v1.8.3 威胁语义（可选）
    "bypass_speech_gate": bool,  # v1.8.3 LV1 专用
    "wait_mode": str,  # v1.8.3 LV2 专用（如 "RISK_LV2_BACKGROUND"）
    "advisory_text": str,  # v1.8.4 风险告知文本（可选）
    "risk_level": float,  # v1.8.4 当前 RiskLevel（可选）
    "risk_object": RiskObject,  # v1.8.4 触发的危险对象（可选）
}
```

---

## 八、集成点分析

### 当前流程
```
process_frame()
  └─> _handle_speech_decision(result)
        └─> decide(scene_state, speech_gate, user_state, motion_state)
              └─> 返回 decision
  └─> _execute_speech_decision(result, decision)
        ├─> action == "RISK_LV1" → _handle_immediate_risk()
        ├─> action == "SPEAK" → _speak_safely()
        ├─> action == "WAIT" → pass
        └─> action == "YIELD" → pass
```

### v1.8.4 集成点
需要在 `_handle_speech_decision()` 中调用 `RiskAdvisoryService.tick()`，并在 `_execute_speech_decision()` 中处理 `action == "ADVISORY"`。

---

## 九、关键约束

1. **优先级顺序**：
   - RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
   - 但 ADVISORY 不应打断用户说话（与 RISK_LV1 不同）

2. **播报入口**：
   - 所有 TTS 调用必须通过 `_speak_safely()` 或 `submit_tts()`
   - 禁止绕过 speech_gate

3. **决策唯一性**：
   - `_handle_speech_decision()` 是唯一决策入口
   - `_execute_speech_decision()` 是唯一执行入口


