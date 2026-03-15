import streamlit as st
import sqlite3
import pandas as pd

# Page Config
st.set_page_config(page_title="AML Compliance Dashboard", layout="wide")

st.title("AML Investigation Dashboard")
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

# 1.5. Transaction Trend Chart
st.subheader("Global Transaction Activity")
# Pull volume grouped by day
trend_query = """
SELECT date(timestamp) as date, SUM(amount) as daily_vol 
FROM transactions 
GROUP BY date(timestamp)
"""
df_trend = pd.read_sql(trend_query, conn)
df_trend = df_trend.set_index('date')

# Display a line chart
st.line_chart(df_trend)

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

# 3. Industry-Level Case Management Tool
st.sidebar.header("🔍 Case Investigation")
user_search = st.sidebar.number_input("Enter User ID", min_value=1, max_value=500)

if st.sidebar.button("Fetch Case File"):
    history = pd.read_sql(f"SELECT * FROM transactions WHERE sender_id = {user_search}", conn)
    user_meta = pd.read_sql(f"SELECT * FROM alerts WHERE user_id = {user_search}", conn)
    
    if not history.empty:
        st.success(f"Case File Opened for User_{user_search}")
        
        # Action Panel
        st.subheader("🛠️ Investigator Actions")
        col_a, col_b = st.columns(2)
        
        with col_a:
            new_status = st.selectbox("Update Status", ["Pending", "Under Review", "Resolved - No Fraud", "Reported (SAR)"])
            if st.button("Update Database"):
                conn.execute(f"UPDATE alerts SET status = '{new_status}' WHERE user_id = {user_search}")
                conn.commit()
                st.toast(f"Status updated to {new_status}!")

        with col_b:
            # The "SAR" Download Button
            csv = history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download SAR Evidence (CSV)",
                data=csv,
                file_name=f"SAR_Report_User_{user_search}.csv",
                mime='text/csv',
            )

        # Charts and Logs
        st.write("---")
        st.write(f"### 📈 Activity Trend for User_{user_search}")
        user_trend = history.copy()
        user_trend['date'] = pd.to_datetime(user_trend['timestamp']).dt.date
        st.line_chart(user_trend.groupby('date')['amount'].sum())
        
        st.write("### 📋 Transaction Evidence Log")
        st.dataframe(history, use_container_width=True, hide_index=True)
    else:
        st.warning("No transactions found.")
conn.close()