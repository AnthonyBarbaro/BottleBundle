# bundler.py

import itertools
import math

def generate_bundles(bottles: list[dict], existing_bundles: set) -> list[dict]:
    """
    Creates a list of new bundle dicts from 'bottles'.
    Each bundle has keys: name, price, bottles (list of 2 bottle dicts).
    Priority:
       1) same brand
       2) price difference < 10
    Avoid duplicates by checking 'name' in 'existing_bundles'.
    """
    new_bundles = []

    # Group by brand
    brand_map = {}
    for b in bottles:
        brand_map.setdefault(b['brand'].lower(), []).append(b)

    # Step 1: brand combos
    for brand, group_bottles in brand_map.items():
        # Generate all 2-combinations
        for combo in itertools.combinations(group_bottles, 2):
            b1, b2 = combo
            bundle_name = f"{b1['name']} & {b2['name']}"
            if bundle_name in existing_bundles:
                continue

            # Price is sum minus $5, but round to .99
            combined_price = (b1['price'] + b2['price']) - 5
            price_rounded = round_to_99(combined_price)

            new_bundles.append({
                'name': bundle_name,
                'price': price_rounded,
                'bottles': [b1, b2]
            })

    # Step 2: cross-brand combos within price range (optional)
    # This is an example: pair any 2 if within a certain difference, e.g. $10
    cross_brand_pairs = list(itertools.combinations(bottles, 2))
    for b1, b2 in cross_brand_pairs:
        # skip if same brand (handled above)
        if b1['brand'].lower() == b2['brand'].lower():
            continue
        price_diff = abs(b1['price'] - b2['price'])
        if price_diff <= 10:
            bundle_name = f"{b1['name']} & {b2['name']}"
            if bundle_name in existing_bundles:
                continue

            combined_price = (b1['price'] + b2['price']) - 5
            price_rounded = round_to_99(combined_price)

            new_bundles.append({
                'name': bundle_name,
                'price': price_rounded,
                'bottles': [b1, b2]
            })

    return new_bundles

def round_to_99(price: float) -> float:
    """
    Takes a float price and rounds up/down so it ends in .99
    E.g. 194.98 -> 194.99, 131.40 -> 131.99, 99.1 -> 99.99
    """
    integer_part = math.floor(price)
    decimal_part = price - integer_part

    # If decimal_part < .99, push it to .99
    if decimal_part < 0.99:
        return float(f"{integer_part}.99")
    else:
        # e.g. 12.992 -> 13.99
        return float(f"{integer_part + 1}.99")
