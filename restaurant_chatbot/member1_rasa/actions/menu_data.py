"""
Utility module for loading and querying Malaysian restaurant menu data.

Provides functions for loading menu from JSON, fuzzy searching items,
filtering by category, dietary preferences, budget, and popularity.
"""

import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Dict, Optional, Any


# Path to the shared menu data JSON file
MENU_FILE_PATH = Path(__file__).parent.parent.parent / "shared" / "menu_data.json"

# Cached menu data
_cached_menu: Optional[Dict[str, Any]] = None


def load_menu(force_reload: bool = False) -> Dict[str, Any]:
    """
    Load menu from shared/menu_data.json.

    Uses caching to avoid repeated file reads. Pass force_reload=True
    to reload from disk.

    Args:
        force_reload: If True, bypass cache and reload from file.

    Returns:
        Dictionary containing menu data.

    Raises:
        FileNotFoundError: If menu file does not exist.
        json.JSONDecodeError: If menu file contains invalid JSON.
    """
    global _cached_menu

    if _cached_menu is not None and not force_reload:
        return _cached_menu

    if not MENU_FILE_PATH.exists():
        raise FileNotFoundError(f"Menu data file not found: {MENU_FILE_PATH}")

    with open(MENU_FILE_PATH, "r", encoding="utf-8") as f:
        _cached_menu = json.load(f)

    return _cached_menu


def _normalize(text: str) -> str:
    """Normalize text for case-insensitive comparison."""
    return text.strip().lower()


def _fuzzy_ratio(a: str, b: str) -> float:
    """Calculate fuzzy similarity ratio between two strings."""
    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()


def _all_items() -> List[Dict[str, Any]]:
    """Return all menu items as a flat list."""
    menu = load_menu()
    items = menu.get("items", [])
    # Handle case where menu is a list or has nested categories
    if isinstance(menu, list):
        return menu
    return items


def get_item_by_name(name: str, threshold: float = 0.6) -> Optional[Dict[str, Any]]:
    """
    Find a menu item by fuzzy name match.

    Args:
        name: The item name to search for.
        threshold: Minimum similarity ratio (0.0 to 1.0) to consider a match.
                   Default is 0.6.

    Returns:
        The best matching item dict, or None if no match above threshold.
    """
    items = _all_items()
    best_match = None
    best_score = 0.0

    for item in items:
        item_name = item.get("name", "")
        # Exact match (case-insensitive) always wins
        if _normalize(item_name) == _normalize(name):
            return item

        score = _fuzzy_ratio(name, item_name)
        if score > best_score and score >= threshold:
            best_score = score
            best_match = item

    return best_match


def get_items_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Filter menu items by category.

    Args:
        category: Category name to filter by (case-insensitive).

    Returns:
        List of items matching the category.
    """
    items = _all_items()
    normalized_cat = _normalize(category)

    return [
        item for item in items
        if _normalize(item.get("category", "")) == normalized_cat
    ]


def get_spicy_items() -> List[Dict[str, Any]]:
    """
    Return all spicy menu items.

    Checks for 'spicy' field being True, or 'spicy' in tags,
    or spice level indicators.

    Returns:
        List of spicy items.
    """
    items = _all_items()
    spicy_items = []

    for item in items:
        # Check boolean spicy field
        if item.get("spicy") is True:
            spicy_items.append(item)
            continue

        # Check tags for spicy indicator
        tags = item.get("tags", [])
        if any("spicy" in _normalize(tag) for tag in tags):
            spicy_items.append(item)
            continue

        # Check spice_level field
        spice_level = item.get("spice_level", "")
        if spice_level and _normalize(spice_level) not in ("none", "mild", "0", "no"):
            spicy_items.append(item)

    return spicy_items


def get_vegetarian_items() -> List[Dict[str, Any]]:
    """
    Return all vegetarian menu items.

    Checks for 'vegetarian' field being True, or 'vegetarian'/'vegan' in tags.

    Returns:
        List of vegetarian items.
    """
    items = _all_items()
    veg_items = []

    for item in items:
        # Check boolean vegetarian/vegan fields
        if item.get("vegetarian") is True or item.get("vegan") is True:
            veg_items.append(item)
            continue

        # Check tags for vegetarian/vegan indicators
        tags = item.get("tags", [])
        if any(
            _normalize(tag) in ("vegetarian", "vegan", "veg")
            for tag in tags
        ):
            veg_items.append(item)
            continue

        # Check dietary field
        dietary = item.get("dietary", [])
        if isinstance(dietary, list) and any(
            "veg" in _normalize(d) for d in dietary
        ):
            veg_items.append(item)

    return veg_items


def get_budget_items(max_price: float = 10.0) -> List[Dict[str, Any]]:
    """
    Return menu items under the specified budget.

    Args:
        max_price: Maximum price threshold. Default is 10.0.

    Returns:
        List of items with price less than or equal to max_price.
    """
    items = _all_items()
    budget_items = []

    for item in items:
        price = item.get("price")
        if price is not None:
            try:
                if float(price) <= max_price:
                    budget_items.append(item)
            except (ValueError, TypeError):
                continue

    return budget_items


def get_popular_items() -> List[Dict[str, Any]]:
    """
    Return popular or signature menu items.

    Checks for 'popular' or 'signature' in tags, or boolean
    'popular'/'signature' fields.

    Returns:
        List of popular/signature items.
    """
    items = _all_items()
    popular_items = []

    for item in items:
        # Check boolean fields
        if item.get("popular") is True or item.get("signature") is True:
            popular_items.append(item)
            continue

        # Check tags for popular/signature indicators
        tags = item.get("tags", [])
        if any(
            _normalize(tag) in ("popular", "signature", "bestseller", "best_seller", "recommended")
            for tag in tags
        ):
            popular_items.append(item)

    return popular_items


def get_item_price(name: str) -> Optional[float]:
    """
    Get the price of a specific menu item by name.

    Uses fuzzy matching to find the item.

    Args:
        name: The item name to look up.

    Returns:
        Price as a float, or None if item not found or has no price.
    """
    item = get_item_by_name(name)
    if item is None:
        return None

    price = item.get("price")
    if price is not None:
        try:
            return float(price)
        except (ValueError, TypeError):
            return None

    return None


def search_items(query: str, threshold: float = 0.3) -> List[Dict[str, Any]]:
    """
    Fuzzy search across all menu items.

    Searches item names, descriptions, categories, and tags.
    Returns items sorted by relevance (best match first).

    Args:
        query: Search query string.
        threshold: Minimum similarity ratio to include in results.
                   Default is 0.3.

    Returns:
        List of matching items sorted by relevance (descending).
    """
    items = _all_items()
    normalized_query = _normalize(query)
    scored_items = []

    for item in items:
        # Calculate the best score across multiple fields
        scores = []

        # Match against name (highest weight)
        name = item.get("name", "")
        if name:
            scores.append(_fuzzy_ratio(query, name) * 1.0)

        # Match against description
        description = item.get("description", "")
        if description:
            scores.append(_fuzzy_ratio(query, description) * 0.7)

        # Match against category
        category = item.get("category", "")
        if category:
            scores.append(_fuzzy_ratio(query, category) * 0.5)

        # Match against tags
        tags = item.get("tags", [])
        for tag in tags:
            scores.append(_fuzzy_ratio(query, tag) * 0.6)

        # Match against ingredients
        ingredients = item.get("ingredients", [])
        if isinstance(ingredients, list):
            for ingredient in ingredients:
                scores.append(_fuzzy_ratio(query, ingredient) * 0.5)

        # Use the best score for this item
        best_score = max(scores) if scores else 0.0

        # Also check for substring matches (case-insensitive)
        # This helps with partial keyword searches
        if normalized_query in _normalize(name):
            best_score = max(best_score, 0.8)
        if normalized_query in _normalize(description):
            best_score = max(best_score, 0.6)
        if any(normalized_query in _normalize(tag) for tag in tags):
            best_score = max(best_score, 0.7)

        if best_score >= threshold:
            scored_items.append((best_score, item))

    # Sort by score descending
    scored_items.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in scored_items]
