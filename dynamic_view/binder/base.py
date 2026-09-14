from abc import ABC, abstractmethod
from typing import Optional
from dynamic_view.descriptors import EntityDescriptor


class DescriptorBinder(ABC):
    """
    A11-lite：只定义接口
    - match: 尝试返回已有 entity_id
    - match_or_create: 返回 entity_id（必要时创建）
    """

    @abstractmethod
    def match(self, descriptor: EntityDescriptor) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def match_or_create(self, descriptor: EntityDescriptor) -> str:
        raise NotImplementedError
