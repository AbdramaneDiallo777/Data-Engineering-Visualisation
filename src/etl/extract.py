# src/etl/extract.py
from pathlib import Path
import pandas as pd


DATA_RAW_DIR = Path("data/raw")


def extract_transactions(filename: str, sheet_name=0) -> pd.DataFrame:
    """
    Lit un fichier Excel (.xls / .xlsx) dans data/raw et renvoie un DataFrame.
    - filename: nom du fichier (ex: 'ventes.xlsx')
    - sheet_name: nom ou index de la feuille (0 par défaut)
    """
    file_path = DATA_RAW_DIR / filename
    print(f"[EXTRACT] Lecture du fichier : {file_path}")

    # Si nécessaire, ajoute engine="openpyxl" pour .xlsx ou engine="xlrd" pour .xls
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    print(f"[EXTRACT] Shape = {df.shape}")
    return df
