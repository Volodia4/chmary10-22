import re
from typing import Optional

def sanitize_fact_text(text: str) -> str:
    """Clean and sanitize fact text"""
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text.strip())
    # Ensure proper capitalization
    if cleaned and not cleaned[0].isupper():
        cleaned = cleaned[0].upper() + cleaned[1:]
    return cleaned

def validate_fact_length(fact: str, min_length: int = 10, max_length: int = 500) -> bool:
    """Validate fact length constraints"""
    return min_length <= len(fact) <= max_length
