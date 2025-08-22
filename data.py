import json
import os

# Default menu data structure - now only stores base prices
DEFAULT_MENU = {
    "Coffee": {
        "Americano": 2.50,
        "Latte": 3.00,
        "Cappuccino": 3.00,
        "Espresso": 2.00
    },
    "Tea": {
        "Green Tea": 2.00,
        "Black Tea": 2.00,
        "Chai Latte": 3.00,
        "Herbal Tea": 2.50
    },
    "Smoothie": {
        "Mango Berry": 4.50,
        "Strawberry Banana": 4.50,
        "Tropical Blend": 5.00,
        "Matcha Fusion": 5.50
    }
}


SIZE_MODIFIERS = {
    "Small": 0,
    "Medium": 50,
    "Large": 100
}

ADDON_PRICES = {
    "Syrup": 300,
    "Extra shot": 500,
    "Soy Milk": 400,
    "Almond Milk": 400
}


DATA_FILE = "menu_data.json"


def load_menu_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                data = json.load(file)
                # Validate the loaded data structure
                if isinstance(data, dict) and all(isinstance(v, dict) for v in data.values()):
                    return data
                else:
                    print("Invalid data structure, using default menu")
                    return DEFAULT_MENU
        except (json.JSONDecodeError, FileNotFoundError, TypeError) as e:
            print(f"Error loading menu data: {e}, using default menu")
            return DEFAULT_MENU
    return DEFAULT_MENU


def get_item_prices(category, item_name):
    """Get prices for all sizes of a specific item"""
    base_price = get_item_base_price(category, item_name)
    size_modifiers = get_size_modifiers()

    prices = {}
    for size, modifier in size_modifiers.items():
        # Calculate price for each size (base price + size modifier)
        total_price = base_price + (modifier / 100)  # Convert cents to dollars
        prices[size] = total_price

    return prices


def save_menu_data(menu_data):
    """Save menu data to file with proper error handling"""
    try:
        # Validate data structure before saving
        if not isinstance(menu_data, dict):
            raise ValueError("Menu data must be a dictionary")

        for category, items in menu_data.items():
            if not isinstance(items, dict):
                raise ValueError(
                    f"Category {category} must contain a dictionary of items")

        with open(DATA_FILE, 'w') as file:
            json.dump(menu_data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving menu data: {e}")
        return False


def get_categories():
    """Get all available categories"""
    menu_data = load_menu_data()
    return list(menu_data.keys())


def get_items_by_category(category):
    """Get all items in a specific category"""
    menu_data = load_menu_data()
    return list(menu_data.get(category, {}).keys())


def get_item_base_price(category, item_name):
    """Get base price for a specific item"""
    menu_data = load_menu_data()
    return menu_data.get(category, {}).get(item_name, 0)


def calculate_item_price(base_price, size, addons):
    """Calculate total price based on base price, size, and addons"""
    # Convert base price to cents
    total_cents = int(base_price * 100)

    # Add size modifier
    total_cents += SIZE_MODIFIERS.get(size, 0)

    # Add addon prices
    for addon in addons:
        total_cents += ADDON_PRICES.get(addon, 0)

    # Convert back to dollars
    return total_cents / 100


def get_size_modifiers():
    """Get available size modifiers"""
    return SIZE_MODIFIERS


def get_addon_prices():
    """Get available addon prices"""
    return ADDON_PRICES


def add_menu_item(category, item_name, base_price):
    """Add a new menu item with base price only"""
    menu_data = load_menu_data()

    if category not in menu_data:
        menu_data[category] = {}

    menu_data[category][item_name] = float(base_price)
    save_menu_data(menu_data)
    return True


def update_menu_item(category, item_name, base_price):
    """Update an existing menu item's base price"""
    menu_data = load_menu_data()

    if category in menu_data and item_name in menu_data[category]:
        menu_data[category][item_name] = float(base_price)
        save_menu_data(menu_data)
        return True
    return False


def delete_menu_item(category, item_name):
    """Delete a menu item"""
    menu_data = load_menu_data()

    if category in menu_data and item_name in menu_data[category]:
        del menu_data[category][item_name]
        # Remove category if it's empty
        if not menu_data[category]:
            del menu_data[category]
        save_menu_data(menu_data)
        return True
    return False


def get_all_items():
    """Get all items across all categories"""
    menu_data = load_menu_data()
    all_items = []

    for category, items in menu_data.items():
        for item_name, base_price in items.items():
            all_items.append({
                "category": category,
                "name": item_name,
                "base_price": base_price
            })

    return all_items


def debug_menu_data():
    """Debug function to check current menu data"""
    menu_data = load_menu_data()
    print("Current Menu Data:")
    print(json.dumps(menu_data, indent=2))
    return menu_data
