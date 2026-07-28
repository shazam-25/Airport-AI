import streamlit as st
from airport_ai.config import config
from airport_ai.config.settings import DATABASE_PATH, CAMERAS
from airport_ai.dashboard.components import DashboardComponents
from airport_ai.dashboard.database import DashboardDatabase

st.set_page_config(
    page_title="Airport AI Monitoring",
    layout="wide"
)

st.title("Airport AI Monitoring Dashboard")

database = DashboardDatabase()
components = DashboardComponents()

camera = st.sidebar.selectbox(
    "Camera",
    ["All"]+[c["camera_id"] for c in CAMERAS]
)

events = database.recent_events(camera_id=None if camera=="All" else camera)

components.summary_cards(events) # Display Event Summary Cards

st.divider()

st.subheader("Recent Events")
components.event_table(events)  # Display Events

alerts = database.active_alerts()
st.metric("Active Alerts", len(alerts)) # Display Alert Counts
components.active_alerts_table(alerts)  # Display Alerts



