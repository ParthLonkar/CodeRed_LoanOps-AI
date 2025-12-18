def fetch_credit_score(customer_id: str) -> int:
    """
    Mock implementation of fetching a credit score for a customer.
    """
    # Mock data for demonstration purposes
    mock_credit_scores = {
        "1": 750,
        "2": 600,
        "3": 680
    }
    return mock_credit_scores.get(customer_id, 650)  # Default to 650 if not found