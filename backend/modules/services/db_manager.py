from modules.services.supabase_client import supabase

class DBManager:
    def __init__(self):
        self.supabase = supabase

    def save_product(self, data):
        """
        Saves product and price. 
        Dynamically handles categories and brands instead of hardcoding 'Electronics'.
        """
        if not data:
            return None

        try:
            # Check if Product Exists
            existing = self.supabase.table('products').select("id").eq("name", data['title']).execute()
            
            product_id = None

            if existing.data:
                product_id = existing.data[0]['id']
            else:
                # --- NEW DYNAMIC MAPPING ---
                # We extract the brand from the title if it's 'Unknown'
                brand_name = data.get('brand', 'Unknown')
                if brand_name == 'Unknown':
                    brand_name = data['title'].split(' ')[0] # Simple heuristic: first word is often brand

                new_product = {
                    "name": data['title'],
                    "brand": brand_name,
                    "category": data.get('category', 'General'), # Use scraped category or 'General'
                    "image_url": data['image']
                }
                res = self.supabase.table('products').insert(new_product).execute()
                product_id = res.data[0]['id']

            # Insert Price History entry
            new_price = {
                "product_id": product_id,
                "price_inr": data['price'],
                "site_name": data['source'],
                "product_link": data['url']
            }
            
            self.supabase.table('prices').insert(new_price).execute()
            return product_id

        except Exception as e:
            print(f"🔥 Database Error: {e}")
            return None

    def get_price_history(self, product_id):
        """Fetches price AND timestamp for the chart using the correct column name"""
        try:
            # Changed 'created_at' to 'scraped_at' to match your schema
            response = self.supabase.table('prices')\
                .select('price_inr, scraped_at')\
                .eq('product_id', product_id)\
                .order('scraped_at', desc=True)\
                .execute()
            
            if response.data:
                return response.data
            return []
            
        except Exception as e:
            print(f"DB History Error: {e}")
            return []