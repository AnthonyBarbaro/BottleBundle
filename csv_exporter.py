# csv_exporter.py
import csv, os, re
from category_utils import get_product_category

def _handle(text: str) -> str:
    """Shopify handle (lowercase, hyphens, ascii)."""
    return re.sub(r'[^\w\s-]', '', text).lower().replace(' ', '-')

# -- the exact header list you provided earlier -------------------
SHOPIFY_HEADERS = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type',
    'Tags', 'Published', 'Option1 Name', 'Option1 Value', 'Option1 Linked To',
    'Option2 Name', 'Option2 Value', 'Option2 Linked To', 'Option3 Name',
    'Option3 Value', 'Option3 Linked To', 'Variant SKU', 'Variant Grams',
    'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy',
    'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src',
    'Image Position', 'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
    'Google Shopping / Google Product Category', 'Google Shopping / Gender',
    'Google Shopping / Age Group', 'Google Shopping / MPN',
    'Google Shopping / Condition', 'Google Shopping / Custom Product',
    'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1',
    'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3',
    'Google Shopping / Custom Label 4', 'Google: Custom Product (product.metafields.mm-google-shopping.custom_product)',
    'Product rating count (product.metafields.reviews.rating_count)',
    'Color (product.metafields.shopify.color-pattern)',
    'Country (product.metafields.shopify.country)',
    'Dietary preferences (product.metafields.shopify.dietary-preferences)',
    'Gin variety (product.metafields.shopify.gin-variety)',
    'Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products)',
    'Related products (product.metafields.shopify--discovery--product_recommendation.related_products)',
    'Related products settings (product.metafields.shopify--discovery--product_recommendation.related_products_display)',
    'Variant Image', 'Variant Weight Unit', 'Variant Tax Code', 'Cost per item',
    'Included / United States', 'Price / United States', 'Compare At Price / United States',
    'Status'
]

# --- bundle-dict → shopify-row -----------------------------------
def map_bundle_to_shopify_fields(bundle: dict) -> dict:
    """
    Convert a bundle produced by your pipeline into a fully-populated
    Shopify CSV row (matching SHOPIFY_HEADERS).
    """
    row = {header: '' for header in SHOPIFY_HEADERS}

    row['Handle']        = _handle(bundle['name'])
    row['Title']         = bundle['name']
    row['Body (HTML)']   = bundle.get('description', '')
    row['Vendor']        = 'Bottle Buzz'
    row['Product Category'] = get_product_category(bundle.get('category', ''))
    row['Type']          = 'Bundle'
    row['Tags']          = bundle.get('tags', 'Bundles, Liquor')
    row['Published']     = 'TRUE'
    row['Option1 Name']  = 'Title'
    row['Option1 Value'] = 'Default Title'

    # --- variant fields ---
    row['Variant SKU']   = bundle.get('sku', '')
    row['Variant Grams'] = 1361
    row['Variant Inventory Tracker'] = 'shopify'
    row['Variant Inventory Qty']     = 10
    row['Variant Inventory Policy']  = 'deny'
    row['Variant Fulfillment Service'] = 'manual'
    row['Variant Price']   = f"{bundle['price']:.2f}"
    row['Variant Requires Shipping'] = 'TRUE'
    row['Variant Taxable'] = 'TRUE'

    row['Image Src']      = bundle.get('image_src', '')
    row['Image Position'] = 1
    row['Image Alt Text'] = bundle['name']
    row['Gift Card']      = 'FALSE'
    row['SEO Title']      = f"Buy {bundle['name']} Online | Bottle Buzz"
    row['SEO Description'] = f"Shop {bundle['name']} at the best price on Bottle Buzz."
    row['Google Shopping / Google Product Category'] = row['Product Category']
    row['Google Shopping / Age Group'] = 'adult'
    row['Google Shopping / Condition'] = 'new'
    row['Google Shopping / Custom Label 0'] = 'Bundle'
    row['Variant Weight Unit'] = 'g'
    row['Status'] = 'draft'

    return row

# -----------------------------------------------------------------
def export_to_shopify_csv(bundles: list[dict], output_file='shopify_bundles.csv'):
    """
    Write bundles to a fully-featured Shopify template CSV.
    """
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=SHOPIFY_HEADERS)
        writer.writeheader()
        for b in bundles:
            writer.writerow(map_bundle_to_shopify_fields(b))

    print(f"[✔] Exported {len(bundles)} bundles → {output_file}")
