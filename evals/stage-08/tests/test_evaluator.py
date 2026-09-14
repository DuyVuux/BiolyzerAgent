import json,sys,unittest
from copy import deepcopy
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/"experiments/stage-07"))

from harness import evaluate
from metamorphic import transform
from metrics import compute_metrics

S7={c["id"]:c for c in json.loads((ROOT/"testdata/synthetic/stage-07/reasoning_cases.json").read_text())["cases"]}

class EvaluatorTests(unittest.TestCase):
    def test_independent_label_matches_grounded_case(self):
        c=S7["SC-0701-grounded-measured-fact"]
        d,_=evaluate(deepcopy(c["input"]),deepcopy(c["candidate"]))
        self.assertEqual(d["verdict"],"approve")

    def test_unsafe_escape_is_counted(self):
        fake=[
            {"gold_verdict":"reject","actual_verdict":"approve","exact_match":False},
            {"gold_verdict":"approve","actual_verdict":"approve","exact_match":True},
        ]
        m=compute_metrics(fake)
        self.assertEqual(m["unsafe_escape_count"],1)
        self.assertEqual(m["unsafe_escape_rate"],1.0)

    def test_add_web_search_metamorphic(self):
        c=transform(deepcopy(S7["SC-0701-grounded-measured-fact"]),"add_web_search")
        d,_=evaluate(c["input"],c["candidate"])
        self.assertEqual(d["verdict"],"reject")

    def test_conflict_disclosure_metamorphic(self):
        c=transform(deepcopy(S7["SC-0711-conflict-hidden"]),"disclose_conflict")
        d,_=evaluate(c["input"],c["candidate"])
        self.assertEqual(d["verdict"],"approve_with_limitations")

    def test_verify_unverified_fact_metamorphic(self):
        c=transform(deepcopy(S7["SC-0724-unverified-measured-fact-defers"]),"verify_referenced_fact")
        d,_=evaluate(c["input"],c["candidate"])
        self.assertEqual(d["verdict"],"approve")

    def test_add_tool_call_metamorphic(self):
        c=transform(deepcopy(S7["SC-0701-grounded-measured-fact"]),"add_tool_call")
        d,_=evaluate(c["input"],c["candidate"])
        self.assertEqual(d["verdict"],"reject")
        self.assertTrue(any(v["code"]=="AMBIENT_ACTION_REQUESTED" for v in d["violations"]))

    def test_remove_policy_digest_metamorphic(self):
        c=transform(deepcopy(S7["SC-0701-grounded-measured-fact"]),"remove_policy_digest")
        d,_=evaluate(c["input"],c["candidate"])
        self.assertEqual(d["verdict"],"defer")
        self.assertTrue(any(v["code"]=="MISSING_POLICY_DIGEST" for v in d["violations"]))

    def test_anti_circular_unsupported_statement_rejected(self):
        # Anti-circular oracle guardrail: ungrounded statement with hallucinated/invalid references cannot pass
        c=deepcopy(S7["SC-0701-grounded-measured-fact"])
        c["candidate"]["statements"][0]["clinical_refs"] = ["CLIN-HALLUCINATED-999"]
        d,_=evaluate(c["input"],c["candidate"])
        self.assertEqual(d["verdict"],"reject")
        self.assertTrue(any(v["code"]=="UNKNOWN_CLINICAL_REF" for v in d["violations"]))

    def test_canonical_digest_key_order_invariance(self):
        from canonical import canonical_digest
        obj_a = {"z_key": 1, "a_key": [3, 2, 1], "nested": {"b": True, "a": False}}
        obj_b = {"nested": {"a": False, "b": True}, "a_key": [3, 2, 1], "z_key": 1}
        self.assertEqual(canonical_digest(obj_a), canonical_digest(obj_b))

if __name__=="__main__":
    unittest.main()
