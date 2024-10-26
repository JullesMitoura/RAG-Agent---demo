import streamlit as st
from app.pages.third import rag_page
from app.pages.first import dashboard
from app.pages.chatbot import chat
from app.agent import CustomAgent
from app.services.qdrant_service import QdrantService

st.set_page_config(layout="wide")
st.markdown("""
<style>
    [data-testid=stSidebar] {
        width: 240px; 
        min-width: 240px;
        max-width: 240px;
    }
    [data-testid=stSidebar] * {
        color: grey;
    }
    [data-testid="stImage"] {
        display: block;
        margin-left: 50px;
        margin-right: auto;
    }
    .css-18e3th9 {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    .css-1d391kg {
        padding-top: 0rem;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="center-image">', unsafe_allow_html=True)
st.sidebar.image("./imgs/bot.png", width=80)

qdrant_service = QdrantService()
collections_response = qdrant_service.collections_verify()
collections = [collection.name for collection in collections_response.collections]

collections = collections
selected_collection = st.sidebar.selectbox("Select Collection:", collections)
pagina = st.sidebar.radio("", ["Dashboard", "RAG Service"])

if pagina == "Dashboard":
    dashboard()
    st.markdown("---")
    chat(selected_collection)

elif pagina == "RAG Service":
    rag_page()