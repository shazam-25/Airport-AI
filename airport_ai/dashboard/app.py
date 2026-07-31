import time
from io import BytesIO
from datetime import datetime

import pandas as pd
import streamlit as st
import sqlite3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from airport_ai.config import config
from airport_ai.dashboard.runtime_store import RuntimeStore

# store = RuntimeStore("data/database/runtime.db")


# # =============================================================================
# # Camera Grid
# # =============================================================================

# camera_ids = [
#     "GATE_A01",
#     "GATE_B03",
#     "GATE_C04"
# ]

# cols = st.columns(len(camera_ids))

# camera_slots = {}

# for col, camera_id in zip(cols, camera_ids):
#     with col:
#         st.subheader(camera_id)
#         camera_slots[camera_id] = st.empty()


# # =============================================================================
# # Refresh Loop
# # =============================================================================

# while True:

#     for camera_id in camera_ids:

#         frame = store.get_frame(camera_id)

#         if frame is not None:
#             camera_slots[camera_id].image(
#                 frame,
#                 channels="BGR",
#                 use_container_width=True
#             )
#         else:
#             camera_slots[camera_id].warning(
#                 "Waiting for frames..."
#             )

#     time.sleep(0.5)


# =============================================================================
# Runtime Store
# =============================================================================

store = RuntimeStore(
    str(config.resolve_path(
        config.get("dashboard")["runtime_db"]
    ))
)


# =============================================================================
# Helper Functions
# =============================================================================

def severity_icon(severity: str) -> str:
    """
    Returns emoji corresponding to severity.
    """

    severity = severity.upper()

    icons = {
        "HIGH": "🔴",
        "MEDIUM": "🟠",
        "LOW": "🟢"
    }

    return icons.get(severity, "⚪")


def format_timestamp(ts):

    if ts is None:
        return "--"

    return datetime.fromtimestamp(
        ts
    ).strftime("%H:%M:%S")


# =============================================================================
# Streamlit Configuration
# =============================================================================

st.set_page_config(
    page_title="Airport AI Dashboard",
    page_icon="🛫",
    layout="wide"
)

st.title("🛫 Airport AI Live Monitoring Dashboard")


# =============================================================================
# Camera Grid
# =============================================================================

camera_ids = [
    "GATE_A01",
    "GATE_B03",
    "GATE_C04"
]

camera_columns = st.columns(len(camera_ids))

camera_placeholders = {}

for column, camera_id in zip(camera_columns, camera_ids):

    with column:

        st.markdown(
            f"### 🎥 {camera_id}"
        )

        camera_placeholders[camera_id] = st.empty()


# =============================================================================
# Latest Events
# =============================================================================

st.divider()

st.subheader("🚨 Latest Events")

event_columns = st.columns(3)

high_event_placeholder = event_columns[0].empty()

medium_event_placeholder = event_columns[1].empty()

low_event_placeholder = event_columns[2].empty()


# =============================================================================
# Analytics
# =============================================================================

st.divider()

st.subheader("📊 Analytics")


# -----------------------------------------------------------------------------
# KPI Cards
# -----------------------------------------------------------------------------

kpi_columns = st.columns(4)

total_events_placeholder = kpi_columns[0].empty()

high_events_placeholder = kpi_columns[1].empty()

medium_events_placeholder = kpi_columns[2].empty()

low_events_placeholder = kpi_columns[3].empty()


# -----------------------------------------------------------------------------
# Severity Distribution
# -----------------------------------------------------------------------------

st.markdown("#### Severity Distribution")

severity_chart_placeholder = st.empty()

# =============================================================================
# System Status
# =============================================================================

st.divider()

st.subheader("⚙️ System Status")

status_cols = st.columns(5)

camera_status_placeholder = status_cols[0].empty()

pipeline_status_placeholder = status_cols[1].empty()

database_status_placeholder = status_cols[2].empty()

fps_placeholder = status_cols[3].empty()

last_update_placeholder = status_cols[4].empty()

# st.write("Shatakshi Mondal - M.Tech Dissertation")


# =============================================================================
# Live Dashboard Refresh
# =============================================================================

REFRESH_INTERVAL = 0.5

while True:
    loop_start = time.time()
    # -------------------------------------------------------------------------
    # Camera Streams
    # -------------------------------------------------------------------------

    for camera_id in camera_ids:

        frame = store.get_frame(camera_id)
        # print(f"{camera_id}: {'Frame OK' if frame is not None else 'No Frame'}")

        if frame is not None:
            camera_placeholders[camera_id].image(
                frame,
                channels="BGR",
                # width="stretch"
            )

        else:

            camera_placeholders[camera_id].warning(
                "Waiting for camera pipeline..."
            )
    # print("Camera section completed")

    # -------------------------------------------------------------------------
    # Latest Events
    # -------------------------------------------------------------------------

    high_event = store.get_latest_event_by_severity("HIGH")
    medium_event = store.get_latest_event_by_severity("MEDIUM")
    low_event = store.get_latest_event_by_severity("LOW")


    # HIGH
    with high_event_placeholder.container():

        st.markdown("### 🔴 HIGH")

        if high_event:

            st.write(
                f"**Time:** {format_timestamp(high_event[5])}"
            )

            st.write(
                f"**Camera:** {high_event[1]}"
            )

            st.write(
                f"**Event:** {high_event[2]}"
            )

            st.write(
                high_event[4]
            )

        else:

            st.info(
                "No HIGH events."
            )


    # MEDIUM
    with medium_event_placeholder.container():

        st.markdown("### 🟠 MEDIUM")

        if medium_event:

            st.write(
                f"**Time:** {format_timestamp(medium_event[5])}"
            )

            st.write(
                f"**Camera:** {medium_event[1]}"
            )

            st.write(
                f"**Event:** {medium_event[2]}"
            )

            st.write(
                medium_event[4]
            )

        else:

            st.info(
                "No MEDIUM events."
            )


    # LOW
    with low_event_placeholder.container():

        st.markdown("### 🟢 LOW")

        if low_event:

            st.write(
                f"**Time:** {format_timestamp(low_event[5])}"
            )

            st.write(
                f"**Camera:** {low_event[1]}"
            )

            st.write(
                f"**Event:** {low_event[2]}"
            )

            st.write(
                low_event[4]
            )

        else:

            st.info(
                "No LOW events."
            )


    # -------------------------------------------------------------------------
    # KPI Cards
    # -------------------------------------------------------------------------

    counts = store.get_event_counts()

    total_events_placeholder.metric(
        "Total Events",
        counts["TOTAL"]
    )

    high_events_placeholder.metric(
        "🔴 High",
        counts["HIGH"]
    )

    medium_events_placeholder.metric(
        "🟠 Medium",
        counts["MEDIUM"]
    )

    low_events_placeholder.metric(
        "🟢 Low",
        counts["LOW"]
    )


    # -------------------------------------------------------------------------
    # Severity Distribution
    # -------------------------------------------------------------------------

    distribution = store.get_severity_distribution()

    chart_df = pd.DataFrame(
        distribution,
        columns=[
            "Severity",
            "Count"
        ]
    )

    if not chart_df.empty:

        chart_df["Severity"] = pd.Categorical(
            chart_df["Severity"],
            categories=[
                "HIGH",
                "MEDIUM",
                "LOW"
            ],
            ordered=True
        )

        chart_df = chart_df.sort_values(
            "Severity"
        )

        severity_chart_placeholder.bar_chart(
            chart_df.set_index("Severity")
        )

    else:

        severity_chart_placeholder.info(
            "No event data available."
        )

    # -------------------------------------------------------------------------
    # System Status
    # -------------------------------------------------------------------------
    online_cameras = 0
    for camera_id in camera_ids:
        frame = store.get_frame(camera_id)
        if frame is not None:
            online_cameras += 1
            camera_placeholders[camera_id].image(
                frame,
                channels="BGR",
                width="stretch"
            )
        else:
            camera_placeholders[camera_id].warning(
                "Waiting for camera pipeline..."
            )
        camera_status_placeholder.metric(
            "🎥 Cameras",
            f"{online_cameras}/{len(camera_ids)}"
        )
    pipeline_status = (
        "🟢 Running"
        if online_cameras > 0
        else "🔴 Stopped"
    )
    pipeline_status_placeholder.metric(
        "AI Pipeline",
        pipeline_status
    )
    try:
        conn = sqlite3.connect(store.path)
        conn.close()
        db_status = "🟢 Connected"
    except Exception:
        db_status = "🔴 Error"
    database_status_placeholder.metric(
        "Database",
        db_status
    )
    elapsed = time.time() - loop_start
    fps = 1.0 / elapsed if elapsed > 0 else 0
    fps_placeholder.metric(
        "Refresh FPS",
        f"{fps:.1f}"
    )
    last_update_placeholder.metric(
        "Last Update",
        datetime.now().strftime("%H:%M:%S")
    )

    # -------------------------------------------------------------------------
    # Refresh Interval
    # -------------------------------------------------------------------------

    time.sleep(REFRESH_INTERVAL)

    