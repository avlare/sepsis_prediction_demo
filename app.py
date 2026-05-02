import streamlit as st
import pandas as pd

from model_lgbm.initialization import predict, explainer, preprocess_patient, threshold
from components.sidebar import sidebar
from components.risk_chart import risk_chart
from components.explanation import render_explanation

st.set_page_config(page_title="Early sepsis prediction", layout="wide")
st.title("Early sepsis prediction")

raw_df = sidebar()

if raw_df is None:
    st.info("Upload a patient file or select a demo patient from the sidebar to begin.")
    st.stop()


df = pd.DataFrame(raw_df)
probs, preds = predict(df)
X_processed = preprocess_patient(df)
shap_values = explainer(X_processed)

hours = df['ICULOS'].values

tab_chart, tab_table, tab_input = st.tabs(
    ["Prediction chart", "Prediction table", "Input data"]
)

with tab_input:
    st.dataframe(df, use_container_width=True)

with tab_table:
    results_df = pd.DataFrame({
        'Hour (ICULOS)': hours,
        'Sepsis Probability': probs.round(4),
        'Prediction': ['Sepsis' if p == 1 else 'No Sepsis' for p in preds],
    })
    st.dataframe(results_df, use_container_width=True)

with tab_chart:
    st.subheader("Sepsis risk over time")
    st.caption("Click on a point to see which factors influenced the risk score at that hour")
    event = risk_chart(hours, probs, threshold)

    points = event.get("selection", {}).get("points", [])

    if points:
        selected_idx = points[0]["point_index"]
        prob = probs[selected_idx]
        pred = preds[selected_idx]

        st.divider()

        pred_label = "Sepsis" if pred == 1 else "No Sepsis"
        pred_color = "#c0392b" if pred == 1 else "#bc0404"
        st.markdown(
            f"**Hour {selected_idx + 1}** &nbsp;|&nbsp; "
            f'<span style="color:{pred_color};font-weight:600">{pred_label}</span>',
            unsafe_allow_html=True,
        )

        render_explanation(shap_values, X_processed, selected_idx)