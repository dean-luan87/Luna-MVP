# -*- coding: utf-8 -*-

from __future__ import annotations

from capabilities.voice.bridge.voice_long_input_prefilter_v0 import prefilter_long_voice_text_v0


def test_prefilter_simple_routes_to_turbo() -> None:
    r = prefilter_long_voice_text_v0("导航到协和医院东门。")
    assert r.routing_suggestion == "route_to_turbo"
    assert r.simple_or_complex == "simple"


def test_prefilter_mixed_routes_to_plus() -> None:
    r = prefilter_long_voice_text_v0("我今天有点焦虑，帮我导航到最近的加油站。")
    assert r.routing_suggestion == "route_to_plus"
    assert r.mixed_risk in ("med", "high")


def test_prefilter_unsupported_routes_to_rule_or_reject() -> None:
    r = prefilter_long_voice_text_v0("你帮我自动挂明天上午的号，挂好了再导航去医院。")
    assert r.routing_suggestion == "route_to_rule_or_reject"


def test_prefilter_ordered_itinerary_multi_step_med_stays_turbo_m3_c4() -> None:
    """M3.4 审计：纯顺序型多段导航，multi_step=med 仍 route_to_turbo（L2/L4/L5_C4 形态）。"""
    l2 = prefilter_long_voice_text_v0("先去加油站加满油，再去超市，最后回家。")
    assert l2.multi_step_risk == "med"
    assert l2.mixed_risk == "low"
    assert l2.ordered_itinerary_hint is True
    assert l2.routing_suggestion == "route_to_turbo"

    l4 = prefilter_long_voice_text_v0(
        "明天上午先去税务局办税，然后回公司取公章，中午和客户在陆家嘴吃饭，下午去银行办对公业务，最后回张江办公室。请按顺序帮我拆成可执行的导航步骤，不要合并成一步。"
    )
    assert l4.multi_step_risk == "med"
    assert l4.ordered_itinerary_hint is True
    assert l4.routing_suggestion == "route_to_turbo"

    l5 = prefilter_long_voice_text_v0(
        "我今天的动线比较碎，我慢慢说：早上先去A点取合同，再去B点和法务盖章，中午到C点和合作方吃饭，下午回D点公司上传扫描件，傍晚去E点幼儿园接孩子，晚上回F点小区。每段之间都有真实地点切换，请你按时间顺序拆成多条导航意图，不要压成一条模糊指令。"
    )
    assert l5.multi_step_risk == "med"
    assert l5.ordered_itinerary_hint is True
    assert l5.routing_suggestion == "route_to_turbo"


def test_prefilter_multi_step_med_non_itinerary_stays_plus() -> None:
    """非导航多步（如开发流程）不因 multi_step 误判 turbo。"""
    r = prefilter_long_voice_text_v0("先写代码再测试最后上线。")
    assert r.multi_step_risk == "med"
    assert r.ordered_itinerary_hint is False
    assert r.routing_suggestion == "route_to_plus"


def test_prefilter_cleaned_text_conservative_drops_fillers() -> None:
    r = prefilter_long_voice_text_v0("呃，那个，我想说，导航回家。")
    assert "导航回家" in r.cleaned_text
    assert "呃" not in r.cleaned_text

