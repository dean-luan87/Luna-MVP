from __future__ import annotations

"""
SceneIntegration: 场景系统对上层（TaskEngine / DecisionCore）的统一入口。

职责（v1.4.7）：
- 将 SceneClassifier / SceneRegistry / SceneContext 串成一条调用链；
- 提供一个高层接口：根据 OCR / objects / gps_hint 等输入，识别场景并更新全局 SceneContext；
- 上层只需调用 ensure_scene_context(...)，即可拿到最新场景上下文。

注意：
- 这一层不直接触碰 TaskChainManager / FlowEngine，只暴露场景信息；
- 后续可以在本模块中增加"场景 → 任务链推荐"的策略。
"""

from dataclasses import dataclass, field
from typing import List, Optional

from task_engine.scene.scene_classifier import SceneClassifier, SceneGuess
from task_engine.scene.scene_context import SceneContext, scene_context_manager
from task_engine.scene.scene_registry import SceneRegistry, ScenePackRef
from task_engine.scene.scene_observer import SceneObserver
from task_engine.scene.scene_pack_loader import ScenePack


@dataclass
class SceneIntegrationResult:
    """
    场景集成结果封装，便于上层使用与测试。

    - context: 更新后的 SceneContext；
    - guess: 本次识别的 SceneGuess；
    - pack_ref: 绑定的 ScenePackRef（可能为 None）。
    - P5-3: 新增自动播报字段
    """

    context: SceneContext
    guess: SceneGuess
    pack_ref: Optional[ScenePackRef]
    # P5-3: 新增自动播报
    enter_voice: Optional[str] = None  # 进入场景时 TTS 文本
    hints: List[str] = field(default_factory=list)  # 场景内事件提示 TTS
    exit_voice: Optional[str] = None  # 离开场景时 TTS 文本


class SceneIntegrationService:
    """
    场景集成服务。

    持有：
    - SceneClassifier：用于场景识别；
    - SceneRegistry：用于从识别结果中找到对应 ScenePackRef。

    提供：
    - ensure_scene_context(): 根据输入识别场景并更新全局 SceneContext。
    """

    def __init__(
        self,
        classifier: SceneClassifier,
        registry: SceneRegistry,
    ) -> None:
        self._classifier = classifier
        self._registry = registry

    def ensure_scene_context(
        self,
        *,
        ocr_text: Optional[str] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
        history_tags: Optional[List[str]] = None,
    ) -> SceneIntegrationResult:
        """
        核心入口：根据 OCR / objects / gps_hint 等信息识别场景，并更新全局 SceneContext。

        行为：
        1. 调用 SceneClassifier.classify(...) 得到 SceneGuess；
        2. 通过 SceneRegistry.get(...) 获取对应 ScenePackRef（若有）；
        3. 若当前上下文为空或 has_scene_changed() 返回 True，则创建新的 SceneContext；
           否则，更新现有 SceneContext；
        4. 将更新后的 SceneContext 写入 scene_context_manager；
        5. 返回 SceneIntegrationResult（context + guess + pack_ref）。
        """
        # 1. 识别场景
        guess: SceneGuess = self._classifier.classify(
            ocr_text=ocr_text,
            objects=objects,
            gps_hint=gps_hint,
            history_tags=history_tags,
        )

        # 2. 绑定 ScenePackRef（若注册过）
        pack_ref: Optional[ScenePackRef] = None
        if guess.scene is not None:
            pack_ref = self._registry.get(guess.scene, guess.tag)

        # 3. 获取当前上下文
        current_ctx: Optional[SceneContext] = scene_context_manager.get_current()

        # 4. 判定是否需要创建新上下文
        # 如果 scene 和 tag 都相同，即使 confidence 有变化，也应该复用上下文
        should_create_new = current_ctx is None
        if current_ctx is not None:
            # 检查 scene 和 tag 是否相同
            if current_ctx.scene != guess.scene or current_ctx.tag != guess.tag:
                # scene 或 tag 不同，需要创建新上下文
                should_create_new = True
            else:
                # scene 和 tag 相同，复用现有上下文（即使 confidence 有变化）
                should_create_new = False

        if should_create_new:
            # 初始化新的上下文（history_tags 从外部输入，也可以包含老的）
            # 如果当前上下文存在，可以保留其 history_tags
            merged_history_tags = history_tags or []
            if current_ctx is not None and current_ctx.history_tags:
                # 合并历史标签，去重
                for tag in current_ctx.history_tags:
                    if tag not in merged_history_tags:
                        merged_history_tags.append(tag)

            ctx = SceneContext.from_guess(
                guess,
                pack_ref=pack_ref,
                ocr_text=ocr_text,
                objects=objects,
                gps_hint=gps_hint,
                history_tags=merged_history_tags,
                metadata={},
            )
        else:
            # 更新现有上下文
            ctx = current_ctx
            ctx.update_from_guess(
                guess,
                pack_ref=pack_ref,
                ocr_text=ocr_text,
                objects=objects,
                gps_hint=gps_hint,
                append_history_tag=True,
            )

        # 5. 写回全局管理器
        scene_context_manager.set_current(ctx)

        # P5-3: 生成进入场景/事件/退出场景的文本
        enter_voice = None
        hints = []
        if should_create_new:
            # 新场景：生成进入播报
            if guess.tag:
                enter_voice = f"您现在处于 {guess.tag} 环境。"
            elif guess.scene:
                enter_voice = f"您现在处于 {guess.scene} 环境。"
        
        # 提取场景包中的 voice_hint
        if pack_ref:
            hints = self._extract_hints_from_pack_ref(pack_ref)

        return SceneIntegrationResult(
            context=ctx,
            guess=guess,
            pack_ref=pack_ref,
            enter_voice=enter_voice,
            hints=hints,
            exit_voice=None,  # 退出场景将在下一个场景进入时生成
        )

    def from_vision(
        self,
        ocr_lines: Optional[List[str]] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
    ) -> SceneIntegrationResult:
        """
        Pro API: 从视觉输入（OCR + YOLO）识别场景并更新 SceneContext。

        这是 Pro 阶段新增的入口，专门用于处理视觉模块的输出。

        Args:
            ocr_lines: OCR 识别到的文本行列表
            objects: YOLO 识别到的物体标签列表
            gps_hint: 可选的 GPS 文本提示

        Returns:
            SceneIntegrationResult: 场景集成结果，包含更新后的 context、guess 和 pack_ref
        """
        # 使用 SceneObserver 进行转换
        observer = SceneObserver(self._classifier)
        
        # 获取当前上下文的 history_tags（如果有）
        current_ctx = scene_context_manager.get_current()
        history_tags = current_ctx.history_tags if current_ctx else None
        
        # 观察视觉输入
        guess = observer.observe(
            ocr_lines=ocr_lines,
            objects=objects,
            history_tags=history_tags,
            gps_hint=gps_hint,
        )

        # 绑定 ScenePackRef（若注册过）
        pack_ref: Optional[ScenePackRef] = None
        if guess.scene is not None:
            pack_ref = self._registry.get(guess.scene, guess.tag)

        # 获取当前上下文
        current_ctx = scene_context_manager.get_current()

        # 判定是否需要创建新上下文
        should_create_new = current_ctx is None
        if current_ctx is not None:
            if current_ctx.scene != guess.scene or current_ctx.tag != guess.tag:
                should_create_new = True
            else:
                should_create_new = False

        if should_create_new:
            # 合并历史标签
            merged_history_tags = history_tags or []
            if current_ctx is not None and current_ctx.history_tags:
                for tag in current_ctx.history_tags:
                    if tag not in merged_history_tags:
                        merged_history_tags.append(tag)

            # 将 OCR 行列表合并为文本
            ocr_text = " ".join(ocr_lines or []) if ocr_lines else None

            ctx = SceneContext.from_guess(
                guess,
                pack_ref=pack_ref,
                ocr_text=ocr_text,
                objects=objects,
                gps_hint=gps_hint,
                history_tags=merged_history_tags,
                metadata={},
            )
        else:
            # 更新现有上下文
            ctx = current_ctx
            ocr_text = " ".join(ocr_lines or []) if ocr_lines else None
            ctx.update_from_guess(
                guess,
                pack_ref=pack_ref,
                ocr_text=ocr_text,
                objects=objects,
                gps_hint=gps_hint,
                append_history_tag=True,
            )

        # 写回全局管理器
        scene_context_manager.set_current(ctx)

        # P5-3: 生成进入场景/事件/退出场景的文本
        enter_voice = None
        hints = []
        if should_create_new:
            # 新场景：生成进入播报
            if guess.tag:
                enter_voice = f"您现在处于 {guess.tag} 环境。"
            elif guess.scene:
                enter_voice = f"您现在处于 {guess.scene} 环境。"
        
        # 提取场景包中的 voice_hint
        if pack_ref:
            hints = self._extract_hints_from_pack_ref(pack_ref)

        return SceneIntegrationResult(
            context=ctx,
            guess=guess,
            pack_ref=pack_ref,
            enter_voice=enter_voice,
            hints=hints,
            exit_voice=None,  # 退出场景将在下一个场景进入时生成
        )
