#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动图片搜索（使用 DuckDuckGo，无需 API key）
"""

import os
import requests
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    logger.warning("duckduckgo_search 未安装，自动搜图功能不可用。安装命令: pip install duckduckgo-search")


def search_images(keyword: str, max_results: int = 20, save_dir: Optional[str] = None) -> List[str]:
    """
    使用 DuckDuckGo 搜索图片（无需 API key）
    
    Args:
        keyword: 搜索关键词
        max_results: 最多下载多少张
        save_dir: 保存目录（默认：downloads/<keyword>）
    
    Returns:
        下载成功的图片路径列表
    """
    if not DDGS_AVAILABLE:
        logger.error("DuckDuckGo 搜索不可用：duckduckgo_search 未安装")
        return []
    
    if save_dir is None:
        save_dir = f"./downloads/{keyword}"
    
    os.makedirs(save_dir, exist_ok=True)
    
    paths = []
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(keyword, max_results=max_results))
            
            for idx, r in enumerate(results):
                url = r.get("image")
                if not url:
                    continue
                
                try:
                    img_resp = requests.get(url, timeout=5, headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                    })
                    if img_resp.status_code == 200:
                        # 检查是否是图片
                        content_type = img_resp.headers.get("content-type", "").lower()
                        if not content_type.startswith("image/"):
                            continue
                        
                        # 根据内容类型确定扩展名
                        ext = ".jpg"
                        if "png" in content_type:
                            ext = ".png"
                        elif "webp" in content_type:
                            ext = ".webp"
                        
                        fp = os.path.join(save_dir, f"{idx}{ext}")
                        with open(fp, "wb") as f:
                            f.write(img_resp.content)
                        paths.append(fp)
                        logger.debug(f"下载图片成功: {fp}")
                except Exception as e:
                    logger.warning(f"下载图片失败 {url}: {e}")
                    continue
        
        logger.info(f"关键词 '{keyword}' 下载了 {len(paths)} 张图片")
        return paths
    except Exception as e:
        logger.error(f"DuckDuckGo 搜索失败: {e}")
        return []


