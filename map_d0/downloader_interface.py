from __future__ import annotations

from abc import ABC, abstractmethod

from map_d0.packages import LayerPackage, LocalPackageState


class MapDownloader(ABC):
    """
    下载器接口（D0 仅定义，不实现）
    - 不允许在 planner/provider 中直接调用
    - 只能由上层 orchestration 显式触发
    """

    @abstractmethod
    def can_download(self) -> bool:
        """当前环境是否允许下载（电量/网络/权限）"""
        raise NotImplementedError

    @abstractmethod
    def prepare(self, pkg: LayerPackage) -> None:
        """下载前准备（目录/空间校验）"""
        raise NotImplementedError

    @abstractmethod
    def download(self, pkg: LayerPackage) -> LocalPackageState:
        """执行下载并返回本地状态"""
        raise NotImplementedError

    @abstractmethod
    def verify(self, state: LocalPackageState, pkg: LayerPackage) -> bool:
        """校验下载结果（checksum/version）"""
        raise NotImplementedError
