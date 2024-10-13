import pandas as pd
import streamlit as st

def upload_file():
    uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xls", "xlsx"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        return df
    else:
        st.warning("Please upload an Excel file to proceed.")
        return None
