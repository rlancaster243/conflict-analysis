# conflict_timeline_streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ---------------------------------------------------------------------------
# PARAMETERS
# ---------------------------------------------------------------------------
USE_RSS = False  # toggle live Google‑News enrichment
MAPBOX_TOKEN = ""  # optional Mapbox token for high‑detail tiles
KEYWORDS = [
    "Pahalgam attack Kashmir 26 tourists",
    "Operation Sindoor May 2025 civilian deaths",
    "LoC artillery clash May 9 2025 casualties",
    "Operation Bunyan al-Marsus May 2025",
]

# ---------------------------------------------------------------------------
# DATA SEEDING
# ---------------------------------------------------------------------------

def seed_base_events() -> pd.DataFrame:
    data = {
        "Date": [
            "2025-04-22",
            "2025-05-07",
            "2025-05-07",
            "2025-05-08",
            "2025-05-09",
            "2025-05-10",
            "2025-05-10",
            "2025-05-11",
        ],
        "Event": [
            "Pahalgam militant attack",
            "Operation Sindoor missile strike",
            "Pak claims of shooting Indian jets",
            "Drone & missile exchange",
            "LoC artillery duel",
            "Operation Bunyan al‑Marsus (Pak retaliation)",
            "Post‑ceasefire Jammu/Srinagar blasts",
            "Pak briefing – claims 5 Indian KIA",
        ],
        "Location": [
            "Pahalgam",
            "Multiple (AJK/Punjab)",
            "Not specified",
            "Lahore / Amritsar axis",
            "LoC arc",
            "Various Indian bases",
            "Jammu & Srinagar",
            "Not disclosed",
        ],
        "Belligerent": [
            "The Resistance Front",
            "India",
            "Pakistan",
            "India & Pakistan",
            "India & Pakistan",
            "Pakistan",
            "Unknown",
            "Pakistan",
        ],
        "Operation": [
            "None",
            "Operation Sindoor",
            "None",
            "None",
            "None",
            "Operation Bunyan al‑Marsus",
            "None",
            "Operation Bunyan al‑Marsus",
        ],
        "Killed": [26, 31, 0, 1, 5, 0, 0, 5],
    }
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# ---------------------------------------------------------------------------
# OPTIONAL RSS (disabled by default)
# ---------------------------------------------------------------------------
if USE_RSS:
    import feedparser

    def fetch_rss_hits(keyword: str, limit: int = 5):
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}")
        for entry in feed.entries[:limit]:
            yield pd.to_datetime(entry.published), entry.title, entry.link

    def enrich_with_rss(df: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for kw in KEYWORDS:
            for date_val, title, url in fetch_rss_hits(kw):
                rows.append({
                    "Date": date_val,
                    "Event": title,
                    "Location": "RSS‑N/A",
                    "Belligerent": "TBD",
                    "Operation": "TBD",
                    "Killed": 0,
                    "SourceURL": url,
                })
        return pd.concat([df, pd.DataFrame(rows)], ignore_index=True) if rows else df
else:
    def enrich_with_rss(df: pd.DataFrame) -> pd.DataFrame:  # noqa: D401
        return df

# ---------------------------------------------------------------------------
# GEO COORD LOOKUP
# ---------------------------------------------------------------------------
COORDS = {
    "Pahalgam": (34.0161, 75.3150),
    "Lahore / Amritsar axis": (31.6, 74.8),
    "LoC arc": (34.1, 74.0),
    "Various Indian bases": (23.5, 78.5),
    "Jammu & Srinagar": (33.5, 75.1),
    "Multiple (AJK/Punjab)": (32.8, 73.8),
    "Not specified": (31.0, 74.0),
    "Not disclosed": (30.0, 70.0),
}

# ---------------------------------------------------------------------------
# PLOTTING HELPERS
# ---------------------------------------------------------------------------

def timeline_chart(df: pd.DataFrame):
    counts = df.groupby("Date").size().rename("Events")
    fig = px.line(counts, y="Events", markers=True, title="Daily Event Count")
    fig.update_layout(xaxis_title="Date", yaxis_title="Number of Events")
    return fig


def cumulative_chart(df: pd.DataFrame):
    ser = df.groupby("Date")["Killed"].sum().sort_index().cumsum()
    fig = px.area(ser, title="Cumulative Confirmed Fatalities")
    fig.update_layout(xaxis_title="Date", yaxis_title="Cumulative Killed")
    return fig


def operation_chart(df: pd.DataFrame):
    data = df["Operation"].value_counts().reset_index(name="Count")
    data.columns = ["Operation", "Count"]
    fig = px.bar(data, x="Operation", y="Count", title="Events per Operation")
    fig.update_layout(xaxis_title="Operation", yaxis_title="Event Count")
    return fig


def map_chart(df: pd.DataFrame):
    if MAPBOX_TOKEN:
        px.set_mapbox_access_token(MAPBOX_TOKEN)
    geo_df = df.copy()
    geo_df["lat"] = geo_df["Location"].map(lambda x: COORDS.get(x, (None, None))[0])
    geo_df["lon"] = geo_df["Location"].map(lambda x: COORDS.get(x, (None, None))[1])
    geo_df = geo_df.dropna(subset=["lat", "lon"])
    fig = px.scatter_mapbox(
        geo_df,
        lat="lat",
        lon="lon",
        color="Killed",
        size="Killed",
        text="Location",
        hover_name="Event",
        zoom=4,
        mapbox_style="open-street-map",
        title="Event Locations (size & colour = fatalities)",
    )
    fig.update_traces(textposition="top center")
    return fig

# ---------------------------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Conflict Timeline Analysis", layout="wide")
    st.title("Comprehensive Conflict Timeline Analysis – April–May 2025")

    df = seed_base_events()
    df = enrich_with_rss(df)

    with st.sidebar:
        st.header("Filters")
        belligerent_opt = st.selectbox("Belligerent", ["All"] + sorted(df["Belligerent"].unique()))
        operation_opt = st.selectbox("Operation", ["All"] + sorted(df["Operation"].unique()))
        date_min, date_max = df["Date"].min().date(), df["Date"].max().date()
        date_range = st.slider("Date range", min_value=date_min, max_value=date_max, value=(date_min, date_max))

    mask = pd.Series(True, index=df.index)
    if belligerent_opt != "All":
        mask &= df["Belligerent"] == belligerent_opt
    if operation_opt != "All":
        mask &= df["Operation"] == operation_opt
    mask &= df["Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
    view_df = df[mask]

    st.subheader("Event Table")
    st.dataframe(view_df[["Date", "Event", "Location", "Killed"]].sort_values("Date"))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(timeline_chart(view_df), use_container_width=True)
        st.plotly_chart(operation_chart(view_df), use_container_width=True)
    with col2:
        st.plotly_chart(cumulative_chart(view_df), use_container_width=True)
        st.plotly_chart(map_chart(view_df), use_container_width=True)


if __name__ == "__main__":
    main()
