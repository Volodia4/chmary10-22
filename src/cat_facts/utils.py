def validate_fact_length(fact: str) -> bool:
    """Validate fact length"""
    return 10 <= len(fact) <= 500
