from components.file_uploader import upload_file
import streamlit as st
from components.data_processing2 import clean_and_process_data
from components.user_inputs import get_user_inputs
from components.display_metrics import display_metrics, display_charts
from components.calculations import calculate_unsold_stock,calculate_overstock, calculate_understock, calculate_negative_stock


st.set_page_config(page_title='Inventory Analysis',  layout='wide', page_icon=':ambulance:')

st.title("Inventory Analysis")

lead_time, days_stock_to_maintain, num_days = get_user_inputs()
df = upload_file()


with st.spinner('Updating Report...'):
    if df is not None and num_days is not None:
    # Clean and process data
        filtered_df = clean_and_process_data(df, num_days, lead_time)

        # Filter by voucher types (can add this functionality)
      

        # Perform calculations
        overstock = calculate_overstock(filtered_df, days_stock_to_maintain)
        understock = calculate_understock(filtered_df, lead_time)
        negative_stock = calculate_negative_stock(filtered_df)
        unsold_stock = calculate_unsold_stock(filtered_df)

        total_sales = (filtered_df['Out_quantity'] * filtered_df['Out_rate']).sum()
        total_purchases = (filtered_df['In_quantity'] * filtered_df['In_rate']).sum()
        total_closing_stock_value = (filtered_df['Close_quantity'] * filtered_df['Close_rate']).sum()
        total_opening_stock_value = (filtered_df['Open_quantity'] * filtered_df['Open_rate']).sum()
        unsold_stock_value = (filtered_df[filtered_df['Out_quantity'] == 0]['Close_quantity'] * filtered_df['Close_rate']).sum()
        excess_stock_value = overstock['Excess_Stock_Value'].sum()

        # Display metrics and charts
        display_metrics(total_opening_stock_value,excess_stock_value,overstock, understock, negative_stock, total_sales, total_purchases, unsold_stock_value, total_closing_stock_value)
        display_charts(overstock, understock,negative_stock,filtered_df,unsold_stock)
     
    else:
        st.warning("Please upload an Excel file to proceed.")