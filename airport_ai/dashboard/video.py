import streamlit as st

class LiveVideo:
    def __init__(self):
        self.placeholder = st.empty()

    def update(self, frame):
        self.placeholder.image(
            frame,
            channels="BGR",
            use_container_width=True
        )