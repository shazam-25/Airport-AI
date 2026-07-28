import pandas as pd
import streamlit as st

class DashboardComponents:
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
