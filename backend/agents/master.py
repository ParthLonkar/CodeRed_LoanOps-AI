"""
Master Agent (Supervisor)
=========================
Orchestrates the flow between specialized agents using a simple state machine.

Flow: Sales → Verification → Underwriting → Sanction/Rejected

This is a DEMO-FIRST implementation for hackathon demonstration.
Stability > Intelligence.
"""

from typing import Dict, Literal, Any
from agents.sales import sales_agent_node
from agents.verification import verification_agent_node
from agents.underwriting import underwriting_agent_node
from agents.sanction import sanction_agent_node

# ============================================================================
# LangGraph State Definition (Simple Dict)
# ============================================================================

def create_initial_state() -> Dict[str, Any]:
    """Create a fresh state for a new conversation."""
    return {
        "stage": "sales",
        "active_agent": "SalesAgent",
        "messages": [],
        "user_data": {},
        "verification_status": None,
        "underwriting_decision": None,
        "loan_details": {},
    }


# ============================================================================
# Agent Routing Map
# ============================================================================

STAGE_TO_AGENT = {
    "sales": ("SalesAgent", sales_agent_node),
    "verification": ("VerificationAgent", verification_agent_node),
    "underwriting": ("UnderwritingAgent", underwriting_agent_node),
    "sanction": ("SanctionAgent", sanction_agent_node),
    "rejected": ("SanctionAgent", None),  # No agent for rejected, just returns message
}


# ============================================================================
# Supervisor Logic
# ============================================================================

def determine_next_stage(state: Dict, user_message: str) -> str:
    """
    Determine the next stage based on current state and user message.
    
    SIMPLE & DETERMINISTIC routing for demo safety:
    - Start at "sales"
    - After intent captured → "verification"
    - After KYC verified → "underwriting"
    - After underwriting → "sanction" or "rejected"
    
    TODO: Integrate with actual LangGraph routing when ready.
    """
    current_stage = state.get("stage", "sales")
    message_lower = user_message.lower()
    
    print(f"[SUPERVISOR] Current stage: {current_stage}")
    print(f"[SUPERVISOR] User message: {user_message[:50]}...")
    
    if current_stage == "sales":
        # Move to verification when user expresses loan intent
        if any(keyword in message_lower for keyword in ["loan", "lakh", "amount", "borrow", "need", "want", "rupees", "₹"]):
            print("[SUPERVISOR] Loan intent detected → Moving to VERIFICATION")
            return "verification"
        return "sales"
    
    elif current_stage == "verification":
        # Move to underwriting when verification keywords detected
        if any(keyword in message_lower for keyword in ["pan", "aadhaar", "verified", "confirm", "yes", "proceed", "id"]):
            print("[SUPERVISOR] Verification confirmed → Moving to UNDERWRITING")
            return "underwriting"
        return "verification"
    
    elif current_stage == "underwriting":
        # Underwriting auto-transitions based on decision
        # TODO: Plug in real underwriting_rules.check_eligibility() here
        decision = state.get("underwriting_decision")
        if decision == "approved":
            print("[SUPERVISOR] Loan APPROVED → Moving to SANCTION")
            return "sanction"
        elif decision == "rejected":
            print("[SUPERVISOR] Loan REJECTED → Moving to REJECTED")
            return "rejected"
        # Default: stay in underwriting until decision is made
        return "underwriting"
    
    elif current_stage == "sanction":
        # Terminal state - stay here
        return "sanction"
    
    elif current_stage == "rejected":
        # Terminal state - stay here
        return "rejected"
    
    return current_stage


def supervisor_node(state: Dict, user_message: str) -> Dict[str, Any]:
    """
    Main supervisor function that orchestrates the agent workflow.
    
    This is the entry point called from the /chat endpoint.
    
    Args:
        state: Current conversation state
        user_message: User's input message
    
    Returns:
        Dict with: reply, stage, active_agent
    
    DEMO SAFETY:
    - Never crashes
    - Always returns valid response
    - Clear logging for mentor visibility
    """
    try:
        print("\n" + "="*60)
        print("[SUPERVISOR] Processing message...")
        print("="*60)
        
        # Determine the next stage
        next_stage = determine_next_stage(state, user_message)
        state["stage"] = next_stage
        
        # Get the appropriate agent
        agent_name, agent_func = STAGE_TO_AGENT.get(next_stage, ("SalesAgent", sales_agent_node))
        state["active_agent"] = agent_name
        
        print(f"[SUPERVISOR] Routing to: {agent_name}")
        
        # Call the agent to get response
        if agent_func:
            agent_response = agent_func(state, user_message)
        else:
            # Fallback for terminal states without agent
            agent_response = {
                "reply": "Thank you for your interest. Is there anything else I can help you with?",
                "underwriting_decision": state.get("underwriting_decision")
            }
        
        # Extract reply from agent response
        reply = agent_response.get("reply", "How can I assist you today?")
        
        # Update state with any agent-provided data
        if "underwriting_decision" in agent_response:
            state["underwriting_decision"] = agent_response["underwriting_decision"]
        
        # Check if we need to auto-transition after underwriting
        if next_stage == "underwriting" and state.get("underwriting_decision"):
            # Re-route based on decision
            final_stage = determine_next_stage(state, user_message)
            state["stage"] = final_stage
            final_agent_name = STAGE_TO_AGENT.get(final_stage, ("SalesAgent", None))[0]
            state["active_agent"] = final_agent_name
            
            # Get sanction/rejection message
            if final_stage == "sanction":
                sanction_response = sanction_agent_node(state, user_message)
                reply = sanction_response.get("reply", reply)
            elif final_stage == "rejected":
                reply = "We regret to inform you that your loan application could not be approved at this time based on our eligibility criteria. Please contact our support team for more information."
        
        print(f"[SUPERVISOR] Final stage: {state['stage']}")
        print(f"[SUPERVISOR] Active agent: {state['active_agent']}")
        print(f"[SUPERVISOR] Reply: {reply[:50]}...")
        print("="*60 + "\n")
        
        return {
            "reply": reply,
            "stage": state["stage"],
            "active_agent": state["active_agent"]
        }
    
    except Exception as e:
        # DEMO SAFETY: Never crash during live presentation
        print(f"[SUPERVISOR ERROR] {str(e)}")
        return {
            "reply": "I apologize, but I encountered an issue. Let me help you with your loan application. What type of loan are you interested in?",
            "stage": "sales",
            "active_agent": "SalesAgent"
        }
