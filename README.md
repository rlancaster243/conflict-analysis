📊 Project Title: Comprehensive Conflict Timeline Analysis (April–May 2025)


🎯 Objective:
To provide a data-driven, geospatial and temporal analysis of the military escalation between India and Pakistan during April–May 2025, using confirmed fatality counts, operation names, and strategic event details — presented interactively via a Streamlit web app.

📦 Core Features:
Verified Event Log

Based on 8 high-profile incidents, each tagged with:

Date

Event Description

Location

Belligerents Involved

Operation Code Name

Confirmed Fatality Counts

Dynamic Filtering UI (via Streamlit Sidebar)

Filter by:

Date range

Belligerent

Operation

Interactive Charts (Plotly-based):

📈 Timeline of daily conflict events

📊 Cumulative fatalities over time

📌 Frequency of military operations

🗺️ Interactive map (Mapbox) of strikes by location and severity

Optional RSS Enrichment

Uses Google News RSS feeds to enrich the dataset with live media reports (toggle with USE_RSS = True)

🛠️ Technical Stack:
Backend: Python (Pandas, datetime)

Frontend/Visualization: Streamlit + Plotly

Optional Data Source: feedparser for Google News RSS

Geolocation: Static lat/lon mappings for known hotspots (e.g., Pahalgam, LoC, Lahore)

🔍 Use Cases:
Conflict monitoring dashboards for NGOs / defense analysts

Event timeline visualization in geopolitical research

Real-time narrative construction with RSS integration

Teaching tool for conflict data science workflows
