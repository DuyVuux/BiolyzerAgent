PROHIBITED_CLASSES = {
    "diagnosis",
    "treatment_recommendation",
    "medication_change",
    "dosage_change",
    "emergency_triage",
}

PROHIBITED_INFERENCE_MODES = {
    "diagnostic",
    "therapeutic",
    "triage",
    "patient_specific_causal",
}

ALLOWED_FINAL_CLASSES = {
    "measured_fact",
    "derived_fact",
    "evidence_context",
    "bounded_interpretation",
    "limitation",
    "physician_question",
}

AMBIENT_ACTIONS = {
    "web_search",
    "retrieval",
    "tool_call",
    "dynamic_schema",
    "dynamic_model",
}

VERDICT_PRIORITY = {
    "approve": 0,
    "approve_with_limitations": 1,
    "defer": 2,
    "reject": 3,
}
