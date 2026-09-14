/**
 * Luna Badge 导航系统诊断脚本
 * 用于快速定位导航不启动的原因
 * 
 * 使用方法：
 * 1. 在浏览器控制台运行：直接复制粘贴整个文件内容
 * 2. 或调用：window.runNavigationDiagnosis()
 */

(function() {
  'use strict';

  function runDiagnosis() {
    console.log("=".repeat(60));
    console.log("🔍 Vision Navigation Diagnosis");
    console.log("=".repeat(60));

    const results = {
      yolo: {},
      visionEnhancer: {},
      navigationFSM: {},
      tts: {},
      eventDispatcher: {},
      overall: {}
    };

    // 1️⃣ 检查 YOLO 输出
    console.log("\n📋 1. YOLO 输出检查");
    console.log("-".repeat(60));
    
    results.yolo.lastOutput = window.lastYoloOutput;
    results.yolo.exists = typeof window.lastYoloOutput !== 'undefined';
    results.yolo.isNull = window.lastYoloOutput === null;
    results.yolo.isEmpty = window.lastYoloOutput && Object.keys(window.lastYoloOutput).length === 0;
    
    console.log("   lastYoloOutput:", results.yolo.lastOutput);
    console.log("   存在:", results.yolo.exists);
    console.log("   是否为null:", results.yolo.isNull);
    console.log("   是否为空对象:", results.yolo.isEmpty);
    
    if (!results.yolo.exists) {
      console.log("   ❌ YOLO 没有输出（undefined）");
    } else if (results.yolo.isNull) {
      console.log("   ❌ YOLO 输出为 null（可能报错）");
    } else if (results.yolo.isEmpty) {
      console.log("   ⚠️  YOLO 输出为空对象（格式可能不对）");
    } else {
      console.log("   ✅ YOLO 有输出");
    }

    // 检查 YOLO 就绪状态
    results.yolo.ready = window.yoloReady;
    console.log("   yoloReady:", results.yolo.ready);
    if (results.yolo.ready === false) {
      console.log("   ❌ YOLO 模型未加载");
    } else if (typeof results.yolo.ready === 'undefined') {
      console.log("   ⚠️  YOLO 脚本可能未执行");
    } else {
      console.log("   ✅ YOLO 已就绪");
    }

    // 2️⃣ 检查 VisionEnhancer
    console.log("\n📋 2. VisionEnhancer 检查");
    console.log("-".repeat(60));
    
    results.visionEnhancer.exists = !!window.VisionEnhancer;
    results.visionEnhancer.hasProcessFrame = typeof window.VisionEnhancer?.processFrame === 'function';
    results.visionEnhancer.hasAnalyzeRisk = typeof window.VisionEnhancer?.analyzeRisk === 'function';
    results.visionEnhancer.lastSummary = window.VisionEnhancer?.lastSummary;
    
    console.log("   VisionEnhancer 存在:", results.visionEnhancer.exists);
    console.log("   processFrame 方法:", results.visionEnhancer.hasProcessFrame ? "✅" : "❌");
    console.log("   analyzeRisk 方法:", results.visionEnhancer.hasAnalyzeRisk ? "✅" : "❌");
    console.log("   lastSummary:", results.visionEnhancer.lastSummary);
    
    if (!results.visionEnhancer.exists) {
      console.log("   ❌ VisionEnhancer 模块未加载");
    } else if (!results.visionEnhancer.hasProcessFrame) {
      console.log("   ❌ VisionEnhancer.processFrame 不可用");
    } else {
      console.log("   ✅ VisionEnhancer 正常");
    }

    // 3️⃣ 检查 NavigationFSM
    console.log("\n📋 3. NavigationFSM 检查");
    console.log("-".repeat(60));
    
    results.navigationFSM.exists = !!window.NavigationFSM;
    results.navigationFSM.state = window.NavigationFSM?.state;
    results.navigationFSM.hasStart = typeof window.NavigationFSM?.start === 'function';
    results.navigationFSM.hasHandleEvent = typeof window.NavigationFSM?.handleEvent === 'function';
    
    console.log("   NavigationFSM 存在:", results.navigationFSM.exists);
    console.log("   当前状态:", results.navigationFSM.state || "undefined");
    console.log("   start 方法:", results.navigationFSM.hasStart ? "✅" : "❌");
    console.log("   handleEvent 方法:", results.navigationFSM.hasHandleEvent ? "✅" : "❌");
    
    if (!results.navigationFSM.exists) {
      console.log("   ❌ NavigationFSM 模块未加载");
    } else if (results.navigationFSM.state === 'idle') {
      console.log("   ⚠️  导航处于 idle 状态（未启动）");
    } else if (results.navigationFSM.state === 'paused') {
      console.log("   ⚠️  导航处于 paused 状态（可能被挂起）");
    } else if (results.navigationFSM.state === 'active' || results.navigationFSM.state === 'NAVIGATING') {
      console.log("   ✅ 导航已启动");
    } else {
      console.log("   ⚠️  导航状态未知:", results.navigationFSM.state);
    }

    // 4️⃣ 检查 TTS 系统
    console.log("\n📋 4. TTS 系统检查");
    console.log("-".repeat(60));
    
    results.tts.hasSpeakText = typeof window.speakText === 'function';
    results.tts.hasPriorityTTS = !!window.PriorityTTSQueue;
    results.tts.hasTTS = !!window.TTS;
    
    console.log("   speakText 函数:", results.tts.hasSpeakText ? "✅" : "❌");
    console.log("   PriorityTTSQueue:", results.tts.hasPriorityTTS ? "✅" : "❌");
    console.log("   TTS 对象:", results.tts.hasTTS ? "✅" : "❌");
    
    if (!results.tts.hasSpeakText && !results.tts.hasPriorityTTS && !results.tts.hasTTS) {
      console.log("   ❌ TTS 系统未初始化");
    } else {
      console.log("   ✅ TTS 系统可用");
    }

    // 5️⃣ 检查 EventDispatcher
    console.log("\n📋 5. EventDispatcher 检查");
    console.log("-".repeat(60));
    
    results.eventDispatcher.exists = !!window.EventDispatcher;
    results.eventDispatcher.hasEmitHazard = typeof window.EventDispatcher?.emitHazardEvent === 'function';
    results.eventDispatcher.hasEmitNav = typeof window.EventDispatcher?.emitNavigationEvent === 'function';
    
    console.log("   EventDispatcher 存在:", results.eventDispatcher.exists);
    console.log("   emitHazardEvent:", results.eventDispatcher.hasEmitHazard ? "✅" : "❌");
    console.log("   emitNavigationEvent:", results.eventDispatcher.hasEmitNav ? "✅" : "❌");
    
    if (!results.eventDispatcher.exists) {
      console.log("   ❌ EventDispatcher 模块未加载");
    } else {
      console.log("   ✅ EventDispatcher 正常");
    }

    // 6️⃣ 综合诊断
    console.log("\n📋 6. 综合诊断结果");
    console.log("=".repeat(60));
    
    const issues = [];
    
    if (!results.yolo.exists || results.yolo.isNull) {
      issues.push("❌ YOLO 没有输出 → 导航永远不会启动");
    }
    
    if (!results.visionEnhancer.exists || !results.visionEnhancer.hasProcessFrame) {
      issues.push("❌ VisionEnhancer 未加载或不可用 → 视觉处理中断");
    }
    
    if (!results.navigationFSM.exists) {
      issues.push("❌ NavigationFSM 未加载 → 导航状态机不存在");
    } else if (results.navigationFSM.state === 'idle') {
      issues.push("⚠️  NavigationFSM 处于 idle 状态 → 导航未启动");
    }
    
    if (!results.tts.hasSpeakText && !results.tts.hasPriorityTTS) {
      issues.push("❌ TTS 系统不可用 → 无法播报");
    }
    
    if (!results.eventDispatcher.exists) {
      issues.push("❌ EventDispatcher 未加载 → 事件无法分发");
    }

    if (issues.length === 0) {
      console.log("✅ 所有模块正常，导航系统应该可以工作");
      console.log("\n💡 如果仍然没有播报，可能的原因：");
      console.log("   1. YOLO 没有检测到物体（正常，需要等待）");
      console.log("   2. 导航没有收到视觉更新（检查 YOLO 回调绑定）");
      console.log("   3. TTS 权限未授予（Safari 需要用户交互）");
    } else {
      console.log("⚠️  发现以下问题：");
      issues.forEach((issue, i) => {
        console.log(`   ${i + 1}. ${issue}`);
      });
    }

    console.log("\n" + "=".repeat(60));
    console.log("📊 诊断完成");
    console.log("=".repeat(60));
    
    // 返回结果供进一步分析
    return results;
  }

  // 导出到全局
  window.runNavigationDiagnosis = runDiagnosis;
  
  // 如果页面已加载完成，自动运行一次
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(runDiagnosis, 1000); // 延迟1秒确保所有模块加载完成
  } else {
    window.addEventListener('load', () => {
      setTimeout(runDiagnosis, 1000);
    });
  }

  console.log("💡 导航诊断脚本已加载");
  console.log("   手动运行: window.runNavigationDiagnosis()");
})();

