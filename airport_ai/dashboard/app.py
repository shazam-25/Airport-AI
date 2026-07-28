import streamlit as st

from airport_ai.config.settings import DATABASE_PATH
from airport_ai.dashboard.components import DashboardComponents
from airport_ai.dashboard.database import DashboardDatabase

st.set_page_config(
    page_title="Airport AI Monitoring",
    layout="wide"
)

st.title("Airport AI Monitoring Dashboard")

database = DashboardDatabase(DATABASE_PATH)
components = DashboardComponents()

events = database.recent_events()

components.summary_cards(events)

st.divider()

st.subheader("Recent Events")
components.event_table(events)