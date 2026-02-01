#  **Data Engineering & Analytics - Superstore Sales Dashboard**
# Auteur : Abdramane Diallo 
Date : 27/01/2026

**Projet complet Data Engineering** : ETL 10 000 transactions → Dashboard interactif Plotly/Dash → Prédicteur ML temps réel

[![Dashboard Preview](screenshots/dashboard-preview.png)](http://127.0.0.1:8050)

##  **Contexte métier**

**Superstore** : chaîne magasins US avec **10 000 transactions** (793 clients, 49 États).

**Problèmes identifiés :**
- Données Excel brutes non structurées
- Pas de KPIs temps réel
- Segmentation clients manuelle
- Décisions marketing sans prédiction

##  **Objectifs**

| **Phase** | **Objectif** | **Résultat** |
|-----------|--------------|--------------|
| **ETL** | Excel → Parquet optimisé | 9 994 transactions prêtes |
| **Analytics** | KPIs + graphiques interactifs | CA **$2.2M** / Profit **$216k** |
| **Machine Learning** | Segmenter 793 clients | **3 clusters prédictifs** |
| **Dashboard** | Interface décisionnelle | Prédicteur ML + filtres live |

##  **Quick Start** )

git clone https://github.com/AbdramaneDiallo777/Data-Engineering-Visualisation.git
cd Data-Engineering-Visualisation
pip install -r requirements.txt

# ETL + données
python main.py

# Modèle ML
python pipeline_ml.py

# Dashboard LIVE
python src/app/dashboard.py
 → http://127.0.0.1:8050

Architecture

graph TD
    A[Excel<br/>10k transactions] --> B[ETL Pandas]
    B --> C[data/processed<br/>transactions_clean.parquet]
    C --> D[K-Means<br/>Scikit-learn]
    D --> E[data/processed<br/>clients_clusters.parquet]
    E --> F[Dash/Plotly<br/>Dashboard]
    F --> G["Dashboard<br/>http://127.0.0.1:8050"]

Résultats clés
|  Métrique      | Valeur      | Insight              |
| ------------ | ---------- | -------------------- |
|  Transactions **| 9 994      | ETL 100%             |
|  CA Total     | $2,297,201 | California = 32%     |
|  Profit Net    | $216,989   | Marge 11.1%          |
|  Clients      | 793        | 17% VIP              |
|  États        | 49         | Couverture nationale |
|  Clusters      | 3          | Prédiction précise   |

Dashboard interactif

 KPIs temps réel (CA/Profit/Clients/États)
 **Prédicteur ML live** : [3 cmd][120$][360$] → "CLIENT RÉGULIER"
 Graphiques : États / Segments / Évolution
 Filtres : État + Date + Reset
 Design responsive Bootstrap

Stack technologique
Backend Data    : Python 3.13, Pandas, Parquet, Scikit-learn
Dashboard       : Dash 3.0, Plotly, dash-bootstrap-components  
DevOps          : Git, Modular, requirements.txt
ML Pipeline     : K-Means, StandardScaler, joblib

Segmentation prédictive K-Means
| Cluster |  Profil          | Clients   | Stratégie       |
| ------- | --------------- | --------- | --------------- |
| 0       |  Gros comptes | 15% (119) | Prioriser sales |
| 1       |  Réguliers     | 55% (436) | Fidélisation    |
| 2       |  Potentiels   | 30% (238) | Prospection     |

Démonstration
1. python main.py                     ETL 
2. python pipeline_ml.py              ML   
3. python src/app/dashboard.py          LIVE 
4. Test prédicteur :  → " GROS COMPTE" 1 2

