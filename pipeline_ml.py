# pipeline_ml.py - Crée le modèle K-Means pour prédicteur
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import joblib

print(" CRÉATION MODÈLE K-MEANS")

# Charger transactions
df = pd.read_parquet("data/processed/transactions_clean.parquet")
print(f"Transactions: {df.shape}")

# Features clients (793)
features = df.groupby('Customer ID').agg({
    'Sales': ['count', 'mean', 'sum'],
    'Profit': ['sum']
}).round(2)

features.columns = ['freq', 'panier_moyen', 'ca_total', 'profit_total']
features = features.reset_index().fillna(0)
print(f"Clients: {features.shape}")

# K-Means optimal
X = features[['freq', 'panier_moyen', 'ca_total', 'profit_total']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

meilleur_k = 3  # On fixe 3 clusters clairs
kmeans = KMeans(n_clusters=meilleur_k, random_state=42, n_init=10)
features['cluster'] = kmeans.fit_predict(X_scaled)

# SAUVEGARDE
Path("models").mkdir(exist_ok=True)
features.to_parquet("data/processed/clients_clusters.parquet", index=False)
joblib.dump(kmeans, "models/kmeans.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print(f"\n {meilleur_k} clusters créés:")
print(features['cluster'].value_counts().sort_index())
print(" Modèles sauvés: kmeans.pkl + scaler.pkl")
print(" Prédicteur prêt pour dashboard !")
