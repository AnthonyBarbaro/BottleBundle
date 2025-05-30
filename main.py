# main.py

import os
import openai
from dotenv import load_dotenv
from scraper import scrape_bottlebuzz_category
from duplicate_checker import load_processed_items, save_processed_item
from bundler import generate_bundles
from image_composer import ImageComposer
from description_builder import generate_description
from csv_exporter import export_to_shopify_csv
load_dotenv()

# 1) Set your OpenAI key
CATEGORY_NAME   = "Tequila"
openai.api_key = os.getenv("OPENAI_API_KEY")
CSV_OUT         = f"exported_bundles_{CATEGORY_NAME.lower()}.csv"
def main():
    # 2) Scrape the site
    category_url = "https://bottlebuzz.com/collections/tequila"
    scraped_bottles = scrape_bottlebuzz_category(category_url, total_pages=3)  # or more pages if needed
    print(f"[i] Scraped {len(scraped_bottles)} tequila bottles.")

    # 3) Load existing bundles from log (avoid duplicates)
    existing_bundles = load_processed_items('bundles_log.json')

    # 4) Generate new bundles
    new_bundles = generate_bundles(scraped_bottles, existing_bundles)
    print(f"[i] Generated {len(new_bundles)} potential new bundles.")

    # 5) Compose images for each new bundle (optional)
    composer = ImageComposer((1200, 1200))
    final_bundles = []
    for b in new_bundles:
        # ------------------ images (skip if missing) -------------
        b1, b2   = b["bottles"][0]["name"], b["bottles"][1]["name"]
        p1, p2   = os.path.join("images", f"{b1}.jpg"), os.path.join("images", f"{b2}.jpg")
        if os.path.exists(p1) and os.path.exists(p2):
            out_path = os.path.join("bundle_images", b["name"].replace(' ', '_') + ".jpg")
            os.makedirs("bundle_images", exist_ok=True)
            composer.create_bundle_image([p1, p2], out_path)
            b["image_src"] = out_path
        # ------------------ add metadata -------------------------
        b["description"] = generate_description(b["name"])
        b["category"]    = CATEGORY_NAME          # 👈 add the category tag
        final_bundles.append(b)
        save_processed_item(b["name"], 'bundles_log.json')

    # 7) Export to Shopify CSV
    export_to_shopify_csv(final_bundles, output_file=CSV_OUT)

    print("[✓] Pipeline completed successfully.")

if __name__ == "__main__":
    main()
