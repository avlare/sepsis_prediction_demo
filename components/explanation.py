import numpy as np
import streamlit as st
import plotly.graph_objects as go

from components.config import COLORS, TOP_N_FEATURES
from components.utils import get_feature_color, is_raw_feature

def _color_legend_html() -> str:
    labels = {
        'Lab result': COLORS['raw'],
        'Trend over time': COLORS['window'],
        'Measurement frequency': COLORS['frequency'],
        'Measurement gap': COLORS['missingness'],
    }
    items = " &nbsp;&nbsp; ".join(
        f'<span style="display:inline-flex;align-items:center;gap:5px;">'
        f'<span style="width:11px;height:11px;border-radius:2px;background:{c};'
        f'flex-shrink:0;"></span>'
        f'<span style="font-size:12px;color:#444">{label}</span></span>'
        for label, c in labels.items()
    )
    return f'<div style="margin:4px 0 10px 0">{items}</div>'

def render_explanation(shap_values, X_processed, point_idx: int):
    values = shap_values[point_idx].values
    feature_names = X_processed.columns.tolist()

    view = st.radio(
        "Show features",
        ["All features (lab + engineered)", "Lab features only"],
        horizontal=True
    )

    if view == "Lab features only":
        mask = [is_raw_feature(n) for n in feature_names]
        feat_filtered = [n for n, m in zip(feature_names, mask) if m]
        vals_filtered = values[np.array(mask)]
    else:
        feat_filtered = feature_names
        vals_filtered = values

    top_idx = np.argsort(np.abs(vals_filtered))[-TOP_N_FEATURES:]
    top_names = [feat_filtered[i] for i in top_idx]
    top_vals = vals_filtered[top_idx]
    top_feat_vals = X_processed.iloc[point_idx][top_names].values
    bar_colors = [get_feature_color(n) for n in top_names]

    st.markdown(_color_legend_html(), unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        orientation='h',
        y=top_names,
        x=top_vals,
        marker_color=bar_colors,
        marker_line_width=0,
        text=[f"{'+' if v > 0 else ''}{v:.3f}" for v in top_vals],
        customdata=[f"{v:.2f}" for v in top_feat_vals],
        hovertemplate="<b>%{y}</b><br>Influence: %{x:.4f}<br>Value: %{customdata}<extra></extra>",
    ))

    fig.add_vline(x=0, line_color='#dddddd', line_width=1)

    fig.update_layout(
        xaxis_title='Influence on risk score',
        height=500,
        margin=dict(t=0),
        xaxis=dict(showgrid=True, gridcolor='#eeeeee', zeroline=False),
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("How to read this chart"):
        st.markdown("**All features** — raw lab results, trend indicators computed over a sliding time window and missingness indicators.")
        st.markdown("**Lab results only** — direct measurements at this hour only.")
        st.divider()
        st.markdown("**Feature suffixes**")
        st.markdown("`_Freq_` — how often this parameter was measured over a time window.")
        st.markdown("`_Max_` `_Min_` `_Mean_` `_Std_` — statistic over a time window.")
        st.markdown("`_Freq_` — how often this parameter was measured over a time window.")
        st.markdown("`_missing` — parameter was not recorded at this hour.")