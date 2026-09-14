from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class S1FixtureCaseV1:
    case_id: str
    title: str
    input_text: str
    ingress_kind: str = "USER_INPUT"
    sensitivity: str = "NORMAL"
    correction_ref: str = ""
    expected_accepted: bool = True
    expected_normalized: str = ""
    expected_rejection_code: str = ""
    duplicate_probe: bool = False
    differential_probe: bool = False


def build_s1_fixture_cases() -> Tuple[S1FixtureCaseV1, ...]:
    return (
        S1FixtureCaseV1("S1-01", "normal Chinese user text", "前面的路封了", expected_normalized="前面的路封了"),
        S1FixtureCaseV1("S1-02", "normal English user text", "The road ahead is closed", expected_normalized="The road ahead is closed"),
        S1FixtureCaseV1("S1-03", "mixed Chinese and English", "前面的 gate closed 了", expected_normalized="前面的 gate closed 了"),
        S1FixtureCaseV1("S1-04", "whitespace normalization", "  请   看   前方\n  ", expected_normalized="请 看 前方"),
        S1FixtureCaseV1("S1-05", "empty input rejection", " \n\t ", expected_accepted=False, expected_rejection_code="EMPTY_INPUT"),
        S1FixtureCaseV1("S1-06", "oversized input rejection", "x" * 4097, expected_accepted=False, expected_rejection_code="INPUT_TOO_LARGE"),
        S1FixtureCaseV1("S1-07", "explicit USER_INPUT", "请告诉我现在的状态", expected_normalized="请告诉我现在的状态"),
        S1FixtureCaseV1("S1-08", "USER_CORRECTION lineage", "刚才的判断不对", ingress_kind="USER_CORRECTION", correction_ref="correction:S1-08", expected_normalized="刚才的判断不对"),
        S1FixtureCaseV1("S1-09", "duplicate input idempotency", "重复输入", duplicate_probe=True, expected_normalized="重复输入"),
        S1FixtureCaseV1("S1-10", "sensitivity preservation", "这是敏感输入", sensitivity="HIGH_SENSITIVITY", expected_normalized="这是敏感输入"),
        S1FixtureCaseV1("S1-11", "trace and provenance reverse lookup", "追踪这条输入", expected_normalized="追踪这条输入"),
        S1FixtureCaseV1("S1-12", "user statement is not Field truth", "前面的路封了", expected_normalized="前面的路封了"),
        S1FixtureCaseV1("S1-13", "user input does not directly create Intent", "我要去那里", expected_normalized="我要去那里"),
        S1FixtureCaseV1("S1-14", "user input does not directly create Task", "帮我处理一下", expected_normalized="帮我处理一下"),
        S1FixtureCaseV1("S1-15", "no provider model or runtime execution", "保持受控", expected_normalized="保持受控"),
        S1FixtureCaseV1("S1-16", "S0 synthetic path remains available", "保留合成回归", expected_normalized="保留合成回归"),
        S1FixtureCaseV1("S1-17", "synthetic versus real contract differential", "比较输入合同", expected_normalized="比较输入合同", differential_probe=True),
        S1FixtureCaseV1("S1-18", "downstream S0 state compatibility", "兼容既有状态", expected_normalized="兼容既有状态"),
        S1FixtureCaseV1("S1-19", "negative guards unchanged", "不触发副作用", expected_normalized="不触发副作用"),
        S1FixtureCaseV1("S1-20", "unrelated S0 behavior unchanged", "不改变其他阶段", expected_normalized="不改变其他阶段"),
    )


__all__ = ["S1FixtureCaseV1", "build_s1_fixture_cases"]
