#!/bin/bash
echo "检查需要恢复的文件..."
missing=()
[ ! -f "Luna-mid/core/user_habit_analyzer.py" ] && missing+=("user_habit_analyzer.py")
[ ! -f "Luna-mid/core/visual_learning.py" ] && missing+=("visual_learning.py")
[ ! -f "Luna-mid/core/learning_manager.py" ] && missing+=("learning_manager.py")
[ ! -f "Luna-mid/core/__init__.py" ] && missing+=("__init__.py")
[ ! -f "test_learning_systems.py" ] && missing+=("test_learning_systems.py")
[ ! -f "test_learning_manager.py" ] && missing+=("test_learning_manager.py")
echo "缺失文件数量: ${#missing[@]}"
echo "缺失文件: ${missing[@]}"
