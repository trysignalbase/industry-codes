"""Industry category matching using Levenshtein distance."""

from typing import Any

import httpx
from Levenshtein import distance as levenshtein_distance

# CDN URL for industry codes data
INDUSTRY_CODES_CDN_URL = (
    "https://cdn.jsdelivr.net/gh/trysignalbase/industry-codes@main/industry_codes.json"
)


class IndustryMatcher:
    """Matcher for finding closestindustry categories."""

    def __init__(self, industries_data: list[dict[str, Any]]):
        """
        Initialize the matcher with industry data.

        Args:
            industries_data: List of industry dictionaries (required).
        """
        self.industries = industries_data
        self._build_search_index()

    @classmethod
    async def create(
        cls, industries_data: list[dict[str, Any]] | None = None
    ) -> "IndustryMatcher":
        """
        Create an IndustryMatcher instance.

        Args:
            industries_data: Optional list of industry dictionaries.
                           If None, downloads from GitHub CDN.

        Returns:
            Initialized IndustryMatcher instance.

        Raises:
            RuntimeError: If downloading from GitHub fails.
        """
        if industries_data is None:
            industries_data = await cls._download_from_github()

        return cls(industries_data)

    @staticmethod
    async def _download_from_github() -> list[dict[str, Any]]:
        """
        Download industry data from GitHub CDN (jsDelivr).

        Returns:
            List of industry dictionaries.

        Raises:
            RuntimeError: If download fails.
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(INDUSTRY_CODES_CDN_URL)
                response.raise_for_status()
                data = response.json()
                return data.get("industries", [])
        except Exception as e:
            raise RuntimeError(
                f"Failed to download industry codes from CDN: {e}. "
                "Please check your internet connection or provide industries_data directly."
            ) from e

    def _build_search_index(self) -> None:
        """Build search index for efficient matching."""
        self.labels = [industry["label"] for industry in self.industries]
        self.hierarchies = [industry["hierarchy"] for industry in self.industries]

    def find_closest(
        self,
        query: str,
        top_n: int = 1,
        search_field: str = "label",
    ) -> list[dict[str, Any]]:
        """
        Find closest matching industry categories using Levenshtein distance.

        Args:
            query: The search query string.
            top_n: Number of top results to return.
            search_field: Field to search in ('label', 'hierarchy', or 'both').

        Returns:
            List of dictionaries containing matched industries with similarity scores.
        """
        query_lower = query.lower()
        results = []

        for industry in self.industries:
            if search_field == "label":
                search_text = industry["label"].lower()
            elif search_field == "hierarchy":
                search_text = industry["hierarchy"].lower()
            else:  # both
                search_text = f"{industry['label']} {industry['hierarchy']}".lower()

            # Calculate Levenshtein distance
            distance = levenshtein_distance(query_lower, search_text)

            # Calculate similarity score (0 to 1, where 1 is perfect match)
            max_len = max(len(query_lower), len(search_text))
            similarity = 1 - (distance / max_len) if max_len > 0 else 0

            results.append(
                {
                    **industry,
                    "similarity_score": similarity,
                    "levenshtein_distance": distance,
                }
            )

        # Sort by similarity (highest first)
        results.sort(key=lambda x: x["similarity_score"], reverse=True)

        return results[:top_n]

    def find_by_category(self, category: str) -> list[dict[str, Any]]:
        """
        Find all industries in a specific category.

        Args:
            category: The category name to filter by.

        Returns:
            List of industries in the specified category.
        """
        return [
            industry
            for industry in self.industries
            if industry["category"].lower() == category.lower()
        ]

    def get_all_categories(self) -> list[str]:
        """
        Get a list of all unique top-level categories.

        Returns:
            List of unique category names.
        """
        categories = set(industry["category"] for industry in self.industries)
        return sorted(categories)


# Convenience function
async def get_closest_category(
    query: str,
    top_n: int = 1,
    industries_data: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """
    Find the closest matchingindustry category.

    This is a convenience function that creates a matcher and returns results.
    For multiple queries, create an IndustryMatcher instance and reuse it.

    Args:
        query: The search query string.
        top_n: Number of top results to return.
        industries_data: Optional industry data. If None, downloads from GitHub.

    Returns:
        List of matched industries with similarity scores.

    Example:
        >>> results = await get_closest_category("software development")
        >>> print(results[0]["label"])
        >>> print(results[0]["similarity_score"])
    """
    matcher = await IndustryMatcher.create(industries_data)
    return matcher.find_closest(query, top_n=top_n)
