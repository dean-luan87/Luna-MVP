"""
测试 NavPhraseMapper: 结构化事件 → speech_event 映射
"""

import sys
import os
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.navigation.nav_phrase_mapper import nav_phrase_mapper


def test_obstacle_front_converts_to_safety():
    """测试前方障碍物 → 安全类播报"""
    events = [
        {'type': 'danger', 'code': 'obstacle_front', 'distance': 0.7}
    ]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 1
    ev = speech_events[0]
    assert ev['category'] == 'safety'
    assert ev['decision'] == 'STOP'
    assert ev['priority'] == 2
    assert ev['interruptible'] is True
    assert '障碍物' in ev['text']
    assert '0.7' in ev['text']


def test_stairs_down_converts_to_safety():
    """测试下台阶 → 安全类播报"""
    events = [
        {'type': 'danger', 'code': 'stairs_down', 'distance': 1.5}
    ]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 1
    ev = speech_events[0]
    assert ev['category'] == 'safety'
    assert ev['decision'] == 'CAUTION'
    assert '台阶' in ev['text']


def test_road_narrow_converts_to_navigation():
    """测试道路变窄 → 导航类播报"""
    events = [
        {'type': 'navigation', 'code': 'road_narrow'}
    ]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 1
    ev = speech_events[0]
    assert ev['category'] == 'navigation'
    assert ev['priority'] == 1
    assert ev['interruptible'] is False
    assert '变窄' in ev['text']


def test_multiple_events_converted():
    """测试多个事件同时转换"""
    events = [
        {'type': 'danger', 'code': 'obstacle_front', 'distance': 0.8},
        {'type': 'danger', 'code': 'stairs_down', 'distance': 1.2},
        {'type': 'navigation', 'code': 'road_narrow'},
    ]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 3
    # 检查第一个是安全类
    assert speech_events[0]['category'] == 'safety'
    # 检查第二个也是安全类
    assert speech_events[1]['category'] == 'safety'
    # 检查第三个是导航类
    assert speech_events[2]['category'] == 'navigation'


def test_unknown_code_skipped():
    """测试未知代码被跳过"""
    events = [
        {'type': 'danger', 'code': 'unknown_code', 'distance': 0.5}
    ]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 0


def test_missing_code_skipped():
    """测试缺少 code 的事件被跳过"""
    events = [
        {'type': 'danger', 'distance': 0.5}
    ]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 0


def test_event_without_distance():
    """测试没有距离信息的事件"""
    events = [
        {'type': 'navigation', 'code': 'road_narrow'}
    ]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 1
    ev = speech_events[0]
    assert '变窄' in ev['text']
    # 没有距离占位符
    assert '{distance}' not in ev['text']


def test_raw_event_preserved():
    """测试原始事件被保留在 raw_event 字段"""
    original_event = {'type': 'danger', 'code': 'obstacle_front', 'distance': 0.7, 'custom': 'value'}
    events = [original_event]
    speech_events = nav_phrase_mapper.convert_events(events)
    
    assert len(speech_events) == 1
    assert speech_events[0]['raw_event'] == original_event


if __name__ == "__main__":
    pytest.main([__file__, "-v"])












