#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从本地 test_images/<keyword>/ 中随机取图
"""

import os
import random


class LocalImageLoader:
    """
    从本地 test_images/<keyword>/ 中随机取图
    """
    BASE_DIR = "test_images"

    @staticmethod
    def load_random(keyword):
        folder = os.path.join(LocalImageLoader.BASE_DIR, keyword)
        if not os.path.exists(folder):
            return None, f"本地目录不存在: {folder}"

        files = [
            f for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]

        if len(files) == 0:
            return None, f"目录为空: {folder}"

        path = os.path.join(folder, random.choice(files))
        with open(path, "rb") as f:
            return f.read(), None


