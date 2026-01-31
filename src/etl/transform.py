# src/etl/transform.py
import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoyage de base : doublons + valeurs manquantes simples.
    """
    initial_shape = df.shape
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Doublons supprimés : {initial_shape[0] - df.shape[0]} lignes")

    # Exemple simple : suppression des lignes complètement vides
    df = df.dropna(how="all")
    print(f"[TRANSFORM] Lignes totalement vides supprimées, shape = {df.shape}")

    return df


def convert_currency(
    df: pd.DataFrame,
    rate_map: dict,
    amount_col: str,
    currency_col: str,
    target_col: str = "amount_converted",
) -> pd.DataFrame:
    """
    Conversion d'un montant dans une devise cible via un dictionnaire de taux.
    - rate_map: {'USD': 0.92, 'EUR': 1.0, ...} (vers une devise de référence)
    - amount_col: nom de la colonne montant d'origine
    - currency_col: nom de la colonne devise
    - target_col: nouvelle colonne avec le montant converti
    """
    print(f"[TRANSFORM] Conversion monnaie via colonne '{amount_col}' et '{currency_col}'")

    def _convert(row):
        cur = row[currency_col]
        rate = rate_map.get(cur, 1.0)
        return row[amount_col] * rate

    df[target_col] = df.apply(_convert, axis=1)
    print(f"[TRANSFORM] Colonne '{target_col}' ajoutée")
    return df


def compute_tax(
    df: pd.DataFrame,
    state_tax_map: dict,
    state_col: str,
    base_amount_col: str = "amount_converted",
    tax_col: str = "tax_amount",
) -> pd.DataFrame:
    """
    Calcule le montant de taxe à partir d'un mapping Etat -> taux.
    - state_tax_map: {'CA': 0.075, 'TX': 0.06, ...}
    - state_col: colonne Etat
    - base_amount_col: montant sur lequel appliquer la taxe
    """
    print(f"[TRANSFORM] Calcul des taxes via colonne '{state_col}'")

    def _tax(row):
        state = row[state_col]
        taux = state_tax_map.get(state, 0.0)
        return row[base_amount_col] * taux

    df[tax_col] = df.apply(_tax, axis=1)
    print(f"[TRANSFORM] Colonne '{tax_col}' ajoutée")
    return df


def compute_profit(
    df: pd.DataFrame,
    revenue_col: str,
    cost_col: str,
    profit_col: str = "profit",
) -> pd.DataFrame:
    """
    Calcule le profit = revenue - cost.
    """
    print(f"[TRANSFORM] Calcul du profit = {revenue_col} - {cost_col}")
    df[profit_col] = df[revenue_col] - df[cost_col]
    print(f"[TRANSFORM] Colonne '{profit_col}' ajoutée")
    return df
