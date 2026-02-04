import uuid
from typing import Optional, Dict
from dynamic_view.descriptors import EntityDescriptor
from .base import DescriptorBinder


class SimpleBinder(DescriptorBinder):
    """
    A11-lite 最小可用 binder：
    - 若 descriptor.signature 存在，则用 signature 做稳定映射
    - 不存在 signature：每次创建新 entity_id
    - 不做相似度、不做 re-id，只做“确定性 key 映射”
    """

    def __init__(self):
        self._sig2id: Dict[str, str] = {}

    def match(self, descriptor: EntityDescriptor) -> Optional[str]:
        if descriptor.signature is None:
            return None
        return self._sig2id.get(descriptor.signature)

    def match_or_create(self, descriptor: EntityDescriptor) -> str:
        existing = self.match(descriptor)
        if existing is not None:
            return existing

        # 生成可读 entity_id：kind + short uuid
        eid = f"{descriptor.kind}_{uuid.uuid4().hex[:8]}"

        if descriptor.signature is not None:
            self._sig2id[descriptor.signature] = eid
        return eid
