import plotly.graph_objects as go

def plot_growth(yearly_data):

    years = []
    portfolio_values = []
    invested_values = []

    for entry in yearly_data:
        years.append(entry["year"])
        portfolio_values.append(entry["portfolio_value"])
        invested_values.append(entry["total_invested"])

    fig = go.Figure()

    # Portfolio line
    fig.add_trace(go.Scatter(
        x=years,
        y=portfolio_values,
        mode='lines+markers',
        name='Portfolio Value'
    ))

    # Invested line
    fig.add_trace(go.Scatter(
        x=years,
        y=invested_values,
        mode='lines+markers',
        name='Total Invested'
    ))

    fig.update_layout(
        title="Investment Growth Over Time",
        xaxis_title="Years",
        yaxis_title="Dollars"
    )

    fig.show()