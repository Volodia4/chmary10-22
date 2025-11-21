from dataclasses import dataclass


@dataclass
class CatFactsConfig:
    """Configuration for Cat Facts API and models"""

    # API Configuration
    api_url: str = "https://catfact.ninja/fact"
    timeout: int = 10

    # Model constraints
    min_fact_length: int = 5
    max_fact_length: int = 500
    min_length_value: int = 1
    max_length_value: int = 1000


cat_facts_config = CatFactsConfig()
