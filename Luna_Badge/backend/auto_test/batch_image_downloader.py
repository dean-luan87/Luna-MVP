#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量图片下载工具
支持 URL 列表、关键词搜索、本地文件解析
"""

import os
import json
import csv
import re
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    logger.warning("duckduckgo_search 未安装，关键词搜索功能不可用")


class BatchImageDownloader:
    """
    批量图片下载器
    """
    
    def __init__(
        self,
        output_dir: str = "downloads",
        max_workers: int = 5,
        timeout: int = 10,
        retry_times: int = 3,
        retry_delay: float = 1.0
    ):
        """
        初始化批量下载器
        
        Args:
            output_dir: 输出目录
            max_workers: 最大并发数
            timeout: 请求超时时间（秒）
            retry_times: 重试次数
            retry_delay: 重试延迟（秒）
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        self.timeout = timeout
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        
        self.success_count = 0
        self.fail_count = 0
        self.failed_urls = []
        self.success_urls = []
    
    def download_image(self, url: str, filename: str = None) -> Tuple[bool, str]:
        """
        下载单张图片
        
        Args:
            url: 图片 URL
            filename: 保存的文件名（可选）
            
        Returns:
            (成功标志, 错误信息或文件路径)
        """
        if not filename:
            # 从 URL 生成文件名
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename or '.' not in filename:
                filename = f"image_{int(time.time() * 1000)}.jpg"
        
        filepath = self.output_dir / filename
        
        # 如果文件已存在，跳过
        if filepath.exists():
            return True, str(filepath)
        
        # 重试下载
        for attempt in range(self.retry_times):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                }
                response = requests.get(url, headers=headers, timeout=self.timeout, stream=True)
                response.raise_for_status()
                
                # 检查内容类型
                content_type = response.headers.get("Content-Type", "")
                if not content_type.startswith("image/"):
                    return False, f"不是图片类型: {content_type}"
                
                # 保存文件
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return True, str(filepath)
                
            except Exception as e:
                if attempt < self.retry_times - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    return False, str(e)
        
        return False, "重试次数用尽"
    
    def download_from_urls(self, urls: List[str], subfolder: str = None) -> Dict[str, Any]:
        """
        从 URL 列表批量下载
        
        Args:
            urls: URL 列表
            subfolder: 子文件夹名称（可选）
            
        Returns:
            下载统计信息
        """
        if subfolder:
            output_dir = self.output_dir / subfolder
            output_dir.mkdir(parents=True, exist_ok=True)
            original_dir = self.output_dir
            self.output_dir = output_dir
        
        self.success_count = 0
        self.fail_count = 0
        self.failed_urls = []
        self.success_urls = []
        
        def download_with_index(url_index):
            url, index = url_index
            filename = f"image_{index:04d}.jpg"
            success, result = self.download_image(url, filename)
            return url, success, result
        
        # 多线程下载
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(download_with_index, (url, idx)): url
                for idx, url in enumerate(urls)
            }
            
            for future in as_completed(futures):
                url = futures[future]
                try:
                    url, success, result = future.result()
                    if success:
                        self.success_count += 1
                        self.success_urls.append({"url": url, "file": result})
                    else:
                        self.fail_count += 1
                        self.failed_urls.append({"url": url, "error": result})
                except Exception as e:
                    self.fail_count += 1
                    self.failed_urls.append({"url": url, "error": str(e)})
        
        if subfolder:
            self.output_dir = original_dir
        
        return self._generate_summary()
    
    def download_from_keywords(
        self,
        keywords: List[str],
        max_per_keyword: int = 20
    ) -> Dict[str, Any]:
        """
        从关键词批量搜索并下载
        
        Args:
            keywords: 关键词列表
            max_per_keyword: 每个关键词最多下载数量
            
        Returns:
            下载统计信息
        """
        if not DDGS_AVAILABLE:
            return {
                "success": False,
                "error": "duckduckgo_search 未安装，请运行: pip install duckduckgo-search"
            }
        
        all_urls = []
        url_keyword_map = {}
        
        # 搜索图片
        with DDGS() as ddgs:
            for keyword in keywords:
                try:
                    results = ddgs.images(keyword, max_results=max_per_keyword)
                    for result in results:
                        url = result.get("image")
                        if url:
                            all_urls.append(url)
                            url_keyword_map[url] = keyword
                except Exception as e:
                    logger.warning(f"搜索关键词 {keyword} 失败: {e}")
        
        # 按关键词分组下载
        summary = {
            "total_keywords": len(keywords),
            "total_urls": len(all_urls),
            "keywords": {}
        }
        
        for keyword in keywords:
            keyword_urls = [url for url, kw in url_keyword_map.items() if kw == keyword]
            if keyword_urls:
                result = self.download_from_urls(keyword_urls, subfolder=keyword)
                summary["keywords"][keyword] = result
        
        # 汇总统计
        total_success = sum(r.get("success_count", 0) for r in summary["keywords"].values())
        total_fail = sum(r.get("fail_count", 0) for r in summary["keywords"].values())
        
        summary["total_success"] = total_success
        summary["total_fail"] = total_fail
        
        return summary
    
    def extract_urls_from_file(self, filepath: str) -> List[str]:
        """
        从文件中提取图片 URL
        
        支持格式:
        - .txt: 每行一个 URL
        - .json: JSON 数组或对象数组
        - .csv: CSV 文件中的 URL 列
        - .md: Markdown 文件中的图片链接
        
        Args:
            filepath: 文件路径
            
        Returns:
            URL 列表
        """
        filepath = Path(filepath)
        if not filepath.exists():
            return []
        
        urls = []
        ext = filepath.suffix.lower()
        
        try:
            if ext == ".txt":
                with open(filepath, "r", encoding="utf-8") as f:
                    urls = [line.strip() for line in f if line.strip()]
            
            elif ext == ".json":
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        urls = [item if isinstance(item, str) else item.get("url", "") for item in data]
                    elif isinstance(data, dict):
                        urls = data.get("urls", [])
            
            elif ext == ".csv":
                with open(filepath, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # 尝试多个可能的列名
                        for col in ["url", "image_url", "link", "image"]:
                            if col in row and row[col]:
                                urls.append(row[col])
                                break
            
            elif ext == ".md":
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 提取 Markdown 图片链接: ![alt](url)
                    pattern = r'!\[.*?\]\((.*?)\)'
                    urls = re.findall(pattern, content)
                    # 提取 HTML 图片标签: <img src="url">
                    pattern2 = r'<img[^>]+src=["\'](.*?)["\']'
                    urls.extend(re.findall(pattern2, content))
            
        except Exception as e:
            logger.error(f"解析文件 {filepath} 失败: {e}")
        
        # 过滤有效的 URL
        valid_urls = []
        for url in urls:
            url = url.strip()
            if url and (url.startswith("http://") or url.startswith("https://")):
                valid_urls.append(url)
        
        return valid_urls
    
    def download_from_file(self, filepath: str, subfolder: str = None) -> Dict[str, Any]:
        """
        从文件批量下载
        
        Args:
            filepath: 文件路径
            subfolder: 子文件夹名称（可选）
            
        Returns:
            下载统计信息
        """
        urls = self.extract_urls_from_file(filepath)
        if not urls:
            return {
                "success": False,
                "error": f"未从文件 {filepath} 中提取到有效 URL"
            }
        
        return self.download_from_urls(urls, subfolder=subfolder)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """
        生成下载统计摘要
        
        Returns:
            统计信息字典
        """
        return {
            "success": True,
            "total": self.success_count + self.fail_count,
            "success_count": self.success_count,
            "fail_count": self.fail_count,
            "success_rate": self.success_count / (self.success_count + self.fail_count) if (self.success_count + self.fail_count) > 0 else 0,
            "success_urls": self.success_urls,
            "failed_urls": self.failed_urls,
            "output_dir": str(self.output_dir)
        }
    
    def save_summary(self, summary: Dict[str, Any], filename: str = "download_summary.json"):
        """
        保存下载统计摘要到文件
        
        Args:
            summary: 统计信息字典
            filename: 文件名
        """
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        logger.info(f"下载统计已保存到: {filepath}")


def download_images_from_urls(
    urls: List[str],
    output_dir: str = "downloads",
    subfolder: str = None,
    max_workers: int = 5
) -> Dict[str, Any]:
    """
    便捷函数：从 URL 列表下载图片
    
    Args:
        urls: URL 列表
        output_dir: 输出目录
        subfolder: 子文件夹名称
        max_workers: 最大并发数
        
    Returns:
        下载统计信息
    """
    downloader = BatchImageDownloader(output_dir=output_dir, max_workers=max_workers)
    return downloader.download_from_urls(urls, subfolder=subfolder)


def download_images_from_keywords(
    keywords: List[str],
    output_dir: str = "downloads",
    max_per_keyword: int = 20,
    max_workers: int = 5
) -> Dict[str, Any]:
    """
    便捷函数：从关键词搜索并下载图片
    
    Args:
        keywords: 关键词列表
        output_dir: 输出目录
        max_per_keyword: 每个关键词最多下载数量
        max_workers: 最大并发数
        
    Returns:
        下载统计信息
    """
    downloader = BatchImageDownloader(output_dir=output_dir, max_workers=max_workers)
    return downloader.download_from_keywords(keywords, max_per_keyword=max_per_keyword)


def download_images_from_file(
    filepath: str,
    output_dir: str = "downloads",
    subfolder: str = None,
    max_workers: int = 5
) -> Dict[str, Any]:
    """
    便捷函数：从文件批量下载图片
    
    Args:
        filepath: 文件路径
        output_dir: 输出目录
        subfolder: 子文件夹名称
        max_workers: 最大并发数
        
    Returns:
        下载统计信息
    """
    downloader = BatchImageDownloader(output_dir=output_dir, max_workers=max_workers)
    return downloader.download_from_file(filepath, subfolder=subfolder)


