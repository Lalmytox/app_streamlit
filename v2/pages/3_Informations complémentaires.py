import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


import streamlit as st


st.title("ℹ️ À propos de l’Open Data RATP")

st.markdown(
    """
    ## Pourquoi Open Data ?  
    La **RATP** a choisi de s’associer à la démarche publique d’**Open Data**, initiée par l’État, pour **rendre accessibles à tous** certaines de ses données.  
    L’objectif est de permettre à des **citoyens, développeurs, chercheurs ou entreprises** d’exploiter ces données — pour créer des applications, outils, analyses, ou visualisations innovantes.  
    Grâce à cette ouverture, chacun peut contribuer à améliorer la mobilité, la transparence, et l’accès aux informations du réseau en Île-de-France.  
    """
)

st.markdown(
    """
    ## 📚 Types de données disponibles  
    - Plans du métro, RER, tramways, bus — géographies, correspondances… :contentReference[oaicite:5]{index=5}  
    - Localisation d’équipements ou services (comme les défibrillateurs, sanitaires, etc.) :contentReference[oaicite:6]{index=6}  
    - Données de trafic, horaires, potentiellement flux ou fréquentation (selon dataset) :contentReference[oaicite:7]{index=7}  
    - Données de qualité de service, accessibilité, infrastructures, et plus selon ce qui est publié. :contentReference[oaicite:8]{index=8}  
    """
)

st.markdown(
    """
    ## 🚀 Ce que ça permet  
    - Construire des **cartes personnalisées** (stations, équipements, services)  
    - Proposer des **applications mobiles ou web** : itinéraires, accessibilité, alertes, etc.  
    - Réaliser des **analyses** (statistiques, couverture territoriale, densité, besoins, etc.)  
    - Favoriser **l’innovation citoyenne** : tout le monde peut contribuer, créer, partager — améliorer le service public.  
    """
)

st.markdown("---")

st.markdown(
    "### 🔗 Pour explorer les données vous‑même"
)
st.markdown(
    "[Open Data RATP — Portail officiel](https://www.ratp.fr/la-ratp-et-lopen-data)", 
    unsafe_allow_html=True
)

st.markdown(
    "[Dataset « Défibrillateurs du réseau RATP » (exemple)](https://data.gouv.fr/datasets/defibrillateurs-du-reseau-ratp)", 
    unsafe_allow_html=True
)

st.markdown("---")

st.title("ℹ️ Qu'est-ce qu'un défibrilateur ? ")
st.markdown("Site externe : www.drexcomedical.fr")
st.components.v1.iframe("https://www.drexcomedical.fr/blog/quand-et-comment-utiliser-un-defibrillateur/", height=600, scrolling=True)
