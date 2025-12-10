"""
SceneRuntime: 管理场景进入/事件播报/场景结束的 runtime。

P5-3: 提供场景自动播报能力，与 TTS 系统集成。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from task_engine.tts import tts_manager
from task_engine.tts.router_facade import get_tts_router_facade
from task_engine.scene.scene_integration import SceneIntegrationResult
from task_engine.scene.scene_context import SceneContext


@dataclass
class SceneRuntimeOutput:
    """SceneRuntime 的输出结果（P5-3-D: 增强结构化事件）"""
    enter_voice: Optional[str] = None
    hints: List[str] = field(default_factory=list)
    exit_voice: Optional[str] = None
    event_type: Optional[str] = None  # "enter" / "event" / "exit"
    scene_id: Optional[str] = None
    tag: Optional[str] = None


class SceneRuntime:
    """
    管理场景进入/事件播报/场景结束的 runtime。
    
    P5-3: 提供场景自动播报能力，与 TTS 系统集成。
    """

    def handle_enter(self, result: SceneIntegrationResult) -> SceneRuntimeOutput:
        """
        进入新场景时自动播报。
        
        Args:
            result: SceneIntegrationResult 实例
            
        Returns:
            SceneRuntimeOutput: 播报输出结果
        """
        enter_voice = result.enter_voice
        if enter_voice:
            # Step 13: 使用统一入口
            get_tts_router_facade().speak_task(
                enter_voice,
                meta={"stage": "scene_enter", "scene_id": result.context.scene or "", "tag": result.context.tag or ""},
            )
        return SceneRuntimeOutput(
            enter_voice=enter_voice,
            hints=[],
            exit_voice=None,
            event_type="enter" if enter_voice else None,
            scene_id=result.context.scene,
            tag=result.context.tag,
        )

    def handle_events(self, result: SceneIntegrationResult) -> SceneRuntimeOutput:
        """
        播报场景内部关键事件（避免重复）。
        
        Args:
            result: SceneIntegrationResult 实例
            
        Returns:
            SceneRuntimeOutput: 播报输出结果
        """
        spoken = []
        ctx: SceneContext = result.context

        if result.hints:
            for h in result.hints:
                # 使用 hint 文本作为唯一标识，避免重复播报
                hint_id = str(h)
                if hint_id not in ctx.spoken_flags:
                    # Step 13: 使用统一入口
                    get_tts_router_facade().speak_task(
                        h,
                        meta={"stage": "scene_event", "scene_id": ctx.scene or ""},
                    )
                    ctx.spoken_flags.add(hint_id)
                    spoken.append(h)

        return SceneRuntimeOutput(
            enter_voice=None,
            hints=spoken,
            exit_voice=None,
            event_type="event" if spoken else None,
            scene_id=ctx.scene,
            tag=ctx.tag,
        )

    def handle_exit(self, result: SceneIntegrationResult) -> SceneRuntimeOutput:
        """
        当场景结束时播报。
        
        Args:
            result: SceneIntegrationResult 实例
            
        Returns:
            SceneRuntimeOutput: 播报输出结果
        """
        exit_voice = result.exit_voice
        if exit_voice:
            # Step 13: 使用统一入口
            get_tts_router_facade().speak_task(
                exit_voice,
                meta={"stage": "scene_exit", "scene_id": result.context.scene or ""},
            )
        return SceneRuntimeOutput(
            enter_voice=None,
            hints=[],
            exit_voice=exit_voice,
            event_type="exit" if exit_voice else None,
            scene_id=result.context.scene,
            tag=result.context.tag,
        )

