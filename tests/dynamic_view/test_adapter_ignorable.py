from dynamic_view.attention import AttentionManager
from dynamic_view.adapter import DynamicViewAttentionAdapter


def test_adapter_is_ignorable():
    m = AttentionManager()
    a = DynamicViewAttentionAdapter(m)
    assert m.get() == []
