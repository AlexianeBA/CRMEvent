from fastapi import HTTPException

OPPORTUNITY_TRANSITIONS = {
    "new": {"qualification"},
    "qualification": {"proposal", "closed_lost"},
    "proposal": {"negotiation", "closed_lost"},
    "negotiation": {"closed_won", "closed_lost"},
    "closed_won": set(),
    "closed_lost": set(),
}

QUOTE_TRANSITIONS = {
    "draft": {"sent"},
    "sent": {"accepted", "rejected", "expired"},
    "accepted": {"locked"},
    "rejected": {"locked"},
    "expired": {"locked"},
    "locked": set(),
}

INVOICE_TRANSITIONS = {
    "draft": {"sent", "canceled"},
    "sent": {"paid", "overdue", "canceled"},
    "overdue": {"paid", "canceled"},
    "paid": {"locked"},
    "canceled": {"locked"},
    "locked": set(),
}

ACTIVITY_TRANSITIONS = {
    "draft": {"planned", "canceled"},
    "planned": {"done", "canceled"},
    "done": set(),
    "canceled": set(),
}

EVENT_TRANSITIONS = {
    "draft": {"scheduled", "canceled"},
    "scheduled": {"held", "canceled"},
    "held": {"locked"},
    "canceled": {"locked"},
    "locked": set(),
}

def ensure_transition_allowed(transitions: dict, current_status: str, new_status: str, entity_name: str):
    allowed = transitions.get(current_status, set())
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {entity_name} transition: {current_status} -> {new_status}",
        )

def ensure_fields_immutable(payload: dict, immutable_fields: set[str], entity_name: str):
    forbidden = immutable_fields.intersection(payload.keys())
    if forbidden:
        raise HTTPException(
            status_code=400,
            detail=f"Immutable fields for {entity_name}: {', '.join(sorted(forbidden))}",
        )

def block_if_final_status(current_status: str, final_statuses: set[str], entity_name: str):
    if current_status in final_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"{entity_name} is locked in status {current_status}",
        )