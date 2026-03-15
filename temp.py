import sqlite3
conn = sqlite3.connect('aml_system.db')
# Add columns for Case Management
try:
    conn.execute("ALTER TABLE alerts ADD COLUMN status TEXT DEFAULT 'Pending'")
    conn.execute("ALTER TABLE alerts ADD COLUMN investigator_notes TEXT")
    print("Database updated for Case Management!")
except:
    print("Columns already exist.")
conn.close()