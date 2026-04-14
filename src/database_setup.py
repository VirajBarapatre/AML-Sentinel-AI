import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('aml_system.db')
cursor = conn.cursor()

# 1. NEW TABLE SCHEMA: Added City, Lat, and Lon
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS transactions')

cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    risk_level TEXT,
    country_code TEXT,
    city TEXT,
    lat REAL,
    lon REAL
)
''')

cursor.execute('''
CREATE TABLE transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    amount REAL,
    timestamp DATETIME,
    method TEXT,
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
)
''')

# 2. GLOBAL CITY REPOSITORY (Exact Coordinates)
city_data = [
    ("New York", "US", 40.7128, -74.0060),
    ("London", "GB", 51.5074, -0.1278),
    ("Mumbai", "IN", 19.0760, 72.8777),
    ("George Town", "KY", 19.3000, -81.3833),
    ("Dubai", "AE", 25.2048, 55.2708),
    ("Singapore", "SG", 1.3521, 103.8198),
    ("Zurich", "CH", 47.3769, 8.5417),
    ("Hong Kong", "HK", 22.3193, 114.1694),
    ("Luxembourg City", "LU", 49.6116, 6.1319),
    ("Panama City", "PA", 8.9833, -79.5167)
]

# 3. GENERATE 2,000 GLOBAL USERS
users = []
for i in range(1, 2001):
    city_choice = random.choice(city_data)
    risk = random.choices(['Low', 'Medium', 'High'], weights=[85, 12, 3])[0]
    
    # Add small random offset so markers don't stack exactly on top of each other
    lat_offset = city_choice[2] + random.uniform(-0.05, 0.05)
    lon_offset = city_choice[3] + random.uniform(-0.05, 0.05)
    
    users.append((i, f"User_{i}", risk, city_choice[1], city_choice[0], lat_offset, lon_offset))

conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", users)

# 4. GENERATE 15,000 TRANSACTIONS (Normal + Anomalous)
txns = []
base_date = datetime.now()

# Normal Traffic
for _ in range(14800):
    s, r = random.sample(range(1, 2001), 2)
    amt = round(random.uniform(50, 3000), 2)
    txn_time = base_date - timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1440))
    txns.append((s, r, amt, txn_time.strftime('%Y-%m-%d %H:%M:%S'), 'Wire'))

# --- INJECTING GLOBAL ANOMALIES ---

# Pattern 1: Cayman Islands Hub (User 400 - Large Crypto Outflows)
for _ in range(100):
    # Let's force User 400 to be in George Town, KY for this pattern
    s, r = 400, random.randint(1, 2000)
    amt = round(random.uniform(20000, 50000), 2)
    txn_time = base_date - timedelta(days=2, minutes=random.randint(1, 500))
    txns.append((s, r, amt, txn_time.strftime('%Y-%m-%d %H:%M:%S'), 'Crypto'))

# Pattern 2: Dubai Structuring (User 88 - Rapid Cash Deposits)
for _ in range(100):
    s, r = 88, 1  # Routing to a single offshore entity
    amt = round(random.uniform(9000, 9999), 2) # Structuring under 10k limit
    txn_time = base_date - timedelta(minutes=random.randint(1, 120))
    txns.append((s, r, amt, txn_time.strftime('%Y-%m-%d %H:%M:%S'), 'Cash'))

conn.executemany("INSERT INTO transactions (sender_id, receiver_id, amount, timestamp, method) VALUES (?, ?, ?, ?, ?)", txns)

conn.commit()
print(f"✅ Success! 2,000 Global Users and 15,000 transactions created with Geo-coordinates.")
conn.close()