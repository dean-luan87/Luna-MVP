// node_inference.js
// 基于 YOLO + OCR 的节点推理（社会节点 + 推理节点）

(function () {
  'use strict';

  function log(event, payload) {
    if (window.__lunaLog) {
      window.__lunaLog(event, payload);
    } else {
      // console.log('[NodeInference]', event, payload);
    }
  }

  // 一些基础 keyword 表，先写小集合，可后续扩展
  const KEYWORDS = {
    toilet: ['厕所', '卫生间', '洗手间', 'WC', 'Toilet', 'Restroom'],
    elevator: ['电梯', '升降机', 'Elevator', 'Lift'],
    exit: ['出口', '安全出口', 'Exit'],
    entrance: ['入口', '大门', 'Entrance', 'Gate'],
    register: ['挂号', '登记', 'Registration'],
    payment: ['收费', '缴费', '收银', '收费处', '支付', '扫码支付', '收银台', '收费窗口'],
    inquiry: ['咨询', '问询', '服务台', '服务中心', 'Information'],
    lab: ['检验科', '检验', '化验', '化验室', '检验室'],
    waiting: ['候诊', '等候区', '候车', 'Waiting Area', '等候'],
    subway: ['地铁', 'Metro', 'Subway', '站台', '站厅'],
    bus: ['公交车站', '车站', 'Bus Stop', '公交站'],
    crosswalk: ['斑马线', '人行横道']
  };

  // 简单包含判断
  function textContainsAny(text, list) {
    if (!text) return false;
    return list.some(k => text.includes(k));
  }

  // 将 YOLO 结果中 label 简单归类，便于推理
  function groupObjects(yoloObjects) {
    const res = {
      persons: [],
      counters: [],
      screens: [],
      qrCodes: [],
      doors: [],
      elevators: [],
      others: []
    };
    if (!Array.isArray(yoloObjects)) return res;

    for (const obj of yoloObjects) {
      const label = (obj.label || '').toLowerCase();
      if (label === 'person' || label === 'people' || label === 'human') {
        res.persons.push(obj);
      } else if (label.includes('counter') || label.includes('desk') || label.includes('table')) {
        res.counters.push(obj);
      } else if (label.includes('screen') || label.includes('monitor')) {
        res.screens.push(obj);
      } else if (label.includes('qr') || label.includes('qrcode') || label.includes('barcode')) {
        res.qrCodes.push(obj);
      } else if (label.includes('door') || label.includes('entrance') || label.includes('gate')) {
        res.doors.push(obj);
      } else if (label.includes('elevator') || label.includes('escalator')) {
        res.elevators.push(obj);
      } else {
        res.others.push(obj);
      }
    }
    return res;
  }

  /**
   * inferNodes
   * @param {Object} frame
   *  - regionId
   *  - yoloObjects: [{label, bbox, confidence, ...}]
   *  - ocrText: string
   *  - positionHint: {x, y, z?} 可选
   * 
   * @returns {Array} nodeCandidates
   *  - { type, role, confidence, source, position, meta }
   */
  function inferNodes(frame) {
    const { regionId, yoloObjects, ocrText, positionHint } = frame || {};
    if (!yoloObjects && !ocrText) return [];

    const nodes = [];
    const grouped = groupObjects(yoloObjects || []);

    const pos = positionHint || null;

    // 1) 社会定义节点：通过明确 OCR 词语识别
    if (textContainsAny(ocrText, KEYWORDS.toilet)) {
      nodes.push({
        type: 'facility',
        role: 'toilet',
        confidence: 0.95,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'toilet' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.elevator)) {
      nodes.push({
        type: 'facility',
        role: 'elevator',
        confidence: 0.9,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'elevator' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.exit)) {
      nodes.push({
        type: 'facility',
        role: 'exit',
        confidence: 0.9,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'exit' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.entrance)) {
      nodes.push({
        type: 'facility',
        role: 'entrance',
        confidence: 0.9,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'entrance' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.register)) {
      nodes.push({
        type: 'service',
        role: 'registration',
        confidence: 0.9,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'register' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.payment)) {
      nodes.push({
        type: 'service',
        role: 'payment',
        confidence: 0.92,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'payment' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.inquiry)) {
      nodes.push({
        type: 'service',
        role: 'inquiry',
        confidence: 0.9,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'inquiry' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.lab)) {
      nodes.push({
        type: 'department',
        role: 'lab',
        confidence: 0.9,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'lab' }
      });
    }
    if (textContainsAny(ocrText, KEYWORDS.waiting)) {
      nodes.push({
        type: 'area',
        role: 'waiting_area',
        confidence: 0.88,
        source: 'social',
        position: pos,
        meta: { keywordsHit: 'waiting' }
      });
    }

    // 2) 推理节点：没有明确 OCR，但行为/结构像某种节点
    // 2.1 支付候选节点：有柜台 + 二维码 + 人
    if (grouped.counters.length && grouped.qrCodes.length && grouped.persons.length) {
      nodes.push({
        type: 'service',
        role: 'payment_candidate',
        confidence: 0.7,
        source: 'inferred',
        position: pos,
        meta: {
          counters: grouped.counters.length,
          qrCodes: grouped.qrCodes.length,
          persons: grouped.persons.length
        }
      });
    }

    // 2.2 排队/办理候选节点：有柜台 + 人群
    if (grouped.counters.length && grouped.persons.length >= 3) {
      nodes.push({
        type: 'service',
        role: 'queue_candidate',
        confidence: 0.65,
        source: 'inferred',
        position: pos,
        meta: {
          counters: grouped.counters.length,
          persons: grouped.persons.length
        }
      });
    }

    // 2.3 入口/门类推断：有 door + 人群进出
    if (grouped.doors.length && grouped.persons.length >= 2) {
      nodes.push({
        type: 'facility',
        role: 'entrance_candidate',
        confidence: 0.6,
        source: 'inferred',
        position: pos,
        meta: {
          doors: grouped.doors.length,
          persons: grouped.persons.length
        }
      });
    }

    // 2.4 电梯候选：有 elevator label + 门/人
    if (grouped.elevators.length) {
      nodes.push({
        type: 'facility',
        role: 'elevator_candidate',
        confidence: 0.7,
        source: 'inferred',
        position: pos,
        meta: {
          elevators: grouped.elevators.length
        }
      });
    }

    if (nodes.length > 0) {
      log('node_inference_result', {
        regionId,
        ocrText,
        counts: {
          total: nodes.length,
          social: nodes.filter(n => n.source === 'social').length,
          inferred: nodes.filter(n => n.source === 'inferred').length
        }
      });
    }

    return nodes;
  }

  window.NodeInference = {
    inferNodes
  };

})();

