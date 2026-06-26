"""
SmartBite Chatbot - Main Application
ML-based Malaysian restaurant chatbot using TF-IDF + LinearSVC for intent classification.
"""

import json
import os
import sys
import io
from typing import Any, Dict, List, Optional, Tuple

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from intent_classifier import IntentClassifier
from entity_extractor import EntityExtractor


class SmartBiteChatbot:
    """Main chatbot class that handles conversation flow."""

    def __init__(self, base_path: str):
        self.base_path = os.path.abspath(base_path)
        self.menu_data = self._load_menu()
        self.order: List[Dict[str, Any]] = []

        # Initialize ML components
        classifier_path = os.path.join(self.base_path, 'models', 'intent_classifier.pkl')
        training_data_path = os.path.join(self.base_path, 'data', 'training_data.json')
        menu_path = os.path.join(self.base_path, '..', 'shared', 'menu_data.json')

        self.classifier = IntentClassifier()
        if os.path.exists(classifier_path):
            self.classifier.load(classifier_path)
        else:
            print("[INFO] Training new model...")
            self.classifier.load_training_data(training_data_path)
            self.classifier.train()
            self.classifier.save(classifier_path)

        self.entity_extractor = EntityExtractor(menu_path)

    def _load_menu(self) -> Dict[str, Any]:
        """Load menu data."""
        menu_path = os.path.normpath(os.path.join(self.base_path, '..', 'shared', 'menu_data.json'))
        with open(menu_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_item_details(self, item_name: str) -> Optional[Dict[str, Any]]:
        """Get menu item details by name."""
        for item in self.menu_data['menu']:
            if item['name'].lower() == item_name.lower():
                return item
        return None

    def _format_order_summary(self) -> str:
        """Format current order as a summary."""
        if not self.order:
            return "Your order is empty. Would you like to order something?"

        lines = ["📋 **Your Order:**\n"]
        total = 0
        for i, item in enumerate(self.order, 1):
            subtotal = item['price'] * item['quantity']
            total += subtotal
            lines.append(f"{i}. {item['name']} x{item['quantity']} - RM{subtotal:.2f}")

        lines.append(f"\n💰 **Total: RM{total:.2f}**")
        return '\n'.join(lines)

    def _handle_greet(self, text: str, entities: Dict) -> str:
        return "Welcome to Warung SmartBite! 🍽️ Selamat datang! How can I help you today?\n\nYou can:\n- Browse our menu\n- Get recommendations\n- Place an order\n- Ask about hours, location, or reservations"

    def _handle_goodbye(self, text: str, entities: Dict) -> str:
        return "Thank you for visiting Warung SmartBite! Selamat jalan! See you again! 👋"

    def _handle_menu_browse(self, text: str, entities: Dict) -> str:
        category = entities.get('category')
        if category:
            items = [i for i in self.menu_data['menu'] if i['category'] == category]
            if items:
                lines = [f"🍽️ **{category.title()} Menu:**\n"]
                for item in items:
                    veg = " 🌿" if item['vegetarian'] else ""
                    spicy = " 🌶️" if item['spicy'] else ""
                    lines.append(f"- {item['name']}{spicy}{veg} - RM{item['price']:.2f}")
                    lines.append(f"  {item['description']}")
                return '\n'.join(lines)
            return f"Sorry, no items found in the {category} category."

        # Show full menu
        lines = ["🍽️ **Warung SmartBite Menu:**\n"]
        current_category = ""
        for item in self.menu_data['menu']:
            if item['category'] != current_category:
                current_category = item['category']
                lines.append(f"\n**{current_category.title()}:**")
            veg = " 🌿" if item['vegetarian'] else ""
            spicy = " 🌶️" if item['spicy'] else ""
            lines.append(f"  - {item['name']}{spicy}{veg} - RM{item['price']:.2f}")
        lines.append("\nWould you like to order something?")
        return '\n'.join(lines)

    def _handle_menu_ask_price(self, text: str, entities: Dict) -> str:
        food_item = entities.get('food_item')
        if food_item:
            item = self._get_item_details(food_item)
            if item:
                return f"💰 **{item['name']}** costs **RM{item['price']:.2f}**\n{item['description']}"
            return f"Sorry, I couldn't find '{food_item}' on our menu."

        # Show price list
        lines = ["💰 **Price List:**\n"]
        for item in self.menu_data['menu']:
            lines.append(f"- {item['name']}: RM{item['price']:.2f}")
        return '\n'.join(lines)

    def _handle_order_place(self, text: str, entities: Dict) -> str:
        food_item = entities.get('food_item')
        quantity = entities.get('quantity') or 1

        if food_item:
            item = self._get_item_details(food_item)
            if item:
                self.order.append({
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': quantity
                })
                total = sum(i['price'] * i['quantity'] for i in self.order)
                return (f"✅ Added to your order:\n"
                        f"**{item['name']}** x{quantity} - RM{item['price'] * quantity:.2f}\n\n"
                        f"💰 Current total: RM{total:.2f}\n\n"
                        f"Anything else you'd like to add?")
            return f"Sorry, '{food_item}' is not on our menu. Would you like to see the menu?"

        return "What would you like to order? You can say something like 'I want nasi lemak' or browse our menu first."

    def _handle_order_modify(self, text: str, entities: Dict) -> str:
        if not self.order:
            return "You don't have any items in your order yet. Would you like to order something?"

        food_item = entities.get('food_item')
        if food_item:
            # Check if item is in order
            for i, order_item in enumerate(self.order):
                if order_item['name'].lower() == food_item.lower():
                    if 'remove' in text.lower() or 'cancel' in text.lower():
                        removed = self.order.pop(i)
                        return f"❌ Removed **{removed['name']}** from your order.\n\n{self._format_order_summary()}"
                    else:
                        quantity = entities.get('quantity') or 1
                        self.order[i]['quantity'] = quantity
                        return f"✅ Updated **{order_item['name']}** quantity to {quantity}.\n\n{self._format_order_summary()}"

        return f"I couldn't find that item in your order.\n\n{self._format_order_summary()}"

    def _handle_order_cancel(self, text: str, entities: Dict) -> str:
        if not self.order:
            return "Your order is already empty."
        self.order.clear()
        return "❌ Your order has been cancelled. Would you like to start a new order?"

    def _handle_order_check(self, text: str, entities: Dict) -> str:
        return self._format_order_summary()

    def _handle_recommend(self, text: str, entities: Dict) -> str:
        items = self.menu_data['menu']

        # Filter based on preference
        preference = entities.get('preference')
        if preference == 'spicy':
            items = [i for i in items if i.get('spicy')]
            emoji = "🔥"
            label = "Spicy Picks"
        elif preference == 'vegetarian':
            items = [i for i in items if i.get('vegetarian')]
            emoji = "🌿"
            label = "Vegetarian Options"
        elif preference == 'budget':
            budget = entities.get('budget') or 10.0
            items = [i for i in items if i['price'] <= budget]
            emoji = "💰"
            label = f"Budget Options (under RM{budget:.0f})"
        else:
            # Default: popular/signature items
            items = [i for i in items if 'popular' in i.get('tags', []) or 'signature' in i.get('tags', [])]
            emoji = "⭐"
            label = "Top Picks"

        if not items:
            return f"Sorry, no items match your preference. Would you like to see our full menu?"

        # Limit to top 5
        items = items[:5]
        lines = [f"{emoji} **{label}:**\n"]
        for i, item in enumerate(items, 1):
            veg = " 🌿" if item['vegetarian'] else ""
            spicy = " 🌶️" if item['spicy'] else ""
            lines.append(f"{i}. {item['name']}{spicy}{veg} - RM{item['price']:.2f}")
            lines.append(f"   {item['description']}")

        lines.append("\nWould you like to order any of these?")
        return '\n'.join(lines)

    def _handle_dietary_info(self, text: str, entities: Dict) -> str:
        food_item = entities.get('food_item')
        if food_item:
            item = self._get_item_details(food_item)
            if item:
                lines = [f"ℹ️ **{item['name']} - Dietary Info:**\n"]
                lines.append(f"- Halal: ✅ Yes" if self.menu_data['restaurant']['halal'] else "- Halal: ❌ No")
                lines.append(f"- Vegetarian: {'✅ Yes' if item['vegetarian'] else '❌ No'}")
                lines.append(f"- Spicy: {'🌶️ Yes' if item['spicy'] else '❌ No'}")
                lines.append(f"- Price: RM{item['price']:.2f}")
                return '\n'.join(lines)

        return ("ℹ️ **Dietary Information:**\n\n"
                "- ✅ All food is HALAL certified\n"
                "- 🌶️ Spicy dishes are marked on the menu\n"
                "- 🌿 Vegetarian options available\n"
                "- ⚠️ Please inform us of any allergies!")

    def _handle_complaint_food(self, text: str, entities: Dict) -> str:
        return ("We're really sorry about that! 😔\n\n"
                "We take food quality seriously. Here's what we can do:\n"
                "- 🔄 Replace the dish immediately\n"
                "- 💰 Offer a discount on your next visit\n"
                "- 📝 Log your complaint for our kitchen team\n\n"
                "Please let our staff know, and we'll fix this right away!")

    def _handle_complaint_service(self, text: str, entities: Dict) -> str:
        return ("We apologize for the wait! 😔\n\n"
                "We'll look into this right away. Here's what we can do:\n"
                "- ⚡ Prioritize your order\n"
                "- 🎁 Offer a complimentary drink while you wait\n"
                "- 📝 Escalate to our manager\n\n"
                "Please let our staff know your order number.")

    def _handle_complaint_other(self, text: str, entities: Dict) -> str:
        return ("We're sorry about your experience! 😔\n\n"
                "We value your feedback and will address this immediately.\n"
                "Please let our manager know, and we'll do our best to make it right.\n\n"
                "Thank you for bringing this to our attention.")

    def _handle_ask_hours(self, text: str, entities: Dict) -> str:
        return ("🕐 **Operating Hours:**\n\n"
                "- Open daily: 10:00 AM - 10:00 PM\n"
                "- Last order: 9:30 PM\n"
                "- Open on weekends and public holidays")

    def _handle_ask_location(self, text: str, entities: Dict) -> str:
        return ("📍 **Location:**\n\n"
                "Warung SmartBite\n"
                "TARUMT Campus, Setapak\n"
                "53300 Kuala Lumpur\n\n"
                "Near the main entrance, ground floor!")

    def _handle_ask_reservation(self, text: str, entities: Dict) -> str:
        return ("📞 **Reservations:**\n\n"
                "- Walk-in: No reservation needed!\n"
                "- Groups of 8+: Please call +60 3-1234 5678\n"
                "- VIP room available for 15+ people\n"
                "- Private dining options available")

    def _handle_ask_payment(self, text: str, entities: Dict) -> str:
        return ("💳 **Payment Methods:**\n\n"
                "- Cash\n"
                "- Touch 'n Go\n"
                "- GrabPay\n"
                "- Debit/Credit Card (PayWave)\n"
                "- QR Payment")

    def _handle_thanks(self, text: str, entities: Dict) -> str:
        return "You're welcome! 😊 Anything else I can help with?"

    def _handle_default(self, text: str, entities: Dict) -> str:
        return ("I'm not sure I understand. 🤔\n\n"
                "You can:\n"
                "- Ask about our menu\n"
                "- Place an order\n"
                "- Get recommendations\n"
                "- Ask about hours, location, or reservations\n\n"
                "What would you like to do?")

    def process_message(self, user_input: str) -> str:
        """Process user input and return chatbot response."""
        # Classify intent
        intent, confidence = self.classifier.predict(user_input)

        # Extract entities
        entities = self.entity_extractor.extract_all(user_input)

        # Log for debugging
        print(f"[DEBUG] Input: {user_input}")
        print(f"[DEBUG] Intent: {intent} (confidence: {confidence:.2f})")
        print(f"[DEBUG] Entities: {entities}")

        # Route to handler
        handlers = {
            'greet': self._handle_greet,
            'goodbye': self._handle_goodbye,
            'menu_browse': self._handle_menu_browse,
            'menu_ask_price': self._handle_menu_ask_price,
            'order_place': self._handle_order_place,
            'order_modify': self._handle_order_modify,
            'order_cancel': self._handle_order_cancel,
            'order_check': self._handle_order_check,
            'recommend': self._handle_recommend,
            'recommend_spicy': self._handle_recommend,
            'recommend_vegetarian': self._handle_recommend,
            'recommend_budget': self._handle_recommend,
            'dietary_info': self._handle_dietary_info,
            'complaint_food': self._handle_complaint_food,
            'complaint_service': self._handle_complaint_service,
            'complaint_other': self._handle_complaint_other,
            'ask_hours': self._handle_ask_hours,
            'ask_location': self._handle_ask_location,
            'ask_reservation': self._handle_ask_reservation,
            'ask_payment': self._handle_ask_payment,
            'thanks': self._handle_thanks,
        }

        handler = handlers.get(intent, self._handle_default)
        response = handler(user_input, entities)

        # Add low confidence warning
        if confidence < 0.5:
            response = f"[I'm not very confident about this, but...]\n\n{response}"

        return response


def main():
    """Run chatbot in terminal mode."""
    # Go up two levels: chatbot/ -> member1_rasa/ -> restaurant_chatbot/
    base_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    chatbot = SmartBiteChatbot(base_path)

    print("=" * 50)
    print("🍽️  SmartBite Chatbot - Terminal Mode")
    print("=" * 50)
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye! 👋")
            break
        if not user_input:
            continue

        response = chatbot.process_message(user_input)
        print(f"\n🤖 SmartBite: {response}\n")


if __name__ == '__main__':
    main()
