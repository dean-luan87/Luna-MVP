from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_detector")
"""
Vision Detector 测试脚本（F1）

测试视觉检测模块
"""

import sys
import os
import logging
from pathlib import Path
import json

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

try:
    import cv2
except ImportError:
    log.info("❌ OpenCV 未安装。请运行: pip install opencv-python")
    sys.exit(1)

from core.vision.detector import VisionDetector

logger = logging.getLogger(__name__)


def setup_logging():
    """设置日志目录"""
    os.makedirs("logs", exist_ok=True)
    log.info("✅ 日志目录已创建")


def test_detector_from_camera():
    """从摄像头测试检测器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Vision Detector 测试（摄像头）")
    log.info("=" * 80")

    # 模型路径
    model_path = "yolov8n.pt"

    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        log.info(f"\n⚠️ 模型文件不存在: {model_path}")
        log.info("   请先下载模型文件，或修改 model_path 为你的模型路径")
        log.info("   下载命令: wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt")
        return False

    try:
        # 创建检测器
        log.info(f"\n📦 正在初始化 Vision Detector...")
        log.info(f"   模型路径: {model_path}")
        detector = VisionDetector(model_path, conf_threshold=0.5)
        log.info("✅ Vision Detector 初始化成功")

        # 打开摄像头
        log.info(f"\n📹 正在打开摄像头...")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            log.info("❌ 无法打开摄像头")
            return False

        log.info("✅ 摄像头打开成功")
        log.info("\n💡 提示:")
        log.info("   - 按 'q' 键退出")
        log.info("   - 检测结果会打印在控制台")
        log.info("   - 检测框会显示在窗口上")

        frame_count = 0

        while True:
            # 读取一帧
            ret, frame = cap.read()
            if not ret:
                log.info("⚠️ 无法读取摄像头画面")
                break

            frame_count += 1

            # 执行检测
            result = detector.detect(frame)

            # 打印检测结果（每 10 帧打印一次，避免刷屏）
            if frame_count % 10 == 0:
                log.info(f"\n📊 帧 #{result.frame_id} 检测结果:")
                log.info(f"   风险等级: {result.risk_level}")
                log.info(f"   检测到对象数: {result.get_object_count()}")
                if result.objects:
                    log.info(f"   对象列表:")
                    for i, obj in enumerate(result.objects[:5], 1):  # 只显示前5个
                        log.info(f"     [{i}] {obj.cls} (置信度: {obj.conf:.2f}, 面积: {obj.area()})")

            # 在画面上画检测框
            for obj in result.objects:
                x1, y1, x2, y2 = obj.bbox
                
                # 画绿色矩形框
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # 在框上方写类别名称和置信度
                label = f"{obj.cls} {obj.conf:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                label_y = y1 - 10 if y1 - 10 > 10 else y1 + 20
                cv2.rectangle(
                    frame,
                    (x1, label_y - label_size[1] - 5),
                    (x1 + label_size[0], label_y + 5),
                    (0, 255, 0),
                    -1,
                )
                cv2.putText(
                    frame,
                    label,
                    (x1, label_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    2,
                )

            # 显示风险等级
            risk_color = (0, 255, 0) if result.risk_level == "low" else (0, 165, 255)
            cv2.putText(
                frame,
                f"Risk: {result.risk_level.upper()}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                risk_color,
                2,
            )

            # 显示画面
            cv2.imshow("Luna Vision Detector", frame)

            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                log.info("\n👋 用户退出")
                break

        # 清理
        cap.release()
        cv2.destroyAllWindows()

        log.info(f"\n✅ 测试完成，共处理 {frame_count} 帧")
        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detector_from_image(image_path: str):
    """从图片文件测试检测器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Vision Detector 测试（图片文件）")
    log.info("=" * 80")

    model_path = "yolov8n.pt"

    if not os.path.exists(model_path):
        log.info(f"\n⚠️ 模型文件不存在: {model_path}")
        return False

    if not os.path.exists(image_path):
        log.info(f"\n⚠️ 图片文件不存在: {image_path}")
        return False

    try:
        # 创建检测器
        log.info(f"\n📦 正在初始化 Vision Detector...")
        detector = VisionDetector(model_path, conf_threshold=0.5)
        log.info("✅ Vision Detector 初始化成功")

        # 读取图片
        log.info(f"\n📷 正在读取图片: {image_path}")
        frame = cv2.imread(image_path)

        if frame is None:
            log.info("❌ 无法读取图片")
            return False

        log.info("✅ 图片读取成功")

        # 执行检测
        log.info("\n🔍 正在执行检测...")
        result = detector.detect(frame)

        # 打印结果
        log.info(f"\n📊 检测结果:")
        result_dict = result.to_dict()
        log.info("json.dumps(result_dict, indent=2, ensure_ascii=False)")

        # 在图片上画框
        for obj in result.objects:
            x1, y1, x2, y2 = obj.bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{obj.cls} {obj.conf:.2f}"
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        # 保存结果图片
        output_path = "detection_result.jpg"
        cv2.imwrite(output_path, frame)
        log.info(f"\n✅ 结果已保存到: {output_path}")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    log.info("🚀 Vision Detector 测试开始")
    log.info("=" * 80")

    # 设置日志目录
    setup_logging()

    import argparse
    parser = argparse.ArgumentParser(description="Vision Detector 测试")
    parser.add_argument(
        "--image",
        type=str,
        help="使用图片文件进行测试（而不是摄像头）",
    )
    args = parser.parse_args()

    try:
        if args.image:
            # 从图片文件测试
            success = test_detector_from_image(args.image)
        else:
            # 从摄像头测试
            success = test_detector_from_camera()

        if success:
            log.info(f"\n{'='*80}")
            log.info("🎉 测试完成！")
            log.info(f"{'='*80}")
            return 0
        else:
            log.info(f"\n{'='*80}")
            log.info("❌ 测试失败")
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









