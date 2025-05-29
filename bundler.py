# bundler.py

import itertools
import math
import re
def generate_bundles(bottles: list[dict], existing_bundles: set, max_bundles=10) -> list[dict]:
    """
    Creates a list of new bundle dicts from 'bottles' (only 750ml or 1.5L).
    Each bundle:
       - name: e.g. "BottleA & BottleB"
       - price: (sum - 5) -> round to .99
       - bottles: [dict, dict]

    Priority:
      1) same brand combos
      2) cross-brand combos within a $10 price difference

    We skip duplicates in 'existing_bundles'.
    We then sort by price descending and limit to 'max_bundles'.
    """

    # 1) Filter bottles by valid volume (750 ml or 1500 ml).
    valid_bottles = []
    for b in bottles:
        vol = extract_volume(b['name']) or extract_volume(b['brand'])
        if vol in (750, 1500):
            valid_bottles.append(b)
    if not valid_bottles:
        print("[!] No valid bottles found (750ml or 1.5L). No bundles generated.")
        return []

    # 2) Generate brand combos
    brand_map = {}
    for b in valid_bottles:
        brand_map.setdefault(b['brand'].lower(), []).append(b)

    all_bundles = []
    for brand, group_bottles in brand_map.items():
        for b1, b2 in itertools.combinations(group_bottles, 2):
            bundle_name = f"{b1['name']} & {b2['name']}"
            if bundle_name in existing_bundles:
                continue
            combined_price = (b1['price'] + b2['price']) - 5
            price_rounded = round_to_99(combined_price)

            all_bundles.append({
                'name': bundle_name,
                'price': price_rounded,
                'bottles': [b1, b2]
            })

    # 3) Cross-brand combos (price difference <= $10)
    for b1, b2 in itertools.combinations(valid_bottles, 2):
        if b1['brand'].lower() == b2['brand'].lower():
            continue
        price_diff = abs(b1['price'] - b2['price'])
        if price_diff <= 10:
            bundle_name = f"{b1['name']} & {b2['name']}"
            if bundle_name in existing_bundles:
                continue
            combined_price = (b1['price'] + b2['price']) - 5
            price_rounded = round_to_99(combined_price)

            all_bundles.append({
                'name': bundle_name,
                'price': price_rounded,
                'bottles': [b1, b2]
            })

    # 4) Sort by price descending
    all_bundles.sort(key=lambda b: b['price'], reverse=True)

    # 5) Keep only top N bundles
    limited_bundles = all_bundles[:max_bundles]

    print(f"[i] After filtering volumes (750ml or 1.5L), we found {len(valid_bottles)} bottles.")
    print(f"[i] Generated {len(all_bundles)} combos, returning top {len(limited_bundles)} bundles.")
    return limited_bundles
def extract_volume(bottle_name: str) -> int:
    """
    Return bottle volume in millilitres:

    • '750 ml' or implicit/blank  →  750  
    • '1.5 L'                     → 1500  
    • '1.75 L'                    → 1750  
    • Anything else               → 0
    """
    text = bottle_name.lower()

    # explicit patterns first
    pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(ml|l)')
    m = pattern.search(text)
    if m:
        vol_str, unit = m.groups()
        vol = float(vol_str)
        return int(vol) if unit == 'ml' else int(vol * 1000)

    # no explicit volume found  →  assume standard 750 ml
    return 750
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
