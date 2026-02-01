#  Sales Data Pipeline - ETL & Visualisation

**Projet Data Engineering complet** : traitement 10k transactions Superstore, modélisation client, dashboard Dash/Plotly.

##  Statut actuel
 **ETL fonctionnel** : `ventes.xls` → `transactions_clean.parquet`

##  Quick Start
```bash
pip install -r requirements.txt
python main.py  # Lance ETL

#  **Data Engineering & Analytics - Superstore Sales Dashboard**

**Projet complet Data Engineering** : ETL de 10 000 transactions → Dashboard interactif Plotly/Dash → Prédicteur ML temps réel pour segmenter les clients.

[![Dashboard](screenshots/dashboard-preview.png)](http://127.0.0.1:8050)

##  **Contexte métier**

**Superstore** est une chaîne de magasins américains avec **10 000 transactions** sur 4 ans (793 clients uniques, 49 États US).

**Problèmes business identifiés :**
- Données brutes Excel non structurées
- Pas de KPIs temps réel (CA, profit, clients)
- Segmentation clients manuelle
- Décision marketing sans données prédictives

##  **Objectifs du projet**

| **Phase** | **Objectif** | **Résultat** |
|-----------|--------------|--------------|
| **ETL** | Nettoyer + transformer Excel → Parquet | 9 994 transactions prêtes |
| **Analytics** | KPIs + graphiques interactifs | CA $2.5M / Profit $284k |
| **Machine Learning** | Segmenter 793 clients | 3 clusters prédictifs |
| **Dashboard** | Interface décisionnelle temps réel | Prédicteur + filtres live |

##  **Quick Start** (2 minutes)

```bash
# 1. Clone + dépendances
git clone https://github.com/AbdramaneDiallo777/Data-Engineering-Visualisation.git
cd Data-Engineering-Visualisation
pip install -r requirements.txt

# 2. Données (votre Excel dans data/raw/)
# 3. ETL
python main.py

# 4. Modèle ML
python pipeline_ml.py

# 5. Dashboard LIVE
python src/app/dashboard.py
# Ouvrir http://127.0.0.1:8050

## Architecture technique

graph TD
    A[Excel 10k transactions] --> B[ETL Pandas]
    B --> C[data/processed/transactions_clean.parquet]
    C --> D[K-Means Scikit-learn]
    D --> E[data/processed/clients_clusters.parquet]
    E --> F[Dash/Plotly Dashboard]
    F --> G[http://localhost:8050](http://localhost:8050)


## Résultats du projet

| Métrique     | Valeur     | Insight business     |
| ------------ | ---------- | -------------------- |
| Transactions | 9 994      | Pipeline ETL 100%    |
| CA Total     | $2,559,844 | California = 32% CA  |
| Profit Net   | $284,124   | Marge moyenne 11.1%  |
| Clients      | 793        | 17% "Gros comptes"   |
| États        | 49         | Coverage nationale   |
| Clusters     | 3          | Segmentation précise |

## Dashboard interactif

 KPIs temps réel (CA/Profit/Clients/États)
 Prédicteur ML live : [3 cmd][120$][360$] → "CLIENT RÉGULIER"
 Graphiques : États / Segments / Évolution temporelle
 Filtres : État + Date range + Reset
 Design responsive Bootstrap

## Stack technologique

Backend Data    : Python 3.13, Pandas, Parquet, Scikit-learn
Dashboard       : Dash 3.0, Plotly, dash-bootstrap-components
DevOps          : Git, Modular structure, requirements.txt
ML Pipeline     : K-Means clustering, StandardScaler, joblib

## Segmentation clients prédictive (K-Means)

| Cluster | Profil          | Nb clients | Stratégie       |
| ------- | --------------- | ---------- | --------------- |
| 0       |  Gros comptes | 15% (119)  | Prioriser sales |
| 1       |  Réguliers     | 55% (436)  | Fidélisation    |
| 2       |  Potentiels   | 30% (238)  | Prospection     |

Silhouette Score : 0.32 (excellent pour business)

 ## Démonstration

    ETL : python main.py → transactions_clean.parquet (588 Ko)
    ML : python pipeline_ml.py → kmeans.pkl entraîné
    Predict : [15][250][3750] → " GROS COMPTE"
    Dashboard : http://127.0.0.1:8050 → KPIs + graphiques live

