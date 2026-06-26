"""
Entity Extractor for SmartBite Chatbot.
Extracts food items, categories, quantities, preferences, and budget from user input.
Uses pattern matching and fuzzy string matching.
"""

import json
import os
import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple


class EntityExtractor:
    """Extract entities from user input using pattern matching and fuzzy matching."""

    def __init__(self, menu_path: str):
        self.menu_items: List[Dict[str, Any]] = []
        self.item_names: List[str] = []
        self.categories: List[str] = []
        self._load_menu(menu_path)

    def _load_menu(self, path: str) -> None:
        """Load menu data from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.menu_items = data['menu']
        self.item_names = [item['name'].lower() for item in self.menu_items]
        self.categories = list(set(item['category'] for item in self.menu_items))

    def _fuzzy_match(self, query: str, candidates: List[str], threshold: float = 0.6) -> Optional[str]:
        """Find the best fuzzy match for a query string."""
        query = query.lower().strip()
        best_match = None
        best_score = 0

        for candidate in candidates:
            # Exact substring match
            if query in candidate or candidate in query:
                return candidate

            # SequenceMatcher ratio
            score = SequenceMatcher(None, query, candidate).ratio()
            if score > best_score and score >= threshold:
                best_score = score
                best_match = candidate

        return best_match

    def extract_food_item(self, text: str) -> Optional[str]:
        """Extract food item from text."""
        text_lower = text.lower()

        # Try exact match first
        for item_name in self.item_names:
            if item_name in text_lower:
                return item_name.title()

        # Try fuzzy match on words
        words = text_lower.split()
        for i in range(len(words)):
            for j in range(i + 1, min(i + 4, len(words) + 1)):
                phrase = ' '.join(words[i:j])
                match = self._fuzzy_match(phrase, self.item_names, threshold=0.7)
                if match:
                    return match.title()

        return None

    def extract_category(self, text: str) -> Optional[str]:
        """Extract menu category from text."""
        text_lower = text.lower()

        category_keywords = {
            'rice': ['rice', 'nasi'],
            'noodles': ['noodle', 'noodles', 'mee', 'laksa', 'kuey teow'],
            'snacks': ['snack', 'snacks', 'roti', 'satay', 'popiah', 'curry puff', 'pisang'],
            'drinks': ['drink', 'drinks', 'beverage', 'beverages', 'teh', 'kopi', 'milo', 'air'],
            'desserts': ['dessert', 'desserts', 'sweet', 'sweets', 'cendol', 'ais kacang', 'kuih']
        }

        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category

        return None

    def extract_quantity(self, text: str) -> Optional[int]:
        """Extract quantity from text."""
        text_lower = text.lower()

        # Number words
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'a': 1, 'an': 1, 'single': 1, 'double': 2, 'triple': 3
        }

        for word, num in number_words.items():
            if re.search(rf'\b{word}\b', text_lower):
                return num

        # Numeric digits
        match = re.search(r'\b(\d+)\b', text_lower)
        if match:
            return int(match.group(1))

        return None

    def extract_preference(self, text: str) -> Optional[str]:
        """Extract preference (spicy, vegetarian, budget) from text."""
        text_lower = text.lower()

        preference_keywords = {
            'spicy': ['spicy', 'hot', 'pedas', 'chili', 'sambal', 'fiery'],
            'vegetarian': ['vegetarian', 'vegan', 'veggie', 'no meat', 'plant-based', 'meat-free'],
            'budget': ['cheap', 'budget', 'affordable', 'economical', 'inexpensive', 'value']
        }

        for preference, keywords in preference_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return preference

        return None

    def extract_budget(self, text: str) -> Optional[float]:
        """Extract budget amount from text."""
        text_lower = text.lower()

        # Match "under RM10" or "below RM15"
        match = re.search(r'(?:under|below|less than|max|maximum)\s*(?:rm)?(\d+(?:\.\d+)?)', text_lower)
        if match:
            return float(match.group(1))

        # Match "RM10" or "rm 10"
        match = re.search(r'rm\s*(\d+(?:\.\d+)?)', text_lower)
        if match:
            return float(match.group(1))

        return None

    def extract_all(self, text: str) -> Dict[str, Optional[Any]]:
        """Extract all entities from text."""
        return {
            'food_item': self.extract_food_item(text),
            'category': self.extract_category(text),
            'quantity': self.extract_quantity(text),
            'preference': self.extract_preference(text),
            'budget': self.extract_budget(text)
        }


if __name__ == '__main__':
    # Demo
    menu_path = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'menu_data.json')
    extractor = EntityExtractor(menu_path)

    test_inputs = [
        "I want nasi lemak",
        "show me rice dishes",
        "two roti canai please",
        "something spicy",
        "under RM10 options",
        "I'll have 3 satay"
    ]

    for text in test_inputs:
        entities = extractor.extract_all(text)
        print(f"\nInput: {text}")
        print(f"Entities: {entities}")
