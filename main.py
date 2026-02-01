# main.py (version SUPERSSTORE)
import pandas as pd
from src.etl.extract import extract_transactions
from src.etl.transform import (
    clean_transactions,
    convert_currency,
    compute_tax,
    compute_profit,
)
from src.etl.load import save_processed_parquet

# === PARAMÈTRES ADAPTÉS À TON DATASET ===
EXCEL_FILE_NAME = "ventes.xls"

CURRENCY_RATES = {"USD": 1.0}  # Dataset US uniquement
STATE_TAX = {
    "California": 0.075, "Texas": 0.06, "New York": 0.08,
    "Washington": 0.065, "Florida": 0.06
}

def run_etl():
    print("=== ETL SALES PIPELINE (SUPERSTORE) ===")

    # 1. EXTRACT
    df = extract_transactions(EXCEL_FILE_NAME)
    print("[DEBUG] Toutes les colonnes:", list(df.columns))

    # 2. TRANSFORM - Nettoyage
    df = clean_transactions(df)

    # Dates en format datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    print("[TRANSFORM] Dates converties")

    # Conversion devise (simplifiée - tout en USD)
    df = convert_currency(
        df, rate_map=CURRENCY_RATES,
        amount_col="Sales",      # ✅ colonne standard Superstore
        currency_col="Country",  # proxy (tous US)
        target_col="sales_usd",
    )

    # Taxes par État
    df = compute_tax(
        df, state_tax_map=STATE_TAX,
        state_col="State",
        base_amount_col="sales_usd",
        tax_col="tax_amount",
    )

    # Profit (si colonne Profit existe déjà, sinon calcul simplifié)
    if 'Profit' in df.columns:
        df['profit_net'] = df['Profit'] - df['tax_amount']
        print("[TRANSFORM] Profit net calculé (Profit existant - taxes)")
    else:
        print("[TRANSFORM] Pas de colonne Profit, profit_net = sales_usd")

    print("[TRANSFORM] Shape final:", df.shape)
    print("[TRANSFORM] Preview profit par State:")
    print(df.groupby('State')['profit_net'].sum().head())

    # 3. LOAD
    save_processed_parquet(df, "transactions_clean.parquet")
    print("=== ETL TERMINÉ ✅ ===")

if __name__ == "__main__":
    run_etl()
