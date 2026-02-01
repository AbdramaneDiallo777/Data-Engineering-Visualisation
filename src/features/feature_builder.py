# src/features/feature_builder.py
import pandas as pd
from pathlib import Path

DATA_PROCESSED_DIR = Path("../data/processed")

def build_customer_features():
    """Agrège transactions → features clients."""
    df = pd.read_parquet(DATA_PROCESSED_DIR / "supertore_clean.parquet")
    print("[FEATURES] Données chargées, shape =", df.shape)

    customer_features = df.groupby('Customer ID').agg({
        'Sales': ['count', 'mean', 'sum'],
        'Profit': ['sum', 'mean'],
        'Discount': 'mean',
        'Quantity': 'mean',
        'State': 'nunique',
    }).round(2)

    customer_features.columns = [
        'freq_orders', 'avg_basket', 'total_sales',
        'total_profit', 'avg_profit', 'avg_discount',
        'avg_quantity', 'nb_states'
    ]

    print("[FEATURES] Features créées, shape =", customer_features.shape)
    return customer_features.reset_index()
