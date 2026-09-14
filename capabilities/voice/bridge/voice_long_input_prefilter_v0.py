# -*- coding: utf-8 -*-
"""
Pre-Filter Layer（最小实现 v0）

目标：给“分档路由设计（M3.3）”提供一个**纯函数**的粗分类/路由建议实现：
- 不改 schema / validator / builder / provider
- 生产消费由 ``LUNA_VOICE_ENABLE_PREFILTER_ROUTING`` 显式开关控制（默认关闭）
- 仅输出 routing_suggestion 与白盒解释字段，便于灰度/回归对照
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Literal, Optional


RoutingSuggestion = Literal["route_to_turbo", "route_to_plus", "route_to_rule_or_reject"]
SimpleOrComplex = Literal["simple", "complex"]
RiskLevel = Literal["low", "med", "high"]


@dataclass(frozen=True)
class VoiceLongInputPreFilterResultV0:
    cleaned_text: str
    non_task_fragments: List[str]

    simple_or_complex: SimpleOrComplex
    mixed_risk: RiskLevel
    unsupported_risk: RiskLevel
    clarification_risk: RiskLevel
    multi_step_risk: RiskLevel
    # 纯顺序型多段导航/行程；与 multi_step=med 组合时可仍走 turbo（M3.4 审计补丁）
    ordered_itinerary_hint: bool

    routing_suggestion: RoutingSuggestion
    notes: str = ""


# mixed：尽量与 M3 case 的 mixed_keywords 对齐，避免把 “背景词” 误判成 mixed。
_MIXED_MARKERS = (
    "头疼",
    "焦虑",
    "反酸",
    "胃",
    "睡眠",
    "低落",
    "失眠",
    # 覆盖 “胃不舒服” 等
    "不舒服",
)

# multi-step：不要把单独出现的 “先” 判成多步；而是用“命中数量阈值”。
_MULTISTEP_CUES = (
    "先",
    "再",
    "然后",
    "接着",
    "之后",
    "最后",
    "上午",
    "中午",
    "下午",
    "晚上",
    "傍晚",
)

# 去冗余：极保守的口头禅/停顿词（仅做轻量清理，不做语义重写）
_FILLER_PREFIXES = (
    "呃",
    "嗯",
    "啊",
    "那个",
    "就是",
    "我想说",
)

# unsupported：优先覆盖 M3 case 里已知的不可执行模式，减少 rule_or_reject 的漏判。
# 顺序型导航/行程：命中其一即视为「明显 itinerary」（与 multi_step cue 解耦，避免非导航多步误判 turbo）
_ITINERARY_EXPLICIT = (
    "导航",
    "路线",
    "动线",
    "按顺序",
    "按时间顺序",
    "行程",
    "每段",
    "拆成",
    "帮我规划",
    "回家",
)

_UNSUPPORTED_MARKERS = (
    "挂号",
    "预约挂号",
    "代挂号",
    "自动挂号",
    "过户",
    "车牌",
    "远程解锁",
    "解锁",
    "门禁",
    "房门",
    "快递",
    "12123",
    "学法",
    "减分",
    "罚款",
    "代缴",
    "年检",
    "检测场",
    "自动下单",
    "下单",
    "外卖",
    "邮件",
    "请假",
    "智能家居",
    "车机系统",
    "全自动",
    "支付",
    "付款",
    "转账",
    "代买",
    "代付",
)


def _norm(text: str) -> str:
    return (text or "").strip()

_FILLER_PREFIX_RE = re.compile(r"^(?:嗯+|呃+|啊+|那个|就是|我想说)(?:[，,。！!？?\s]+)?")
_FILLER_MID_RE = re.compile(r"(?:[，,]\s*)(?:嗯+|呃+|啊+|那个|就是)(?:\s*[，,])")


def _clean_conservative(raw: str) -> str:
    """
    极保守清洗：只剔除明显无意义的口头禅/停顿词，不动 mixed/时间/地点/约束等内容。

    - 仅处理前缀与「逗号夹心」的 filler
    - 不做摘要、不做重排、不做语义改写
    """
    s = _norm(raw)
    if not s:
        return s
    for _ in range(3):
        ns = _FILLER_PREFIX_RE.sub("", s).strip()
        if ns == s:
            break
        s = ns
    s = _FILLER_MID_RE.sub("，", s)
    s = re.sub(r"[，,]{2,}", "，", s).strip(" ，,")
    return s or _norm(raw)


def _ordered_itinerary_hint(cleaned: str) -> bool:
    """
    轻量：纯顺序型多段导航/行程拆解（非 mixed/unsupported 前提下与 multi_step=med 配合用于路由补丁）。

    - 显式导航/行程词（含「回家」等常见终点语义）
    - 或：明显顺序链（先+再/然后/接着，或 最后+先/再）且出现 导航/路线/行程 之一
    """
    if any(k in cleaned for k in _ITINERARY_EXPLICIT):
        return True
    chain = (
        ("先" in cleaned and ("再" in cleaned or "然后" in cleaned or "接着" in cleaned))
        or ("最后" in cleaned and ("先" in cleaned or "再" in cleaned))
    )
    if chain and ("导航" in cleaned or "路线" in cleaned or "行程" in cleaned):
        return True
    return False


def prefilter_long_voice_text_v0(
    raw_text: str,
    *,
    session_hint: str = "",
    max_turbo_chars: int = 60,
    max_plus_chars: int = 220,
) -> VoiceLongInputPreFilterResultV0:
    """
    规则版最小分档：
    - turbo：短、单步、低 mixed/unsupported/clarification 风险
    - plus：mixed/多步/长句/高风险
    - rule_or_reject：高 unsupported 风险（示例：挂号/代付等）
    """
    raw = _norm(raw_text)
    cleaned = _clean_conservative(raw)

    # 风险：unsupported（v0：宁可保守一些；“挂…号”常见表达不一定包含连续“挂号”二字）
    unsup_hit = any(m in cleaned for m in _UNSUPPORTED_MARKERS) or ("挂" in cleaned and "号" in cleaned)
    unsupported_risk: RiskLevel = "high" if unsup_hit else "low"

    # 风险：mixed（仅用弱启发式，后续可接更细的非任务片段抽取）
    mixed_hit = any(m in cleaned for m in _MIXED_MARKERS)
    mixed_risk: RiskLevel = "med" if mixed_hit else "low"

    # 风险：multi-step
    multi_step_hits = sum(1 for cue in _MULTISTEP_CUES if cue in cleaned)
    # 多步阈值：至少命中 3 个 cue，才认为是 multi-step 风险
    multi_step_risk: RiskLevel = "med" if multi_step_hits >= 3 else "low"

    # 风险：clarification（极简：指代词 + 目标缺失倾向；v0 只给占位）
    clarification_risk: RiskLevel = "low"
    if any(p in cleaned for p in ("那个", "那边", "那里", "这个", "它", "他", "她")) and len(cleaned) < 18:
        clarification_risk = "med"

    # non_task_fragments：v0 仅保留命中的 mixed marker 片段（供白盒对照）
    non_task_frags = [m for m in _MIXED_MARKERS if m in cleaned][:3]

    # simple/complex 粗判（不因 ordered_itinerary 改写，便于白盒对照）
    simple_or_complex: SimpleOrComplex = "simple"
    if unsupported_risk == "high" or mixed_risk != "low" or multi_step_risk != "low":
        simple_or_complex = "complex"

    itinerary = _ordered_itinerary_hint(cleaned)

    # 路由建议
    if unsupported_risk == "high":
        routing: RoutingSuggestion = "route_to_rule_or_reject"
    elif clarification_risk != "low":
        routing = "route_to_plus"
    elif simple_or_complex == "simple":
        routing = "route_to_turbo"
    elif (
        mixed_risk == "low"
        and unsupported_risk == "low"
        and multi_step_risk == "med"
        and itinerary
    ):
        # M3.4：纯顺序型多段导航行程不因 multi_step=med 一律进 plus
        routing = "route_to_turbo"
    else:
        routing = "route_to_plus"

    notes = (
        f"len={len(cleaned)};"
        f"mixed={mixed_risk};multi_step={multi_step_risk};unsupported={unsupported_risk};clar={clarification_risk};"
        f"ordered_itinerary={itinerary};"
        f"hint_len={len(_norm(session_hint))}"
    )

    return VoiceLongInputPreFilterResultV0(
        cleaned_text=cleaned,
        non_task_fragments=non_task_frags,
        simple_or_complex=simple_or_complex,
        mixed_risk=mixed_risk,
        unsupported_risk=unsupported_risk,
        clarification_risk=clarification_risk,
        multi_step_risk=multi_step_risk,
        ordered_itinerary_hint=itinerary,
        routing_suggestion=routing,
        notes=notes,
    )

