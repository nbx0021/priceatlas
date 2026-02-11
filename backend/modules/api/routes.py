from flask import Blueprint, jsonify, request
from modules.scraper.engine import get_price_amazon
from modules.services.db_manager import save_scraped_data

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "PriceAtlas API"})

@api_bp.route('/search', methods=['GET'])
def search_product():
    """
    Example: /api/search?q=iphone+15
    1. Receives query.
    2. Scrapes Amazon.
    3. Saves to DB.
    4. Returns JSON to Frontend.
    """
    query = request.args.get('q')
    
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    print(f"🔎 API received search for: {query}")

    # 1. Run Scraper
    data = get_price_amazon(query)

    if not data:
        return jsonify({"error": "Failed to scrape product"}), 500

    # 2. Save to Database (Async-ish)
    save_result = save_scraped_data(data)

    # 3. Return Combined Result
    return jsonify({
        "result": data,
        "db_status": save_result
    })