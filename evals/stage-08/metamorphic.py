from __future__ import annotations
from copy import deepcopy

def transform(case, name):
    out=deepcopy(case)
    if name=="reverse_statements":
        out["candidate"]["statements"]=list(reversed(out["candidate"].get("statements",[])))
        return out
    if name=="add_web_search":
        out["candidate"]["requested_actions"]=sorted(set(out["candidate"].get("requested_actions",[])+["web_search"]))
        return out
    if name=="disclose_conflict":
        for s in out["candidate"]["statements"]:
            s["conflict_disclosed"]=True
        return out
    if name=="ack_missing_context":
        for s in out["candidate"]["statements"]:
            s["missing_context_acknowledged"]=True
        return out
    if name=="verify_referenced_fact":
        used=set()
        for s in out["candidate"]["statements"]:
            used.update(s.get("clinical_refs",[]))
        for ref in out["input"]["clinical_refs"]:
            if ref["ref_id"] in used:
                ref["verification_state"]="verified"
        return out
    if name=="add_tool_call":
        out["candidate"]["requested_actions"]=sorted(set(out["candidate"].get("requested_actions",[])+["tool_call"]))
        return out
    if name=="remove_policy_digest":
        out["input"]["policies"]["safety_policy"]["digest"]=""
        return out
    raise ValueError(name)
