"""
Sanction Letter Generator
=========================
Final stage - Generates PDF sanction letter for approved loans.

Uses FPDF2 for PDF generation.
Implements policy-based automated approval vs human-in-the-loop gating.
"""

import os
from datetime import datetime
from typing import Dict, Any
from fpdf import FPDF
from utils.crypto_utils import decrypt_data


# =============================================================================
# POLICY CONFIGURATION
# =============================================================================
# Maximum loan amount eligible for automated approval (no human review required)
# Loans above this threshold require human-in-the-loop review
AUTO_APPROVAL_LIMIT = 50000  # Rs. 50,000


# Ensure the generated folder exists
GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "generated")


def ensure_generated_dir():
    """Create the generated directory if it doesn't exist."""
    if not os.path.exists(GENERATED_DIR):
        os.makedirs(GENERATED_DIR)
        print(f"[SANCTION AGENT] Created directory: {GENERATED_DIR}")


def generate_sanction_letter(data: dict) -> dict:
    """
    Generate a PDF sanction letter for approved loans.
    
    Args:
        data: Dict containing loan details:
            - session_id: str
            - customer_name: str
            - loan_amount: int
            - tenure: int (months)
            - emi: float
            - interest_rate: float
    
    Returns:
        Dict with status and file path:
            - status: "generated" or "error"
            - file: filename of generated PDF
    """
    try:
        ensure_generated_dir()
        
        # Extract data with defaults
        session_id = data.get("session_id", "unknown")
        customer_name = data.get("customer_name", "Valued Customer")
        loan_amount = data.get("loan_amount", 100000)
        tenure = data.get("tenure", 24)
        emi = data.get("emi", 4650.0)
        interest_rate = data.get("interest_rate", 10.5)
        
        # Generate filename
        filename = f"sanction_{session_id}.pdf"
        filepath = os.path.join(GENERATED_DIR, filename)
        
        # Current date for the letter
        approval_date = datetime.now().strftime("%d %B %Y")
        
        print(f"[SANCTION AGENT] Generating PDF: {filename}")
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # =====================================================================
        # HEADER
        # =====================================================================
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 15, "LOANOPS FINANCIAL SERVICES", ln=True, align="C")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "Registered NBFC | CIN: U65100MH2024PLC123456", ln=True, align="C")
        pdf.cell(0, 6, "Email: support@loanops.ai | Phone: 1800-XXX-XXXX", ln=True, align="C")
        
        pdf.ln(10)
        
        # Horizontal line
        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # =====================================================================
        # TITLE
        # =====================================================================
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, "PERSONAL LOAN SANCTION LETTER", ln=True, align="C")
        pdf.ln(5)
        
        # =====================================================================
        # DATE AND REFERENCE
        # =====================================================================
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f"Date: {approval_date}", ln=True)
        pdf.cell(0, 8, f"Reference No: LOA/{session_id.upper()}/{datetime.now().strftime('%Y%m%d')}", ln=True)
        pdf.ln(5)
        
        # =====================================================================
        # SALUTATION
        # =====================================================================
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f"Dear {customer_name},", ln=True)
        pdf.ln(3)
        
        # =====================================================================
        # BODY TEXT
        # =====================================================================
        pdf.set_font("Helvetica", "", 11)
        body_text = (
            "We are pleased to inform you that your Personal Loan application has been "
            "approved. Please find the details of your sanctioned loan below:"
        )
        pdf.multi_cell(0, 7, body_text)
        pdf.ln(8)
        
        # =====================================================================
        # LOAN DETAILS TABLE
        # =====================================================================
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "LOAN DETAILS", ln=True)
        
        pdf.set_font("Helvetica", "", 11)
        
        # Table with loan details
        col_width = 95
        row_height = 10
        
        # Draw table rows
        details_table = [
            ("Applicant Name", customer_name),
            ("Sanctioned Loan Amount", f"Rs. {loan_amount:,}"),
            ("Rate of Interest", f"{interest_rate}% per annum"),
            ("Loan Tenure", f"{tenure} months"),
            ("Equated Monthly Instalment (EMI)", f"Rs. {emi:,.2f}"),
            ("Processing Fee", "Rs. 1,000 + GST"),
            ("Disbursement Mode", "Direct Bank Transfer"),
        ]
        
        for label, value in details_table:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(col_width, row_height, label, border=1)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(col_width, row_height, str(value), border=1, ln=True)
        
        pdf.ln(10)
        
        # =====================================================================
        # TERMS AND CONDITIONS
        # =====================================================================
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "TERMS AND CONDITIONS", ln=True)
        
        pdf.set_font("Helvetica", "", 10)
        terms = [
            "1. This sanction is valid for 30 days from the date of issue.",
            "2. Loan disbursement is subject to document verification.",
            "3. Prepayment charges may apply as per RBI guidelines.",
            "4. EMI payment via auto-debit/NACH mandate is mandatory.",
            "5. The borrower agrees to all terms in the loan agreement.",
        ]
        
        for term in terms:
            pdf.cell(0, 7, term, ln=True)
        
        pdf.ln(10)
        
        # =====================================================================
        # SIGNATURE SECTION
        # =====================================================================
        pdf.cell(0, 8, "For LoanOps Financial Services,", ln=True)
        pdf.ln(15)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "Authorized Signatory", ln=True)
        
        pdf.ln(10)
        
        # =====================================================================
        # FOOTER
        # =====================================================================
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, "This is a system-generated sanction letter and does not require a physical signature.", ln=True, align="C")
        pdf.cell(0, 6, "For any queries, please contact our customer support.", ln=True, align="C")
        
        # Save PDF
        pdf.output(filepath)
        
        print(f"[SANCTION AGENT] PDF generated successfully: {filepath}")
        
        return {
            "status": "generated",
            "file": filename,
            "path": filepath
        }
    
    except Exception as e:
        print(f"[SANCTION AGENT] PDF generation failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "file": None
        }


def sanction_agent_node(state: Dict, user_message: str) -> Dict[str, Any]:
    """
    Sanction Agent - Handles loan approval finalization with policy-based gating.
    
    Policy:
    - Loans <= AUTO_APPROVAL_LIMIT (Rs. 50,000): Automated approval
    - Loans > AUTO_APPROVAL_LIMIT: Forwarded to human review
    
    Args:
        state: Current conversation state
        user_message: User's input message
    
    Returns:
        Dict with reply, sanction details, and decision metadata
    """
    print("[SANCTION AGENT] Processing sanction request...")
    
    # Ensure verification completed
    if not state.get("verified"):
        print("[SANCTION AGENT] Attempted sanction without verification")
        return {
            "reply": "Cannot proceed: verification incomplete. Please complete identity verification first.",
            "sanction_status": "blocked",
            "loan_details": None,
            "pdf_result": None,
            "decision_type": None,
            "decision_reason": None,
            "policy_applied": None
        }
    
    # Get session_id from state (fallback to timestamp if not available)
    session_id = state.get("session_id", datetime.now().strftime("%Y%m%d%H%M%S"))
    
    # Loan details - in production, these would come from underwriting
    loan_amount = state.get("loan_amount", 100000)
    
    loan_details = {
        "session_id": session_id,
        "customer_name": state.get("customer_name", "Valued Customer"),
        "loan_amount": loan_amount,
        "tenure": state.get("tenure", 24),
        "emi": state.get("emi", 4650.0),
        "interest_rate": state.get("interest_rate", 10.5),
    }

    # If encrypted verification blob exists, attempt to decrypt to enrich letter
    encrypted_blob = state.get("verification_encrypted")
    if encrypted_blob:
        try:
            decrypted = decrypt_data(encrypted_blob.encode("utf-8"))
            # best-effort parse
            import json
            parsed = json.loads(decrypted.decode("utf-8"))
            # prefer name from verified payload
            loan_details["customer_name"] = parsed.get("name") or parsed.get("full_name") or loan_details["customer_name"]
        except Exception as e:
            print(f"[SANCTION AGENT] Failed to decrypt verification blob: {e}")
    
    # =========================================================================
    # POLICY-BASED DECISION: AUTOMATED vs HUMAN REVIEW
    # =========================================================================
    if loan_amount <= AUTO_APPROVAL_LIMIT:
        # AUTOMATED APPROVAL - within policy threshold
        decision_type = "AUTOMATED"
        decision_source = "System (Policy-Based)"
        decision_reason = f"Loan amount (Rs. {loan_amount:,}) is within the automated approval limit of Rs. {AUTO_APPROVAL_LIMIT:,}"
        policy_applied = f"AUTO_APPROVAL_LIMIT: Rs. {AUTO_APPROVAL_LIMIT:,}"
        
        print(f"[SANCTION AGENT] Automated approval: {loan_amount} <= {AUTO_APPROVAL_LIMIT}")
        
        # Generate PDF sanction letter
        pdf_result = generate_sanction_letter(loan_details)
        
        if pdf_result["status"] == "generated":
            try:
                from utils.gemini_explainer import generate_explanation
                
                explanation = generate_explanation({
                    "status": "APPROVED_AUTOMATED",
                    "reason": "All eligibility criteria met - within automated approval policy",
                    "loan_amount": loan_details["loan_amount"],
                    "salary": state.get("salary", "N/A"),
                    "emi": loan_details["emi"]
                })
                
                reply = f"""{explanation}

📄 Loan Summary:
- Amount: Rs. {loan_details['loan_amount']:,}
- Interest Rate: {loan_details['interest_rate']}% p.a.
- Tenure: {loan_details['tenure']} months
- Monthly EMI: Rs. {loan_details['emi']:,.2f}

✅ This loan falls within the automated approval policy (up to Rs. {AUTO_APPROVAL_LIMIT:,}) and has been approved.

📋 Decision: Approved by System (Policy-Based)
Your sanction letter has been generated: {pdf_result['file']}"""
                
            except Exception as e:
                print(f"[SANCTION AGENT] Gemini explainer failed, using default: {e}")
                reply = f"""🎉 LOAN SANCTIONED SUCCESSFULLY!

Congratulations! Your loan application has been approved.

📄 Loan Summary:
- Amount: Rs. {loan_details['loan_amount']:,}
- Interest Rate: {loan_details['interest_rate']}% p.a.
- Tenure: {loan_details['tenure']} months
- Monthly EMI: Rs. {loan_details['emi']:,.2f}

✅ This loan falls within the automated approval policy (up to Rs. {AUTO_APPROVAL_LIMIT:,}) and has been approved.

📋 Decision: Approved by System (Policy-Based)
Your sanction letter has been generated: {pdf_result['file']}"""
            
            # Store sanction letter filename in state
            state["sanction_letter"] = pdf_result["file"]
            sanction_status = "completed"
            
        else:
            reply = f"""✅ LOAN APPROVED!

Your loan has been approved under the automated approval policy. However, there was an issue generating the sanction letter.
Our team will send you the sanction letter shortly via email.

📋 Decision: Approved by System (Policy-Based)"""
            sanction_status = "completed"
            
        print("[SANCTION AGENT] Automated approval completed!")
        
    else:
        # HUMAN REVIEW REQUIRED - exceeds policy threshold
        decision_type = "HUMAN_REVIEW"
        decision_source = "Human-in-the-Loop"
        decision_reason = f"Loan amount (Rs. {loan_amount:,}) exceeds the automated approval limit of Rs. {AUTO_APPROVAL_LIMIT:,}"
        policy_applied = f"AUTO_APPROVAL_LIMIT: Rs. {AUTO_APPROVAL_LIMIT:,}"
        pdf_result = {"status": "not_generated", "file": None}
        
        print(f"[SANCTION AGENT] Human review required: {loan_amount} > {AUTO_APPROVAL_LIMIT}")
        
        reply = f"""📋 APPLICATION FORWARDED FOR REVIEW

Your loan application has passed all automated eligibility checks and has been forwarded for manual review.

📄 Application Summary:
- Requested Amount: Rs. {loan_details['loan_amount']:,}
- Interest Rate: {loan_details['interest_rate']}% p.a.
- Tenure: {loan_details['tenure']} months
- Monthly EMI: Rs. {loan_details['emi']:,.2f}

⏳ This loan exceeds the automated approval limit (Rs. {AUTO_APPROVAL_LIMIT:,}) and has been forwarded for manual review by our credit team.

📋 Decision: Pending Human Review
Expected turnaround: 1-2 business days

You will receive an update via email once the review is complete. Thank you for your patience."""

        sanction_status = "pending_human_review"
        
        print("[SANCTION AGENT] Forwarded to human review")
    
    # Store decision metadata in state
    state["decision_type"] = decision_type
    state["decision_source"] = decision_source
    
    return {
        "reply": reply,
        "sanction_status": sanction_status,
        "loan_details": loan_details,
        "pdf_result": pdf_result,
        "sanction_letter": pdf_result.get("file"),
        # Decision Metadata
        "decision_type": decision_type,
        "decision_reason": decision_reason,
        "decision_source": decision_source,
        "policy_applied": policy_applied
    }

