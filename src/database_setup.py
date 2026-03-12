import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('aml_system.db')
cursor = conn.cursor()

# 1. Create the Users table (KYC data)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    risk_level TEXT, -- 'Low', 'Medium', 'High' (e.g. PEPs)
    country_code TEXT
)
''')

# 2. Create the Transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    amount REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    method TEXT, -- 'Wire', 'Cash', 'Crypto'
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
)
''')

conn.commit()
print("Database and AML tables created successfully!")

import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('aml_system.db')

# 1. Create 500 Random Users
users = []
for i in range(1, 501):
    risk = random.choices(['Low', 'Medium', 'High'], weights=[80, 15, 5])[0]
    users.append((i, f"User_{i}", risk, random.choice(['US', 'GB', 'KY', 'LU', 'CH'])))

conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users)

# 2. Generate 9,900 Normal Transactions with Random Timestamps
txns = []
base_date = datetime.now()

for _ in range(9900):
    s, r = random.sample(range(1, 501), 2)
    amt = round(random.uniform(10, 2000), 2)
    # Generate a random offset within the last 30 days
    random_days = random.randint(0, 30)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    txn_time = base_date - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
    
    txns.append((s, r, amt, 'Wire', txn_time.strftime('%Y-%m-%d %H:%M:%S')))

# 3. Inject 100 Anomalous Transactions
# Pattern: Structuring (All happening very close together in time)
for _ in range(50):
    s, r = 99, 100
    amt = round(random.uniform(9000, 9999), 2)
    # These happen within the same hour to simulate "Rapid Movement"
    txn_time = base_date - timedelta(minutes=random.randint(1, 60))
    txns.append((s, r, amt, 'Cash', txn_time.strftime('%Y-%m-%d %H:%M:%S')))

# Pattern: Rapid Outflow
for _ in range(50):
    s = 400
    r = random.randint(1, 50)
    amt = 50000.00
    txn_time = base_date - timedelta(days=1, minutes=random.randint(1, 120))
    txns.append((s, r, amt, 'Crypto', txn_time.strftime('%Y-%m-%d %H:%M:%S')))

# Update the INSERT statement to include the timestamp
conn.executemany("INSERT INTO transactions (sender_id, receiver_id, amount, method, timestamp) VALUES (?, ?, ?, ?, ?)", txns)

conn.commit()
print("Data Injection Complete: 10,000 records added.")