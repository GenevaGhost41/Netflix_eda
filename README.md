# Mini-Projet – Analyse des contenus Netflix (8PRO408)

Ce dépôt contient le mini-projet 2 du cours **8PRO408 – Outils de programmation pour la science des données**.

## Contenu du projet

- `data/netflix_titles.csv` : jeu de données Netflix (Kaggle).
- `notebooks/netflix_eda.ipynb` : notebook principal d'analyse exploratoire (EDA).
- `app/app.py` : mini application Streamlit (visualisations interactives).
- `report/` : dossier contenant le rapport PDF (1–2 pages).
- `README.md` : ce fichier.

## Objectifs

- Explorer la structure et la qualité du dataset Netflix.
- Analyser la répartition des contenus (films vs séries).
- Étudier les genres, pays et années de sortie.
- Analyser la dimension temporelle (date_added, year_added).
- Produire des visualisations avec **Pandas**, **Matplotlib**, **Seaborn** et **Plotly**.
- Proposer une mini application interactive avec **Streamlit**.

## Installation

```bash
git clone <URL_DU_DEPOT>
cd netflix_eda
python -m venv venv
source venv/bin/activate  # sous Windows: venv\Scripts\activate
pip install -r requirements.txt
