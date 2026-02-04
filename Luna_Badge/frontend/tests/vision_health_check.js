/**
 * Luna Badge Vision Health Check
 * 用于自动检测 vision_enhancer.js 是否仍然会触发 null/undefined 崩溃
 * 可在无摄像头、无 YOLO 输入的情况下运行
 * 
 * 使用方法：
 * 1. 在浏览器控制台运行：直接复制粘贴整个文件内容
 * 2. 或在 HTML 中引入：<script src="frontend/tests/vision_health_check.js"></script>
 */

(function() {
  'use strict';

  // 等待 VisionEnhancer 加载完成
  function waitForVisionEnhancer(callback, maxAttempts = 50) {
    let attempts = 0;
    const checkInterval = setInterval(() => {
      attempts++;
      if (window.VisionEnhancer && typeof window.VisionEnhancer.analyzeRisk === 'function') {
        clearInterval(checkInterval);
        callback();
      } else if (attempts >= maxAttempts) {
        clearInterval(checkInterval);
        console.error('❌ VisionEnhancer 未加载，请确保 vision_enhancer.js 已加载');
      }
    }, 100);
  }

  function safeAnalyze(input, label) {
    try {
      if (!window.VisionEnhancer || typeof window.VisionEnhancer.analyzeRisk !== 'function') {
        console.error(`❌ [${label}] VisionEnhancer.analyzeRisk 不可用`);
        return;
      }

      const result = window.VisionEnhancer.analyzeRisk(input);
      
      // 验证返回结果格式
      if (result && typeof result === 'object') {
        console.log(`✔ [${label}] 正常运行`, {
          hasSummary: !!result,
          riskLevel: result.riskLevel || 'unknown',
          hazardsCount: (result.hazards || []).length,
          hasDangerFrame: result.hasDangerFrame || false
        });
      } else {
        console.warn(`⚠️ [${label}] 返回结果格式异常`, result);
      }
    } catch (err) {
      console.error(`❌ [${label}] 崩溃:`, {
        error: err.toString(),
        message: err.message,
        stack: err.stack
      });
    }
  }

  function runHealthCheck() {
    console.log('='.repeat(60));
    console.log('🔍 Vision Health Check Start');
    console.log('='.repeat(60));

    // 1️⃣ 测试 null 输入
    safeAnalyze(null, '输入 null');

    // 2️⃣ 测试 undefined 输入
    safeAnalyze(undefined, '输入 undefined');

    // 3️⃣ 测试缺少 detections 字段
    safeAnalyze({}, '无 detections');

    // 4️⃣ 测试 detections: null
    safeAnalyze({ detections: null }, 'detections:null');

    // 5️⃣ 测试 detections: undefined
    safeAnalyze({ detections: undefined }, 'detections:undefined');

    // 6️⃣ detections 空数组
    safeAnalyze({ detections: [] }, 'detections:[]');

    // 7️⃣ detections 非数组（字符串）
    safeAnalyze({ detections: 'not an array' }, 'detections:字符串');

    // 8️⃣ detections 含 undefined / null
    safeAnalyze({
      detections: [null, undefined, {}, { box: null }, { box: { x1: 5, y1: 5, x2: 20, y2: 20 } }]
    }, 'detections 含 null/undefined');

    // 9️⃣ detections 含 null box
    safeAnalyze({
      detections: [
        { box: null },
        { bbox: undefined },
        { rect: null }
      ]
    }, 'detections 含 null box');

    // 🔟 模拟正常 YOLO 输出
    safeAnalyze({
      detections: [
        { label: 'person', class: 'person', box: { x1: 10, y1: 10, x2: 100, y2: 200 }, confidence: 0.9 },
        { label: 'obstacle', class: 'obstacle', bbox: { x1: 200, y1: 50, x2: 260, y2: 180 }, confidence: 0.8 }
      ],
      frameWidth: 640,
      frameHeight: 480
    }, '正常 YOLO 输入');

    // 1️⃣1️⃣ 模拟部分字段缺失
    safeAnalyze({
      detections: [
        { label: 'person' }, // 缺少 box
        { box: { x1: 10, y1: 10, x2: 100, y2: 200 } } // 缺少 label
      ],
      frameWidth: 640
      // 缺少 frameHeight
    }, '部分字段缺失');

    // 1️⃣2️⃣ 模拟极端情况：所有字段都是 null
    safeAnalyze({
      detections: [
        null,
        undefined,
        { box: null, label: null, class: null },
        { bbox: undefined, confidence: null }
      ],
      frameWidth: null,
      frameHeight: undefined
    }, '极端情况：所有字段都是 null');

    console.log('='.repeat(60));
    console.log('✅ Vision Health Check Done');
    console.log('='.repeat(60));
    console.log('\n📊 检查结果说明：');
    console.log('   ✔ = 正常运行，无崩溃');
    console.log('   ❌ = 出现崩溃，需要修复');
    console.log('   ⚠️  = 返回结果异常，但未崩溃');
  }

  // 如果 VisionEnhancer 已加载，直接运行
  if (window.VisionEnhancer && typeof window.VisionEnhancer.analyzeRisk === 'function') {
    runHealthCheck();
  } else {
    // 否则等待加载
    console.log('⏳ 等待 VisionEnhancer 加载...');
    waitForVisionEnhancer(runHealthCheck);
  }

  // 导出到全局，方便手动调用
  window.runVisionHealthCheck = runHealthCheck;
  console.log('\n💡 提示：可以随时调用 window.runVisionHealthCheck() 重新运行测试');
})();



