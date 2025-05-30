# category_utils.py
def get_product_category(category: str) -> str:
    """
    Return a Google-product-category style string for Shopify.
    Extend as needed.
    """
    mapping = {
        'Tequila':  'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Tequila',
        'Whiskey':  'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Whiskey',
        'Vodka':    'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Vodka',
        'Gin':      'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Gin',
        'Rum':      'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Rum',
        'Cognac':   'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Cognac',
        'Mezcal':   'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Mezcal',
        'Liqueur':  'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Liqueurs',
        'Brandy':   'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages > Liquor & Spirits > Brandy',
        # fallback
    }
    return mapping.get(category, 'Food, Beverages & Tobacco > Beverages > Alcoholic Beverages')
