import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
# Ensure your extract_features() in feature_eng.py is updated to pull 'lat' and 'lon' from the users table!

def run_anomaly_detection():
    # 1. Get features (Now including Lat/Lon from the new DB setup)
    # Ensure your SQL query inside extract_features() JOINs the users table to get lat/lon
    from feature_eng import extract_features 
    df = extract_features()
    
    # 2. Select numerical columns + Geospatial data
    # We add lat/lon so the AI can learn geographic clusters of fraud
    model_features = [
        'txn_count', 
        'total_volume', 
        'avg_txn_amount', 
        'risk_score', 
        'lat', 
        'lon'
    ]
    X = df[model_features]
    
    # 3. Initialize the Isolation Forest
    # Contamination 0.02 = flag top 2% (approx 40 users out of 2000)
    model = IsolationForest(contamination=0.02, random_state=42)
    
    # 4. Predict
    df['is_anomaly'] = model.fit_predict(X)
    
    # 5. Filter only suspicious accounts
    alerts = df[df['is_anomaly'] == -1].copy()
    
    # NEW: Add a default 'status' column for your dashboard's Case Management
    if 'status' not in alerts.columns:
        alerts['status'] = 'Pending'
    
    # 6. Save back to SQLite
    conn = sqlite3.connect('aml_system.db')
    alerts.to_sql('alerts', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"✅ AI Analysis Complete! {len(alerts)} suspicious accounts flagged globally.")
    print("Coordinates and risk vectors saved to 'alerts' table.")

if __name__ == "__main__":
    run_anomaly_detection()