🌐 AML Sentinel: Global Geospatial Financial Intelligence
AML Sentinel is a high-fidelity Anti-Money Laundering (AML) platform designed to detect, visualize, and investigate financial crimes across a global scale. The system utilizes Unsupervised Machine Learning to flag anomalies and High-Resolution Geospatial Mapping to provide investigators with actionable intelligence.

🚀 Key Features
AI-Driven Detection: Implements an Isolation Forest model to identify "outlier" behavior in a dataset of 15,000+ transactions.

Geospatial "Glow" Mapping: A dual-layer 3D/Heatmap visualization that normalizes risk intensity, ensuring visibility for both massive offshore flows and smaller regional "smurfing" patterns.

Case Management System: A persistent investigator workflow allowing for status updates (Pending, Under Review, SAR), sanctions checking, and CSV evidence extraction.

Industry-Standard Schemas: Utilizes a relational SQLite database with structured KYC (Know Your Customer) and transaction logs.

🏗️ Technical Architecture
1. Data Layer (database_setup.py)
Generates a realistic global environment with 2,000 users across 10+ international financial hubs.

Coordinates: Precise City-level Lat/Lon mapping.

Synthetic Patterns: Injects specific laundering behaviors like Structuring (transactions under $10k) and Rapid Outflows (high-volume crypto transfers).

2. AI Engine (model_engine.py)
The "Brain" of the system. It processes a multi-dimensional feature vector:

[Transaction Count, Total Volume, Avg Amount, Risk Score, Latitude, Longitude]

By including Geospatial coordinates in the ML training, the model learns to identify "Jurisdictional Risk" as an anomaly factor.

3. Intelligence Dashboard (dashboard.py)
Built with Streamlit and PyDeck, featuring:

Logarithmic Heatmap: Uses a color_domain cap to prevent high-volume outliers (like Luxembourg) from drowning out smaller alerts (like Mumbai).

Invisible Sensor Layer: A transparent ScatterplotLayer that enables high-performance tooltips, showing User ID, Risk Score, and Timestamp on hover.

🛠️ Tech Stack
Language: Python 3.9+

Machine Learning: Scikit-Learn (Isolation Forest)

Database: SQLite3

Visualization: PyDeck (Deck.gl), Pandas, Streamlit

Map Styles: CartoDB Dark Matter

📋 Installation & Setup
1. Clone the repository and install dependencies:
Bash
pip install streamlit pandas scikit-learn pydeck
2. Initialize the Global Database:
Bash
python database_setup.py
3. Run the AI Detection Engine:
Bash
python model_engine.py
4. Launch the Dashboard:
Bash
streamlit run dashboard.py
🛡️ Investigative Use Cases
This dashboard is pre-configured to detect and visualize three primary risk types:

The Tax Haven Hub: Large volume spikes in jurisdictions like the Cayman Islands or Panama.

The Structuring Pattern: Dozens of transactions just below $10,000 to evade automated reporting triggers.

The Rapid Mover: Users with high-velocity crypto outflows in cities like Dubai or Singapore.