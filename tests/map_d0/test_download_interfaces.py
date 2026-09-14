import inspect

from map_d0.downloader_interface import MapDownloader


def test_downloader_is_interface_only():
    methods = [m for m in dir(MapDownloader) if not m.startswith("_")]
    for name in ("can_download", "prepare", "download", "verify"):
        assert name in methods
    assert inspect.isabstract(MapDownloader)
