# csv_exporter.py

import csv
import re
import os

def create_handle(name: str) -> str:
    """Convert name to a Shopify handle (lowercase, hyphens)."""
    handle = re.sub(r'[^\w\s-]', '', name).lower()
    return handle.replace(' ', '-')

def export_to_shopify_csv(bundles: list[dict], output_file='shopify_bundles.csv'):
    """
    Export each bundle as a row in a Shopify-compatible CSV.
    This is a minimal example using a subset of all possible Shopify fields.
    """
    fieldnames = [
        'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type',
        'Tags', 'Published', 'Option1 Name', 'Option1 Value',
        'Variant SKU', 'Variant Price', 'Variant Inventory Qty',
        'Image Src', 'Status'
    ]

    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for bundle in bundles:
            row = {
                'Handle': create_handle(bundle['name']),
                'Title': bundle['name'],
                'Body (HTML)': bundle.get('description', ''),
                'Vendor': 'Liquor Bundle',       # or brand?
                'Type': 'Bundle',
                'Tags': 'Bundles, Liquor',
                'Published': 'TRUE',
                'Option1 Name': 'Title',
                'Option1 Value': 'Default Title',
                'Variant SKU': bundle.get('sku', ''),  # optional
                'Variant Price': f"{bundle['price']:.2f}",
                'Variant Inventory Qty': 10,
                'Image Src': bundle.get('image_src', ''),  # path or hosted URL
                'Status': 'active'
            }
            writer.writerow(row)
    print(f"[✔] Exported {len(bundles)} bundles to {output_file}")
