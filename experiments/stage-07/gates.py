from __future__ import annotations
from policy import (
    PROHIBITED_CLASSES,
    PROHIBITED_INFERENCE_MODES,
    AMBIENT_ACTIONS,
)

def violation(gate, code, statement_id=None, detail=""):
    return {
        "gate": gate,
        "code": code,
        "statement_id": statement_id,
        "detail": detail,
    }

def index_input(inp):
    clinical = {x["ref_id"]:x for x in inp["clinical_refs"]}
    claims = {x["claim_id"]:x for x in inp["evidence_bundle"]["claims"]}
    return clinical, claims

def evaluate_statement(inp, st, clinical, claims):
    out = []
    sid = st["statement_id"]
    cls = st["statement_class"]

    # G4: prohibited behavior.
    if cls in PROHIBITED_CLASSES:
        out.append(violation("G4","PROHIBITED_STATEMENT_CLASS",sid,cls))
    if st["inference_mode"] in PROHIBITED_INFERENCE_MODES:
        out.append(violation("G4","PROHIBITED_INFERENCE_MODE",sid,st["inference_mode"]))

    # G1: clinical references.
    for ref in st["clinical_refs"]:
        if ref not in clinical:
            out.append(violation("G1","UNKNOWN_CLINICAL_REF",sid,ref))
            continue
        c = clinical[ref]
        if c["reconciliation_state"] == "reconciliation_required":
            out.append(violation("G1","CLINICAL_RECONCILIATION_REQUIRED",sid,ref))
        if cls in {"measured_fact","bounded_interpretation","derived_fact"} and c["verification_state"] == "unverified":
            out.append(violation("G1","UNVERIFIED_CLINICAL_INPUT",sid,ref))
        if cls == "bounded_interpretation" and c["terminology_state"] in {"candidate","unmapped"}:
            out.append(violation("G1","TERMINOLOGY_NOT_VALIDATED",sid,ref))
        if (
            c.get("source_signal") == "critical"
            and inp.get("critical_value_policy_state") == "disabled_pending_approved_clinical_policy"
        ):
            out.append(violation(
                "G6",
                "CRITICAL_SIGNAL_PRESENT_POLICY_DISABLED",
                sid,
                ref,
            ))

    # G2: evidence references.
    used_conflict = False
    for ref in st["evidence_claim_refs"]:
        if ref not in claims:
            out.append(violation("G2","UNKNOWN_EVIDENCE_CLAIM",sid,ref))
            continue
        status = claims[ref]["status"]
        if status == "unsupported":
            out.append(violation("G2","UNSUPPORTED_EVIDENCE_CLAIM",sid,ref))
        elif status == "claim_identity_conflict":
            out.append(violation("G2","EVIDENCE_CLAIM_IDENTITY_CONFLICT",sid,ref))
        elif status == "conflicted":
            used_conflict = True

    # G5: grounding.
    if cls == "measured_fact" and not st["clinical_refs"]:
        out.append(violation("G5","MEASURED_FACT_WITHOUT_CLINICAL_REF",sid))
    if cls == "derived_fact":
        if not st["clinical_refs"]:
            out.append(violation("G5","DERIVED_FACT_WITHOUT_CLINICAL_REF",sid))
        if not st.get("derivation_ref"):
            out.append(violation("G5","DERIVED_FACT_WITHOUT_DERIVATION",sid))
    if cls == "evidence_context" and not st["evidence_claim_refs"]:
        out.append(violation("G5","EVIDENCE_CONTEXT_WITHOUT_CLAIM",sid))
    if cls == "bounded_interpretation":
        if not st["clinical_refs"]:
            out.append(violation("G5","INTERPRETATION_WITHOUT_CLINICAL_REF",sid))
        if not st["evidence_claim_refs"]:
            out.append(violation("G5","INTERPRETATION_WITHOUT_EVIDENCE_REF",sid))
        if st["assertion_strength"] == "definitive":
            out.append(violation("G5","DEFINITIVE_PATIENT_INTERPRETATION",sid))

    # G6: conflict / missing context.
    if used_conflict and not st["conflict_disclosed"]:
        out.append(violation("G6","CONFLICT_NOT_DISCLOSED",sid))
    if inp["missing_context"] and cls == "bounded_interpretation" and not st["missing_context_acknowledged"]:
        out.append(violation("G6","MISSING_CONTEXT_NOT_ACKNOWLEDGED",sid))

    # Evidence bundle completeness.
    if inp["evidence_bundle"]["status"] == "incomplete" and cls in {"evidence_context","bounded_interpretation"}:
        out.append(violation("G2","EVIDENCE_BUNDLE_INCOMPLETE",sid))

    return out
