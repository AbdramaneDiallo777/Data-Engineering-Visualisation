# main.py FINAL - fonctionne à 100%
import pandas as pd
from pathlib import Path
from src.etl.extract import extract_transactions
from src.etl.transform import clean_transactions
from src.etl.load import save_processed_parquet

def run_etl():
    print("=== ETL SUPERSTORE FINAL ===")
    
    # Extract
    df = extract_transactions("ventes.xls")
    print(f" Shape: {df.shape}")
    print("Colonnes:", list(df.columns))
    
    # Clean + dates
    df = clean_transactions(df)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Taxes simplifiées par State
    state_tax = {"California": 0.075, "Texas": 0.06, "New York": 0.08}
    df['tax_amount'] = df['Sales'] * df['State'].map(state_tax).fillna(0)
    df['profit_net'] = df['Profit'] - df['tax_amount']
    
    print(" Profit net calculé")
    print(df[['State', 'Sales', 'Profit', 'tax_amount', 'profit_net']].head())
    
    # Save
    save_processed_parquet(df, "transactions_clean.parquet")
    print(" data/processed/transactions_clean.parquet créé!")

if __name__ == "__main__":
    run_etl()
