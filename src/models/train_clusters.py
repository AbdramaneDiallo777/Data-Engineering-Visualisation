# src/models/train_clusters.py
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import joblib

DATA_PROCESSED_DIR = Path("../data/processed")  # remonte à la racine
MODELS_DIR = Path("../models")
MODELS_DIR.mkdir(exist_ok=True)

def train_customer_clusters(features_df: pd.DataFrame, n_clusters=4):
    """Entraîne K-Means sur features clients."""
    feature_cols = ['freq_orders', 'avg_basket', 'total_sales', 
                   'total_profit', 'avg_profit', 'avg_discount']
    
    X = features_df[feature_cols].fillna(0)
    print("[KMEANS] Features shape =", X.shape)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Test silhouette pour K=2 à 7
    sil_scores = []
    for k in range(2, 8):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels)
        sil_scores.append(sil)
        print(f"k={k}, silhouette={sil:.3f}")

    best_k = np.argmax(sil_scores) + 2
    print(f"[KMEANS] Meilleur K = {best_k}")

    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    features_df['cluster'] = labels
    output_path = DATA_PROCESSED_DIR / "customers_clustered.parquet"
    features_df.to_parquet(output_path, index=False)
    
    joblib.dump(kmeans, MODELS_DIR / "kmeans_clusters.pkl")
    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
    
    print(f"[KMEANS] Clusters sauvés : {output_path}")
    print("Répartition:", features_df['cluster'].value_counts().sort_index())
    
    return features_df
