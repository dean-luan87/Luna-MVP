"""
测试 demo_askchain.py 的稳定性
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest


def test_demo_import():
    """测试 demo 模块可以正确导入"""
    import scripts.demo_askchain as demo
    assert hasattr(demo, "run_demo")


def test_demo_runs_without_error():
    """测试 demo 可以运行且不报错"""
    import scripts.demo_askchain as demo
    ok = demo.run_demo()
    assert ok is True


def test_demo_has_expected_output(capsys):
    """测试 demo 输出包含预期内容"""
    import scripts.demo_askchain as demo
    demo.run_demo()
    captured = capsys.readouterr()
    assert "AskChain Started" in captured.out
    assert "AskChain Completed" in captured.out












