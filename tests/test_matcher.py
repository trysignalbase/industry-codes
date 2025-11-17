"""Tests for industry_codes package (async version)."""

import pytest
from industry_codes import IndustryMatcher, get_closest_category


@pytest.mark.asyncio
async def test_get_closest_category():
    """Test the async convenience function."""
    results = await get_closest_category("software", top_n=1)
    assert len(results) == 1
    assert "label" in results[0]
    assert "industry_id" in results[0]
    assert "similarity_score" in results[0]


@pytest.mark.asyncio
async def test_industry_matcher_async_creation():
    """Test IndustryMatcher async creation with GitHub download."""
    matcher = await IndustryMatcher.create()
    assert matcher.industries is not None


def test_industry_matcher_requires_data():
    """Test IndustryMatcher requires data when initialized directly."""
    # Should work with data
    matcher = IndustryMatcher(
        [
            {
                "industry_id": 1,
                "label": "Test",
                "hierarchy": "Test",
                "description": "Test",
                "category": "Test",
                "subcategories": [],
                "depth": 1,
            }
        ]
    )
    assert matcher.industries is not None

    # Should work with empty list
    matcher = IndustryMatcher([])
    assert len(matcher.industries) == 0


@pytest.mark.asyncio
async def test_find_closest():
    """Test find_closest method."""
    matcher = await IndustryMatcher.create()
    results = matcher.find_closest("technology", top_n=3)

    assert len(results) <= 3
    assert all("similarity_score" in r for r in results)
    assert results[0]["similarity_score"] >= results[-1]["similarity_score"]


def test_get_all_categories():
    """Test get_all_categories method."""
    # Create with dummy data
    dummy_data = [
        {
            "industry_id": 1,
            "label": "Test1",
            "hierarchy": "Cat1",
            "description": "Test",
            "category": "Cat1",
            "subcategories": [],
            "depth": 1,
        },
        {
            "industry_id": 2,
            "label": "Test2",
            "hierarchy": "Cat2",
            "description": "Test",
            "category": "Cat2",
            "subcategories": [],
            "depth": 1,
        },
    ]
    matcher = IndustryMatcher(dummy_data)
    categories = matcher.get_all_categories()

    assert isinstance(categories, list)
    assert len(categories) > 0
    assert all(isinstance(c, str) for c in categories)


def test_find_by_category():
    """Test find_by_category method."""
    dummy_data = [
        {
            "industry_id": 1,
            "label": "Test1",
            "hierarchy": "Cat1",
            "description": "Test",
            "category": "Cat1",
            "subcategories": [],
            "depth": 1,
        },
        {
            "industry_id": 2,
            "label": "Test2",
            "hierarchy": "Cat2",
            "description": "Test",
            "category": "Cat2",
            "subcategories": [],
            "depth": 1,
        },
    ]
    matcher = IndustryMatcher(dummy_data)
    results = matcher.find_by_category("Cat1")
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["label"] == "Test1"


@pytest.mark.asyncio
async def test_similarity_score_range():
    """Test that similarity scores are in valid range."""
    matcher = await IndustryMatcher.create()
    results = matcher.find_closest("test query", top_n=5)

    for result in results:
        score = result["similarity_score"]
        assert 0 <= score <= 1, f"Similarity score {score} out of range"


@pytest.mark.asyncio
async def test_search_fields():
    """Test different search field options."""
    matcher = await IndustryMatcher.create()

    query = "software"

    # Test each search field
    for field in ["label", "hierarchy", "both"]:
        results = matcher.find_closest(query, top_n=1, search_field=field)
        assert len(results) == 1
        assert "similarity_score" in results[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
