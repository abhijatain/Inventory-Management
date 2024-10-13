import streamlit as st
from datetime import datetime

def get_user_inputs():
    col1, col2, col3 = st.columns(3)

    with col1:
        lead_time = st.sidebar.number_input("Enter Lead Time (in days)", min_value=1, value=5,help='Time Taken for Items to be delivered')

    with col2:
        days_stock_to_maintain = st.sidebar.number_input("Enter Days of Stock to Maintain", min_value=1, value=30,help='Enter Days for which you wish to maintain stock')

    with col3:
        date_range = st.sidebar.date_input("Select Date Range for Data", [datetime.today(), datetime.today()],help='Enter the time period for which you have the data')

    if len(date_range) == 2:
        start_date = date_range[0]
        end_date = date_range[1]
        num_days = (end_date - start_date).days
    else:
        st.warning("Please select a valid date range.")
        num_days = None

    return lead_time, days_stock_to_maintain, num_days
