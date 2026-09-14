/**
 * Scene profile candidate — UI state wrapper (candidate_only · not_fact).
 */
(function (global) {
  "use strict";

  var Policy = function () { return global.SceneProfilePolicy; };

  function buildCandidate(envelope, fileName) {
    var P = Policy();
    if (envelope && envelope.scene_profile_candidate) return envelope.scene_profile_candidate;
    if (P) return P.inferFromFileName(fileName || "");
    return {
      scene_profile_id: "spc_unknown",
      scene_type_candidate: "unknown_scene",
      confidence: 0.5,
      candidate_only: true,
      not_fact: true
    };
  }

  global.SceneProfileCandidate = {
    version: "scene_profile_candidate_v1",
    buildCandidate: buildCandidate
  };
})(typeof window !== "undefined" ? window : this);
