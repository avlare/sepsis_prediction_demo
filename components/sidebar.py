import streamlit as st
import pandas as pd

from components.config import DEMO_PATIENTS


def sidebar():
    with st.sidebar:
        st.header("Patient data")
        st.divider()
        st.caption("Upload a patient file in PSV format or choose a demo patient below")

        uploaded_file = st.file_uploader("Upload PSV file", type=["psv"])
        demo = st.selectbox(
            "Demo patient",
            index=None,
            options=list(DEMO_PATIENTS.keys()),
            placeholder="Select a demo patient...",
        )
        st.divider()

    if uploaded_file is not None:
        return pd.read_csv(uploaded_file, sep='|')

    if demo is not None:
        return pd.read_csv(f"./demo_data/{DEMO_PATIENTS[demo]}", sep='|')

    return None
