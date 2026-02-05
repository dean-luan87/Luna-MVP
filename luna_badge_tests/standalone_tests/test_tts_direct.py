#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接测试 pyttsx3 播报（不通过子进程）"""

import pyttsx3
import time

print('=' * 60)
print('直接测试 pyttsx3 播报（主进程）')
print('=' * 60)

try:
    engine = pyttsx3.init(driverName='nsss')
    print('✅ pyttsx3 初始化成功')
    
    # 设置参数
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    print('✅ 已设置语速: 150, 音量: 1.0')
    
    # 选择 Tingting
    voices = engine.getProperty('voices')
    for v in voices:
        if 'tingting' in v.name.lower() and 'zh-cn' in v.id.lower():
            engine.setProperty('voice', v.id)
            print(f'✅ 已选择: {v.name}')
            break
    
    print('\n开始播报测试...')
    print('（如果你听到声音，说明 pyttsx3 在主进程中工作正常）')
    print('（如果没听到，可能是 macOS 权限问题）')
    
    engine.say('这是直接测试语音播报，在主进程中')
    engine.runAndWait()
    
    print('\n✅ 播报完成')
    
except Exception as e:
    print(f'\n❌ 错误: {e}')
    import traceback
    traceback.print_exc()


