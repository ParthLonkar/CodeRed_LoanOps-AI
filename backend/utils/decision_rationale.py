"""
Decision Rationale Generator
============================
Generates structured, explainable decision rationale from existing computed values.

This module provides transparency into loan decisions by:
- Summarizing why a decision was made
- Listing key factors that influenced the outcome
- Displaying relevant metrics in a human-readable format

IMPORTANT: This is EXPLANATION ONLY - no decision logic is implemented here.
All values are read-only from existing computations.
"""

from typing import Dict, List, Any, Optional


# =============================================================================
# POLICY THRESHOLDS (mirrors existing values for explanation only)
# =============================================================================
AUTO_APPROVAL_LIMIT = 50000  # Rs. - loans above this need human review
EMI_INCOME_THRESHOLD = 0.5   # 50% - max EMI-to-income ratio for approval


def generate_decision_rationale(
    decision: str,
    loan_amount: float,
    salary: float,
    emi: float,
    risk_score: Optional[int] = None,
    risk_level: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a structured decision rationale from existing computed values.
    
    This function ONLY explains decisions - it does not make them.
    All inputs must come from already-finalized decision data.
    
    Args:
        decision: Final decision - "APPROVED", "REJECTED", or "MANUAL_REVIEW"
        loan_amount: Requested loan amount
        salary: Monthly salary
        emi: Calculated EMI
        risk_score: Risk score 0-100 (optional)
        risk_level: Risk level Low/Medium/High (optional)
    
    Returns:
        Structured rationale dict with:
        - decision: str
        - confidence: "HIGH" | "MEDIUM" | "LOW"
        - key_factors: List[str] - human-readable explanation points
        - metrics: dict - relevant numeric values
        - decision_mode: str - always "AI-assisted, rule-based underwriting"
    """
    # Calculate derived values
    emi_ratio = (emi / salary * 100) if salary > 0 else 0
    emi_ratio_str = f"{emi_ratio:.1f}%"
    
    # Build key factors based on decision type
    key_factors: List[str] = []
    confidence = "HIGH"
    
    if decision == "APPROVED":
        # Explain why approved
        key_factors.append("EMI-to-income ratio is within acceptable limits (≤50%)")
        key_factors.append(f"Loan amount (Rs. {loan_amount:,.0f}) qualifies for automated approval")
        
        if risk_level == "Low":
            key_factors.append("Risk assessment indicates low-risk profile")
            confidence = "HIGH"
        elif risk_level == "Medium":
            key_factors.append("Risk assessment indicates moderate profile")
            confidence = "HIGH"
        else:
            confidence = "MEDIUM"
        
        if emi_ratio <= 30:
            key_factors.append("Excellent debt-to-income ratio")
        elif emi_ratio <= 40:
            key_factors.append("Healthy EMI burden relative to income")
            
    elif decision == "REJECTED":
        # Explain why rejected
        if emi_ratio > 50:
            key_factors.append(f"EMI-to-income ratio ({emi_ratio_str}) exceeds 50% threshold")
            key_factors.append("Monthly EMI burden is too high relative to income")
        
        key_factors.append("Based on current eligibility rules, approval is not possible")
        key_factors.append("This decision can be reviewed upon change in financial circumstances")
        confidence = "HIGH"
        
    elif decision == "MANUAL_REVIEW":
        # Explain why manual review needed
        if loan_amount > AUTO_APPROVAL_LIMIT:
            key_factors.append(f"Loan amount (Rs. {loan_amount:,.0f}) exceeds auto-approval limit (Rs. {AUTO_APPROVAL_LIMIT:,})")
            key_factors.append("Higher loan amounts require human verification")
        
        if risk_level == "High":
            key_factors.append("Elevated risk score requires manual assessment")
            confidence = "MEDIUM"
        else:
            confidence = "HIGH"
            
        key_factors.append("A credit officer will review your application")
        key_factors.append("Expected turnaround: 1-2 business days")
    
    # Build metrics dictionary
    metrics = {
        "loan_amount": loan_amount,
        "monthly_income": salary,
        "emi": round(emi, 2),
        "emi_ratio": emi_ratio_str,
    }
    
    if risk_score is not None:
        metrics["risk_score"] = risk_score
    if risk_level is not None:
        metrics["risk_level"] = risk_level
    
    return {
        "decision": decision,
        "confidence": confidence,
        "key_factors": key_factors,
        "metrics": metrics,
        "decision_mode": "AI-assisted, rule-based underwriting"
    }
