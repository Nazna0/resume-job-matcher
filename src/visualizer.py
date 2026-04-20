"""
visualizer.py
Creates Plotly charts: score gauge + skill gap bar chart.
"""

import plotly.graph_objects as go


def plot_score_gauge(score: int) -> go.Figure:
    """Gauge chart showing the match score."""
    if score >= 75:
        bar_color = "#059669"
    elif score >= 50:
        bar_color = "#D97706"
    else:
        bar_color = "#DC2626"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 32, "color": bar_color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#9CA3AF",
                     "tickvals": [0, 25, 50, 75, 100]},
            "bar": {"color": bar_color, "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50],  "color": "#FEF2F2"},
                {"range": [50, 75], "color": "#FFFBEB"},
                {"range": [75, 100],"color": "#ECFDF5"},
            ],
            "threshold": {
                "line": {"color": bar_color, "width": 3},
                "thickness": 0.8,
                "value": score
            }
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ))

    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#374151", "family": "Arial"}
    )
    return fig


def plot_skill_gap(matched: set, missing: set) -> go.Figure:
    """Horizontal bar showing matched vs missing skill counts."""
    all_skills = sorted(list(matched))[:12] + sorted(list(missing))[:12]
    if not all_skills:
        fig = go.Figure()
        fig.update_layout(title="No keywords detected", height=100)
        return fig

    labels = sorted(list(matched))[:12] + sorted(list(missing))[:12]
    colors = ["#059669"] * min(len(matched), 12) + ["#DC2626"] * min(len(missing), 12)
    values = [1] * len(labels)

    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation="h",
        marker_color=colors,
        text=["✅ Have" if c == "#059669" else "❌ Missing" for c in colors],
        textposition="inside",
        insidetextanchor="middle",
        hovertemplate="%{y}<extra></extra>",
    ))

    fig.update_layout(
        height=max(300, len(labels) * 28),
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"visible": False},
        yaxis={"tickfont": {"size": 11}},
        showlegend=False,
        bargap=0.25,
    )
    return fig
