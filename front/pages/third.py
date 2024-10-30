import streamlit as st
from app.services.rag_service import RagService
from app.services.qdrant_service import QdrantService
import os

def rag_page():
    st.header("RAG Service Manage")
    st.markdown("---")
    
    qdrant_service = QdrantService()
    collections_response = qdrant_service.collections_verify()
    collections = [collection.name for collection in collections_response.collections]
    
    st.subheader("Select or Create Collection")
    collection_names = collections
    collection_names.append("New Collection")  

    selected_collection = st.selectbox("Select an existing collection or create a new one:", collection_names)

    if selected_collection == "New Collection":
        collection_name = st.text_input("Enter the name for the new collection:")
    else:
        collection_name = selected_collection
    
    uploaded_file = st.file_uploader("Upload a document (PDF, TXT, etc.):", type=["pdf", "txt", "docx", "pptx"])

    if uploaded_file is not None:
        service = RagService()
        file_content = uploaded_file.read()
        file_name = uploaded_file.name
        file_type = os.path.splitext(file_name)[1].lower()
        service.qdrant_processing(file_content=file_content, file_name=uploaded_file.name, collection_name=collection_name, file_type = file_type)
        st.success(f"File '{uploaded_file.name}' has been uploaded and processed in collection '{collection_name}'.")

    st.markdown("---")

    dashboard_link = os.getenv("DASH_LINK")

    if dashboard_link:
        # Create a button that links directly to the dashboard
        st.link_button(label="Go to Dashboard", url=dashboard_link, type="primary")
    else:
        st.error("Dashboard link is not set in the environment.")