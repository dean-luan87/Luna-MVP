#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动测试场景组（Playlist）配置
"""

PLAYLISTS = {
    "出门散步": [
        "小区道路",
        "人行道",
        "台阶",
        "斑马线",
    ],
    "去坐地铁": [
        "小区道路",
        "路口",
        "地铁入口",
        "扶梯",
        "站台",
    ],
    "坐公交": [
        "小区道路",
        "公交站牌",
        "上车台阶",
        "车内扶手",
    ],
}


def list_playlists():
    """
    返回所有可用的场景组列表
    
    Returns:
        list: [{"name": "场景组名", "keywords": ["关键字1", "关键字2", ...]}, ...]
    """
    return [
        {"name": name, "keywords": kws}
        for name, kws in PLAYLISTS.items()
    ]


def get_playlist(name):
    """
    获取指定场景组的关键字列表
    
    Args:
        name: 场景组名称
        
    Returns:
        list: 关键字列表，如果不存在则返回 None
    """
    return PLAYLISTS.get(name)


