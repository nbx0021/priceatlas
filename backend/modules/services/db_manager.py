from modules.services.supabase_client import supabase

def save_scraped_data(data):
    """
    Takes a single product dictionary (from scraper) and saves it to Supabase.
    1. Checks if product exists (by name).
    2. If yes -> Gets ID.
    3. If no -> Creates new Product.
    4. Inserts new Price entry linked to that Product.
    """
    if not data:
        return {"error": "No data to save"}

    try:
        # --- 1. Check if Product Exists ---
        # We query the 'products' table for a matching name
        existing = supabase.table('products').select("id").eq("name", data['name']).execute()
        
        product_id = None

        if existing.data:
            # Product exists, grab its ID
            product_id = existing.data[0]['id']
            print(f"🔄 Product exists: {product_id}")
        else:
            # Product is new, insert it
            new_product = {
                "name": data['name'],
                "brand": "Unknown", # We can improve this later
                "category": "Electronics",
                "image_url": data['image']
            }
            res = supabase.table('products').insert(new_product).execute()
            product_id = res.data[0]['id']
            print(f"🆕 New Product Created: {product_id}")

        # --- 2. Insert Price History ---
        new_price = {
            "product_id": product_id,
            "price_inr": data['price'],
            "site_name": data['source'],
            "product_link": data['url']
        }
        
        supabase.table('prices').insert(new_price).execute()
        print("💰 Price saved successfully!")

        return {"status": "success", "product_id": product_id}

    except Exception as e:
        print(f"🔥 Database Error: {e}")
        return {"error": str(e)}