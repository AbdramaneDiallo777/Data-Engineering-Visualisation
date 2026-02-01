# src/app/dashboard.py - VERSION FONCTIONNELLE
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import dash_bootstrap_components as dbc

# Chemins absolus depuis la racine
BASE_DIR = Path(__file__).resolve().parents[2]  # remonte à C:\Data-Engineering-Visualisation
DATA_DIR = BASE_DIR / "data" / "processed"

# Charger UNIQUEMENT transactions_clean.parquet (qui existe)
df = pd.read_parquet(DATA_DIR / "transactions_clean.parquet")
print("✅ Transactions chargées:", df.shape)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout Dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🛒 Sales Superstore Dashboard", className="text-center mb-4")
        ])
    ]),
    
    # KPIs
    dbc.Row([
        dbc.Col([
            html.Div(id="kpi-ca", className="card p-4 bg-primary text-white text-center")
        ], width=3),
        dbc.Col([
            html.Div(id="kpi-profit", className="card p-4 bg-success text-white text-center")
        ], width=3),
        dbc.Col([
            html.Div(id="kpi-orders", className="card p-4 bg-info text-white text-center")
        ], width=3),
        dbc.Col([
            html.Div(id="kpi-states", className="card p-4 bg-warning text-white text-center")
        ], width=3),
    ], className="mb-4"),
    
    # Filtres
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="state-dropdown", placeholder="Sélectionner État")
        ], width=4),
        dbc.Col([
            dcc.DatePickerRange(id="date-picker", className="mb-3")
        ], width=4)
    ], className="mb-4"),
    
    # Graphs
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-map"), width=6),
        dbc.Col(dcc.Graph(id="profit-bar"), width=6)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-trend"), width=12)
    ])
], fluid=True)

# Callbacks
@callback(
    [Output("kpi-ca", "children"), Output("kpi-profit", "children"),
     Output("kpi-orders", "children"), Output("kpi-states", "children"),
     Output("state-dropdown", "options")],
    [Input("date-picker", "start_date"), Input("date-picker", "end_date")]
)
def update_kpis(start_date, end_date):
    df_filt = df.copy()
    
    if start_date:
        df_filt = df_filt[df_filt['Order Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df_filt = df_filt[df_filt['Order Date'] <= pd.to_datetime(end_date)]
    
    ca = html.Div([html.H2(f"${df_filt['Sales'].sum():,.0f}"), 
                   html.P("Chiffre d'Affaires")], 
                  className="text-center")
    profit = html.Div([html.H2(f"${df_filt['profit_net'].sum():,.0f}"), 
                       html.P("Profit Net")], 
                      className="text-center")
    orders = html.Div([html.H2(f"{len(df_filt):,}"), 
                       html.P("Commandes")], 
                      className="text-center")
    states = html.Div([html.H2(f"{df_filt['State'].nunique()}"), 
                       html.P("États")], 
                      className="text-center")
    
    state_options = [{'label': s, 'value': s} for s in sorted(df_filt['State'].unique())]
    
    return ca, profit, orders, states, state_options

@callback(
    Output("sales-map", "figure"),
    [Input("state-dropdown", "value"), Input("date-picker", "start_date"), 
     Input("date-picker", "end_date")]
)
def update_map(state_val, start_date, end_date):
    df_map = df.copy()
    
    if state_val:
        df_map = df_map[df_map['State'] == state_val]
    if start_date:
        df_map = df_map[df_map['Order Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df_map = df_map[df_map['Order Date'] <= pd.to_datetime(end_date)]
    
    state_sales = df_map.groupby('State')['Sales'].sum().reset_index()
    
    fig = px.bar(state_sales, x='State', y='Sales', 
                title="Ventes par État",
                color='Sales',
                color_continuous_scale='Viridis')
    fig.update_layout(height=400)
    return fig

@callback(
    Output("profit-bar", "figure"),
    [Input("state-dropdown", "value"), Input("date-picker", "start_date"), 
     Input("date-picker", "end_date")]
)
def update_profit_bar(state_val, start_date, end_date):
    df_profit = df.copy()
    
    if state_val:
        df_profit = df_profit[df_profit['State'] == state_val]
    if start_date:
        df_profit = df_profit[df_profit['Order Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df_profit = df_profit[df_profit['Order Date'] <= pd.to_datetime(end_date)]
    
    state_profit = df_profit.groupby('Segment')['profit_net'].sum().reset_index()
    
    fig = px.bar(state_profit, x='Segment', y='profit_net',
                title="Profit par Segment Client",
                color='profit_net',
                color_continuous_scale='Blues')
    fig.update_layout(height=400)
    return fig

@callback(
    Output("sales-trend", "figure"),
    [Input("date-picker", "start_date"), Input("date-picker", "end_date")]
)
def update_trend(start_date, end_date):
    df_trend = df.copy()
    
    if start_date:
        df_trend = df_trend[df_trend['Order Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df_trend = df_trend[df_trend['Order Date'] <= pd.to_datetime(end_date)]
    
    df_monthly = df_trend.groupby(df_trend['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    df_monthly['Order Date'] = df_monthly['Order Date'].astype(str)
    
    fig = px.line(df_monthly, x='Order Date', y='Sales',
                 title="Évolution des Ventes")
    fig.update_layout(height=400, xaxis_title="Mois", yaxis_title="Ventes ($)")
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050, host='127.0.0.1')

