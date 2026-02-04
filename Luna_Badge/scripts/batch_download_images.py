#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量图片下载脚本（可直接运行）
支持 URL 列表、关键词搜索、本地文件解析
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.auto_test.batch_image_downloader import (
    BatchImageDownloader,
    download_images_from_urls,
    download_images_from_keywords,
    download_images_from_file
)


def main():
    parser = argparse.ArgumentParser(description="批量图片下载工具")
    parser.add_argument(
        "--mode",
        choices=["urls", "keywords", "file"],
        required=True,
        help="下载模式: urls(URL列表), keywords(关键词搜索), file(从文件解析)"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="输入: URL列表(逗号分隔) / 关键词列表(逗号分隔) / 文件路径"
    )
    parser.add_argument(
        "--output",
        default="downloads",
        help="输出目录 (默认: downloads)"
    )
    parser.add_argument(
        "--subfolder",
        help="子文件夹名称（可选）"
    )
    parser.add_argument(
        "--max-per-keyword",
        type=int,
        default=20,
        help="每个关键词最多下载数量（仅 keywords 模式）"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="最大并发数 (默认: 5)"
    )
    parser.add_argument(
        "--save-summary",
        action="store_true",
        help="保存下载统计到 summary.json"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("批量图片下载工具")
    print("=" * 70)
    print()
    
    downloader = BatchImageDownloader(
        output_dir=args.output,
        max_workers=args.max_workers
    )
    
    if args.mode == "urls":
        # URL 列表模式
        urls = [url.strip() for url in args.input.split(",")]
        print(f"📥 模式: URL 列表")
        print(f"📋 URL 数量: {len(urls)}")
        print(f"📁 输出目录: {args.output}")
        print()
        
        summary = downloader.download_from_urls(urls, subfolder=args.subfolder)
        
    elif args.mode == "keywords":
        # 关键词搜索模式
        keywords = [kw.strip() for kw in args.input.split(",")]
        print(f"🔍 模式: 关键词搜索")
        print(f"📋 关键词: {', '.join(keywords)}")
        print(f"📊 每个关键词最多下载: {args.max_per_keyword} 张")
        print(f"📁 输出目录: {args.output}")
        print()
        
        summary = downloader.download_from_keywords(keywords, max_per_keyword=args.max_per_keyword)
        
    elif args.mode == "file":
        # 文件解析模式
        filepath = args.input
        print(f"📄 模式: 文件解析")
        print(f"📋 文件路径: {filepath}")
        print(f"📁 输出目录: {args.output}")
        print()
        
        summary = downloader.download_from_file(filepath, subfolder=args.subfolder)
    
    # 输出结果
    print("=" * 70)
    print("下载完成")
    print("=" * 70)
    print()
    
    if summary.get("success", False):
        print(f"✅ 成功: {summary.get('success_count', 0)} 张")
        print(f"❌ 失败: {summary.get('fail_count', 0)} 张")
        print(f"📊 成功率: {summary.get('success_rate', 0) * 100:.1f}%")
        print(f"📁 输出目录: {summary.get('output_dir', args.output)}")
        
        if args.save_summary:
            downloader.save_summary(summary)
            print(f"📄 统计已保存到: {summary.get('output_dir', args.output)}/download_summary.json")
        
        if summary.get("failed_urls"):
            print()
            print("⚠️  失败的 URL:")
            for item in summary["failed_urls"][:10]:  # 只显示前10个
                print(f"   - {item.get('url', '')[:60]}... ({item.get('error', '')})")
    else:
        print(f"❌ 下载失败: {summary.get('error', '未知错误')}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()


