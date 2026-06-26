"""
Custom Rasa Actions for Warung SmartBite Malaysian Restaurant Chatbot.

This module implements order management, menu browsing, dish recommendations,
and complaint handling actions for the restaurant chatbot.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectionDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# Resolve the path to menu_data.json relative to this file.
# Expected layout:  project_root/shared/menu_data.json
#                   project_root/member1_rasa/actions/actions.py
_MENU_DATA_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "shared", "menu_data.json")
)

# Budget thresholds used by ActionRecommendDish
_BUDGET_LOW = 6.00   # items priced at or below RM 6
_BUDGET_MID = 10.00  # items priced at or below RM 10


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_menu() -> List[Dict[str, Any]]:
    """Load menu items from the shared JSON data file.

    Returns:
        A list of menu item dictionaries.

    Raises:
        FileNotFoundError: If the menu data file cannot be located.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    if not os.path.isfile(_MENU_DATA_PATH):
        logger.error("Menu data file not found at: %s", _MENU_DATA_PATH)
        raise FileNotFoundError(f"Menu data not found: {_MENU_DATA_PATH}")

    with open(_MENU_DATA_PATH, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    return data.get("menu", [])


def _find_menu_item(item_name: str, menu: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Case-insensitive lookup of a menu item by name.

    Args:
        item_name: The item name to search for.
        menu: The list of menu item dicts.

    Returns:
        The matching menu item dict, or None if not found.
    """
    normalized = item_name.strip().lower()
    for item in menu:
        if item["name"].lower() == normalized:
            return item
    # Fuzzy fallback: check if the searched name is a substring of any item
    for item in menu:
        if normalized in item["name"].lower():
            return item
    return None


def _format_currency(amount: float) -> str:
    """Format a numeric amount as Malaysian Ringgit."""
    return f"RM {amount:.2f}"


# ---------------------------------------------------------------------------
# 1. ActionPlaceOrder
# ---------------------------------------------------------------------------

class ActionPlaceOrder(Action):
    """Add a food item to the customer's order.

    Reads the ``food_item`` and ``quantity`` slots, validates the item against
    the menu, appends it to the ``order_list`` slot, and responds with a
    confirmation including the running total.
    """

    def name(self) -> Text:
        return "action_place_order"

    def run(
        self,
        dispatcher: CollectionDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # -- Extract slots -------------------------------------------------------
        food_item: Optional[str] = tracker.get_slot("food_item")
        quantity_raw: Any = tracker.get_slot("quantity")

        if not food_item:
            dispatcher.utter_message(text="I didn't catch what you'd like to order. Could you tell me the item name?")
            return []

        # Default quantity to 1 when not provided or invalid
        try:
            quantity: int = max(1, int(float(str(quantity_raw))))
        except (TypeError, ValueError):
            quantity = 1

        # -- Load menu & validate ------------------------------------------------
        try:
            menu = _load_menu()
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I'm having trouble accessing our menu right now. Please try again later.")
            logger.exception("Failed to load menu data.")
            return []

        matched_item = _find_menu_item(food_item, menu)
        if matched_item is None:
            available_names = ", ".join(item["name"] for item in menu[:8])
            dispatcher.utter_message(
                text=(
                    f"Sorry, I couldn't find \"{food_item}\" on our menu. "
                    f"Here are some items we have: {available_names}..."
                )
            )
            return []

        # -- Build order entry ---------------------------------------------------
        price: float = matched_item["price"]
        order_entry = {
            "item": matched_item["name"],
            "quantity": quantity,
            "price": price,
        }

        # -- Update order_list slot ---------------------------------------------
        current_order: List[Dict[str, Any]] = tracker.get_slot("order_list") or []
        # Create a new list so Rasa detects the slot change
        updated_order = list(current_order)
        updated_order.append(order_entry)

        total = sum(entry["price"] * entry["quantity"] for entry in updated_order)

        dispatcher.utter_message(
            text=(
                f"Added {quantity}x {matched_item['name']} ({_format_currency(price)} each) "
                f"to your order.\n"
                f"Running total: {_format_currency(total)}"
            )
        )

        return [SlotSet("order_list", updated_order)]


# ---------------------------------------------------------------------------
# 2. ActionModifyOrder
# ---------------------------------------------------------------------------

class ActionModifyOrder(Action):
    """Modify an existing order entry.

    Supported modification intents / entity patterns:
      * "change X to Y"  -- replace item X with item Y (same quantity)
      * "remove X"       -- delete item X from the order
      * "add more X"     -- increase the quantity of item X
    The action inspects the ``modify_type`` and ``food_item`` slots (plus
    ``food_item_new`` for change operations) to determine the operation.
    """

    def name(self) -> Text:
        return "action_modify_order"

    def run(
        self,
        dispatcher: CollectionDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        modify_type: Optional[str] = tracker.get_slot("modify_type")
        food_item: Optional[str] = tracker.get_slot("food_item")
        food_item_new: Optional[str] = tracker.get_slot("food_item_new")
        quantity_raw: Any = tracker.get_slot("quantity")

        current_order: List[Dict[str, Any]] = tracker.get_slot("order_list") or []

        if not current_order:
            dispatcher.utter_message(text="You don't have any items in your order yet.")
            return []

        if not food_item:
            dispatcher.utter_message(text="Which item would you like to modify?")
            return []

        # Normalise for comparison
        target_lower = food_item.strip().lower()

        # Find the index of the target item in the order
        target_idx: Optional[int] = None
        for idx, entry in enumerate(current_order):
            if entry["item"].lower() == target_lower or target_lower in entry["item"].lower():
                target_idx = idx
                break

        if target_idx is None:
            item_names = ", ".join(e["item"] for e in current_order)
            dispatcher.utter_message(
                text=f"I couldn't find \"{food_item}\" in your current order. Your order has: {item_names}."
            )
            return []

        updated_order = list(current_order)  # shallow copy
        message = ""

        # -- REMOVE -------------------------------------------------------------
        if modify_type and modify_type.lower() in ("remove", "delete"):
            removed = updated_order.pop(target_idx)
            message = f"Removed {removed['item']} from your order."

        # -- CHANGE (replace with new item) -------------------------------------
        elif modify_type and modify_type.lower() in ("change", "replace", "swap"):
            if not food_item_new:
                dispatcher.utter_message(text="What would you like to change it to?")
                return []

            try:
                menu = _load_menu()
            except FileNotFoundError:
                dispatcher.utter_message(text="Sorry, I can't access the menu right now. Please try again later.")
                return []

            new_matched = _find_menu_item(food_item_new, menu)
            if new_matched is None:
                dispatcher.utter_message(text=f"Sorry, \"{food_item_new}\" is not on our menu.")
                return []

            old_item = updated_order[target_idx]["item"]
            old_qty = updated_order[target_idx]["quantity"]
            updated_order[target_idx] = {
                "item": new_matched["name"],
                "quantity": old_qty,
                "price": new_matched["price"],
            }
            message = f"Changed {old_item} to {new_matched['name']} (quantity: {old_qty})."

        # -- ADD MORE (increase quantity) ---------------------------------------
        elif modify_type and modify_type.lower() in ("add_more", "add more", "increase"):
            try:
                extra_qty: int = max(1, int(float(str(quantity_raw))))
            except (TypeError, ValueError):
                extra_qty = 1

            updated_order[target_idx]["quantity"] += extra_qty
            new_qty = updated_order[target_idx]["quantity"]
            message = f"Updated {updated_order[target_idx]['item']} quantity to {new_qty}."

        else:
            dispatcher.utter_message(
                text="I'm not sure what modification you'd like. You can say 'change', 'remove', or 'add more'."
            )
            return []

        # -- Recalculate total & respond ----------------------------------------
        total = sum(e["price"] * e["quantity"] for e in updated_order)
        dispatcher.utter_message(text=f"{message}\nYour updated total is {_format_currency(total)}.")

        return [SlotSet("order_list", updated_order)]


# ---------------------------------------------------------------------------
# 3. ActionCancelOrder
# ---------------------------------------------------------------------------

class ActionCancelOrder(Action):
    """Cancel the entire order by resetting the order_list slot."""

    def name(self) -> Text:
        return "action_cancel_order"

    def run(
        self,
        dispatcher: CollectionDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        current_order: List[Dict[str, Any]] = tracker.get_slot("order_list") or []

        if not current_order:
            dispatcher.utter_message(text="You don't have any items in your order to cancel.")
            return []

        dispatcher.utter_message(
            text="Your order has been cancelled. Feel free to start a new order anytime!"
        )

        return [SlotSet("order_list", [])]


# ---------------------------------------------------------------------------
# 4. ActionCheckOrder
# ---------------------------------------------------------------------------

class ActionCheckOrder(Action):
    """Display the current order as an itemized receipt."""

    def name(self) -> Text:
        return "action_check_order"

    def run(
        self,
        dispatcher: CollectionDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        current_order: List[Dict[str, Any]] = tracker.get_slot("order_list") or []

        if not current_order:
            dispatcher.utter_message(text="Your order is empty. Would you like to see our menu?")
            return []

        # Build a formatted receipt
        lines: List[str] = ["--- Your Order ---"]
        total = 0.0
        for idx, entry in enumerate(current_order, start=1):
            line_total = entry["price"] * entry["quantity"]
            total += line_total
            lines.append(
                f"  {idx}. {entry['item']} x{entry['quantity']}  =  {_format_currency(line_total)}"
            )

        lines.append("-------------------")
        lines.append(f"  Total: {_format_currency(total)}")

        dispatcher.utter_message(text="\n".join(lines))

        return []


# ---------------------------------------------------------------------------
# 5. ActionShowMenuByCategory
# ---------------------------------------------------------------------------

class ActionShowMenuByCategory(Action):
    """Show menu items filtered by a specific category.

    Recognised categories: rice, noodles, snacks, drinks, desserts.
    """

    # Map common synonyms / partial matches to canonical category names
    _CATEGORY_ALIASES: Dict[str, str] = {
        "rice": "rice",
        "nasi": "rice",
        "noodle": "noodles",
        "noodles": "noodles",
        "mee": "noodles",
        "mi": "noodles",
        "snack": "snacks",
        "snacks": "snacks",
        "starter": "snacks",
        "starters": "snacks",
        "appetizer": "snacks",
        "appetizers": "snacks",
        "drink": "drinks",
        "drinks": "drinks",
        "beverage": "drinks",
        "beverages": "drinks",
        "minuman": "drinks",
        "dessert": "desserts",
        "desserts": "desserts",
        "pencuci mulut": "desserts",
    }

    def name(self) -> Text:
        return "action_show_menu_by_category"

    def run(
        self,
        dispatcher: CollectionDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        category_raw: Optional[str] = tracker.get_slot("category")

        if not category_raw:
            dispatcher.utter_message(text="Which category are you interested in? We have: rice, noodles, snacks, drinks, and desserts.")
            return []

        # Normalize
        category_key = category_raw.strip().lower()
        canonical = self._CATEGORY_ALIASES.get(category_key)

        if canonical is None:
            dispatcher.utter_message(
                text=(
                    f"Sorry, I don't recognise the category \"{category_raw}\". "
                    "We have: rice, noodles, snacks, drinks, and desserts."
                )
            )
            return []

        try:
            menu = _load_menu()
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I can't access the menu right now.")
            return []

        items = [item for item in menu if item.get("category", "").lower() == canonical]

        if not items:
            dispatcher.utter_message(text=f"No items found in the \"{canonical}\" category.")
            return []

        lines = [f"--- {canonical.title()} Menu ---"]
        for item in items:
            veg_tag = " (V)" if item.get("vegetarian") else ""
            spicy_tag = " (Spicy)" if item.get("spicy") else ""
            lines.append(f"  - {item['name']}  {_format_currency(item['price'])}{veg_tag}{spicy_tag}")
            lines.append(f"    {item['description']}")

        dispatcher.utter_message(text="\n".join(lines))

        return []


# ---------------------------------------------------------------------------
# 6. ActionRecommendDish
# ---------------------------------------------------------------------------

class ActionRecommendDish(Action):
    """Recommend up to 5 dishes based on the customer's stated preference.

    Supported preference entities:
      * "spicy"      -- items marked spicy=True
      * "vegetarian" -- items marked vegetarian=True
      * "budget"     -- items priced at or below RM 6
      * "cheap"      -- alias for budget
      * "popular"    -- items tagged 'popular'
      * "signature"  -- items tagged 'signature'
    """

    def name(self) -> Text:
        return "action_recommend_dish"

    def run(
        self,
        dispatcher: CollectionDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        preference: Optional[str] = tracker.get_slot("preference")

        try:
            menu = _load_menu()
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I can't access the menu right now.")
            return []

        if not preference:
            # No preference given -- recommend popular items
            filtered = [i for i in menu if "popular" in i.get("tags", [])]
            label = "our most popular dishes"
        else:
            pref_lower = preference.strip().lower()
            filtered = []
            label = preference

            if pref_lower in ("spicy", "pedas"):
                filtered = [i for i in menu if i.get("spicy") is True]
                label = "spicy dishes"
            elif pref_lower in ("vegetarian", "vegan", "veg"):
                filtered = [i for i in menu if i.get("vegetarian") is True]
                label = "vegetarian dishes"
            elif pref_lower in ("budget", "cheap", "murah", "affordable"):
                filtered = [i for i in menu if i.get("price", 999) <= _BUDGET_LOW]
                label = "budget-friendly dishes"
            elif pref_lower in ("popular", "best", "favourite", "favorite"):
                filtered = [i for i in menu if "popular" in i.get("tags", [])]
                label = "popular dishes"
            elif pref_lower in ("signature", "special", "specialty"):
                filtered = [i for i in menu if "signature" in i.get("tags", [])]
                label = "signature dishes"
            elif pref_lower in ("healthy", "sihat"):
                filtered = [i for i in menu if "healthy" in i.get("tags", [])]
                label = "healthy dishes"
            else:
                # Generic keyword search across name, description, and tags
                for item in menu:
                    searchable = (
                        item["name"].lower()
                        + " " + item.get("description", "").lower()
                        + " " + " ".join(item.get("tags", [])).lower()
                    )
                    if pref_lower in searchable:
                        filtered.append(item)
                label = f"dishes matching '{preference}'"

        if not filtered:
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find any {label}. Would you like me to suggest our popular items instead?"
            )
            return []

        # Limit to top 5
        recommendations = filtered[:5]
        lines = [f"Here are my top recommendations for {label}:"]
        for idx, item in enumerate(recommendations, start=1):
            veg_tag = " (V)" if item.get("vegetarian") else ""
            spicy_tag = " (Spicy)" if item.get("spicy") else ""
            lines.append(
                f"  {idx}. {item['name']} - {_format_currency(item['price'])}{veg_tag}{spicy_tag}"
            )
            lines.append(f"     {item['description']}")

        dispatcher.utter_message(text="\n".join(lines))

        return []


# ---------------------------------------------------------------------------
# 7. ActionHandleComplaint
# ---------------------------------------------------------------------------

class ActionHandleComplaint(Action):
    """Handle customer complaints with empathy and actionable solutions.

    The action inspects the ``complaint_type`` slot to determine the nature of
    the complaint and offers an appropriate resolution.
    """

    # Possible complaint_type values and their responses
    _COMPLAINT_RESPONSES: Dict[str, Dict[str, str]] = {
        "food": {
            "apology": "I'm really sorry about the issue with your food. That's not the standard we aim for.",
            "solution": (
                "We'd like to make it right. We can:\n"
                "  1. Replace the dish immediately\n"
                "  2. Offer a 20% discount on your current order\n"
                "Which would you prefer?"
            ),
        },
        "service": {
            "apology": "I sincerely apologise for the service experience. Your comfort is our priority.",
            "solution": (
                "We take service quality seriously. We can:\n"
                "  1. Have our manager speak with you directly\n"
                "  2. Offer a complimentary drink or dessert\n"
                "How would you like to proceed?"
            ),
        },
        "other": {
            "apology": "I'm sorry to hear about your experience. We want every visit to be enjoyable.",
            "solution": (
                "I'd like to help resolve this. We can:\n"
                "  1. Escalate this to our manager for immediate attention\n"
                "  2. Note your feedback so we can improve\n"
                "What would you prefer?"
            ),
        },
    }

    def name(self) -> Text:
        return "action_handle_complaint"

    def run(
        self,
        dispatcher: CollectionDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        complaint_type: Optional[str] = tracker.get_slot("complaint_type")

        # Default to 'other' when type is missing or unrecognised
        ctype = (complaint_type or "other").strip().lower()
        if ctype not in self._COMPLAINT_RESPONSES:
            ctype = "other"

        response = self._COMPLAINT_RESPONSES[ctype]

        dispatcher.utter_message(text=response["apology"])
        dispatcher.utter_message(text=response["solution"])

        # Log the complaint for operational visibility
        sender_id = tracker.sender_id
        latest_message = tracker.latest_message.get("text", "")
        logger.warning(
            "COMPLAINT | type=%s | sender=%s | message=%s",
            ctype,
            sender_id,
            latest_message,
        )

        return [SlotSet("complaint_type", ctype)]
