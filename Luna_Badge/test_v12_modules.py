"""
Luna Badge v1.2 - 模块1、模块2完整实现与使用示例

本脚本展示了台阶识别和数据持久化的完整实现，以及首次开机流程的实现。
"""

import sys
import os

# 添加路径以便导入模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.step_detector import StepDetector, StepDataMigration
from core.first_boot_manager import run_first_boot_flow


def demo_step_detection():
    """
    演示台阶识别功能
    """
    print("\n" + "=" * 60)
    print("模块1：台阶识别 × 数据持久化演示")
    print("=" * 60)
    
    # 初始化台阶检测器
    detector = StepDetector(data_path="data/step_map.json")
    
    # 模拟检测台阶
    print("\n1. 检测台阶...")
    step_info = detector.detect_step(frame=None)  # 传入图像帧
    
    if step_info:
        print(f"   ✓ 检测到台阶：{step_info}")
        
        # 保存数据
        print("\n2. 保存台阶数据...")
        success = detector.save_step_data(step_info)
        if success:
            print("   ✓ 数据保存成功")
        else:
            print("   ✗ 数据保存失败")
        
        # 加载历史数据
        print("\n3. 加载历史台阶数据...")
        records = detector.load_step_data()
        print(f"   ✓ 共找到 {len(records)} 条台阶记录")
    else:
        print("   ⚠ 未检测到台阶")
    
    # 演示数据迁移
    print("\n4. 演示数据迁移...")
    migration = StepDataMigration()
    
    # 假设有一个账号
    account_id = "user_12345"
    backup_path = migration.migrate_step_data_on_device_change(account_id)
    print(f"   ✓ 数据已迁移至: {backup_path}")
    
    # 演示数据恢复
    print("\n5. 演示数据恢复...")
    restored = migration.restore_step_data(account_id, backup_path)
    if restored:
        print("   ✓ 数据恢复成功")
    else:
        print("   ✗ 数据恢复失败")


def demo_first_boot():
    """
    演示首次开机流程
    """
    print("\n" + "=" * 60)
    print("模块2：首次开机流程演示")
    print("=" * 60)
    
    # 运行首次开机流程
    account_id = run_first_boot_flow()
    
    if account_id:
        print(f"\n✓ 初始化完成，当前账号ID: {account_id}")
    else:
        print("\n✗ 初始化失败")


def main():
    """主函数"""
    print("Luna Badge v1.2 - 模块1、模块2演示")
    
    # 选择演示内容
    print("\n请选择演示内容：")
    print("1) 台阶识别与数据持久化")
    print("2) 首次开机流程")
    print("3) 全部演示")
    
    choice = input("请输入选项（1-3）: ")
    
    if choice == "1":
        demo_step_detection()
    elif choice == "2":
        demo_first_boot()
    elif choice == "3":
        demo_step_detection()
        demo_first_boot()
    else:
        print("无效选项")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

