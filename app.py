import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(
    page_title="Analyse Netflix – 8PRO408",
    layout="wide"
)

st.title("Analyse des contenus Netflix")
st.markdown("Mini-Projet 2 – 8PRO408 · Application Streamlit")

# ================================
# Chargement des données
# ================================
@st.cache_data
def load_data():
    
    base_dir = os.path.dirname(os.path.dirname(__file__))  
    data_path = os.path.join(base_dir, "data", "netflix_titles.csv")
    df = pd.read_csv(data_path)

    # Nettoyage minimal identique au notebook
    df["date_added"] = pd.to_datetime(df["date_added"],
                                     errors="coerce",
                                     infer_datetime_format=True)
    
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month

    return df

df = load_data()


# ================================
# Sidebar : navigation
# ================================
view = st.sidebar.radio(
    "Navigation",
    ["Vue d'ensemble", "Films vs Séries", "Genres & Pays", "Temporalité"]
)

st.sidebar.markdown("---")
st.sidebar.write(f"Nombre total de titres : **{len(df)}**")


# ================================
# Vue d'ensemble
# ================================
if view == "Vue d'ensemble":
    st.header("Vue d'ensemble du catalogue")

    # Quelques KPIs
    nb_movies = (df["type"] == "Movie").sum()
    nb_shows = (df["type"] == "TV Show").sum()
    nb_countries = df["country"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de films", nb_movies)
    col2.metric("Nombre de séries", nb_shows)
    col3.metric("Nombre de pays (non nuls)", nb_countries)

    # Pie chart films vs séries
    type_counts = df["type"].value_counts()
    fig_pie = px.pie(
        names=type_counts.index,
        values=type_counts.values,
        title="Répartition Films vs Séries"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Histogramme des années de sortie
    fig_year = px.histogram(
        df,
        x="release_year",
        nbins=40,
        title="Distribution des années de sortie"
    )
    st.plotly_chart(fig_year, use_container_width=True)


# ================================
# Films vs Séries
# ================================
elif view == "Films vs Séries":
    st.header("Films vs Séries")

    # Filtre sur l'année d'ajout (optionnel)
    years = df["year_added"].dropna().unique()
    years = sorted([int(y) for y in years if pd.notna(y)])
    selected_years = st.slider(
        "Filtrer par année d'ajout",
        min_value=min(years),
        max_value=max(years),
        value=(min(years), max(years)),
        step=1
    )

    mask = (df["year_added"] >= selected_years[0]) & (df["year_added"] <= selected_years[1])
    df_filtered = df[mask]

    st.write(f"Titres entre {selected_years[0]} et {selected_years[1]} : **{len(df_filtered)}**")

    # Bar chart films vs séries
    type_counts_filtered = df_filtered["type"].value_counts().reset_index()
    type_counts_filtered.columns = ["type", "count"]

    fig_bar = px.bar(
        type_counts_filtered,
        x="type",
        y="count",
        title="Nombre de films vs séries (filtré par année d'ajout)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Évolution par année
    added_type_year = (
        df_filtered.dropna(subset=["year_added"])
                  .groupby(["year_added", "type"])
                  .size()
                  .reset_index(name="count")
    )

    fig_line = px.line(
        added_type_year,
        x="year_added",
        y="count",
        color="type",
        markers=True,
        title="Évolution des ajouts de films et séries par année"
    )
    st.plotly_chart(fig_line, use_container_width=True)


# ================================
# Genres & Pays
# ================================
elif view == "Genres & Pays":
    st.header("Genres et pays")

    # --- Genres ---
    st.subheader("Genres les plus fréquents")

    df_genres = df.assign(listed_in=df["listed_in"].str.split(", "))
    df_genres = df_genres.explode("listed_in")

    top_n_genres = st.slider("Nombre de genres à afficher", 5, 30, 15)

    top_genres = df_genres["listed_in"].value_counts().head(top_n_genres).reset_index()
    top_genres.columns = ["genre", "count"]

    fig_genres = px.bar(
        top_genres,
        x="count",
        y="genre",
        orientation="h",
        title=f"Top {top_n_genres} genres"
    )
    st.plotly_chart(fig_genres, use_container_width=True)

    # --- Pays ---
    st.subheader("Pays les plus représentés")

    df_country = df.assign(country=df["country"].str.split(", "))
    df_country = df_country.explode("country").dropna(subset=["country"])

    top_n_countries = st.slider("Nombre de pays à afficher", 5, 30, 15)

    top_countries = df_country["country"].value_counts().head(top_n_countries).reset_index()
    top_countries.columns = ["country", "count"]

    fig_countries = px.bar(
        top_countries,
        x="count",
        y="country",
        orientation="h",
        title=f"Top {top_n_countries} pays"
    )
    st.plotly_chart(fig_countries, use_container_width=True)


# ================================
# Temporalité
# ================================
elif view == "Temporalité":
    st.header("Temporalité des ajouts")

    df_dates = df.dropna(subset=["year_added"])
    added_per_year = df_dates["year_added"].value_counts().sort_index().reset_index()
    added_per_year.columns = ["year_added", "count"]

    fig_added_year = px.line(
        added_per_year,
        x="year_added",
        y="count",
        markers=True,
        title="Nombre de contenus ajoutés par année"
    )
    st.plotly_chart(fig_added_year, use_container_width=True)

    # Heatmap année x mois
    df_dates = df_dates.dropna(subset=["month_added"])
    added_month_year = df_dates.groupby(["year_added", "month_added"]).size().reset_index(name="count")

    fig_heatmap = px.density_heatmap(
        added_month_year,
        x="month_added",
        y="year_added",
        z="count",
        title="Ajouts de contenus par mois et par année",
        nbinsx=12
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
