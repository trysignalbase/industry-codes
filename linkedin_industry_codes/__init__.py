"""LinkedIn Industry Codes library - async-first implementation."""

from .matcher import (
    IndustryMatcher,
    get_closest_categories_batch,
    get_closest_category,
)
from .scraper import scrape_industry_codes

__version__ = "0.1.0"
__all__ = [
    "get_closest_category",
    "get_closest_categories_batch",
    "IndustryMatcher",
    "scrape_industry_codes",
]
