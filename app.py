import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ---------------- Load Data ---------------- #
df = pd.read_csv("clean_weather.csv")
df["Date"] = pd.to_datetime(df["Date"])

# لو Year و Month مش موجودين
if "Year" not in df.columns:
    df["Year"] = df["Date"].dt.year
if "Month" not in df.columns:
    df["Month"] = df["Date"].dt.month

# ---------------- App Setup ---------------- #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# ---------------- Layout ---------------- #
app.layout = dbc.Container([

    html.H1("🌦 Advanced Weather Analytics Dashboard",
            className="text-center my-4"),

    # -------- Filters -------- #
    dbc.Row([

        dbc.Col(
            dcc.Dropdown(
                id="location_filter",
                options=[{"label": i, "value": i} for i in sorted(df["Location"].unique())],
                multi=True,
                placeholder="Select Location"
            ),
            width=4
        ),

        dbc.Col(
            dcc.Dropdown(
                id="year_filter",
                options=[{"label": int(y), "value": int(y)} for y in sorted(df["Year"].unique())],
                multi=True,
                placeholder="Select Year"
            ),
            width=4
        ),

        dbc.Col(
            dcc.DatePickerRange(
                id="date_range",
                start_date=df["Date"].min(),
                end_date=df["Date"].max(),
                display_format="YYYY-MM-DD"
            ),
            width=4
        )

    ], className="mb-4"),

    # -------- KPI Cards -------- #
    dbc.Row([

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total Records"),
            html.H2(id="total_records")
        ])), width=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Rain Probability %"),
            html.H2(id="rain_prob")
        ])), width=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Avg Temp (3PM)"),
            html.H2(id="avg_temp")
        ])), width=3),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Avg Humidity (3PM)"),
            html.H2(id="avg_humidity")
        ])), width=3),

    ], className="mb-4"),

    # -------- Charts Row 1 -------- #
    dbc.Row([
        dbc.Col(dcc.Graph(id="time_series"), width=6),
        dbc.Col(dcc.Graph(id="heatmap"), width=6),
    ]),

    # -------- Charts Row 2 -------- #
    dbc.Row([
        dbc.Col(dcc.Graph(id="scatter_plot"), width=6),
        dbc.Col(dcc.Graph(id="boxplot"), width=6),
    ])

], fluid=True)

# ---------------- Callback ---------------- #
@app.callback(
    [
        Output("total_records", "children"),
        Output("rain_prob", "children"),
        Output("avg_temp", "children"),
        Output("avg_humidity", "children"),
        Output("time_series", "figure"),
        Output("heatmap", "figure"),
        Output("scatter_plot", "figure"),
        Output("boxplot", "figure"),
    ],
    [
        Input("location_filter", "value"),
        Input("year_filter", "value"),
        Input("date_range", "start_date"),
        Input("date_range", "end_date"),
    ]
)
def update_dashboard(locations, years, start_date, end_date):

    filtered = df.copy()

    if locations:
        filtered = filtered[filtered["Location"].isin(locations)]

    if years:
        filtered = filtered[filtered["Year"].isin(years)]

    filtered = filtered[
        (filtered["Date"] >= start_date) &
        (filtered["Date"] <= end_date)
    ]

    # ----- KPIs -----
    total_records = len(filtered)
    rain_prob = round(filtered["RainTomorrow"].mean() * 100, 2) if len(filtered) else 0
    avg_temp = round(filtered["Temp3pm"].mean(), 2) if len(filtered) else 0
    avg_humidity = round(filtered["Humidity3pm"].mean(), 2) if len(filtered) else 0

    # ----- Time Series -----
    ts = filtered.groupby("Date")["RainTomorrow"].mean().reset_index()
    fig_ts = px.line(ts, x="Date", y="RainTomorrow",
                     title="Rain Probability Over Time")

    # ----- Heatmap -----
    heat_data = filtered.pivot_table(
        values="RainTomorrow",
        index="Location",
        columns="Month",
        aggfunc="mean"
    )

    fig_heat = go.Figure(data=go.Heatmap(
        z=heat_data.values,
        x=heat_data.columns,
        y=heat_data.index,
        colorscale="Blues"
    ))

    fig_heat.update_layout(title="Rain Probability Heatmap")

    # ----- Scatter -----
    sample_df = filtered.sample(min(3000, len(filtered))) if len(filtered) > 0 else filtered

    fig_scatter = px.scatter(
        sample_df,
        x="Humidity3pm",
        y="Pressure3pm",
        color="RainTomorrow",
        title="Humidity vs Pressure"
    )

    # ----- Boxplot -----
    fig_box = px.box(
        filtered,
        x="RainTomorrow",
        y="Temp3pm",
        title="Temperature Distribution by Rain"
    )

    return (
        total_records,
        f"{rain_prob}%",
        avg_temp,
        avg_humidity,
        fig_ts,
        fig_heat,
        fig_scatter,
        fig_box
    )

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
