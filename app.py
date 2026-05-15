import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load formatted data from Task 2
df = pd.read_csv("formatted_output.csv")

# Clean and prepare fields
df["Date"] = pd.to_datetime(df["Date"])
df["Region"] = df["Region"].astype(str).str.lower().str.strip()

REGIONS = ["all", "north", "east", "south", "west"]

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    "Soul Foods Pink Morsels Sales Visualiser",
                    style={
                        "marginBottom": "10px",
                        "fontSize": "34px",
                        "color": "#2D3748",
                    },
                ),
                html.P(
                    "Explore Pink Morsels sales over time and compare performance before and after the 15 January 2021 price increase.",
                    style={
                        "fontSize": "16px",
                        "color": "#4A5568",
                        "maxWidth": "850px",
                        "lineHeight": "1.5",
                    },
                ),
            ],
            style={
                "backgroundColor": "#FFFFFF",
                "padding": "30px",
                "borderRadius": "18px",
                "boxShadow": "0 8px 24px rgba(0, 0, 0, 0.08)",
                "marginBottom": "25px",
            },
        ),

        html.Div(
            children=[
                html.H3(
                    "Filter by Region",
                    style={
                        "marginBottom": "15px",
                        "color": "#2D3748",
                    },
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={
                        "display": "flex",
                        "gap": "22px",
                        "fontSize": "15px",
                        "color": "#2D3748",
                    },
                ),
            ],
            style={
                "backgroundColor": "#FFFFFF",
                "padding": "22px 30px",
                "borderRadius": "18px",
                "boxShadow": "0 8px 24px rgba(0, 0, 0, 0.08)",
                "marginBottom": "25px",
            },
        ),

        html.Div(
            children=[
                dcc.Graph(
                    id="sales-chart",
                    config={"displayModeBar": False},
                )
            ],
            style={
                "backgroundColor": "#FFFFFF",
                "padding": "20px",
                "borderRadius": "18px",
                "boxShadow": "0 8px 24px rgba(0, 0, 0, 0.08)",
            },
        ),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#F7FAFC",
        "minHeight": "100vh",
        "padding": "40px",
    },
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.copy()
        chart_title = "Pink Morsels Sales Over Time - All Regions"
    else:
        filtered_df = df[df["Region"] == selected_region].copy()
        chart_title = f"Pink Morsels Sales Over Time - {selected_region.title()} Region"

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=chart_title,
        labels={
            "Date": "Date",
            "Sales": "Total Sales",
        },
        markers=True,
    )

    price_increase_date = pd.to_datetime("2021-01-15")

    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(dash="dash", width=2),
    )

    fig.add_annotation(
        x=price_increase_date,
        y=1,
        yref="paper",
        text="Price Increase",
        showarrow=False,
        yanchor="bottom",
        font=dict(size=12),
    )

    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        title_font_size=22,
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="#2D3748",
        ),
        margin=dict(l=50, r=30, t=70, b=50),
        hovermode="x unified",
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E2E8F0",
        title="Date",
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E2E8F0",
        title="Total Sales",
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)