# bundler.py
# ---------------------------------------------------------------
# Build + rank liquor-bottle bundles, using GPT to score synergy.
# ---------------------------------------------------------------

import itertools, math, re, json, os, time
from ai_matcher import score_pair        # ← your GPT 0-100 scorer

# ----------------------------------------------------------------
# ❶  Simple on-disk cache so we don’t pay twice for the same pair
# ----------------------------------------------------------------
_CACHE_FILE = "ai_bundle_scores.json"
if os.path.exists(_CACHE_FILE):
    with open(_CACHE_FILE, "r", encoding="utf-8") as f:
        _SCORE_CACHE: dict[str, float] = json.load(f)
else:
    _SCORE_CACHE = {}

# ----------------------------------------------------------------
# ❷  Public function: generate_bundles
# ----------------------------------------------------------------
def generate_bundles(
    bottles: list[dict],
    existing_bundles: set,
    max_bundles: int = 10
) -> list[dict]:
    """
    Return up to `max_bundles` high-quality bundles.

    • Only bottles of 750 ml, 1.5 L (1500 ml), or 1.75 L (1750 ml)
    • Same-brand pairs first, then cross-brand pairs (≤ $10 price diff)
    • Price = (sum − $5) → rounded to .99
    • AI ranks bundles (0-100), then we keep the top `max_bundles`
    """

    # 1) size filter -------------------------------------------------
    valid = [
        b for b in bottles
        if (v := extract_volume(b["name"]) or extract_volume(b["brand"]))
           in (750, 1500, 1750)
    ]
    if not valid:
        print("[!] No valid bottles (750 ml | 1.5 L | 1.75 L).")
        return []

    # 2) generate candidate bundles ---------------------------------
    brand_map: dict[str, list] = {}
    for b in valid:
        brand_map.setdefault(b["brand"].lower(), []).append(b)

    combos: list[dict] = []

    # 2-A same-brand
    for group in brand_map.values():
        for b1, b2 in itertools.combinations(group, 2):
            _add_combo(b1, b2, combos, existing_bundles)

    # 2-B cross-brand (price diff ≤ $10)
    for b1, b2 in itertools.combinations(valid, 2):
        if b1["brand"].lower() == b2["brand"].lower():
            continue
        if abs(b1["price"] - b2["price"]) <= 10:
            _add_combo(b1, b2, combos, existing_bundles)

    if not combos:
        print("[!] No combos generated after rules.")
        return []

    # 3) AI score every combo (with caching) -------------------------
    for c in combos:
        key = f'{c["bottles"][0]["name"]}||{c["bottles"][1]["name"]}'
        if key not in _SCORE_CACHE:
            try:
                _SCORE_CACHE[key] = score_pair(*c["bottles"])
                time.sleep(0.3)  # gentle on rate limit
            except Exception as e:
                print(f"[AI] score error → {e}")
                _SCORE_CACHE[key] = 50.0  # neutral
        c["ai_score"] = _SCORE_CACHE[key]

    # persist cache
    with open(_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(_SCORE_CACHE, f, ensure_ascii=False, indent=2)

    # 4) sort by (ai_score ↓ , price ↓) and keep top N --------------
    combos.sort(key=lambda x: (x["ai_score"], x["price"]), reverse=True)
    top = combos[:max_bundles]

    # 5) reporting ---------------------------------------------------
    print(f"[i] {len(valid)} size-valid bottles → {len(combos)} combos "
          f"→ returning top {len(top)} bundles.")
    return top

# ----------------------------------------------------------------
# ❸  helpers
# ----------------------------------------------------------------
def _add_combo(b1, b2, sink, existing):
    name = f"{b1['name']} & {b2['name']}"
    if name in existing:
        return
    price = round_to_99((b1["price"] + b2["price"]) - 5)
    sink.append({"name": name, "price": price, "bottles": [b1, b2]})
def extract_volume(text: str) -> int:
    """
    Parse formats like:
      • 750 ml   →  750
      • 1.5 L    → 1500
      • 1.75 L   → 1750
    If nothing found, treat as the common 750-ml size.
    """
    m = re.search(r'(\d+(?:\.\d+)?)\s*(ml|l)', text.lower())
    if m:
        val, unit = m.groups()
        try:
            vol = float(val)
            return int(vol) if unit == "ml" else int(vol * 1000)
        except ValueError:
            pass
    # ‼ no explicit volume – assume a standard 750 ml bottle
    return 750
def round_to_99(price: float) -> float:
    """
    Force price to end in .99 ( e.g. 131.40 → 131.99 ).
    """
    ipart = math.floor(price)
    return float(f"{ipart}.99") if price - ipart < 0.99 else float(f"{ipart+1}.99")
