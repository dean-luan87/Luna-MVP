# tests/test_query_engine.py
from core.query_engine.query_manager import QueryEngine
from core.flow_engine.flow_types import FlowContext


def test_query_engine_goal_question_and_answer():
    ctx = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={"raw_utterance": "我想去医院"},
    )

    engine = QueryEngine()

    # 初始没有 goal_detail，应触发澄清
    assert engine.should_ask_for_goal_disambiguation(ctx) is True

    q = engine.build_goal_question(ctx)
    assert "我想去医院" in q

    # 写回答案后，应不再触发澄清
    engine.save_answer(ctx, "goal_detail", "去中山医院看内科")
    assert ctx.data["goal_detail"] == "去中山医院看内科"
    assert engine.should_ask_for_goal_disambiguation(ctx) is False

    finish_msg = engine.build_finish_confirmation(ctx)
    assert "已经完成" in finish_msg












