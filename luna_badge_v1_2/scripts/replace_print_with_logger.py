#!/usr/bin/env python3
"""
自动替换 print 为 logger 的脚本
扫描指定目录，将 print 语句替换为统一的 logger
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple


def get_logger_import() -> str:
    """返回 logger 导入语句"""
    return "from core.logging import get_logger\n"


def should_skip_file(file_path: Path) -> bool:
    """判断是否应该跳过该文件"""
    skip_patterns = [
        ".venv",
        "realtime_lab",
        ".git",
        "__pycache__",
        "node_modules",
        "venv",
        "env",
        "scripts/replace_print_with_logger.py",  # 跳过自己
    ]
    file_str = str(file_path)
    return any(pattern in file_str for pattern in skip_patterns)


def analyze_print_statements(content: str) -> List[Tuple[int, str]]:
    """
    分析文件中的 print 语句
    返回: [(行号, print语句内容), ...]
    """
    lines = content.split('\n')
    print_statements = []
    
    for i, line in enumerate(lines, 1):
        # 匹配 print( 开头的语句
        if re.search(r'^\s*print\s*\(', line):
            print_statements.append((i, line.strip()))
    
    return print_statements


def convert_print_to_logger(line: str, module_name: str) -> Tuple[str, bool]:
    """
    将 print 语句转换为 logger 语句
    
    Returns:
        (转换后的行, 是否需要添加 logger 初始化)
    """
    # 提取 print 的内容
    match = re.search(r'print\s*\((.*)\)', line)
    if not match:
        return line, False
    
    content = match.group(1)
    indent = len(line) - len(line.lstrip())
    
    # 判断日志级别
    content_lower = content.lower()
    if any(keyword in content_lower for keyword in ['error', 'exception', 'fail', 'failed']):
        level = "error"
    elif any(keyword in content_lower for keyword in ['warning', 'warn', 'alert']):
        level = "warning"
    elif any(keyword in content_lower for keyword in ['debug', 'trace']):
        level = "debug"
    else:
        level = "info"
    
    # 构建 logger 语句
    # 如果 content 是 f-string 或包含变量，保持原样
    if content.startswith('f"') or content.startswith("f'") or '{' in content:
        new_line = f"{' ' * indent}log.{level}({content})"
    else:
        # 简单字符串，去掉引号
        content_clean = content.strip('"\'')
        new_line = f"{' ' * indent}log.{level}(\"{content_clean}\")"
    
    return new_line, True


def process_file(file_path: Path, dry_run: bool = False) -> dict:
    """
    处理单个文件
    
    Returns:
        dict: 处理结果统计
    """
    result = {
        "file": str(file_path),
        "prints_found": 0,
        "prints_replaced": 0,
        "needs_logger_init": False,
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分析 print 语句
        print_statements = analyze_print_statements(content)
        result["prints_found"] = len(print_statements)
        
        if not print_statements:
            return result
        
        # 检查是否已有 logger
        has_logger_import = "from core.logging import get_logger" in content
        has_logger_init = "log = get_logger" in content
        
        # 确定模块名（用于 logger 初始化）
        module_name = file_path.stem
        
        # 替换 print 语句
        lines = content.split('\n')
        new_lines = []
        modified = False
        
        for i, line in enumerate(lines):
            if re.search(r'^\s*print\s*\(', line):
                new_line, needs_init = convert_print_to_logger(line, module_name)
                new_lines.append(new_line)
                result["prints_replaced"] += 1
                if needs_init:
                    result["needs_logger_init"] = True
                modified = True
            else:
                new_lines.append(line)
        
        # 如果需要添加 logger 初始化
        if modified and (not has_logger_import or not has_logger_init):
            # 找到导入部分
            import_end = 0
            for i, line in enumerate(new_lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_end = i + 1
                elif line.strip() and not line.strip().startswith('#'):
                    break
            
            # 插入 logger 导入
            if not has_logger_import:
                new_lines.insert(import_end, get_logger_import())
                import_end += 1
            
            # 插入 logger 初始化（在导入后，类/函数定义前）
            if not has_logger_init:
                init_line = f"log = get_logger(\"{module_name}\")"
                # 找到第一个非导入、非注释的行
                insert_pos = import_end
                for i in range(import_end, len(new_lines)):
                    line = new_lines[i].strip()
                    if line and not line.startswith('#'):
                        insert_pos = i
                        break
                new_lines.insert(insert_pos, init_line)
        
        # 写入文件
        if modified and not dry_run:
            new_content = '\n'.join(new_lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return result
        
    except Exception as e:
        result["error"] = str(e)
        return result


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="替换 print 为 logger")
    parser.add_argument("--dry-run", action="store_true", help="仅显示，不实际修改")
    parser.add_argument("--path", default=".", help="要处理的目录路径")
    args = parser.parse_args()
    
    base_path = Path(args.path)
    
    print("=" * 60)
    print("替换 print 为 logger")
    print("=" * 60)
    print(f"目标目录: {base_path}")
    print(f"模式: {'预览模式（不修改文件）' if args.dry_run else '执行模式（会修改文件）'}")
    print()
    
    # 查找所有 Python 文件
    python_files = []
    for py_file in base_path.rglob("*.py"):
        if not should_skip_file(py_file):
            python_files.append(py_file)
    
    print(f"找到 {len(python_files)} 个 Python 文件")
    print()
    
    # 处理文件
    results = []
    for py_file in python_files:
        result = process_file(py_file, dry_run=args.dry_run)
        if result["prints_found"] > 0:
            results.append(result)
            status = "✅" if result.get("error") is None else "❌"
            print(f"{status} {py_file.relative_to(base_path)}")
            print(f"   找到 {result['prints_found']} 个 print，替换 {result['prints_replaced']} 个")
            if result.get("error"):
                print(f"   错误: {result['error']}")
    
    # 统计
    print()
    print("=" * 60)
    print("处理完成")
    print("=" * 60)
    total_files = len(results)
    total_prints = sum(r["prints_found"] for r in results)
    total_replaced = sum(r["prints_replaced"] for r in results)
    
    print(f"处理文件数: {total_files}")
    print(f"找到 print 语句: {total_prints}")
    print(f"替换 print 语句: {total_replaced}")
    
    if args.dry_run:
        print("\n这是预览模式，文件未被修改。")
        print("运行时不加 --dry-run 参数来实际执行替换。")


if __name__ == "__main__":
    main()





