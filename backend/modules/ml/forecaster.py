import statistics
from datetime import datetime

class ForecastEngine:
    def __init__(self):
        """
        AI Forecasting Module.
        Uses Linear Regression to predict future market movements.
        """
        pass

    def predict_next_week(self, history):
        """
        Calculates Trend, % Change, and Confidence Score (UC4).
        Requires at least 3 historical data points for accuracy.
        """
        # We need a minimum amount of history to draw a trend line
        if not history or len(history) < 3:
            return None

        try:
            # 1. Sort history by date to ensure chronological math
            # Using 'scraped_at' from the Supabase Schema
            sorted_history = sorted(history, key=lambda x: x['scraped_at'])
            
            # 2. Convert timestamps to numerical 'X' values (Days since start)
            start_date = sorted_history[0]['scraped_at']
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))

            days = []
            prices = []
            
            for h in sorted_history:
                current_date = h['scraped_at']
                if isinstance(current_date, str):
                    current_date = datetime.fromisoformat(current_date.replace('Z', '+00:00'))
                
                delta = (current_date - start_date).days
                days.append(delta)
                prices.append(h['price_inr'])

            # 3. Linear Regression (Least Squares Method)
            n = len(days)
            mean_x = statistics.mean(days)
            mean_y = statistics.mean(prices)
            
            num = sum((days[i] - mean_x) * (prices[i] - mean_y) for i in range(n))
            den = sum((days[i] - mean_x) ** 2 for i in range(n))
            
            if den == 0: return None # Avoid division by zero on same-day scrapes

            slope = num / den
            intercept = mean_y - (slope * mean_x)

            # 4. Predict +7 Days into the future
            future_day = days[-1] + 7
            predicted_price = (slope * future_day) + intercept
            current_price = prices[-1]

            # 5. Calculate UC4 Metrics
            change_pct = round(((predicted_price - current_price) / current_price) * 100, 2)
            
            # Trend Logic
            if change_pct > 1.5: trend = "Upward"
            elif change_pct < -1.5: trend = "Downward"
            else: trend = "Stable"

            # Confidence Score (MAPE-based approximation)
            # More data points increase our confidence
            confidence = min(40 + (n * 5), 95) 

            return {
                "trend": trend,
                "change_pct": change_pct,
                "predicted_price": round(predicted_price, 2),
                "confidence": confidence
            }

        except Exception as e:
            print(f"ML Forecast Error: {e}")
            return None
