import numpy as np
import statistics

def calculate_price_score(current_price, price_history):
    """
    Analyzes the current price against historical data to give a 0-100 score.
    Score 100 = All time low (Best Deal).
    Score 0 = All time high (Worst Deal).
    """
    if not price_history or len(price_history) < 2:
        return 50, "Not enough data"  # Neutral score if no history

    # 1. Extract prices from history objects
    prices = [record['price'] for record in price_history if record.get('price')]
    
    if not prices:
        return 50, "No valid prices"

    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices) / len(prices)

    # 2. Avoid division by zero
    if max_price == min_price:
        return 50, "Stable Price"

    # 3. Calculate Score Formula: (Max - Current) / (Max - Min) * 100
    # Logic: If current == min, numerator is (Max - Min), so score is 100.
    raw_score = ((max_price - current_price) / (max_price - min_price)) * 100
    
    # Clamp score between 0 and 100
    final_score = max(0, min(100, int(raw_score)))

    # 4. Generate Verdict
    if final_score >= 85:
        verdict = "🔥 Great Deal"
    elif final_score >= 60:
        verdict = "✅ Good Price"
    elif final_score >= 40:
        verdict = "⚠️ Fair Price"
    else:
        verdict = "🛑 Overpriced"

    return final_score, verdict




def calculate_volatility(history):
    """
    Calculates the Volatility Score (Standard Deviation) as per PRD.
    """
    if len(history) < 2:
        return 0
    
    try:
        prices = [h.get('price', 0) for h in history]
        # Calculate standard deviation
        stdev = statistics.stdev(prices)
        # Normalize to a 0-100 scale (relative to the average price)
        avg = sum(prices) / len(prices)
        volatility_index = (stdev / avg) * 100 if avg > 0 else 0
        return round(min(volatility_index, 100), 2)
    except:
        return 0