from dataclasses import dataclass

@dataclass
class CatFactsConfig:
    """Configuration limits for cat facts models"""
    min_fact_length: int = 10
    max_fact_length: int = 500
    min_fact_count: int = 0
    max_fact_count: int = 1000000

cat_facts_config = CatFactsConfig()
