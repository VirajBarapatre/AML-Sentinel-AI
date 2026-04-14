🌐 AML Sentinel: End-to-End AI Financial Intelligence
AML Sentinel is a sophisticated Anti-Money Laundering (AML) platform designed to detect, visualize, and manage global financial risks. The system integrates a full-stack data pipeline—from synthetic transaction generation to unsupervised anomaly detection and geospatial intelligence.

📁 Project Structure
The project is organized into a modular pipeline:

database_setup.py: Initializes the SQLite RDBMS and generates 2,000+ global users with high-fidelity geospatial coordinates.

feature_eng.py: Processes raw transaction logs into behavioral vectors (e.g., velocity, structuring indicators, and jurisdictional risk).

model_engine.py: The AI core. Utilizes an Isolation Forest model to identify statistical outliers in financial behavior.

watchlists.py: Manages global sanctions lists and PEP (Politically Exposed Persons) screening logic.

dashboard.py: The interactive Streamlit frontend featuring high-resolution PyDeck heatmaps and case management tools.

🚀 Key Features
1. Advanced Geospatial Heatmapping
Uses a dual-layer PyDeck implementation to visualize risk density:

Logarithmic Intensity: Ensures visibility of emerging risks in smaller markets (e.g., Mumbai) without them being "drowned out" by high-volume hubs like Luxembourg.

Interactive Tooltips: Deep-dive into specific alerts on hover to see User IDs, Risk Scores, and Last Activity Timestamps.

2. AI-Driven Detection Engine
Moving beyond simple rule-based thresholds, the engine identifies complex criminal patterns:

Structuring (Smurfing): Detecting multiple transactions designed to stay just beneath reporting limits.

Rapid Outflows: Flagging high-velocity movements to offshore jurisdictions.

3. Case Management Workflow
Real-time Investigation: Search by User ID to pull a complete transaction "Case File."

Persistent Governance: Update alert statuses (Pending -> Under Review -> SAR) directly from the UI with database persistence.

🛠️ Tech Stack
Language: Python 3.9+

Machine Learning: Scikit-Learn (Isolation Forest)

Data Science: Pandas, NumPy

Database: SQLite3

Visuals: PyDeck (Deck.gl), Streamlit

Map Tiles: CartoDB (Dark Matter)

📋 Quick Start Guide
Environment Setup:

Bash
pip install streamlit pandas scikit-learn pydeck
Initialize Data:

Bash
python src/database_setup.py
Train AI Model:

Bash
python src/model_engine.py
Launch Intelligence Dashboard:

Bash
streamlit run src/dashboard.py
⚖️ Disclaimer
This project is a high-fidelity simulation developed for financial technology research and portfolio demonstration. All data generated is synthetic.