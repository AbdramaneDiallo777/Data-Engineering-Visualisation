from pathlib import Path
import pandas as pd

DATA_PROCESSED_DIR = Path("data/processed")

def save_processed_parquet(df: pd.DataFrame, filename: str = "transactions_clean.parquet") -> None:
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_PROCESSED_DIR / filename
    df.to_parquet(output_path, index=False)
