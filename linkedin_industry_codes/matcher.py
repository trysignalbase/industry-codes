"""Industry category matching using Levenshtein distance."""

import asyncio
import json
from pathlib import Path
from typing import Any

import httpx
from Levenshtein import distance as levenshtein_distance


class IndustryMatcher:
    """Matcher for finding closest LinkedIn industry categories."""
    
    def __init__(self, industries_data: list[dict[str, Any]] | None = None):
        """
        Initialize the matcher synchronously.
        
        Args:
            industries_data: List of industry dictionaries. If None, will load from package data.
        
        Note:
            For async initialization with remote data, use IndustryMatcher.create() instead.
        """
        if industries_data is None:
            industries_data = self._load_default_data_sync()
        
        self.industries = industries_data
        self._build_search_index()
    
    @classmethod
    async def create(cls, industries_data: list[dict[str, Any]] | None = None) -> "IndustryMatcher":
        """
        Create an IndustryMatcher instance asynchronously.
        
        Args:
            industries_data: List of industry dictionaries. If None, will load from package data.
        
        Returns:
            Initialized IndustryMatcher instance.
        """
        if industries_data is None:
            industries_data = await cls._load_default_data_async()
        
        instance = cls.__new__(cls)
        instance.industries = industries_data
        instance._build_search_index()
        return instance
    
    def _load_default_data_sync(self) -> list[dict[str, Any]]:
        """Load industry data synchronously from package resources or remote source."""
        # Try to load from package data first
        package_data_path = Path(__file__).parent / "data" / "industry_codes.json"
        
        if package_data_path.exists():
            with open(package_data_path, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("industries", [])
        
        # Fallback: Load from GitHub synchronously (blocking)
        # You can update this URL after setting up GitHub Actions
        try:
            response = httpx.get(
                "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/industry_codes.json",
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("industries", [])
        except Exception:
            # Return empty list if all else fails
            return []
    
    @staticmethod
    async def _load_default_data_async() -> list[dict[str, Any]]:
        """Load industry data asynchronously from package resources or remote source."""
        # Try to load from package data first
        package_data_path = Path(__file__).parent / "data" / "industry_codes.json"
        
        if package_data_path.exists():
            data = await asyncio.to_thread(
                lambda: json.load(open(package_data_path, encoding="utf-8"))
            )
            return data.get("industries", [])
        
        # Fallback: Load from GitHub asynchronously
        # You can update this URL after setting up GitHub Actions
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/industry_codes.json"
                )
                response.raise_for_status()
                data = response.json()
                return data.get("industries", [])
        except Exception:
            # Return empty list if all else fails
            return []
    
    def _build_search_index(self) -> None:
        """Build search index for efficient matching."""
        self.labels = [industry["label"] for industry in self.industries]
        self.hierarchies = [industry["hierarchy"] for industry in self.industries]
    
    async def find_closest(
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
        # Run CPU-intensive calculation in a thread pool
        return await asyncio.to_thread(
            self._find_closest_sync, query, top_n, search_field
        )
    
    def _find_closest_sync(
        self,
        query: str,
        top_n: int = 1,
        search_field: str = "label",
    ) -> list[dict[str, Any]]:
        """Synchronous implementation of find_closest for thread pool execution."""
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
            
            results.append({
                **industry,
                "similarity_score": similarity,
                "levenshtein_distance": distance,
            })
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return results[:top_n]
    
    async def find_closest_batch(
        self,
        queries: list[str],
        top_n: int = 1,
        search_field: str = "label",
    ) -> list[list[dict[str, Any]]]:
        """
        Find closest matches for multiple queries efficiently in parallel.
        
        Args:
            queries: List of search query strings.
            top_n: Number of top results to return per query.
            search_field: Field to search in ('label', 'hierarchy', or 'both').
        
        Returns:
            List of result lists, one for each query.
        """
        tasks = [
            self.find_closest(query, top_n, search_field)
            for query in queries
        ]
        return await asyncio.gather(*tasks)
    
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


# Convenience functions for simple use cases
async def get_closest_category(query: str, top_n: int = 1) -> list[dict[str, Any]]:
    """
    Find the closest matching LinkedIn industry category asynchronously.
    
    This is a convenience function that creates a matcher and returns results.
    For multiple queries, consider creating an IndustryMatcher instance instead.
    
    Args:
        query: The search query string.
        top_n: Number of top results to return.
    
    Returns:
        List of matched industries with similarity scores.
    
    Example:
        >>> results = await get_closest_category("software development")
        >>> print(results[0]["label"])
        >>> print(results[0]["similarity_score"])
    """
    matcher = await IndustryMatcher.create()
    return await matcher.find_closest(query, top_n=top_n)


async def get_closest_categories_batch(
    queries: list[str], 
    top_n: int = 1
) -> list[list[dict[str, Any]]]:
    """
    Find closest matches for multiple queries efficiently.
    
    This creates a single matcher instance and processes all queries in parallel.
    
    Args:
        queries: List of search query strings.
        top_n: Number of top results to return per query.
    
    Returns:
        List of result lists, one for each query.
    
    Example:
        >>> queries = ["software", "restaurant", "healthcare"]
        >>> results = await get_closest_categories_batch(queries)
        >>> for query, matches in zip(queries, results):
        ...     print(f"{query}: {matches[0]['label']}")
    """
    matcher = await IndustryMatcher.create()
    return await matcher.find_closest_batch(queries, top_n=top_n)

