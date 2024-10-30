import streamlit as st
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

def update_timestamps_in_datasets(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    reference_date = datetime.today().date()
    
    updated_datasets = {}

    for file in files:
        df = pd.read_csv(os.path.join(directory, file))
        
        last_timestamp = pd.to_datetime(df['Timestamp'].iloc[-1]).date()
        days_diff = (reference_date - last_timestamp).days

        df['Timestamp'] = pd.to_datetime(df['Timestamp']) + timedelta(days=days_diff)
        
        updated_datasets[file] = df
        
    return updated_datasets

def dashboard():
    st.markdown("---")
    
    dir_database = os.path.join(os.getcwd(), 'data')
    updated_datasets = update_timestamps_in_datasets(dir_database)
    dataset = updated_datasets.get('heat_exchanger.csv')
    
    if dataset is not None:
        col1, col2 = st.columns([1, 4])

        with col1:
            variable = st.selectbox("Choose a variable:", options=[col for col in dataset.columns if col != "Timestamp"])

        with col2:
            if variable:
                fig = px.line(dataset, x='Timestamp', y=variable, title=f"{variable} vs. Timestamp")
                fig.update_layout(
                    xaxis_title="Timestamp",
                    yaxis_title=variable,
                    height=300
                )
                st.plotly_chart(fig)