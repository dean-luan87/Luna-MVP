# -*- coding: utf-8 -*-
"""
长语音输入模式判定（规则版 v1.1）。

先于任务域分类：区分 task_only / mixed_task_and_non_task / non_task_only，
并切出供 planner 使用的 task 文本与 non_task_payload。
不接模型。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Tuple

from capabilities.voice.schemas.voice_long_input_input_mode import (
    InputModeJudgement,
    NonTaskPayload,
    NonTaskSegment,
)

# 明显任务/可执行意图锚点（与域分类互补，偏「动作」）
_TASK_ANCHOR = re.compile(
    r"带我去|你先带|先带我去|你帮我|帮我|导航|去医院|去商场|去便利店|便利店"
    r"|看看有没有|提醒我|找手机|找一下手机|附近有什么|前面是什么|左边|右边|厕"
    r"所|买点|先去|再.*去|顺便"
)

# 情绪/叙述/背景（无动作锚点时用于 non_task）
_EMOTION_NARRATIVE = re.compile(
    r"我今天|心情不好|很烦|压力大|你知道吗|小时候|其实.*累|其实.*压力|有点不舒服"
    r"|心情不太好|什么都不顺|很害怕|最近挺累|真的很烦|感觉什么都不顺"
)

# 条件/约束从句：必须留在任务侧，不可当非任务叙述切走
_CONDITIONAL_OR_CONSTRAINT = re.compile(r"如果|要是|除非|就算了|太远算了|太远")


@dataclass(frozen=True)
class LongVoiceModeAnalysis:
    judgement: InputModeJudgement
    task_text_for_planner: str
    non_task_payload: NonTaskPayload


def _segment_has_task(s: str) -> bool:
    """含可执行/可分类为系统任务意图的锚点（含须由域分类拒绝的越权请求，避免误入 non_task_only）。"""
    if _TASK_ANCHOR.search(s):
        return True
    if re.search(r"发消息|替.+发|自动挂号|下单买药|替我下单", s):
        return True
    return False


def _segment_is_non_task_only(s: str) -> bool:
    if _segment_has_task(s):
        return False
    return bool(_EMOTION_NARRATIVE.search(s))


def analyze_long_voice_input_mode(raw_text: str) -> LongVoiceModeAnalysis:
    """
    规则写死 v1.1：
    - 多段（逗号）：分别标任务段 / 非任务段 → 可判 mixed。
    - 单段：有任务锚点 → task_only；纯情绪叙述无任务锚点 → non_task_only；否则交给下游澄清。
    """
    raw = (raw_text or "").strip()
    if not raw:
        return LongVoiceModeAnalysis(
            judgement=InputModeJudgement(
                mode="non_task_only",
                has_task_content=False,
                has_non_task_content=False,
                should_generate_task_plan=False,
                should_preserve_non_task_payload=False,
                reason_notes="empty",
            ),
            task_text_for_planner="",
            non_task_payload=NonTaskPayload(exists=False),
        )

    segments = [s.strip() for s in re.split(r"[，,]", raw) if s.strip()]
    if not segments:
        segments = [raw]

    if len(segments) == 1:
        return _analyze_single_segment(segments[0])

    task_segs: List[str] = []
    non_segs: List[str] = []
    for s in segments:
        if _CONDITIONAL_OR_CONSTRAINT.search(s):
            task_segs.append(s)
        elif _segment_has_task(s):
            task_segs.append(s)
        elif _segment_is_non_task_only(s):
            non_segs.append(s)
        else:
            # 未命中情绪模板也无任务锚点：保守并入任务文本，避免丢指令
            if re.search(r"去|帮|带|看|找|买|导航|附近|前面", s):
                task_segs.append(s)
            else:
                non_segs.append(s)

    if task_segs and non_segs:
        task_joined = "，".join(task_segs)
        payload = NonTaskPayload(
            exists=True,
            segments=[
                NonTaskSegment("emotional_context" if _EMOTION_NARRATIVE.search(x) else "narrative", x)
                for x in non_segs
            ],
            handoff_candidate="emotion_engine_future",
        )
        return LongVoiceModeAnalysis(
            judgement=InputModeJudgement(
                mode="mixed_task_and_non_task",
                has_task_content=True,
                has_non_task_content=True,
                should_generate_task_plan=True,
                should_preserve_non_task_payload=True,
                reason_notes="comma_split_task_and_non_task",
            ),
            task_text_for_planner=task_joined,
            non_task_payload=payload,
        )

    if task_segs and not non_segs:
        return LongVoiceModeAnalysis(
            judgement=InputModeJudgement(
                mode="task_only",
                has_task_content=True,
                has_non_task_content=False,
                should_generate_task_plan=True,
                should_preserve_non_task_payload=False,
                reason_notes="comma_split_task_only",
            ),
            task_text_for_planner="，".join(task_segs),
            non_task_payload=NonTaskPayload(exists=False),
        )

    # 仅非任务段
    payload = NonTaskPayload(
        exists=True,
        segments=[
            NonTaskSegment("emotional_context" if _EMOTION_NARRATIVE.search(x) else "other", x)
            for x in non_segs
        ],
        handoff_candidate="emotion_engine_future",
    )
    return LongVoiceModeAnalysis(
        judgement=InputModeJudgement(
            mode="non_task_only",
            has_task_content=False,
            has_non_task_content=True,
            should_generate_task_plan=False,
            should_preserve_non_task_payload=True,
            reason_notes="comma_split_non_task_only",
        ),
        task_text_for_planner="",
        non_task_payload=payload,
    )


def _analyze_single_segment(s: str) -> LongVoiceModeAnalysis:
    if _segment_has_task(s):
        # 单段内可能仍含情绪子串：保留整段给 planner，可选抽 non_task 摘要（轻量规则）
        extra: List[NonTaskSegment] = []
        if _EMOTION_NARRATIVE.search(s):
            m = re.match(r"^(.{2,40}?)[，,]?\s*(你|先|带|帮|导航|去)", s)
            if m and len(m.group(1).strip()) >= 4:
                extra.append(NonTaskSegment("emotional_context", m.group(1).strip()))
        payload = (
            NonTaskPayload(
                exists=True,
                segments=extra,
                handoff_candidate="emotion_engine_future",
            )
            if extra
            else NonTaskPayload(exists=False)
        )
        mixed = bool(extra)
        return LongVoiceModeAnalysis(
            judgement=InputModeJudgement(
                mode="mixed_task_and_non_task" if mixed else "task_only",
                has_task_content=True,
                has_non_task_content=bool(extra),
                should_generate_task_plan=True,
                should_preserve_non_task_payload=bool(extra),
                reason_notes="single_segment_task" + ("_with_emotional_prefix" if extra else ""),
            ),
            task_text_for_planner=s,
            non_task_payload=payload,
        )

    if _segment_is_non_task_only(s) or (len(s) >= 6 and not _TASK_ANCHOR.search(s)):
        payload = NonTaskPayload(
            exists=True,
            segments=[NonTaskSegment("emotional_context", s)],
            handoff_candidate="emotion_engine_future",
        )
        return LongVoiceModeAnalysis(
            judgement=InputModeJudgement(
                mode="non_task_only",
                has_task_content=False,
                has_non_task_content=True,
                should_generate_task_plan=False,
                should_preserve_non_task_payload=True,
                reason_notes="single_segment_non_task_narrative",
            ),
            task_text_for_planner="",
            non_task_payload=payload,
        )

    # 模糊：仍尝试任务规划（下游澄清）
    return LongVoiceModeAnalysis(
        judgement=InputModeJudgement(
            mode="task_only",
            has_task_content=True,
            has_non_task_content=False,
            should_generate_task_plan=True,
            should_preserve_non_task_payload=False,
            reason_notes="single_segment_fallback_task_assumed",
        ),
        task_text_for_planner=s,
        non_task_payload=NonTaskPayload(exists=False),
    )


def merge_notes(base: str, mode: LongVoiceModeAnalysis) -> str:
    j = mode.judgement.mode
    return f"{base};input_mode={j}"
