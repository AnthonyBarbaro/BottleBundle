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
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    for bundle in new_bundles:
        # Attempt to download or reference local images for each bottle
        # For simplicity, assume you have local images in 'images/' with names matching `bottle['name']`.
        # If you only have URLs, you need to download them first.
        b1 = bundle['bottles'][0]['name']
        b2 = bundle['bottles'][1]['name']
        # Example local paths:
        img_path_1 = os.path.join("images", f"{b1}.jpg")
        img_path_2 = os.path.join("images", f"{b2}.jpg")

        # If images exist, create the combined
        if os.path.exists(img_path_1) and os.path.exists(img_path_2):
            combined_name = bundle['name'].replace(' ', '_') + ".jpg"
            output_path = os.path.join("bundle_images", combined_name)
            os.makedirs("bundle_images", exist_ok=True)
            composer.create_bundle_image([img_path_1, img_path_2], output_path)
            bundle['image_src'] = output_path
        else:
            bundle['image_src'] = ""  # or handle differently

        # 6) Generate descriptions
        desc = generate_description(bundle['name'])
        bundle['description'] = desc
        # Add the bundle to final list
        final_bundles.append(bundle)
        # Mark as processed in your log
        save_processed_item(bundle['name'], 'bundles_log.json')

    # 7) Export to Shopify CSV
    export_to_shopify_csv(final_bundles, output_file='exported_bundles.csv')

    print("[✓] Pipeline completed successfully.")

if __name__ == "__main__":
    main()
