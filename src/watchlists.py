import sqlite3

conn = sqlite3.connect('aml_system.db')
cursor = conn.cursor()

# Create a Sanctions Watchlist table
cursor.execute("CREATE TABLE IF NOT EXISTS sanctions_list (user_id INTEGER PRIMARY KEY, reason TEXT)")

# Add some "Blacklisted" IDs (let's pick some random ones from your 500 users)
blacklisted_users = [
    (15, "International Fraud Watchlist"),
    (88, "PEP - High Risk Associate"),
    (405, "Suspected Shell Company")
]

cursor.executemany("INSERT OR REPLACE INTO sanctions_list VALUES (?, ?)", blacklisted_users)
conn.commit()
conn.close()
print("Watchlist initialized!")