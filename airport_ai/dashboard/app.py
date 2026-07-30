import streamlit as st
import cv2

from airport_ai.dashboard.runtime_store import runtime_store


st.set_page_config(
    layout="wide",
    page_title="Airport AI"
)


# @st.cache_resource
# def get_runtime():

#     builder = ApplicationBuilder()

#     application = builder.build()

#     return application.services.runtime_store



# runtime = get_runtime()


st.title(
    "Airport Ground Operations AI"
)


# Multi-camera support
camera_ids = list(runtime_store.frames.keys())
st.write(runtime_store.frames)

if not camera_ids:
    st.warning("Waiting for camera pipeline...")
    st.stop()

cols = st.columns(len(camera_ids))


# # Display metrics
# metrics = runtime_store.get_metrics()

# if camera in metrics:

#     st.json(metrics[camera])

# # Dsiplay event history
# events = runtime_store.get_events()

# for event in reversed(events[-20:]):

#     st.write(
#         f"{event.timestamp} | "
#         f"{event.event_type} | "
#         f"{event.severity}"
#     )