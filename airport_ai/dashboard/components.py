import pandas as pd
import streamlit as st


class DashboardComponents: ## Doubtful
    def summary_cards(self, events):
        turnaround = sum(
            row[1] == 'TURNAROUND' for row in events
        )
        ppe = sum(
            row[1] == "PPE" for row in events
        )
        fod = sum(
            row[1] == "FOD" for row in events
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Turnaround", turnaround)
        c2.metric("PPE", ppe)
        c3.metric("FOD", fod)


    def event_table(self, events):
        df = pd.DataFrame(
            events,
            columns = [
                "Camera",
                "Timestamp",
                "Stream",
                "Track ID",
                "Object",
                "Event",
                "Severity",
                "Message"
            ],
        )
        st.dataframe(
            df,
            use_container_width=True
        )

    def active_alerts_table(self, alerts):
        if len(alerts) == 0:
            st.info("No active alerts")
            return
        df = pd.DataFrame(
            alerts,
            columns=[
                "Timestamp",
                "Camera",
                "Stream",
                "Priority",
                "Status",
                "Message"
            ],
        )
        st.subheader("🚨 Active Alerts")

        def color_priority(value):
            if value == "CRITICAL":
                return "background-color:red;color:white"
            if value == "HIGH":
                return "background-color:orange"
            if value == "MEDIUM":
                return "background-color:yellow"
            if value == "LOW":
                return "background-color:lightgreen"
            return ""

        styled = df.style.map(color_priority, subset=["Priority"])
        st.dataframe(
            styled,
            use_container_width=True,
            hide_index=True
        )
