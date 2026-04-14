import sqlite3
import pandas as pd

def extract_features():
    conn = sqlite3.connect('aml_system.db')
    query = """
    SELECT 
        u.user_id, 
        u.country_code, 
        u.lat, 
        u.lon,
        COUNT(t.txn_id) as txn_count, 
        SUM(t.amount) as total_volume,
        AVG(t.amount) as avg_txn_amount,
        CASE 
            WHEN u.country_code IN ('KY', 'PA', 'LU', 'AE') THEN 10 
            ELSE 1 
        END as risk_score
    FROM users u
    LEFT JOIN transactions t ON u.user_id = t.sender_id
    GROUP BY u.user_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    features = extract_features()
    print("Features extracted successfully!")
    print(features.head())

query = """
SELECT 
    t.sender_id as user_id,
    u.country_code,
    COUNT(t.id) as txn_count,
    SUM(t.amount) as total_volume,
    CASE 
        WHEN s.user_id IS NOT NULL THEN 100 -- Automatic Max Risk if on Sanctions List
        WHEN u.country_code IN ('KY', 'LU', 'CH') THEN 5 
        ELSE 1 
    END as risk_score
FROM transactions t
JOIN users u ON t.sender_id = u.id
LEFT JOIN sanctions_list s ON t.sender_id = s.id  -- CHECK THE WATCHLIST
GROUP BY t.sender_id
"""