def get_preapproved_limit(customer_id: str) -> int:
    """
    Mock implementation of fetching a pre-approved loan limit for a customer.
    """
    # Mock data for demonstration purposes
    mock_preapproved_limits = {
        "1": 500000,
        "2": 200000,
        "3": 300000
    }
    return mock_preapproved_limits.get(customer_id, 100000)  # Default to 100,000 if not found