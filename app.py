import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load the formatted output generated in Task 2
df = pd.read_csv("formatted_output.csv")

# Ensure dates are handled correctly
df["Date"] = pd.to_datetime(df["Date"])

# Group sales by date, then sort chronologically
daily_sales = (
    df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsels Sales Over Time",
    labels={
        "Date": "Date",
        "Sales": "Total Sales"
    }
)

# Mark the price increase date
price_increase_date = pd.to_datetime("2021-01-15")

fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref="paper",
    line=dict(dash="dash")
)

fig.add_annotation(
    x=price_increase_date,
    y=1,
    yref="paper",
    text="Price Increase",
    showarrow=False,
    yanchor="bottom"
)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Soul Foods Pink Morsels Sales Visualiser"),
        html.P(
            "This visualisation shows Pink Morsels sales over time, "
            "with the price increase date marked on 15 January 2021."
        ),
        dcc.Graph(
            id="pink-morsels-sales-chart",
            figure=fig
        )
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "margin": "40px"
    }
)

if __name__ == "__main__":
    app.run(debug=True)