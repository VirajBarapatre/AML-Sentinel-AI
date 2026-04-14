import streamlit as st
import sqlite3
import pandas as pd
import pydeck as pdk

# 1. Page Config
st.set_page_config(page_title="Global AML Intelligence", layout="wide")

st.title("🌐 Global AML Intelligence Dashboard")
st.write("Real-time geospatial monitoring of high-risk financial flows.")

# 2. Connect to Database
conn = sqlite3.connect('aml_system.db')

# 3. Metric Summary
st.subheader("System Overview")
col1, col2, col3 = st.columns(3)

try:
    total_users = pd.read_sql("SELECT COUNT(*) FROM users", conn).iloc[0,0]
    total_alerts = pd.read_sql("SELECT COUNT(*) FROM alerts", conn).iloc[0,0]
    total_vol = pd.read_sql("SELECT SUM(total_volume) FROM alerts", conn).iloc[0,0]

    col1.metric("Total Global Users", f"{total_users:,}")
    col2.metric("Flagged Alerts", total_alerts, delta="High Risk", delta_color="inverse")
    col3.metric("At-Risk Volume", f"${total_vol:,.2f}")
except:
    st.error("Database table 'alerts' not found. Please run your model_engine.py first.")

# 4. GEOSPATIAL RISK VISUALIZATION
st.subheader("🏙️ Global Risk Intelligence Map")

# NEW QUERY: Fetch individual alert details to show in tooltip
map_query = """
    SELECT 
        u.lat, u.lon, u.city, 
        a.user_id, a.total_volume as vol, a.risk_score,
        (SELECT timestamp FROM transactions WHERE sender_id = a.user_id ORDER BY timestamp DESC LIMIT 1) as last_seen
    FROM alerts a 
    JOIN users u ON a.user_id = u.user_id
"""
df_map = pd.read_sql(map_query, conn)

# HEATMAP LAYER: Optimized for global visibility
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=df_map,
    get_position="[lon, lat]",
    get_weight="vol",
    radius_pixels=35,      # Smaller, sharper blobs
    intensity=2,           # Higher intensity to make Mumbai/smaller cities pop
    threshold=0.01,        # Ultra-low threshold so small risks aren't hidden
    color_range=[
        [255, 255, 178], [254, 217, 118], [254, 178, 76],
        [253, 141, 60],  [240, 59, 32],   [189, 0, 38]
    ]
)

# SENSOR LAYER: Provides the detailed Tooltip
sensor_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_map,
    get_position="[lon, lat]",
    get_radius=80000, 
    get_fill_color=[0, 0, 0, 0], 
    pickable=True,
)

st.pydeck_chart(pdk.Deck(
    map_style='https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    initial_view_state=pdk.ViewState(latitude=20, longitude=70, zoom=1.8), # Start near Mumbai/Asia
    layers=[heatmap_layer, sensor_layer],
    tooltip={
        "html": """
            <div style="background:#1a1a1a; padding:12px; border-radius:8px; border: 1px solid #ff4b4b; line-height:1.6;">
                <b style="color:#ff4b4b; font-size:14px;">📍 {city}</b><br/>
                <hr style="margin:5px 0; border:0.5px solid #333;">
                <b>User ID:</b> {user_id}<br/>
                <b>Risk Vol:</b> <span style="color:#ff4b4b;">${vol}</span><br/>
                <b>Risk Score:</b> {risk_score}<br/>
                <b>Last Activity:</b> <span style="font-size:11px; color:#aaa;">{last_seen}</span>
            </div>
        """,
        "style": {"color": "white"}
    }
))

# 5. Transaction Trend Chart
st.subheader("📈 Global Transaction Activity")
trend_query = "SELECT date(timestamp) as date, SUM(amount) as daily_vol FROM transactions GROUP BY date(timestamp)"
df_trend = pd.read_sql(trend_query, conn)
df_trend = df_trend.set_index('date')
st.line_chart(df_trend)

# 6. Alert Table
st.subheader("⚠️ Active Alerts")
df_alerts = pd.read_sql("SELECT user_id, country_code, txn_count, total_volume, risk_score, status FROM alerts ORDER BY total_volume DESC", conn)
df_alerts.index = df_alerts.index + 1
st.dataframe(df_alerts.style.highlight_max(axis=0, subset=['total_volume']), use_container_width=True)

# 7. Sidebar Case Investigation
st.sidebar.header("🔍 Case Investigation")
user_search = st.sidebar.number_input("Enter User ID", min_value=0, max_value=2000, value=0)
fetch_button = st.sidebar.button("Fetch Case File")

if fetch_button or user_search > 0:
    u_id = user_search
    history = pd.read_sql(f"SELECT * FROM transactions WHERE sender_id = {u_id}", conn)
    alert_data = pd.read_sql(f"SELECT status FROM alerts WHERE user_id = {u_id}", conn)
    
    if not history.empty:
        st.divider()
        st.success(f"Case File Opened for User_{u_id}")
        
        if not alert_data.empty:
            current_stat = alert_data.iloc[0,0]
            st.subheader("🛠️ Investigator Actions")
            col_a, col_b = st.columns(2)
            with col_a:
                with st.form(key=f"status_form_{u_id}"):
                    st.write(f"**Current Status:** `{current_stat}`")
                    new_status = st.selectbox("Update Status", ["Pending", "Under Review", "Resolved - No Fraud", "Reported (SAR)"])
                    if st.form_submit_button("Commit to Database"):
                        cursor = conn.cursor()
                        cursor.execute("UPDATE alerts SET status = ? WHERE user_id = ?", (new_status, u_id))
                        conn.commit()
                        st.toast("Database Updated!")
                        st.rerun()
            with col_b:
                csv = history.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download Evidence", data=csv, file_name=f"User_{u_id}_History.csv")
        
        st.write("### 📋 Transaction Log")
        st.dataframe(history, use_container_width=True, hide_index=True)
    elif user_search > 0:
        st.warning(f"No transactions found for User_{u_id}")

conn.close()