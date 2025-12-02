#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动搜图模块（支持百度图片、必应图片）
使用 HTML 解析方式，无需 API key
"""

import requests
import os
import uuid
import logging
from typing import List, Optional

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

logger = logging.getLogger(__name__)


class ImageFetcher:
    """自动搜图模块"""
    
    def __init__(self, save_dir="test_engine/data/fetched/"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def fetch_baidu(self, keyword: str, limit: int = 20) -> List[str]:
        """
        从百度图片搜索并下载
        
        Args:
            keyword: 搜索关键词
            limit: 最多下载数量
        
        Returns:
            下载成功的图片路径列表
        """
        if not BS4_AVAILABLE:
            logger.error("BeautifulSoup 未安装，无法使用百度图片搜索。安装命令: pip install beautifulsoup4")
            return []
        
        try:
            import urllib.parse
            query = urllib.parse.quote(keyword)
            url = f"https://image.baidu.com/search/index?tn=baiduimage&word={query}"
            
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            images = soup.find_all("img")
            downloaded = []
            
            for img in images[:limit * 2]:  # 多取一些，因为有些可能下载失败
                if len(downloaded) >= limit:
                    break
                
                src = img.get("src") or img.get("data-src") or img.get("data-imgurl")
                if not src or src.startswith("data:"):
                    continue
                
                # 处理相对路径
                if src.startswith("//"):
                    src = "https:" + src
                elif src.startswith("/"):
                    src = "https://image.baidu.com" + src
                
                try:
                    img_resp = requests.get(src, headers=self.headers, timeout=5)
                    if img_resp.status_code == 200:
                        content_type = img_resp.headers.get("content-type", "").lower()
                        if not content_type.startswith("image/"):
                            continue
                        
                        ext = ".jpg"
                        if "png" in content_type:
                            ext = ".png"
                        elif "webp" in content_type:
                            ext = ".webp"
                        
                        filename = f"{uuid.uuid4()}{ext}"
                        filepath = os.path.join(self.save_dir, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(img_resp.content)
                        
                        downloaded.append(filepath)
                        logger.debug(f"下载成功: {filepath}")
                except Exception as e:
                    logger.debug(f"下载失败 {src}: {e}")
                    continue
            
            logger.info(f"关键词 '{keyword}' 下载了 {len(downloaded)} 张图片")
            return downloaded
        except Exception as e:
            logger.error(f"百度图片搜索失败: {e}")
            return []
    
    def fetch(self, keyword: str, limit: int = 20, source: str = "baidu") -> List[str]:
        """
        统一搜图接口
        
        Args:
            keyword: 搜索关键词
            limit: 最多下载数量
            source: 图片来源（"baidu" 或其他）
        
        Returns:
            下载成功的图片路径列表
        """
        if source == "baidu":
            return self.fetch_baidu(keyword, limit)
        else:
            logger.warning(f"不支持的图片来源: {source}")
            return []


