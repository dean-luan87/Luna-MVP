# -*- coding: utf-8 -*-
"""
长输入 → 系统指令候选（规则版 v1）。

只映射白名单 id（internal_task_instructions_v1 / 映射表文档）。
"""

from __future__ import annotations

import re
from typing import List

from shared.schemas.domain_classification import DomainClassificationResult
from shared.schemas.internal_task_instructions_v1 import (
    Device,
    Navigation,
    Observation,
    Task,
)
from shared.schemas.task_domain_v1 import (
    DEVICE_CONTROL,
    NAVIGATION,
    OBSERVATION,
    TASK_CONTROL,
    TASK_QUERY,
    UNSUPPORTED_OR_REJECT,
)

from capabilities.voice.schemas.voice_long_input_instruction_candidate import VoiceLongInputInstructionCandidate


def map_long_input_instructions(
    domain_result: DomainClassificationResult,
    text: str,
    segments: List[str],
) -> List[VoiceLongInputInstructionCandidate]:
    """分类结果 + 原文 + 分段 → 指令候选列表（有序）。"""
    if domain_result.should_reject or domain_result.primary_domain == UNSUPPORTED_OR_REJECT:
        return []

    primary = domain_result.primary_domain
    out: List[VoiceLongInputInstructionCandidate] = []

    # 条件从句：两段时第二段为「如果…」→ 合并为单候选，约束写入 param
    if len(segments) == 2 and re.search(r"如果|除非", segments[1]):
        c = _map_navigation_segment(segments[0].strip(), 0, text)
        if c:
            c.param_candidates = dict(c.param_candidates)
            c.param_candidates["conditional_clauses"] = segments[1].strip()
            c.requires_confirmation_candidate = True
            c.relation_hint = "conditional"
            return [c]

    if primary == DEVICE_CONTROL:
        return _map_device(text)

    if primary == TASK_CONTROL:
        return _map_task_control(text)

    if primary == TASK_QUERY:
        return _map_task_query(text)

    if not segments:
        segments = [text.strip()]

    for idx, seg in enumerate(segments):
        seg = seg.strip()
        if not seg:
            continue
        if primary == NAVIGATION:
            if _segment_prefers_observation(seg):
                c = _map_observation_segment(seg, idx, text)
            else:
                c = _map_navigation_segment(seg, idx, text)
            if c:
                out.append(c)
        elif primary == OBSERVATION:
            c = _map_observation_segment(seg, idx, text)
            if c:
                out.append(c)
        else:
            c = _map_observation_segment(seg, idx, text) or _map_navigation_segment(seg, idx, text)
            if c:
                out.append(c)

    return out


def _segment_prefers_observation(seg: str) -> bool:
    if re.match(r"^带我去|^导航|^去", seg) or seg.startswith("先去") and "找" not in seg:
        return False
    if re.search(r"找|便利店|手机|前面|顺便|路上", seg):
        return True
    return False


def _map_device(text: str) -> List[VoiceLongInputInstructionCandidate]:
    t = text
    if "关机" in t:
        return [
            VoiceLongInputInstructionCandidate(
                system_mapping_candidate=Device.SHUTDOWN,
                param_candidates={},
                requires_confirmation_candidate=True,
                confidence=0.88,
                segment_text=text,
            )
        ]
    if "音量大" in t or "大声" in t:
        return [
            VoiceLongInputInstructionCandidate(
                system_mapping_candidate=Device.VOLUME_UP,
                param_candidates={},
                requires_confirmation_candidate=False,
                confidence=0.85,
                segment_text=text,
            )
        ]
    if "音量小" in t or "小声" in t:
        return [
            VoiceLongInputInstructionCandidate(
                system_mapping_candidate=Device.VOLUME_DOWN,
                param_candidates={},
                requires_confirmation_candidate=False,
                confidence=0.85,
                segment_text=text,
            )
        ]
    if "静音" in t:
        return [
            VoiceLongInputInstructionCandidate(
                system_mapping_candidate=Device.MUTE,
                param_candidates={},
                requires_confirmation_candidate=False,
                confidence=0.85,
                segment_text=text,
            )
        ]
    return [
        VoiceLongInputInstructionCandidate(
            system_mapping_candidate=Device.STATUS_QUERY,
            param_candidates={},
            requires_confirmation_candidate=False,
            confidence=0.6,
            segment_text=text,
        )
    ]


def _map_task_control(text: str) -> List[VoiceLongInputInstructionCandidate]:
    if "暂停" in text:
        sid = Task.PAUSE
    elif "继续任务" in text or ("继续" in text and "任务" in text):
        sid = Task.RESUME
    elif "结束" in text:
        sid = Task.STOP
    else:
        sid = Task.SWITCH
    return [
        VoiceLongInputInstructionCandidate(
            system_mapping_candidate=sid,
            param_candidates={},
            requires_confirmation_candidate=sid in (Task.STOP, Task.SWITCH),
            confidence=0.8,
            segment_text=text,
        )
    ]


def _map_task_query(text: str) -> List[VoiceLongInputInstructionCandidate]:
    if "多久" in text or "ETA" in text.upper():
        sid = Navigation.QUERY_ETA
    elif "哪" in text or "进度" in text:
        sid = Navigation.QUERY_PROGRESS
    elif "接下来" in text or "下一步" in text:
        sid = Task.QUERY_NEXT_STEP
    else:
        sid = Task.QUERY_CURRENT
    return [
        VoiceLongInputInstructionCandidate(
            system_mapping_candidate=sid,
            param_candidates={},
            requires_confirmation_candidate=False,
            confidence=0.82,
            segment_text=text,
        )
    ]


def _map_navigation_segment(seg: str, idx: int, full_text: str) -> VoiceLongInputInstructionCandidate | None:
    if re.search(r"如果|除非", seg):
        return VoiceLongInputInstructionCandidate(
            system_mapping_candidate=Navigation.START,
            param_candidates={"destination": _extract_destination(seg), "conditional": seg},
            requires_confirmation_candidate=True,
            confidence=0.7,
            segment_text=seg,
            ordering_index=idx,
            relation_hint="conditional",
        )
    dest = _extract_destination(seg)
    return VoiceLongInputInstructionCandidate(
        system_mapping_candidate=Navigation.START,
        param_candidates={"destination": dest or "unspecified"},
        requires_confirmation_candidate=dest is None,
        confidence=0.78 if dest else 0.55,
        segment_text=seg,
        ordering_index=idx,
        relation_hint="sequential",
    )


def _map_observation_segment(seg: str, idx: int, full_text: str) -> VoiceLongInputInstructionCandidate | None:
    if "手机" in seg:
        return VoiceLongInputInstructionCandidate(
            system_mapping_candidate=Observation.FIND_OBJECT,
            param_candidates={"target_type": "phone"},
            requires_confirmation_candidate=False,
            confidence=0.84,
            segment_text=seg,
            ordering_index=idx,
        )
    if "前面" in seg or "前方" in seg:
        return VoiceLongInputInstructionCandidate(
            system_mapping_candidate=Observation.QUERY_FRONT,
            param_candidates={"scope": "forward"},
            requires_confirmation_candidate=False,
            confidence=0.83,
            segment_text=seg,
            ordering_index=idx,
        )
    if "便利店" in seg or "买" in seg or "找" in seg:
        return VoiceLongInputInstructionCandidate(
            system_mapping_candidate=Observation.FIND_PLACE,
            param_candidates={"target_type": "convenience", "constraints": seg},
            requires_confirmation_candidate=False,
            confidence=0.75,
            segment_text=seg,
            ordering_index=idx,
        )
    if "顺便" in seg or "路上" in seg:
        return VoiceLongInputInstructionCandidate(
            system_mapping_candidate=Observation.QUERY_NEARBY,
            param_candidates={"target_type": "convenience", "scope": "along_route"},
            requires_confirmation_candidate=False,
            confidence=0.72,
            segment_text=seg,
            ordering_index=idx,
            relation_hint="accompanying",
        )
    return VoiceLongInputInstructionCandidate(
        system_mapping_candidate=Observation.QUERY_FRONT,
        param_candidates={},
        requires_confirmation_candidate=False,
        confidence=0.55,
        segment_text=seg,
        ordering_index=idx,
    )


def _extract_destination(seg: str) -> str | None:
    m = re.search(r"带我去(.+)|去(.+?)(?:$|，|再|然后)|去医院|去商场|去便利店|导航到(.+)", seg)
    if not m:
        if "医院" in seg:
            return "hospital"
        if "商场" in seg:
            return "mall"
        if "便利店" in seg:
            return "convenience_store"
        return None
    for g in m.groups():
        if g:
            return g.strip()[:64]
    return None
