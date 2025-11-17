"""Example usage scripts for linkedin-industry-codes (async version)."""

import asyncio
import time

from linkedin_industry_codes import (
    IndustryMatcher,
    get_closest_categories_batch,
    get_closest_category,
)


async def example_simple_search():
    """Example: Simple search using convenience function."""
    print("Example 1: Simple Search (Async)")
    print("-" * 60)

    query = "software development"
    results = await get_closest_category(query, top_n=3)

    print(f"Searching for: '{query}'")
    print("\nTop 3 matches:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['label']}")
        print(f"   Industry ID: {result['industry_id']}")
        print(f"   Hierarchy: {result['hierarchy']}")
        print(f"   Similarity: {result['similarity_score']:.2%}")
        print(f"   Description: {result['description'][:100]}...")


async def example_batch_search():
    """Example: Batch search using IndustryMatcher."""
    print("\n\nExample 2: Batch Search (Async)")
    print("-" * 60)

    # Create a matcher instance asynchronously (loads data once)
    matcher = await IndustryMatcher.create()

    queries = [
        "artificial intelligence",
        "restaurant",
        "cyber security",
        "renewable energy",
    ]

    # Process queries in parallel
    start_time = time.time()
    results_list = await matcher.find_closest_batch(queries, top_n=1)
    elapsed = time.time() - start_time

    for query, results in zip(queries, results_list):
        if results:
            result = results[0]
            print(f"\n'{query}' → {result['label']}")
            print(f"  Similarity: {result['similarity_score']:.2%}")

    print(f"\n⚡ Processed {len(queries)} queries in {elapsed:.3f}s")


async def example_batch_convenience():
    """Example: Batch search using convenience function."""
    print("\n\nExample 3: Batch Search with Convenience Function")
    print("-" * 60)

    queries = [
        "fintech",
        "healthcare",
        "e-commerce",
        "manufacturing",
        "education",
    ]

    start_time = time.time()
    results_list = await get_closest_categories_batch(queries, top_n=1)
    elapsed = time.time() - start_time

    print("Batch results:")
    for query, results in zip(queries, results_list):
        if results:
            print(f"  {query:20} → {results[0]['label']}")

    print(f"\n⚡ Processed {len(queries)} queries in {elapsed:.3f}s")


async def example_category_search():
    """Example: Search by category."""
    print("\n\nExample 4: Browse by Category")
    print("-" * 60)

    matcher = await IndustryMatcher.create()

    # Get all categories
    categories = matcher.get_all_categories()
    print(f"Total categories: {len(categories)}")
    print(f"\nFirst 5 categories: {categories[:5]}")

    # Get all industries in a specific category
    category_name = "Technology, Information and Internet"
    industries = matcher.find_by_category(category_name)
    print(f"\n\nIndustries in '{category_name}':")
    for ind in industries[:5]:  # Show first 5
        print(f"  • {ind['label']} (ID: {ind['industry_id']})")


async def example_hierarchical_search():
    """Example: Search in hierarchy."""
    print("\n\nExample 5: Hierarchical Search (Async)")
    print("-" * 60)

    matcher = await IndustryMatcher.create()

    # Search in hierarchy field
    query = "Accommodation Services > Food"
    results = await matcher.find_closest(query, top_n=5, search_field="hierarchy")

    print(f"Searching in hierarchy for: '{query}'")
    print("\nTop matches:")
    for result in results:
        print(f"\n• {result['label']}")
        print(f"  Hierarchy: {result['hierarchy']}")
        print(f"  Similarity: {result['similarity_score']:.2%}")


async def example_parallel_searches():
    """Example: Multiple parallel searches."""
    print("\n\nExample 6: Parallel Searches")
    print("-" * 60)

    matcher = await IndustryMatcher.create()

    # Run multiple different searches in parallel
    queries = [
        ("tech", "label"),
        ("Accommodation", "hierarchy"),
        ("software", "both"),
    ]

    tasks = [
        matcher.find_closest(query, top_n=1, search_field=field)
        for query, field in queries
    ]

    start_time = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start_time

    for (query, field), result in zip(queries, results):
        if result:
            print(f"\nQuery: '{query}' (field: {field})")
            print(f"  → {result[0]['label']}")
            print(f"  Score: {result[0]['similarity_score']:.2%}")

    print(f"\n⚡ Completed {len(queries)} parallel searches in {elapsed:.3f}s")


async def main():
    """Run all examples."""
    print("=" * 60)
    print("LinkedIn Industry Codes - Async Examples")
    print("=" * 60)

    await example_simple_search()
    await example_batch_search()
    await example_batch_convenience()
    await example_category_search()
    await example_hierarchical_search()
    await example_parallel_searches()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
