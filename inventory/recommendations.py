import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("data/processed", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

def generate_inventory_recommendations():
    print("Building Day 20 Inventory Recommendation Engine...")
    
    # Load Forecast Data (Fallback to Prophet or LightGBM or synthetic)
    forecast_path = "data/processed/forecast_prophet.csv"
    if not os.path.exists(forecast_path):
        forecast_path = "data/processed/forecast_lightgbm.csv"
        
    if os.path.exists(forecast_path):
        forecast_df = pd.read_csv(forecast_path)
    else:
        dates = pd.date_range(start=pd.Timestamp.today(), periods=30, freq='D')
        forecast_df = pd.DataFrame({
            "ds": dates,
            "forecast_sales": np.random.normal(20000, 1500, 30)
        })
        
    # Load Sales / Inventory Data for Product-level details
    db_path = "data/warehouse.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        items_df = pd.read_sql("SELECT DISTINCT item_id, store_id FROM fact_sales LIMIT 20", conn)
        conn.close()
        items_df['category_id'] = items_df['item_id'].apply(lambda x: str(x).split('_')[0] if '_' in str(x) else 'FOODS')
    else:
        items = [f"FOODS_3_{i:03d}" for i in range(1, 21)]
        items_df = pd.DataFrame({"item_id": items, "category_id": "FOODS", "store_id": "CA_1"})

    # Business Parameters
    SERVICE_LEVEL_Z = 1.65 # 95% service level
    LEAD_TIME_DAYS = 7     # Supplier lead time in days
    
    # Calculate aggregate forecast statistics
    total_30_day_forecast = forecast_df['forecast_sales'].sum()
    avg_daily_forecast = forecast_df['forecast_sales'].mean()
    forecast_std = forecast_df['forecast_sales'].std()
    
    recommendations = []
    
    np.random.seed(42)
    for idx, row in items_df.iterrows():
        item_id = row['item_id']
        category_id = row.get('category_id', 'FOODS')
        store_id = row.get('store_id', 'CA_1')
        
        # Product daily demand distribution
        item_weight = np.random.uniform(0.02, 0.10)
        item_avg_daily_demand = avg_daily_forecast * item_weight
        item_demand_std = forecast_std * item_weight
        item_30day_forecast = total_30_day_forecast * item_weight
        
        # 1. Safety Stock Calculation: SS = Z * sigma * sqrt(Lead Time)
        safety_stock = int(np.ceil(SERVICE_LEVEL_Z * item_demand_std * np.sqrt(LEAD_TIME_DAYS)))
        
        # 2. Reorder Point Calculation: ROP = (Average Daily Demand * Lead Time) + Safety Stock
        lead_time_demand = item_avg_daily_demand * LEAD_TIME_DAYS
        reorder_point = int(np.ceil(lead_time_demand + safety_stock))
        
        # Simulated Current Stock Level
        current_stock = int(np.random.uniform(0.3 * reorder_point, 2.5 * reorder_point))
        
        # 3. Recommended Restock Quantity: Order = max(0, ROP + 30-Day Forecast - Current Stock)
        target_stock_level = reorder_point + int(item_30day_forecast)
        restock_quantity = max(0, target_stock_level - current_stock)
        
        # 4. Inventory Status Classification
        if current_stock <= safety_stock:
            status = "CRITICAL_STOCKOUT_RISK"
            action = "EMERGENCY_REORDER"
        elif current_stock <= reorder_point:
            status = "LOW_STOCK"
            action = "REORDER_NOW"
        elif current_stock > (reorder_point + item_30day_forecast):
            status = "OVERSTOCKED"
            action = "HOLD_ORDERS"
        else:
            status = "OPTIMAL"
            action = "MONITOR"
            
        recommendations.append({
            "item_id": item_id,
            "category_id": category_id,
            "store_id": store_id,
            "avg_daily_demand": round(item_avg_daily_demand, 2),
            "forecast_30d": int(np.round(item_30day_forecast)),
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "current_stock": current_stock,
            "recommended_restock": restock_quantity,
            "inventory_status": status,
            "recommended_action": action
        })
        
    rec_df = pd.DataFrame(recommendations)
    
    # Save CSV
    rec_df.to_csv("data/processed/inventory_recommendations.csv", index=False)
    print("Saved recommendations to data/processed/inventory_recommendations.csv")
    
    # Save SQLite Table
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        rec_df.to_sql("inventory_recommendations", conn, if_exists="replace", index=False)
        conn.close()
        print("Stored recommendations to SQLite table `inventory_recommendations`.")
        
    # Generate Inventory Recommendation Visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(rec_df))
    width = 0.25
    
    ax.bar(x - width, rec_df['current_stock'], width, label='Current Stock', color='dodgerblue')
    ax.bar(x, rec_df['reorder_point'], width, label='Reorder Point (ROP)', color='orange')
    ax.bar(x + width, rec_df['safety_stock'], width, label='Safety Stock (SS)', color='crimson')
    
    ax.set_xticks(x)
    ax.set_xticklabels(rec_df['item_id'], rotation=45, ha='right', fontsize=9)
    ax.set_title("Inventory Status: Current Stock vs Reorder Point & Safety Stock")
    ax.set_ylabel("Units")
    ax.legend()
    plt.tight_layout()
    plt.savefig("reports/figures/inventory_recommendations.png")
    plt.close()
    print("Saved inventory status chart to reports/figures/inventory_recommendations.png")

if __name__ == "__main__":
    generate_inventory_recommendations()
