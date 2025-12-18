# Underwriting Agent
# Calls the pure Python rule engine.
# No LLM decisions.

from backend.rules.underwriting_rules import check_eligibility

def underwriting_agent_node(state):
    # TODO: Extract financial data from state
    # TODO: Call check_eligibility()
    # TODO: Update state with decision
    pass
