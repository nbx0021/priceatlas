
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("❌ Supabase keys not found in .env file!")

# Create the connection
supabase: Client = create_client(url, key)

print("✅ Connected to Supabase!")