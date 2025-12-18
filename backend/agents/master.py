from backend.services.credit_bureau import fetch_credit_score
from backend.services.offer_mart import get_preapproved_limit

async def run_underwriting(customer_id: str, loan_details: dict):
    """
    Underwriting rules engine
    """

    loan_amount = loan_details["amount"]
    salary = loan_details.get("salary")
    expected_emi = loan_details.get("expected_emi")

    credit_score = fetch_credit_score(customer_id)
    preapproved_limit = get_preapproved_limit(customer_id)

    # ❌ Rule 3: Reject if credit score < 700
    if credit_score < 700:
        return {
            "status": "rejected",
            "reason": "Low credit score",
            "credit_score": credit_score
        }

    # ✅ Rule 1: Instant approval
    if loan_amount <= preapproved_limit:
        return {
            "status": "approved",
            "approval_type": "instant",
            "credit_score": credit_score
        }

    # ⚠️ Rule 2: Salary slip required
    if loan_amount <= 2 * preapproved_limit:
        if not salary or not expected_emi:
            return {
                "status": "salary_slip_required",
                "message": "Please upload your latest salary slip"
            }

        if expected_emi <= 0.5 * salary:
            return {
                "status": "approved",
                "approval_type": "salary_verified",
                "credit_score": credit_score
            }

        return {
            "status": "rejected",
            "reason": "EMI exceeds 50% of salary"
        }

    # ❌ Rule 3: Loan amount too high
    return {
        "status": "rejected",
        "reason": "Loan amount exceeds eligibility"
    }
