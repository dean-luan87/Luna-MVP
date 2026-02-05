#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 B1 子进程 TTS 方案"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s - %(message)s'
)

print('=' * 60)
print('测试 Voice 模块初始化（B1 子进程方案）')
print('=' * 60)

try:
    import sys
    import os
    # 直接导入 voice.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    voice_path = os.path.join(current_dir, 'modules', 'voice.py')
    import importlib.util
    spec = importlib.util.spec_from_file_location("voice", voice_path)
    voice_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(voice_module)
    Voice = voice_module.Voice
    print('✅ Voice 模块导入成功')
    
    print('\n正在初始化 Voice...')
    voice = Voice()
    print('✅ Voice 初始化完成')
    
    status = voice.get_status()
    print(f'✅ Voice 状态: {status}')
    
    print('\n测试 speak...')
    result = voice.speak('测试语音播报', None)
    print(f'✅ speak 调用结果: {result}')
    
    print('\n等待 5 秒，观察是否有 TTS-WORKER 日志和语音输出...')
    time.sleep(5)
    
    print('\n✅ 测试完成')
    
except Exception as e:
    print(f'\n❌ 错误: {e}')
    import traceback
    traceback.print_exc()

