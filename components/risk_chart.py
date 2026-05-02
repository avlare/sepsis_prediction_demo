import streamlit as st
import plotly.graph_objects as go


def risk_chart(hours, probs, threshold):
    fig = go.Figure()

    fig.add_hline(
        y=threshold,
        line_dash='dash',
        line_color='red',
        annotation_text=f'Alert threshold ({threshold})',
        annotation_position='top left',
        annotation_font_color='red'
    )

    fig.add_trace(go.Scatter(
        x=hours,
        y=probs,
        mode='lines+markers',
        line=dict(color="#46426B"),
        marker=dict(
            color=probs,
            colorscale=[[0, "#008E0E"], [0.2, "#BCDD00"], [1, "#B60000"]],
            cmax=1,
            cmin=0
        )
    ))

    fig.update_layout(
        xaxis_title='Hour in ICU',
        yaxis_title='Sepsis risk'
    )

    return st.plotly_chart(
        fig,
        use_container_width=True,
        on_select='rerun',
        key=f'key',
    )
