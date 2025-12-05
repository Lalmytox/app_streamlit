import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --- Paramètres des onglets ---
st.markdown("""
<style>

    /* Désactiver les arrondis */
    .stTabs [data-baseweb="tab"] {
        border-radius: 0px;
    }

    /* Style des onglets */
    .stTabs [data-baseweb="tab"] {
        background-color: #4bc0ad;
        color: #ffffff;
        padding: 12px 20px;
        margin-right: 4px;
        font-weight: 600;
    }

    /* Onglet actif */
    .stTabs [aria-selected="true"] {
        background-color: #399885; /* version plus foncée */
        color: #ffffff !important;
        border-bottom: 3px solid #4bc0ad; /* joli accent */
    }

    /* Survol */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #005fcb;
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# --- Bannière ---
st.markdown(
    """
    <div style="
        background-color:#4bc0ad;
        padding:20px;
        border-radius:10px;
        text-align:center;
        margin-bottom:20px;
    ">
        <h1 style="color:#ffffff; margin:0; font-size:32px;">
            🚑 Localisation des Défibrillateurs RATP
        </h1>
        <p style="color:#004fa3; font-size:18px; margin:0;">
            Analyse et visualisation des points de secours sur le réseau
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# Charger les données
@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv("defibrillateurs-du-reseau-ratp.csv", sep=";")
    # Renommer les colonnes dès le chargement
    df.rename(columns={'lat_coor1': 'latitude', 'long_coor1': 'longitude'}, inplace=True)
    return df

df = load_data()

st.title("🩺 Défibrillateurs du réseau RATP")
st.markdown("""
Ce tableau de bord interactif vous permet d'explorer la localisation et la répartition des défibrillateurs sur le réseau RATP. Filtrez par ville et type d'accès pour affiner votre recherche.
""")

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

st.sidebar.markdown(
    "[🔗 Voir le dataset sur data.ratp.fr](https://data.ratp.fr/explore/dataset/defibrillateurs-du-reseau-ratp/information/)",
    unsafe_allow_html=True
)

filtered_df = df[(df['Ville'].isin(ville_selection)) & (df['Accès'].isin(type_selection))]


# --- ONGLETS PRINCIPAUX ---

# Organisation en onglets
onglets = st.tabs(["Carte", "Répartition par ville", "Répartition par type d'accès"])

with onglets[0]:
    st.subheader("🗺️ Carte des Défibrillateurs")
    if not filtered_df.empty:
        map_data = filtered_df[['latitude', 'longitude']].dropna()
        st.map(map_data)
    else:
        st.info("Aucun défibrillateur trouvé pour les filtres sélectionnés.")
        st.map(df[['latitude', 'longitude']].dropna())

with onglets[1]:
    st.subheader("📊 Répartition des Défibrillateurs par Ville")
    city_counts = filtered_df['Ville'].value_counts().reset_index()
    city_counts.columns = ['Ville', 'Nombre']
    fig_bar = px.bar(city_counts, x='Ville', y='Nombre', color='Ville', text='Nombre')
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

with onglets[2]:
    st.subheader("🔑 Répartition par Type d'Accès")
    type_counts = filtered_df['Accès'].value_counts().reset_index()
    type_counts.columns = ['Type d\'Accès', 'Nombre']
    fig_type = px.pie(type_counts, names='Type d\'Accès', values='Nombre', title="Répartition des Défibrillateurs par Type d'Accès")
    st.plotly_chart(fig_type, use_container_width=True)