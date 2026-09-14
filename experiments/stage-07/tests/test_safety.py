import json,sys,unittest
from copy import deepcopy
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from harness import evaluate

ROOT=HERE.parents[1]
CASES=json.loads((ROOT/"testdata/synthetic/stage-07/reasoning_cases.json").read_text())["cases"]
BY={c["id"]:c for c in CASES}

class SafetyHarnessTests(unittest.TestCase):
    def verdict(self,name):
        c=BY[name]
        return evaluate(c["input"],c["candidate"])[0]["verdict"]

    def test_grounded_measured_fact_allowed(self):
        self.assertEqual(self.verdict("SC-0701-grounded-measured-fact"),"approve")

    def test_derived_fact_requires_derivation_and_passes_when_present(self):
        self.assertEqual(self.verdict("SC-0702-grounded-derived-fact"),"approve")

    def test_diagnosis_rejected(self):
        self.assertEqual(self.verdict("SC-0705-diagnosis-rejected"),"reject")

    def test_treatment_rejected(self):
        self.assertEqual(self.verdict("SC-0706-treatment-rejected"),"reject")

    def test_dose_change_rejected(self):
        self.assertEqual(self.verdict("SC-0707-dose-change-rejected"),"reject")

    def test_triage_rejected(self):
        self.assertEqual(self.verdict("SC-0708-emergency-triage-rejected"),"reject")

    def test_unknown_clinical_ref_rejected(self):
        self.assertEqual(self.verdict("SC-0709-unknown-clinical-ref"),"reject")

    def test_unsupported_evidence_rejected(self):
        self.assertEqual(self.verdict("SC-0710-unsupported-evidence"),"reject")

    def test_hidden_conflict_rejected(self):
        self.assertEqual(self.verdict("SC-0711-conflict-hidden"),"reject")

    def test_disclosed_conflict_limited(self):
        self.assertEqual(self.verdict("SC-0712-conflict-disclosed"),"approve_with_limitations")

    def test_incomplete_evidence_defers(self):
        self.assertEqual(self.verdict("SC-0713-incomplete-evidence-defers-interpretation"),"defer")

    def test_reconciliation_defers(self):
        self.assertEqual(self.verdict("SC-0714-reconciliation-defers"),"defer")

    def test_ambient_retrieval_rejected(self):
        self.assertEqual(self.verdict("SC-0715-ambient-retrieval-rejected"),"reject")

    def test_claim_collision_rejected(self):
        self.assertEqual(self.verdict("SC-0716-claim-collision-rejected"),"reject")

    def test_missing_context_requires_acknowledgement(self):
        self.assertEqual(self.verdict("SC-0718-missing-context-hidden"),"reject")

    def test_candidate_terminology_defers(self):
        self.assertEqual(self.verdict("SC-0719-candidate-terminology-cannot-upgrade"),"defer")

    def test_patient_specific_causal_rejected(self):
        self.assertEqual(self.verdict("SC-0720-patient-specific-causal-rejected"),"reject")

    def test_source_instruction_cannot_grant_tool(self):
        self.assertEqual(self.verdict("SC-0721-source-instruction-cannot-grant-tool"),"reject")

    def test_source_critical_flag_is_reviewable_without_autonomous_triage(self):
        self.assertEqual(
            self.verdict("SC-0723-critical-source-flag-is-reviewable-not-triage"),
            "approve_with_limitations",
        )

    def test_unverified_measured_fact_defers(self):
        self.assertEqual(
            self.verdict("SC-0724-unverified-measured-fact-defers"),
            "defer",
        )

    def test_approved_output_exposes_independent_review_basis(self):
        c=BY["SC-0704-bounded-interpretation"]
        decision,output=evaluate(deepcopy(c["input"]),deepcopy(c["candidate"]))
        self.assertEqual(decision["verdict"],"approve")
        self.assertEqual(output["review_basis"]["clinical_snapshot_id"],c["input"]["clinical_snapshot_id"])
        self.assertEqual(output["review_basis"]["evidence_bundle_id"],c["input"]["evidence_bundle"]["bundle_id"])
        self.assertIn("timeline_snapshot_id",output["review_basis"])
        self.assertEqual(len(output["review_basis"]["policy_digests"]),len(set(output["review_basis"]["policy_digests"])))

    def test_decision_is_deterministic(self):
        c=BY["SC-0704-bounded-interpretation"]
        a=evaluate(deepcopy(c["input"]),deepcopy(c["candidate"]))[0]
        b=evaluate(deepcopy(c["input"]),deepcopy(c["candidate"]))[0]
        self.assertEqual(a["decision_sha256"],b["decision_sha256"])

if __name__=="__main__":
    unittest.main()
