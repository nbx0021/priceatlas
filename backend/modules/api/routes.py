from flask import Blueprint, request, jsonify
from modules.scraper.engine import ScraperEngine  # Consumer/Retail
from modules.scraper.b2b_engine import B2BEngine  # 🏭 NEW Wholesale Engine
from modules.services.db_manager import DBManager
from modules.analytics.scorer import calculate_price_score, calculate_volatility
from modules.ml.forecaster import ForecastEngine

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/search', methods=['GET'])
def search_product():
    query = request.args.get('query') or request.args.get('q')
    intent = request.args.get('intent', 'single')
    pincode = request.args.get('pincode', '')
    
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    db = DBManager()

    # --- 🏭 LOGIC: IF WHOLESALE, IGNORE RETAIL & USE B2B ENGINE ---
    if intent in ['wholesale', 'bulk']:
        print(f"🏭 B2B MODE: Ignoring Retailers. Searching B2B for: {query}")
        try:
            b2b_engine = B2BEngine()
            b2b_results = b2b_engine.search_b2b(query)
            
            if not b2b_results:
                return jsonify({"error": "No wholesale suppliers found for this product."}), 404
            
            # Wholesale data is often unstructured (Strings like "₹400/kg"), 
            # so we return it directly as B2B intelligence.
            return jsonify(b2b_results)
        except Exception as e:
            print(f"❌ B2B Engine Error: {e}")
            return jsonify({"error": "Wholesale search failed."}), 500

    # --- 🛒 LOGIC: IF SINGLE, USE STANDARD RETAIL ENGINE ---
    else:
        print(f"🛒 RETAIL MODE: Searching Amazon/Flipkart for: {query}")
        try:
            scraper = ScraperEngine()
            forecaster = ForecastEngine()
            
            all_products = scraper.search_product(query, intent=intent)
            if not all_products:
                return jsonify({"error": "No retail products found."}), 404

            enriched_results = []
            for item in all_products:
                product_id = db.save_product(item)
                
                # Handle DB status for history/forecasting
                if product_id:
                    history = db.get_price_history(product_id)
                    formatted_history = [{"price": h['price_inr']} for h in history]
                else:
                    history, formatted_history = [], []

                score, verdict = calculate_price_score(item['price'], formatted_history)
                volatility = calculate_volatility(formatted_history)
                forecast = forecaster.predict_next_week(history) if history else None

                item['analysis'] = {
                    'score': score,
                    'verdict': verdict,
                    'volatility': volatility,
                    'history_count': len(history),
                    'price_history': history,
                    'forecast': forecast
                }
                enriched_results.append(item)

            return jsonify(enriched_results)

        except Exception as e:
            print(f"❌ Retail Engine Error: {e}")
            return jsonify({"error": "Retail search failed."}), 500