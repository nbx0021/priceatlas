import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time

def get_price_amazon(query):
    ua = UserAgent()
    # 1. Use a specific, high-quality Desktop User-Agent first (More stable than random)
    header_list = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
        {
            'User-Agent': ua.random, # Fallback to random
            'Accept-Language': 'en-US,en;q=0.9',
        }
    ]

    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    print(f"🕵️‍♀️ Scraping: {url}")

    # Retry logic: Try twice if the first time fails
    for attempt in range(2):
        try:
            headers = header_list[attempt]
            time.sleep(random.uniform(2, 4)) # Slower = Safer
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️ Status {response.status_code}. Retrying...")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')

            # CHECK: Did we get a CAPTCHA?
            if "captcha" in soup.text.lower() or "robot check" in soup.title.text.lower():
                print("🤖 Amazon blocked us (CAPTCHA). Retrying with new Agent...")
                continue

            # --- STRATEGY 1: Organic Search Results (Best Data) ---
            results = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            # --- STRATEGY 2: Sponsored Results (If Organic fails) ---
            if not results:
                print("⚠️ No organic results. Trying Sponsored/Ads...")
                # Sponsored items often don't have the data-component-type, but live in s-result-item
                results = soup.find_all('div', {'class': 's-result-item'})

            if not results:
                print("❌ No products found (HTML structure might be different).")
                continue

            # Loop through candidates to find the first valid one (with a price)
            found_product = None
            for card in results:
                # Must have a price to be useful
                if card.find('span', {'class': 'a-price-whole'}):
                    found_product = card
                    break
            
            if not found_product:
                print("❌ Found cards, but none had a price.")
                continue

            # --- EXTRACT DATA ---
            # 1. Title
            title_tag = found_product.find('h2')
            title = title_tag.text.strip() if title_tag else "Unknown Product"

            # 2. Price
            price_tag = found_product.find('span', {'class': 'a-price-whole'})
            price = float(price_tag.text.replace(',', '').replace('.', '')) if price_tag else 0.0

            # 3. Image (Smart Loader)
            img_tag = found_product.find('img', {'class': 's-image'})
            image_url = ""
            if img_tag:
                image_url = img_tag.get('src')
                # If it's a pixel or hidden, look for srcset
                if "grey-pixel" in image_url or not image_url:
                    srcset = img_tag.get('srcset')
                    if srcset:
                        image_url = srcset.split(' ')[0] # Take first high-res URL

            # 4. Link
            link_tag = found_product.find('a', {'class': 'a-link-normal'})
            link = "https://amazon.in" + link_tag['href'] if link_tag else ""

            # Validate: If we still have "Unknown" or 0 price, skip
            if price == 0:
                continue

            return {
                "name": title,
                "price": price,
                "currency": "INR",
                "url": link,
                "image": image_url,
                "source": "Amazon"
            }

        except Exception as e:
            print(f"⚠️ Error on attempt {attempt}: {e}")
            continue

    print("❌ All attempts failed.")
    return None

# --- TEST CODE (Only runs if you run this file directly) ---
if __name__ == "__main__":
    result = get_price_amazon("iphone 15")
    print("\n📦 Scrape Result:")
    print(result)