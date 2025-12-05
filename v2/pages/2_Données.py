import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Charger les données
@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv("defibrillateurs-du-reseau-ratp.csv", sep=";")
    # Renommer les colonnes dès le chargement
    df.rename(columns={'lat_coor1': 'latitude', 'long_coor1': 'longitude'}, inplace=True)
    return df

df = load_data()

# Filtrage par ville et type d'accès
villes = df['Ville'].dropna().unique().tolist()
types_acces = df['Accès'].dropna().unique().tolist()


# --- SIDEBAR ---
st.sidebar.header("🔧 Filtres")

st.sidebar.markdown("Affinez les données visibles sur la carte et les graphiques en sélectionnant les critères ci-dessous.")

# Filtre Ville
ville_selection = st.sidebar.multiselect(
    "🏙️ Villes",
    options=villes,
    default=villes,
    help="Sélectionnez une ou plusieurs villes pour filtrer les défibrillateurs."
)

# Filtre Type d'accès
type_selection = st.sidebar.multiselect(
    "🔑 Types d'accès",
    options=types_acces,
    default=types_acces,
    help="Sélectionnez le type d'accès au défibrillateur."
)

st.sidebar.markdown("---")

# Section Source des données
st.sidebar.header("📄 Source des données")
st.sidebar.markdown("""
Les données utilisées dans cette application proviennent du portail Open Data de la RATP.  
Elles recensent l'ensemble des **défibrillateurs installés sur le réseau RATP**.
""")


filtered_df = df[(df['Ville'].isin(ville_selection)) & (df['Accès'].isin(type_selection))]

# --- Affichage avancé ---
# Option pour sélectionner les colonnes à afficher
colonnes = st.multiselect(
    "Sélectionnez les colonnes à afficher",
    options=filtered_df.columns.tolist(),
    default=filtered_df.columns.tolist()
)

# Option pour filtrer par texte
texte_filtre = st.text_input("🔍 Rechercher dans toutes les colonnes (mot-clé)")

df_affiche = filtered_df[colonnes]

if texte_filtre:
    # Filtrer les lignes contenant le mot clé dans n'importe quelle colonne sélectionnée
    df_affiche = df_affiche[df_affiche.apply(lambda row: row.astype(str).str.contains(texte_filtre, case=False).any(), axis=1)]

# Affichage interactif avec largeur complète
st.dataframe(df_affiche, use_container_width=True, height=600)

# Bouton pour télécharger les données filtrées
csv = df_affiche.to_csv(index=False).encode('utf-8')
st.download_button(
    label="💾 Télécharger les données filtrées",
    data=csv,
    file_name='defibrillateurs_filtrés.csv',
    mime='text/csv'
)