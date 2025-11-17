"""Industry Codes library - async-first implementation."""

from .matcher import IndustryMatcher, get_closest_category
from .scraper import scrape_industry_codes

__version__ = "0.1.0"
__all__ = [
    "get_closest_category",
    "IndustryMatcher",
    "scrape_industry_codes",
]
