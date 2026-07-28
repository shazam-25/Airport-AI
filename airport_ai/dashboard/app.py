import streamlit as st

from airport_ai.config.settings import DATABASE_PATH, CAMERAS
from airport_ai.dashboard.components import DashboardComponents
from airport_ai.dashboard.database import DashboardDatabase

st.set_page_config(
    page_title="Airport AI Monitoring",
    layout="wide"
)

st.title("Airport AI Monitoring Dashboard")

database = DashboardDatabase(DATABASE_PATH)
components = DashboardComponents()

camera = st.sidebar.selectbox(
    "Camera",
    ["All"]+[c["camera_id"] for c in CAMERAS]
)

events = database.recent_events(camera_id=None if camera=="All" else camera)

components.summary_cards(events)

st.divider()

st.subheader("Recent Events")
components.event_table(events)