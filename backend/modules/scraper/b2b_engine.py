import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time
import re

class B2BEngine:
    def __init__(self):
        self.mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
        }
        self.ua = UserAgent()

    def search_b2b(self, query):
        print(f"🏭 B2B ENGINE: Starting Multi-Source Scan for '{query}'...")
        results = []
        # Try direct methods first
        results.extend(self._scrape_tradeindia(query))
        results.extend(self._scrape_indiamart_mobile(query))

        if not results:
            print("⚠️ Direct scanning blocked. Engaging Deep-Snippet Backdoor...")
            results.extend(self._search_engine_fallback(query, "indiamart.com"))
        
        return results

    def _scrape_indiamart_mobile(self, query):
        print(f"🇮🇳 Scanning IndiaMART Mobile for '{query}'...")
        url = f"https://m.indiamart.com/impcat/{query.replace(' ', '-').lower()}.html"
        try:
            response = requests.get(url, headers=self.mobile_headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all('div', {'class': re.compile(r'p-cnt|l-crt|card')})
            leads = []
            for card in cards[:6]:
                try:
                    # ✨ IMAGE EXTRACTION FIX
                    img_tag = card.find('img')
                    # Look for data-src or src for lazy-loaded images
                    img_url = img_tag.get('data-src') or img_tag.get('src') if img_tag else None
                    
                    title_tag = card.find('a', {'class': 'p-name'})
                    leads.append({
                        "title": title_tag.get_text(strip=True),
                        "price": card.find('span', {'class': 'p-price'}).get_text(strip=True) if card.find('span', {'class': 'p-price'}) else "Ask Price",
                        "seller": card.find(['div', 'span'], {'class': re.compile(r'c-name|cname')}).get_text(strip=True) if card.find(['div', 'span'], {'class': re.compile(r'c-name|cname')}) else "Verified Supplier",
                        "address": card.find(['div', 'span'], {'class': re.compile(r'c-loc|cloc')}).get_text(strip=True) if card.find(['div', 'span'], {'class': re.compile(r'c-loc|cloc')}) else "India",
                        "url": "https://m.indiamart.com" + title_tag['href'] if title_tag else "#",
                        "image": img_url if img_url and 'http' in img_url else "https://tiimg.tistatic.com/fp/1/007/557/indiamart-logo-584.jpg",
                        "source": "IndiaMART",
                        "type": "B2B"
                    })
                except: continue
            return leads
        except: return []

    def _search_engine_fallback(self, query, site):
        print(f"🕵️‍♂️ Backdoor Search for {site}...")
        try:
            # DuckDuckGo fallback now attempts to find a related image from a placeholder service
            # since search snippets don't contain images
            ddg_url = f"https://html.duckduckgo.com/html/?q=site:{site}+{query.replace(' ', '+')}"
            res = requests.get(ddg_url, headers={'User-Agent': self.ua.random}, timeout=10)
            soup = BeautifulSoup(res.content, 'html.parser')
            results = []
            for result in soup.find_all('div', {'class': 'result'}):
                try:
                    title_tag = result.find('a', {'class': 'result__a'})
                    # Use a dynamic placeholder if no real image is available
                    # This looks much better than a broken icon
                    placeholder = f"https://loremflickr.com/320/240/{query.replace(' ', ',')}"
                    
                    results.append({
                        "title": title_tag.get_text(strip=True),
                        "price": "Wholesale Price", 
                        "seller": title_tag.get_text().split('-')[0].strip(),
                        "address": "Verified Location",
                        "url": title_tag['href'],
                        "source": f"{site} (Verified)",
                        "image": placeholder, # ✨ Placeholder fix for fallback mode
                        "type": "Wholesale"
                    })
                except: continue
            return results[:5]
        except: return []

    # --- SOURCE 1: TRADEINDIA ---
    def _scrape_tradeindia(self, query):
        print(f"🏗️ Scanning TradeIndia for '{query}'...")
        url = f"https://www.tradeindia.com/search.html?keyword={query.replace(' ', '+')}"
        try:
            response = requests.get(url, headers=self.mobile_headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Look for any div containing product-related keywords
            cards = soup.find_all('div', {'class': re.compile(r'product-card|search-product-box|details')})
            
            leads = []
            for card in cards[:6]:
                try:
                    title_tag = card.find('a', href=True)
                    if not title_tag or len(title_tag.text) < 5: continue
                    
                    link = title_tag['href']
                    if not link.startswith('http'): link = "https://www.tradeindia.com" + link
                    
                    # 🧠 Extract City/Location from raw text
                    loc_text = card.get_text()
                    city_match = re.search(r'(Delhi|Mumbai|Pune|Ahmedabad|Chennai|Bangalore|Kolkata|Surat|Jaipur|Lucknow)', loc_text)
                    
                    leads.append({
                        "title": title_tag.get_text(strip=True),
                        "price": "Check Quote",
                        "seller": card.find(['p', 'span'], {'class': re.compile(r'company|seller|name')}).text.strip() if card.find(['p', 'span'], {'class': re.compile(r'company|seller|name')}) else "Verified Supplier",
                        "address": city_match.group(0) if city_match else "India",
                        "contact": "Contact Supplier",
                        "url": link,
                        "image": "https://tiimg.tistatic.com/fp/1/007/557/indiamart-logo-584.jpg",
                        "source": "TradeIndia",
                        "type": "B2B"
                    })
                except: continue
            return leads
        except: return []

    # --- SOURCE 2: INDIAMART (Mobile Version) ---
    def _scrape_indiamart_mobile(self, query):
        print(f"🇮🇳 Scanning IndiaMART (Mobile Mode) for '{query}'...")
        url = f"https://m.indiamart.com/impcat/{query.replace(' ', '-').lower()}.html"
        try:
            response = requests.get(url, headers=self.mobile_headers, timeout=10)
            if response.status_code != 200: return []

            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all('div', {'class': re.compile(r'p-cnt|l-crt|card')})

            leads = []
            for card in cards[:6]:
                try:
                    title_tag = card.find('a', {'class': 'p-name'})
                    if not title_tag: continue
                    
                    link = title_tag['href']
                    if not link.startswith('http'): link = "https://m.indiamart.com" + link

                    price_tag = card.find('span', {'class': 'p-price'})
                    seller_tag = card.find(['div', 'span'], {'class': re.compile(r'c-name|cname')})
                    loc_tag = card.find(['div', 'span'], {'class': re.compile(r'c-loc|cloc')})

                    leads.append({
                        "title": title_tag.get_text(strip=True),
                        "price": price_tag.get_text(strip=True) if price_tag else "Ask Price",
                        "seller": seller_tag.get_text(strip=True) if seller_tag else "Star Supplier",
                        "address": loc_tag.get_text(strip=True) if loc_tag else "India",
                        "contact": "Call Supplier",
                        "url": link,
                        "image": "https://tiimg.tistatic.com/fp/1/007/557/indiamart-logo-584.jpg",
                        "source": "IndiaMART",
                        "type": "B2B"
                    })
                except: continue
            return leads
        except: return []

    # --- SOURCE 3: EXPORTERS INDIA ---
    def _scrape_exportersindia(self, query):
        print(f"🚢 Scanning ExportersIndia for '{query}'...")
        url = f"https://www.exportersindia.com/search.php?term={query.replace(' ', '+')}"
        try:
            response = requests.get(url, headers=self.mobile_headers, timeout=6)
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all('div', {'class': re.compile(r'c-row|ser-row|b-list')})
            leads = []
            for card in cards[:4]:
                try:
                    title_tag = card.find('a', {'class': re.compile(r'pname|title')})
                    if not title_tag: continue
                    
                    leads.append({
                        "title": title_tag.get_text(strip=True),
                        "price": card.find('div', {'class': 'price'}).get_text(strip=True) if card.find('div', {'class': 'price'}) else "Quote Only",
                        "seller": card.find('a', {'class': 'cname'}).get_text(strip=True) if card.find('a', {'class': 'cname'}) else "Verified Exporter",
                        "address": "View Profile",
                        "contact": "Contact Exporter",
                        "url": title_tag['href'],
                        "image": "https://img.etimg.com/thumb/msid-64687661,width-300,imgsize-12497,,resizemode-4,quality-100/exporters-india.jpg",
                        "source": "ExportersIndia",
                        "type": "B2B"
                    })
                except: continue
            return leads
        except: return []

    