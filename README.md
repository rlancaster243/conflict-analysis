# 📊 Comprehensive Conflict Timeline Analysis (April–May 2025)

## 🎯 Objective
To provide a **data-driven, geospatial and temporal analysis** of the military escalation between India and Pakistan during April–May 2025. The project combines confirmed fatality data, strategic incident summaries, and interactive visualizations — deployed as a Streamlit web application.

---

## 📦 Core Features

### ✅ Verified Event Log
Based on 8 confirmed incidents, each tagged with:
- `Date`
- `Event Description`
- `Location`
- `Belligerents`
- `Operation Code Name`
- `Confirmed Fatality Counts`

### 🎛️ Dynamic Filtering (via Streamlit Sidebar)
- Filter events by:
  - Date range
  - Belligerent
  - Operation name

### 📊 Interactive Visualizations
- **Daily Event Timeline**: Line chart showing number of incidents per day
- **Cumulative Fatalities**: Area chart of confirmed deaths over time
- **Operation Frequency**: Bar chart of incidents by operation
- **Geospatial Map**: Mapbox scatter plot of strike locations (color/size = fatalities)

### 📰 Optional RSS Enrichment *(toggle `USE_RSS = True`)*
- Pulls relevant live articles from Google News RSS
- Adds recent titles & URLs as context-rich event entries

---

## 🛠️ Technical Stack

| Component    | Library/Tool            |
|--------------|--------------------------|
| Backend      | Python, Pandas, datetime |
| Frontend     | Streamlit                |
| Visualization| Plotly Express           |
| Mapping      | Mapbox (OpenStreetMap)   |
| RSS Feeds    | `feedparser` *(optional)*|

---

## 🔍 Use Cases
- Conflict escalation dashboards for NGOs or defense analysts
- Geopolitical timeline visualization
- Real-time media correlation (RSS mode)
- Teaching use cases for geospatial data science

---

## 🚀 How to Run

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Launch the app:

    ```bash
    streamlit run conflict_timeline_streamlit_app.py
    ```

3. *(Optional)*: Flip `USE_RSS = True` inside the script to enable live news enrichment.

---

