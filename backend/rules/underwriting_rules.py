# Pure Python rule engine for underwriting
# STRICT: No LLMs here. Deterministic logic only.

def check_eligibility(income: int, debt: int, credit_score: int) -> dict:
    """
    Evaluates loan eligibility based on strict rules.
    Returns a dictionary with 'approved' (bool) and 'reason' (str).
    """
    # TODO: Implement rule logic
    # Example logic (placeholder):
    # if credit_score < 650: return False
    # dti = debt / income...
    
    return {"approved": False, "reason": "Not implemented yet"}
