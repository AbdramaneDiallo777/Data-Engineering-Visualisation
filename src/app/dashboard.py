
import dash
from dash import dcc, html, Input, Output, callback, ALL, ctx
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path
import dash_bootstrap_components as dbc
import joblib

# Chemins
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"

# Données
df = pd.read_parquet(DATA_DIR / "transactions_clean.parquet")
print(" Transactions:", df.shape)

# Modèle ML
PREDICT_MODE = False
try:
    kmeans = joblib.load(MODELS_DIR / "kmeans.pkl")
    scaler = joblib.load(MODELS_DIR / "scaler.pkl")
    PREDICT_MODE = True
    print(" Prédicteur K-Means chargé")
except:
    print(" Modèle manquant")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dummy trigger pour graphiques
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1(" Sales Dashboard + ML Predictor", 
                       className="text-center text-primary mb-4"))
    ]),
    
    # KPIs
    dbc.Row([
        dbc.Col(html.Div(id="kpi-ca", className="card p-4 bg-primary text-white text-center"), width=3),
        dbc.Col(html.Div(id="kpi-profit", className="card p-4 bg-success text-white text-center"), width=3),
        dbc.Col(html.Div(id="kpi-orders", className="card p-4 bg-info text-white text-center"), width=3),
        dbc.Col(html.Div(id="kpi-clients", className="card p-4 bg-warning text-white text-center"), width=3),
    ], className="mb-4"),
    
    # PRÉDICTEUR + RESET
    dbc.Row([
        dbc.Col([
            html.H4(" Prédire Nouveau Client", className="text-center mb-4"),
            dbc.Row([
                dbc.Col([
                    dcc.Input(id="freq-input", type="number", value=3,
                            placeholder="Nb commandes", className="form-control mb-2")
                ], width=3),
                dbc.Col([
                    dcc.Input(id="panier-input", type="number", value=120,
                            placeholder="Panier moyen ($)", className="form-control mb-2")
                ], width=3),
                dbc.Col([
                    dcc.Input(id="ca-input", type="number", value=360,
                            placeholder="CA total ($)", className="form-control mb-2")
                ], width=3),
                dbc.Col([
                    html.Button(" PREDIRE", id="predict-btn", 
                               className="btn btn-success btn-block h-100 me-2"),
                    html.Button(" RESET", id="reset-btn", 
                               className="btn btn-secondary btn-block h-100")
                ], width=3)
            ]),
            html.Div(id="prediction-result", className="mt-4 text-center p-3 border rounded")
        ], className="card p-4 bg-light shadow", width=12)
    ], className="mb-5"),
    
    # Filtres
    dbc.Row([
        dbc.Col(dcc.Dropdown(id="state-dropdown", placeholder="Filtrer État"), width=4),
        dbc.Col(dcc.DatePickerRange(id="date-picker"), width=4),
        dbc.Col(html.Button(" Reset Filtres", id="filter-reset", 
                           className="btn btn-outline-secondary"), width=4)
    ], className="mb-4"),
    
    # Input dummy (fix erreur Dash)
    dcc.Store(id="dummy-trigger", data=1),
    
    # Graphs
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-bar"), width=6),
        dbc.Col(dcc.Graph(id="profit-bar"), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-trend"), width=12)
    ])
], fluid=True)

# KPIs
@callback(
    [Output("kpi-ca", "children"), Output("kpi-profit", "children"),
     Output("kpi-orders", "children"), Output("kpi-clients", "children"),
     Output("state-dropdown", "options")],
    [Input("dummy-trigger", "data"), Input("date-picker", "start_date"), 
     Input("date-picker", "end_date")]
)
def update_kpis(dummy, start, end):
    df_filt = df.copy()
    if start: df_filt = df_filt[df_filt['Order Date'] >= pd.to_datetime(start)]
    if end: df_filt = df_filt[df_filt['Order Date'] <= pd.to_datetime(end)]
    
    return (
        [html.H2(f"${df_filt['Sales'].sum():,.0f}"), html.P("CA Total")],
        [html.H2(f"${df_filt['profit_net'].sum():,.0f}"), html.P("Profit")],
        [html.H2(f"{len(df_filt):,}"), html.P("Commandes")],
        [html.H2(f"{df_filt['Customer ID'].nunique():,}"), html.P("Clients")],
        [{'label': s, 'value': s} for s in sorted(df_filt['State'].unique())]
    )

# PRÉDICTEUR + RESET
@callback(
    [Output("prediction-result", "children"),
     Output("freq-input", "value"), Output("panier-input", "value"), 
     Output("ca-input", "value")],
    [Input("predict-btn", "n_clicks"), Input("reset-btn", "n_clicks"),
     Input("freq-input", "value"), Input("panier-input", "value"), 
     Input("ca-input", "value")]
)
def predict_and_reset(predict_clicks, reset_clicks, freq, panier, ca):
    triggered = ctx.triggered_id
    
    # RESET
    if triggered == "reset-btn":
        return ("", 3, 120, 360)
    
    # PREDIRE
    if predict_clicks and PREDICT_MODE and freq and panier and ca:
        try:
            features = np.array([[freq, panier, ca, ca*0.1]])
            cluster = kmeans.predict(scaler.transform(features))[0]
            profiles = {
                0: " GROS COMPTE (prioriser sales)",
                1: " CLIENT RÉGULIER (fidéliser)", 
                2: " CLIENT POTENTIEL (prospecter)"
            }
            result = html.Div([
                html.H3(profiles.get(cluster, "❓"), className="text-success mb-2"),
                html.P(f"Cluster {cluster} | Fréq:{freq} | Panier:${panier} | CA:${ca}", 
                      className="text-muted")
            ], className="bg-success bg-opacity-10 p-4 rounded shadow")
            return (result, freq, panier, ca)
        except:
            return (" Erreur prédiction", freq, panier, ca)
    
    return ("Cliquez PREDIRE ou RESET", dash.no_update, dash.no_update, dash.no_update)

# Graphs avec dummy trigger
@callback(Output("sales-bar", "figure"), 
          [Input("dummy-trigger", "data"), Input("state-dropdown", "value")])
def sales_bar(dummy, state):
    df_bar = df if not state else df[df['State'] == state]
    return px.bar(df_bar.groupby('State')['Sales'].sum().reset_index(),
                 x='State', y='Sales', title="Ventes par État")

@callback(Output("profit-bar", "figure"), [Input("dummy-trigger", "data")])
def profit_bar(dummy):
    return px.bar(df.groupby('Segment')['profit_net'].sum().reset_index(),
                 x='Segment', y='profit_net', title="Profit par Segment")

@callback(Output("sales-trend", "figure"), [Input("dummy-trigger", "data")])
def sales_trend(dummy):
    df_monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    df_monthly['Order Date'] = df_monthly['Order Date'].astype(str)
    return px.line(df_monthly, x='Order Date', y='Sales', title="Évolution")

if __name__ == '__main__':
    app.run(debug=True, port=8050, host='127.0.0.1')
