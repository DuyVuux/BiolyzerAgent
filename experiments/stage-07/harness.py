from __future__ import annotations
import hashlib, json
from gates import evaluate_statement, index_input, violation
from policy import AMBIENT_ACTIONS, VERDICT_PRIORITY, ALLOWED_FINAL_CLASSES

REJECT_CODES = {
    "PROHIBITED_STATEMENT_CLASS",
    "PROHIBITED_INFERENCE_MODE",
    "UNKNOWN_CLINICAL_REF",
    "UNKNOWN_EVIDENCE_CLAIM",
    "UNSUPPORTED_EVIDENCE_CLAIM",
    "EVIDENCE_CLAIM_IDENTITY_CONFLICT",
    "MEASURED_FACT_WITHOUT_CLINICAL_REF",
    "DERIVED_FACT_WITHOUT_CLINICAL_REF",
    "DERIVED_FACT_WITHOUT_DERIVATION",
    "EVIDENCE_CONTEXT_WITHOUT_CLAIM",
    "INTERPRETATION_WITHOUT_CLINICAL_REF",
    "INTERPRETATION_WITHOUT_EVIDENCE_REF",
    "DEFINITIVE_PATIENT_INTERPRETATION",
    "CONFLICT_NOT_DISCLOSED",
    "MISSING_CONTEXT_NOT_ACKNOWLEDGED",
    "AMBIENT_ACTION_REQUESTED",
}

DEFER_CODES = {
    "CLINICAL_RECONCILIATION_REQUIRED",
    "UNVERIFIED_CLINICAL_INPUT",
    "TERMINOLOGY_NOT_VALIDATED",
    "EVIDENCE_BUNDLE_INCOMPLETE",
    "MISSING_POLICY_DIGEST",
    "MISSING_EVIDENCE_PROCESSING_PROFILE",
}

LIMITATION_CODES = {
    "USED_CONFLICTED_EVIDENCE",
    "KNOWN_MISSING_CONTEXT",
    "CRITICAL_SIGNAL_PRESENT_POLICY_DISABLED",
}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False)

def decision_hash(payload):
    return hashlib.sha256(canonical(payload).encode()).hexdigest()

def evaluate(inp, candidate):
    violations = []

    # G0 closure.
    if not inp["evidence_bundle"].get("processing_profile_digest"):
        violations.append(violation("G0","MISSING_EVIDENCE_PROCESSING_PROFILE"))
    for key in ["reasoning_policy","safety_policy"]:
        if not inp["policies"][key].get("digest"):
            violations.append(violation("G0","MISSING_POLICY_DIGEST",None,key))

    # G3 ambient action closure.
    for action in candidate["requested_actions"]:
        if action in AMBIENT_ACTIONS:
            violations.append(violation("G3","AMBIENT_ACTION_REQUESTED",None,action))

    clinical, claims = index_input(inp)
    for st in candidate["statements"]:
        violations.extend(evaluate_statement(inp, st, clinical, claims))
        if any(claims.get(ref,{}).get("status")=="conflicted" for ref in st["evidence_claim_refs"]) and st["conflict_disclosed"]:
            violations.append(violation("G6","USED_CONFLICTED_EVIDENCE",st["statement_id"]))
        if inp["missing_context"] and st["statement_class"]=="bounded_interpretation" and st["missing_context_acknowledged"]:
            violations.append(violation("G6","KNOWN_MISSING_CONTEXT",st["statement_id"]))

    codes = {v["code"] for v in violations}
    if codes & REJECT_CODES:
        verdict = "reject"
    elif codes & DEFER_CODES:
        verdict = "defer"
    elif codes & LIMITATION_CODES or any(st["statement_class"]=="limitation" for st in candidate["statements"]):
        verdict = "approve_with_limitations"
    else:
        verdict = "approve"

    decision_payload = {
        "schema_version":"1.0",
        "candidate_id":candidate["candidate_id"],
        "verdict":verdict,
        "violations":sorted(
            violations,
            key=lambda x:(x["gate"],x["code"],x["statement_id"] or "",x["detail"])
        )
    }
    decision = dict(decision_payload)
    decision["decision_sha256"] = decision_hash(decision_payload)

    output = None
    if verdict in {"approve","approve_with_limitations"}:
        approved = []
        for st in candidate["statements"]:
            if st["statement_class"] not in ALLOWED_FINAL_CLASSES:
                continue
            item = {
                "statement_id":st["statement_id"],
                "statement_class":st["statement_class"],
                "text":st["text"],
                "inference_mode":st["inference_mode"],
                "clinical_refs":st["clinical_refs"],
                "evidence_claim_refs":st["evidence_claim_refs"],
            }
            if st.get("derivation_ref"):
                item["derivation_ref"]=st["derivation_ref"]
            approved.append(item)

        clinical_refs=sorted({r for st in approved for r in st["clinical_refs"]})
        evidence_refs=sorted({r for st in approved for r in st["evidence_claim_refs"]})
        limitations=list(inp["missing_context"])
        if any(v["code"]=="USED_CONFLICTED_EVIDENCE" for v in violations):
            limitations.append("Included evidence contains an explicit conflict.")
        if any(v["code"]=="CRITICAL_SIGNAL_PRESENT_POLICY_DISABLED" for v in violations):
            limitations.append(
                "A source-provided critical signal is present; no approved autonomous critical-value escalation policy is active."
            )
        output = {
            "schema_version":"1.0",
            "candidate_id":candidate["candidate_id"],
            "verdict":verdict,
            "physician_review_required":True,
            "approved_statements":approved,
            "review_basis":{
                "clinical_snapshot_id":inp["clinical_snapshot_id"],
                **({"timeline_snapshot_id":inp["timeline_snapshot_id"]} if inp.get("timeline_snapshot_id") else {}),
                "evidence_bundle_id":inp["evidence_bundle"]["bundle_id"],
                "clinical_refs":clinical_refs,
                "evidence_claim_refs":evidence_refs,
                "policy_digests":sorted(set([
                    inp["evidence_bundle"]["processing_profile_digest"],
                    inp["policies"]["reasoning_policy"]["digest"],
                    inp["policies"]["safety_policy"]["digest"],
                ]))
            },
            "limitations":limitations,
        }

    return decision, output
