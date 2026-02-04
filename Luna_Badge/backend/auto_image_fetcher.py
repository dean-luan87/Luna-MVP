#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从百度图片自动抓取用于测试的图片
"""

import requests
import urllib.parse
import random
from io import BytesIO
from PIL import Image


class AutoImageFetcher:
    """
    从百度图片自动抓取用于测试的图片
    """

    BAIDU_URL = (
        "https://image.baidu.com/search/acjson"
        "?tn=resultjson_com"
        "&logid=5681327447905431902"
        "&ipn=rj"
        "&ct=201326592"
        "&is=&fp=result"
        "&queryWord={query}"
        "&cl=2"
        "&lm=-1"
        "&ie=utf-8"
        "&oe=utf-8"
        "&st=-1"
        "&ic=0"
        "&word={query}"
        "&face=0"
        "&istype=2"
        "&nc=1"
        "&pn=1"
    )

    HEADERS = {
        "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
    }

    @staticmethod
    def fetch_image(query):
        """抓取指定关键词的一张图片，返回 image_bytes"""
        url = AutoImageFetcher.BAIDU_URL.format(
            query=urllib.parse.quote(query)
        )

        try:
            resp = requests.get(url, headers=AutoImageFetcher.HEADERS, timeout=5)
            data = resp.json().get("data", [])

            candidates = [d.get("thumbURL") for d in data if d.get("thumbURL")]

            if not candidates:
                return None, "NO_IMAGE_FOUND"

            img_url = random.choice(candidates)

            img_resp = requests.get(img_url, timeout=5)
            return img_resp.content, None

        except Exception as e:
            return None, str(e)


