import streamlit as st
import sqlite3
import pandas as pd

# Page Config
st.set_page_config(page_title="AML Compliance Dashboard", layout="wide")

st.title("🚩 AML Investigation Dashboard")
st.write("Displaying high-risk accounts flagged by the Isolation Forest model.")

# Connect to Database
conn = sqlite3.connect('aml_system.db')

# 1. Metric Summary
st.subheader("System Overview")
col1, col2, col3 = st.columns(3)

total_users = pd.read_sql("SELECT COUNT(*) FROM users", conn).iloc[0,0]
total_alerts = pd.read_sql("SELECT COUNT(*) FROM alerts", conn).iloc[0,0]
total_vol = pd.read_sql("SELECT SUM(total_volume) FROM alerts", conn).iloc[0,0]

col1.metric("Total Users", total_users)
col2.metric("Flagged Alerts", total_alerts, delta="Suspicious", delta_color="inverse")
col3.metric("At-Risk Volume", f"${total_vol:,.2f}")

# 2. Alert Table
st.subheader("Active Alerts")
df_alerts = pd.read_sql("SELECT user_id, country_code, txn_count, total_volume, risk_score FROM alerts ORDER BY total_volume DESC", conn)

# --- FIX START ---
# Shift index to start from 1 instead of 0
df_alerts.index = df_alerts.index + 1

# Display the table only ONCE with the styling
st.dataframe(df_alerts.style.highlight_max(axis=0, subset=['total_volume']), use_container_width=True)
# --- FIX END ---

# Styling the dataframe
st.dataframe(df_alerts.style.highlight_max(axis=0, subset=['total_volume']), use_container_width=True)

# 3. Investigation Tool
st.sidebar.header("🔍 Investigate User")
user_search = st.sidebar.number_input("Enter User ID", min_value=1, max_value=500)

if st.sidebar.button("Fetch Transaction History"):
    history = pd.read_sql(f"SELECT * FROM transactions WHERE sender_id = {user_search}", conn)
    
    if not history.empty:
        st.success(f"Showing results for User_{user_search}")
        st.write(f"### Transaction Log for User_{user_search}")
        # hide_index=True makes it look cleaner, and use_container_width fills the screen
        st.dataframe(history, use_container_width=True, hide_index=True)
    else:
        st.warning(f"No transactions found for User_{user_search}")

conn.close()