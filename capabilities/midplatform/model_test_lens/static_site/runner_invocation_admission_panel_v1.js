/**
 * Runner Invocation Admission — panel fragments for request items. No runner execution.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.RunnerInvocationAdmissionCopy || {}; };
  var ExecCopy = function () { return global.ControlledRunnerExecutionCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderAdmissionSection(req) {
    var c = Copy();
    var ar = req.admission_result;
    if (!ar) {
      return "<p class='ria-pending-eval muted'>尚未执行准入检查</p>";
    }
    var reason = ar.admission_decision === "rejected"
      ? "<p class='ria-reject'><span class='muted'>" + escapeHtml(c.labelRejectionReason) + "：</span>" +
        escapeHtml(ar.rejection_reason || "—") + "</p>"
      : "<p class='ria-admit'><span class='muted'>" + escapeHtml(c.labelAdmissionReason) + "：</span>" +
        escapeHtml(ar.admission_reason || "—") + "</p>";
    return (
      "<div class='ria-admission-block'>" +
      "<p class='ria-decision'><span class='muted'>" + escapeHtml(c.labelAdmissionDecision) + "：</span>" +
      "<strong class='ria-decision-" + escapeHtml(ar.admission_decision) + "'>" +
      escapeHtml(ar.admission_decision) + "</strong></p>" +
      reason +
      "<p class='ria-flags muted'>" + escapeHtml(c.labelTraceVerified) + ": " +
      (ar.trace_verified ? "yes" : "no") + " · " + escapeHtml(c.labelRouteMatch) + ": " +
      (ar.route_match_verified ? "yes" : "no") + " · " + escapeHtml(c.labelExecution) + ": " +
      escapeHtml(ar.execution_status) + "</p>" +
      "<p class='ria-policy muted'>" + escapeHtml(c.labelPolicyRefs) + ": " +
      escapeHtml((ar.policy_refs || []).join(", ")) + "</p>" +
      "<p class='ria-notice muted'>" + escapeHtml(c.notExecutionNotice) + "</p>" +
      "</div>"
    );
  }

  function renderActions(req) {
    var c = Copy();
    var rir = req.invocation_request_id;
    if (req.admission_status === "cancelled") {
      return "<span class='muted'>已取消</span>";
    }
    var html = "";
    if (!req.admission_result || req.admission_result.admission_decision === "pending") {
      html += "<button type='button' class='rmt-btn ria-btn-admit' data-req-action='run-admission' data-rir='" +
        escapeHtml(rir) + "'>" + escapeHtml(c.runAdmissionBtn) + "</button>";
    } else {
      html += "<button type='button' class='rmt-btn rmt-btn-ghost' data-req-action='recheck-admission' data-rir='" +
        escapeHtml(rir) + "'>" + escapeHtml(c.recheckAdmissionBtn) + "</button>";
    }
    html += "<button type='button' class='rmt-btn rmt-btn-ghost' data-req-action='cancel' data-rir='" +
      escapeHtml(rir) + "'>" + escapeHtml(c.cancelRequestBtn) + "</button>";
    if (req.admission_result && req.admission_result.admission_decision === "admitted") {
      var ec = ExecCopy();
      html += "<button type='button' class='rmt-btn crec-btn-generate' data-req-action='generate-execution-candidate' data-rir='" +
        escapeHtml(rir) + "'>" + escapeHtml(ec.generateExecutionCandidateBtn || "生成受控执行候选") + "</button>";
      html += "<button type='button' class='rmt-btn crec-btn-mobilesam' data-req-action='generate-mobilesam-candidate' data-rir='" +
        escapeHtml(rir) + "'>" + escapeHtml((global.ResultLayerCopy && global.ResultLayerCopy.prepareMobileSamCandidateBtn) ||
          "生成 MobileSAM 受控执行候选") + "</button>";
      html += "<span class='rmt-admitted-note muted'>" + escapeHtml(c.admittedNotice) + "</span>";
    }
    return html;
  }

  global.RunnerInvocationAdmissionPanel = {
    version: "runner_invocation_admission_panel_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Runner-Invocation-Admission-Execution-And-Post-Review-v1-001",
    admissionCopyMustNotImplyExecution: true,
    noRunnerExecution: true,
    renderAdmissionSection: renderAdmissionSection,
    renderActions: renderActions
  };
})(typeof window !== "undefined" ? window : this);
