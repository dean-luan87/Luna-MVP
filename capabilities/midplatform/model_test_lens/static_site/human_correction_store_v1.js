/**
 * Human Correction Layer V1 — candidate-only local store.
 * Does NOT write fact / semantic / registry. local-only draft storage.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.HumanCorrectionCopy || {}; };

  var _memory = [];
  var _seq = 0;

  function storageKey() {
    return Copy().localStorageKey || "luna_observation_human_corrections_v1";
  }

  function useLocalStorage() {
    try {
      var k = "__lol_hc_test__";
      global.localStorage.setItem(k, "1");
      global.localStorage.removeItem(k);
      return true;
    } catch (e) {
      return false;
    }
  }

  function loadFromLocal() {
    if (!useLocalStorage()) return [];
    try {
      var raw = global.localStorage.getItem(storageKey());
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function persist() {
    if (!useLocalStorage()) return;
    try {
      global.localStorage.setItem(storageKey(), JSON.stringify(_memory));
    } catch (e) { /* quota */ }
  }

  function init() {
    _memory = loadFromLocal();
    _memory.forEach(function (r) {
      var m = (r.correction_id || "").match(/_(\d+)$/);
      if (m) _seq = Math.max(_seq, parseInt(m[1], 10));
    });
  }

  function envelopeRef(envelope, extraRef) {
    if (extraRef) return extraRef;
    if (!envelope) return "";
    if (envelope._source_file_ref) return envelope._source_file_ref;
    if (envelope.test_manifest_ref) return envelope.test_manifest_ref;
    if (envelope.envelope_id) return "envelope://" + envelope.envelope_id;
    return "";
  }

  function newCorrectionId() {
    _seq += 1;
    return "correction_" + Date.now() + "_" + String(_seq).padStart(4, "0");
  }

  function list() {
    return _memory.slice();
  }

  function add(record) {
    var enriched = enrichWithMidplatform(record);
    _memory.unshift(enriched);
    persist();
    return enriched;
  }

  function enrichWithMidplatform(record) {
    var Analyzer = global.HumanCorrectionMidplatformAnalyzer;
    if (!Analyzer || !Analyzer.analyzeCorrection) {
      record.midplatform_analysis_pending = true;
      return record;
    }
    var analysis = Analyzer.analyzeCorrection(record);
    if (!analysis) return record;
    record.midplatform_analysis = analysis;
    record.impact = analysis.impact;
    record.training_candidate = analysis.training_candidate;
    record.routing_destinations = analysis.routing_destinations;
    record.attribution_id = analysis.attribution_id;
    record.must_not_modify_model_output = true;
    return record;
  }

  function submitCorrection(target, envelope, form) {
    var built = buildRecord(target, envelope, form);
    if (!built.ok) return built;
    var saved = add(built.record);
    return { ok: true, record: saved, analysis: saved.midplatform_analysis || null };
  }

  function clearLocalDrafts() {
    _memory = [];
    if (useLocalStorage()) {
      try { global.localStorage.removeItem(storageKey()); } catch (e) { /* */ }
    }
  }

  function exportJSON() {
    return JSON.stringify({ corrections: _memory, exported_at: new Date().toISOString() }, null, 2);
  }

  function problemDomainsFromTypes(types) {
    var domains = [];
    var typeMap = {};
    (Copy().correctionTypes || []).forEach(function (t) { typeMap[t.id] = t.group; });
    (types || []).forEach(function (id) {
      var g = typeMap[id];
      if (g && g !== "other" && domains.indexOf(g) < 0) domains.push(g);
    });
    return domains;
  }

  function validateRecordInput(target, envelope, form) {
    var ref = envelopeRef(envelope, form.source_envelope_ref);
    if (!ref) return { ok: false, error: Copy().missingEnvelope || "缺少结果来源" };
    var types = form.correction_types || (form.correction_type ? [form.correction_type] : []);
    if (!types.length) return { ok: false, error: "请至少选择一个问题类型" };
    if (!target || !target.target_type) return { ok: false, error: "缺少纠错目标" };
    var manual = String(form.manual_annotation || form.user_note || "").trim();
    if (!manual) return { ok: false, error: "请填写问题手写描述" };
    if (types.indexOf("other_custom") >= 0 && manual.length < 4) {
      return { ok: false, error: "选择「其他」时请在手写描述中说明具体问题" };
    }
    return { ok: true, source_envelope_ref: ref };
  }

  function buildRecord(target, envelope, form) {
    var v = validateRecordInput(target, envelope, form);
    if (!v.ok) return v;

    var types = form.correction_types || (form.correction_type ? [form.correction_type] : []);
    var followups = form.recommended_followup_models || [];
    var primaryFollowup = followups[0] || form.recommended_followup_model || "human_review";
    var manual = String(form.manual_annotation || form.user_note || "").trim();

    var record = {
      correction_id: newCorrectionId(),
      phase_ref: Copy().phaseRef,
      source_envelope_ref: v.source_envelope_ref,
      source_test_case_id: envelope.test_case_id || "",
      source_model_id: envelope.model_id || target.source_model_id || "",
      source_model_category: envelope.model_category || target.source_model_category || "",
      correction_target: target,
      correction_types: types,
      correction_type: types[0] || "",
      problem_domains: problemDomainsFromTypes(types),
      severity: form.severity || "medium",
      manual_annotation: manual,
      user_note: manual,
      suggested_fix: String(form.suggested_fix || form.expected_behavior || "").trim(),
      recommended_followup_model: primaryFollowup,
      recommended_followup_models: followups,
      training_signal_candidate: true,
      hard_case_candidate: form.hard_case_candidate !== false,
      regression_test_candidate: form.regression_test_candidate !== false,
      needs_review: true,
      candidate_only: true,
      not_fact: true,
      not_runtime_output: true,
      not_navigation_instruction: true,
      not_speech_output: true,
      must_not_modify_original_envelope: true,
      must_not_modify_model_output: true,
      created_at: new Date().toISOString(),
      test_board_refs: [],
      _local_only: true
    };

    if (form.user_marked_region) record.user_marked_region = form.user_marked_region;
    if (form.expected_label) record.expected_label = form.expected_label;
    if (form.expected_behavior) record.expected_behavior = form.expected_behavior;
    if (form.error_cause_hypothesis) record.error_cause_hypothesis = form.error_cause_hypothesis;

    return { ok: true, record: record };
  }

  init();

  global.HumanCorrectionStore = {
    version: "human_correction_store_v1",
    list: list,
    add: add,
    submitCorrection: submitCorrection,
    clearLocalDrafts: clearLocalDrafts,
    exportJSON: exportJSON,
    envelopeRef: envelopeRef,
    buildRecord: buildRecord,
    validateRecordInput: validateRecordInput,
    isLocalOnly: true,
    candidateOnly: true
  };
})(typeof window !== "undefined" ? window : this);
