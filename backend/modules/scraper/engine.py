import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time
import re
import json
import concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

# Disable SSL Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from modules.analytics.forex_engine import ForexEngine
except ImportError:
    ForexEngine = None

class ScraperEngine:
    def __init__(self):
        self.ua = UserAgent()
        
        # --- 1. ROUTING RULES ---
        self.SOURCE_ROUTING = {
            "fashion": ["amazon", "flipkart", "myntra", "ebay"],
            "electronics": ["amazon", "flipkart", "ebay", "jiomart"], 
            "grocery": ["amazon", "jiomart", "flipkart"],
            "furniture": ["amazon", "flipkart", "ikea", "ebay"],
            "wholesale": ["indiamart", "tradeindia"],
            "general": ["amazon", "flipkart", "ebay", "jiomart"]
        }

        self.CATEGORY_MAP = {
            "fashion": ["shirt", "pant", "shoe", "dress", "watch", "denim", "top", "tee", "sneaker", "jeans"],
            "grocery": ["butter", "oil", "tea", "coffee", "rice", "sugar", "dal", "protein", "food", "chocolate", "biscuits", "shampoo", "soap", "paste"],
            "furniture": ["chair", "table", "sofa", "bed", "desk", "lamp", "shelf"],
            "electronics": ["laptop", "phone", "mobile", "tv", "watch", "earphone", "monitor", "gpu", "keyboard"]
        }
        
        self.forex = ForexEngine() if ForexEngine else None

    def _identify_category(self, query):
        q = query.lower()
        for cat, keywords in self.CATEGORY_MAP.items():
            if any(k in q for k in keywords): return cat
        return "general"

    def search_product(self, query, intent="single"):
        if intent in ['bulk', 'wholesale']:
            target_sources = self.SOURCE_ROUTING["wholesale"]
        else:
            category = self._identify_category(query)
            target_sources = self.SOURCE_ROUTING.get(category, self.SOURCE_ROUTING["general"])
        
        print(f"🚦 Routing '{query}' ({category}) to: {target_sources}")

        results = []
        source_counts = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            for source in target_sources:
                method_name = f"_get_price_{source}"
                if hasattr(self, method_name):
                    futures[executor.submit(getattr(self, method_name), query, category)] = source

            for future in concurrent.futures.as_completed(futures):
                source_name = futures[future]
                try:
                    data = future.result()
                    if data:
                        results.extend(data)
                        source_counts[source_name] = len(data)
                    else:
                        source_counts[source_name] = 0
                except Exception as e:
                    print(f"⚠️ CRASH in {source_name}: {e}") # Print crash details
                    source_counts[source_name] = "ERR"

        print("\n" + "="*45)
        print("🕵️‍♀️  SCRAPER INTELLIGENCE REPORT")
        print("-" * 45)
        for src, count in source_counts.items():
            status = "✅" if isinstance(count, int) and count > 0 else "❌"
            print(f"{status} {src.upper():<12} : Found {count} products")
        print("-" * 45)
        print(f"📦 TOTAL AGGREGATED  : {len(results)} products")
        print("="*45 + "\n")

        return sorted(results, key=lambda x: x['price'])

    # -------------------------------------------------------------------------
    # 🇮🇳  SOURCE: FLIPKART (Furniture Grid Fix)
    # -------------------------------------------------------------------------
    def _get_price_flipkart(self, query, category="general"):
        url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}&otracker=search"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # COMBINED SELECTORS (List + Grid + New)
            cards = soup.find_all('div', {'class': '_1AtVbE'}) or \
                    soup.find_all('div', {'class': '_4ddWXP'}) or \
                    soup.find_all('div', {'class': 'cPHDOP'})
            
            products = []
            for card in cards:
                # 1. Title
                title_tag = card.find('a', {'class': 's1Q9rs'}) or \
                            card.find('div', {'class': '_4rR01T'}) or \
                            card.find('a', {'class': 'wjcEIp'})
                
                # 2. Price
                price_tag = card.find('div', {'class': '_30jeq3'}) or \
                            card.find('div', {'class': 'Nx9bqj'})

                if title_tag and price_tag:
                    title = title_tag.get_text(strip=True)
                    price = float(re.sub(r'[^\d.]', '', price_tag.get_text()))
                    
                    # 3. Link
                    link_tag = card.find('a', href=True)
                    if not link_tag: link_tag = title_tag if title_tag.name == 'a' else None
                    link = "https://www.flipkart.com" + link_tag['href'] if link_tag else ""
                    
                    # 4. Image
                    img_tag = card.find('img')
                    img = img_tag['src'] if img_tag else ""

                    products.append({
                        "title": title, "brand": "Flipkart", "category": category.title(),
                        "price": price, "currency": "INR",
                        "url": link, "image": img, "source": "Flipkart", "type": "Retail"
                    })
                    if len(products) >= 10: break
            return products
        except Exception as e:
            return []

    # -------------------------------------------------------------------------
    # 🪑 SOURCE: IKEA (Fixed Crash)
    # -------------------------------------------------------------------------
    def _get_price_ikea(self, query, category="furniture"):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': '*/*'
        }
        # IKEA uses a specific API-like search URL
        url = f"https://www.ikea.com/in/en/search/?q={query.replace(' ', '%20')}"
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Selector for IKEA Grid
            cards = soup.find_all('div', {'class': 'plp-fragment-wrapper'})
            
            products = []
            for card in cards[:8]:
                try:
                    # JSON Data is often hidden in data attributes
                    title = card.find('span', {'class': 'header-section__title'}).text.strip()
                    price_txt = card.find('span', {'class': 'pip-price__integer'}).text.strip()
                    price = float(re.sub(r'[^\d.]', '', price_txt))
                    
                    link = card.find('a')['href']
                    img = card.find('img')['src']

                    products.append({
                        "title": title, "brand": "IKEA", "category": "Furniture",
                        "price": price, "currency": "INR",
                        "url": link, "image": img, "source": "IKEA", "type": "Retail"
                    })
                except: continue
            return products
        except Exception as e:
            # print(f"IKEA Error: {e}")
            return []

    # -------------------------------------------------------------------------
    # 🌎 SOURCE: EBAY (Simplified)
    # -------------------------------------------------------------------------
    def _get_price_ebay(self, query, category="general"):
        session = requests.Session()
        session.headers.update({'User-Agent': self.ua.random, 'Connection': 'keep-alive'})
        url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
        
        try:
            response = session.get(url, timeout=20, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            items = soup.find_all('div', {'class': 's-item__wrapper'})
            products = []
            for item in items[1:10]: # Skip first (dummy)
                try:
                    title = item.find('div', {'class': 's-item__title'}).text.strip()
                    if "Shop on eBay" in title: continue
                    
                    price_tag = item.find('span', {'class': 's-item__price'})
                    if not price_tag: continue
                    
                    # Robust Price Parsing
                    price_str = price_tag.text.split(' to ')[0] # Handle ranges
                    price_val = float(re.sub(r'[^\d.]', '', price_str))
                    
                    # Convert USD/EUR if needed, else assume INR approx
                    if '$' in price_str: price_val *= 86.5
                    elif 'EUR' in price_str: price_val *= 92.0

                    link = item.find('a')['href']
                    img = item.find('img')['src']

                    products.append({
                        "title": title, "brand": "eBay", "category": "General",
                        "price": round(price_val, 2), "currency": "INR",
                        "url": link, "image": img, "source": "eBay", "type": "Retail"
                    })
                except: continue
            return products
        except: return []

    # -------------------------------------------------------------------------
    # 🥦 SOURCE: JIOMART
    # -------------------------------------------------------------------------
    def _get_price_jiomart(self, query, category="general"):
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://www.jiomart.com/'
        })
        url = f"https://www.jiomart.com/search/{query.replace(' ', '%20')}"
        try:
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            cards = soup.find_all('div', class_=re.compile(r'card|plp-card'))
            products = []
            for card in cards[:10]:
                try:
                    text = card.get_text(strip=True)
                    if '₹' not in text: continue
                    price = float(re.search(r'₹\s?([\d,]+)', text).group(1).replace(',', ''))
                    
                    title_tag = card.find(class_=re.compile(r'name|title'))
                    title = title_tag.text.strip() if title_tag else "JioMart Item"
                    
                    if not any(w in title.lower() for w in query.lower().split()): continue
                    
                    products.append({
                        "title": title, "brand": "JioMart", "category": "Grocery",
                        "price": price, "currency": "INR",
                        "url": "https://www.jiomart.com" + card.find('a')['href'],
                        "image": card.find('img')['src'], "source": "JioMart", "type": "Retail"
                    })
                except: continue
            return products
        except: return []

    # -------------------------------------------------------------------------
    # 👗 SOURCE: MYNTRA
    # -------------------------------------------------------------------------
    def _get_price_myntra(self, query, category="fashion"):
        # Keep existing working Safe JSON Logic
        session = requests.Session()
        headers = {'User-Agent': self.ua.random, 'Referer': 'https://www.myntra.com/'}
        url = f"https://www.myntra.com/{query.replace(' ', '-')}"
        try:
            response = session.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            script = soup.find('script', string=re.compile('window.__myx'))
            if not script: return []
            data = json.loads(script.string.split('window.__myx = ')[1].split(';')[0])
            items = data.get('searchData', {}).get('results', {}).get('products', [])
            products = []
            for item in items[:10]:
                try:
                    imgs = item.get('images', [])
                    img_src = imgs[0].get('src') if imgs else ""
                    products.append({
                        "title": item.get('productName'), "brand": item.get('brand'), "category": "Fashion",
                        "price": float(item.get('price') or item.get('mrp') or 0), "currency": "INR",
                        "url": f"https://www.myntra.com/{item.get('landingPageUrl')}",
                        "image": img_src, "source": "Myntra", "type": "Retail"
                    })
                except: continue
            return products
        except: return []

    # -------------------------------------------------------------------------
    # 🌍 SOURCE: AMAZON
    # -------------------------------------------------------------------------
    def _get_price_amazon(self, query, category="general"):
        # Keep existing working Amazon logic
        header_list = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}]
        url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
        for attempt, headers in enumerate(header_list):
            try:
                time.sleep(1)
                response = requests.get(url, headers=headers, timeout=10)
                if "api-services-support@amazon.com" in response.text: continue
                soup = BeautifulSoup(response.content, 'html.parser')
                results = soup.find_all('div', {'data-component-type': 's-search-result'})
                products = []
                for card in results:
                    title_tag = card.find('h2')
                    if not title_tag: continue
                    price_tag = card.find('span', {'class': 'a-price-whole'})
                    if not price_tag: continue
                    products.append({
                        "title": title_tag.text.strip(), "brand": "Amazon", "category": "Retail",
                        "price": float(re.sub(r'[^\d.]', '', price_tag.text)), "currency": "INR",
                        "url": "https://www.amazon.in" + card.find('a', {'class': 'a-link-normal'})['href'],
                        "image": card.find('img', {'class': 's-image'})['src'], "source": "Amazon", "type": "Retail"
                    })
                    if len(products) >= 10: break
                if products: return products
            except: continue
        return []
    # -------------------------------------------------------------------------
    # 🛠️  HELPER METHODS
    # -------------------------------------------------------------------------
    def _normalize(self, text):
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return [w[:-1] if w.endswith('s') and len(w) > 3 else w for w in clean.split()]

    def _get_synonyms(self, word):
        return self.SYNONYMS.get(word, set())
    
    
    # def _extract_brand(self, title):
    #     return title.split()[0].title() if title else "Unknown"

    def _extract_brand(self, title):
        words = title.strip().split()
        if not words: return "Unknown"
        if len(words[0]) <= 3 and len(words) > 1: return f"{words[0]} {words[1]}".title()
        return words[0].title()