from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_tile_enhancer")
"""
Tile Enhancer 测试脚本（F3）

测试局部关键区增强模块
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

try:
    import cv2
    import numpy as np
except ImportError:
    log.info("❌ OpenCV 或 NumPy 未安装")
    sys.exit(1)

from vision.tile_enhancer import TileEnhancer

logger = logging.getLogger(__name__)


def create_test_image():
    """创建测试图像（包含低光、低对比度区域）"""
    # 创建一个 1080×1920 的测试图像
    height, width = 1080, 1920
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # 区域 1：低光区域（左上）
    frame[0:height//3, 0:width//3] = [20, 20, 20]

    # 区域 2：低对比度区域（中间）
    mid_h, mid_w = height//2, width//2
    gray_val = 128
    frame[mid_h-100:mid_h+100, mid_w-200:mid_w+200] = [gray_val-5, gray_val, gray_val+5]

    # 区域 3：正常区域（右下）
    frame[2*height//3:, 2*width//3:] = [200, 200, 200]

    # 区域 4：添加一些纹理（模拟噪声）
    noise = np.random.randint(0, 30, (height//4, width//4, 3), dtype=np.uint8)
    frame[height//2:height//2+height//4, width//2:width//2+width//4] = noise

    return frame


def test_tile_enhancer_from_image():
    """从测试图像测试增强器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Tile Enhancer 测试（测试图像）")
    log.info("=" * 80")

    try:
        # 创建增强器
        log.info("\n📦 正在初始化 Tile Enhancer...")
        enhancer = TileEnhancer()
        log.info("✅ Tile Enhancer 初始化成功")

        # 创建测试图像
        log.info("\n🖼️ 创建测试图像...")
        test_image = create_test_image()
        log.info(f"✅ 测试图像创建成功: {test_image.shape}")

        # 处理图像
        log.info("\n🔧 正在处理图像...")
        enhanced_image, stats = enhancer.process_with_stats(test_image)

        log.info("\n📊 处理统计:")
        log.info(f"   总 tiles: {stats['total_tiles']}")
        log.info(f"   增强的 tiles: {stats['enhanced_tiles']}")
        log.info(f"   Gamma 校正: {stats['gamma_applied']} tiles")
        log.info(f"   CLAHE: {stats['clahe_applied']} tiles")
        log.info(f"   Bilateral Filter: {stats['bilateral_applied']} tiles")

        # 保存结果
        output_dir = "logs/tile_enhancer"
        os.makedirs(output_dir, exist_ok=True)

        original_path = os.path.join(output_dir, "test_original.jpg")
        enhanced_path = os.path.join(output_dir, "test_enhanced.jpg")

        cv2.imwrite(original_path, test_image)
        cv2.imwrite(enhanced_path, enhanced_image)

        log.info(f"\n💾 结果已保存:")
        log.info(f"   原图: {original_path}")
        log.info(f"   增强后: {enhanced_path}")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tile_enhancer_from_camera():
    """从摄像头测试增强器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Tile Enhancer 测试（摄像头）")
    log.info("=" * 80")

    try:
        # 创建增强器
        log.info("\n📦 正在初始化 Tile Enhancer...")
        enhancer = TileEnhancer()
        log.info("✅ Tile Enhancer 初始化成功")

        # 打开摄像头
        log.info("\n📹 正在打开摄像头...")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            log.info("❌ 无法打开摄像头")
            return False

        log.info("✅ 摄像头打开成功")
        log.info("\n💡 提示:")
        log.info("   - 按 'q' 键退出")
        log.info("   - 按 's' 键保存当前帧")

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                log.info("⚠️ 无法读取摄像头画面")
                break

            frame_count += 1

            # 处理图像
            enhanced_frame, stats = enhancer.process_with_stats(frame)

            # 每 30 帧打印一次统计
            if frame_count % 30 == 0:
                log.info(f"\n📊 帧 #{frame_count} 统计:")
                log.info(f"   增强的 tiles: {stats['enhanced_tiles']}/{stats['total_tiles']}")
                log.info(f"   Gamma: {stats['gamma_applied']}, CLAHE: {stats['clahe_applied']}, Bilateral: {stats['bilateral_applied']}")

            # 显示画面（并排显示原图和增强后）
            combined = np.hstack([frame, enhanced_frame])
            cv2.putText(
                combined,
                "Original | Enhanced",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Tile Enhancer", combined)

            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                log.info("\n👋 用户退出")
                break
            elif key == ord('s'):
                # 保存当前帧
                output_dir = "logs/tile_enhancer"
                os.makedirs(output_dir, exist_ok=True)
                import time
                timestamp = int(time.time())
                original_path = os.path.join(output_dir, f"camera_original_{timestamp}.jpg")
                enhanced_path = os.path.join(output_dir, f"camera_enhanced_{timestamp}.jpg")
                cv2.imwrite(original_path, frame)
                cv2.imwrite(enhanced_path, enhanced_frame)
                log.info(f"\n💾 已保存: {original_path}, {enhanced_path}")

        cap.release()
        cv2.destroyAllWindows()

        log.info(f"\n✅ 测试完成，共处理 {frame_count} 帧")
        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tile_enhancer_scalability():
    """测试可扩展性（不同网格大小）"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Tile Enhancer 可扩展性测试")
    log.info("=" * 80")

    test_image = create_test_image()

    # 测试不同的网格配置
    test_configs = [
        (3, 3),
        (3, 5),
        (5, 3),
        (5, 5),
        (7, 3),
    ]

    log.info("\n📐 测试不同网格配置:")

    for rows, cols in test_configs:
        try:
            enhancer = TileEnhancer(rows=rows, cols=cols)
            enhanced, stats = enhancer.process_with_stats(test_image)
            log.info(f"   ✅ {rows}×{cols}: {stats['total_tiles']} tiles, 增强 {stats['enhanced_tiles']} 个")
        except Exception as e:
            log.info(f"   ❌ {rows}×{cols}: 失败 - {e}")
            return False

    log.info(f"\n✅ 所有配置测试通过")
    return True


def main():
    """主函数"""
    log.info("🚀 Tile Enhancer 测试开始")
    log.info("=" * 80")

    import argparse
    parser = argparse.ArgumentParser(description="Tile Enhancer 测试")
    parser.add_argument(
        "--camera",
        action="store_true",
        help="使用摄像头进行测试（而不是测试图像）",
    )
    args = parser.parse_args()

    try:
        if args.camera:
            # 从摄像头测试
            success = test_tile_enhancer_from_camera()
        else:
            # 从测试图像测试
            success1 = test_tile_enhancer_from_image()
            
            # 可扩展性测试
            success2 = test_tile_enhancer_scalability()
            
            success = success1 and success2

        if success:
            log.info(f"\n{'='*80}")
            log.info("🎉 所有测试完成！")
            log.info(f"{'='*80}")
            log.info("\n💡 提示:")
            log.info("   - 修改 vision/tile_enhancer/config.py 可以调整参数")
            log.info("   - 使用 --camera 参数可以从摄像头测试")
            return 0
        else:
            log.info(f"\n{'='*80}")
            log.info("❌ 部分测试失败")
            log.info(f"{'='*80}")
            return 1

    except KeyboardInterrupt:
        log.info("\n\n👋 用户中断")
        return 0
    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
























