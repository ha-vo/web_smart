import streamlit as st
from pages import recomendationSystem

PAGES = {
    "Recomendation System": recomendationSystem
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    
page = PAGES[selection]
page.app()



