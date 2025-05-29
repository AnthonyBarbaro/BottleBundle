# scraper.py

import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
def extract_price(text: str) -> float | None:
    """
    Return the first float found in a string like '$49.99 — In stock'.
    Returns None if nothing looks like a price.
    """
    m = re.search(r'(\d[\d,]*\.\d{2})', text)
    if m:
        return float(m.group(1).replace(',', ''))
    return None
def clean_text(text: str) -> str:
    """Remove unwanted characters and whitespace from a string."""
    return re.sub(r'[^\w\s-]', '', text).strip()

def scrape_bottlebuzz_category(category_url: str, total_pages: int = 5) -> list[dict]:
    """
    Scrapes 'BottleBuzz' for a specific category (e.g., Tequila),
    returning a list of product dicts with keys: name, brand, price, image_url.
    """

    chrome_options = Options()
    # e.g. run headless for speed:
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    results = []
    for page_num in range(1, total_pages + 1):
        page_url = f"{category_url}?page={page_num}"
        driver.get(page_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'grid-item'))
            )
        except:
            print(f"[!] Page {page_num} load timeout. Skipping.")
            continue

        time.sleep(2)  # Adjust as needed for site responsiveness
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('div', class_='grid-item')

        if not items:
            print(f"[!] No products found on page {page_num}. Stopping.")
            break

        for item in items[:40]:
            name_elem = item.find('div', class_='grid-product__title')
            brand_elem = item.find('div', class_='grid-product__vendor')
            price_elem = item.find('span', class_='grid-product__price--current')
            image_elem = item.find('img')

            if not name_elem or not brand_elem or not price_elem or not image_elem:
                continue

            name = clean_text(name_elem.text)
            brand = clean_text(brand_elem.text)
            # Some sites have the price in different formats; handle carefully:
            raw = price_elem.get_text(" ", strip=True)  # join text nodes with spaces
            price = extract_price(raw)
            if price is None:
                print(f"[!] No price found for {name}")
                continue      

            image_url = image_elem.get('src') or image_elem.get('data-src') or ''
            if image_url.startswith('//'):
                image_url = 'https:' + image_url

            product_data = {
                'name': name,
                'brand': brand,
                'price': price,
                'image_url': image_url
            }
            results.append(product_data)

        print(f"[+] Page {page_num} scraped ({len(items)} items found).")

    driver.quit()
    return results
