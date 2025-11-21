import streamlit as st
import pandas as pd
import plotly.express as px

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

ville_selection = st.sidebar.multiselect("Sélectionnez la/les ville(s)", options=villes, default=villes)
type_selection = st.sidebar.multiselect("Sélectionnez le type d'accès", options=types_acces, default=types_acces)

filtered_df = df[(df['Ville'].isin(ville_selection)) & (df['Accès'].isin(type_selection))]

# Organisation en onglets
onglets = st.tabs(["Carte", "Répartition par ville", "Répartition par type d'accès", "Tableau"])

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

with onglets[3]:
    st.subheader("📋 Tableau des Défibrillateurs Filtrés")
    st.dataframe(filtered_df)
