# test_scrape.py  – small throw-away script
from scraper import scrape_bottlebuzz_category

tequila_url = "https://bottlebuzz.com/collections/tequila"
bottles = scrape_bottlebuzz_category(tequila_url, total_pages=3)

# show first 10 for a quick sanity-check
for b in bottles[:10]:
    print(f"{b['name']:60}  ${b['price']:.2f}")

print(f"\nTotal scraped: {len(bottles)}")
