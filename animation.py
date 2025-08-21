import plotly.graph_objects as go

def get_dharma_animation(tooltip):
    fig = go.Figure()

    # Background parchment layer
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=1, y1=1,
        fillcolor="rgba(245, 222, 179, 0.6)",
        line=dict(color="rgba(0,0,0,0)"),
        layer="below"
    )

    # Symbolic glyphs based on tooltip
    if "lotus" in tooltip.lower():
        fig.add_trace(go.Scatter(
            x=[0.5], y=[0.5],
            mode="markers+text",
            marker=dict(
                size=120,
                symbol="circle",
                color="rgba(255,192,203,0.6)",
                line=dict(width=3, color="darkred")
            ),
            text=["🌸"],
            textposition="middle center",
            hovertext="Lotus of Doubt",
            hoverinfo="text"
        ))

    elif "chakra" in tooltip.lower() or "wheel" in tooltip.lower():
        fig.add_trace(go.Scatter(
            x=[0.5], y=[0.5],
            mode="markers+text",
            marker=dict(
                size=120,
                symbol="circle-open",
                color="rgba(173,216,230,0.5)",
                line=dict(width=4, color="navy")
            ),
            text=["🔄"],
            textposition="middle center",
            hovertext="Chakra of Dharma",
            hoverinfo="text"
        ))

    elif "spiral" in tooltip.lower() or "eternity" in tooltip.lower():
        theta = [i for i in range(0, 360, 5)]
        r = [0.01 * t for t in theta]
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            mode="lines",
            line=dict(color="purple", width=3),
            hovertext="Spiral of Vision",
            hoverinfo="text"
        ))

    elif "sword" in tooltip.lower() or "action" in tooltip.lower():
        fig.add_trace(go.Scatter(
            x=[0.5, 0.5], y=[0.2, 0.8],
            mode="lines+text",
            line=dict(color="firebrick", width=6),
            text=["⚔️"],
            textposition="top center",
            hovertext="Sword of Resolve",
            hoverinfo="text"
        ))

    # Layout styling
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        polar=dict(bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(
            text=tooltip,
            x=0.5, y=0.05,
            showarrow=False,
            font=dict(size=16, color="darkslategray")
        )]
    )

    return fig