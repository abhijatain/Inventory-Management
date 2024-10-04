import pandas as pd
import numpy as np
import streamlit as st
import streamlit_pandas as sp
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder


def display_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
    gb.configure_side_bar()  # Enable sidebar for search and filters
    gb.configure_default_column(editable=True)  # Enable column editing
    gb.configure_grid_options(domLayout='autoHeight')  # Automatically adjust grid height

    grid_options = gb.build()

    # Render AgGrid with wider space for "full-screen" like experience
    AgGrid(
        df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,  # Enable search, filters, etc.
        allow_unsafe_jscode=True,
        height=800,  # Set height to make it occupy more space
    )


# Function to clean and process the data
def clean_and_process_data(df, num_days):
    # Identify the first occurrence of 'Quantity', 'Rate', or 'Value'
    keyword_row_index = df.apply(lambda row: row.astype(str).str.contains('Quantity|Rate|Value').any(), axis=1)
    first_occurrence_index = keyword_row_index[keyword_row_index].index[0]

    # Clean the DataFrame by slicing from the identified row
    cleaned_df = df.iloc[first_occurrence_index + 1:].reset_index(drop=True)

    # Rename columns appropriately
    cleaned_df.columns = ['SKUs', 'Open_quantity', 'Open_rate', 'Open_value', 
                          'In_quantity', 'In_rate', 'In_value', 
                          'Out_quantity', 'Out_rate', 'Out_value', 
                          'Close_quantity', 'Close_rate', 'Close_value']

    # Replace NaN values with 0 for simpler calculations
    cleaned_df = cleaned_df.fillna(0).infer_objects(copy=False)

    # Calculate average daily sales based on the date range (num_days)
    cleaned_df['Average_sales'] = cleaned_df['Out_quantity'] / num_days
    cleaned_df['Average_sales'].replace(0, np.nan, inplace=True)  # Handle zero sales

    # Calculate Days of Stock
    cleaned_df['Days_of_Stock'] = np.where(cleaned_df['Average_sales'] != 0,
                                           cleaned_df['Close_quantity'] / cleaned_df['Average_sales'], np.nan)
    cleaned_df['Days_of_Stock'] = pd.to_numeric(cleaned_df['Days_of_Stock'], errors='coerce')

    return cleaned_df

# Streamlit file uploader
st.set_page_config(page_title='Inventory Analysis',  layout='wide', page_icon=':ambulance:')

st.title("Inventory Analysis")

        # Ask for lead time and days of stock to maintain before file upload
lead_time = st.number_input("Enter Lead Time (in days)", min_value=1, value=5)
days_stock_to_maintain = st.number_input("Enter Days of Stock to Maintain", min_value=1, value=30)
date_range = st.date_input("Select Date Range for Data", [datetime.today(), datetime.today()])

if len(date_range) == 2:
    start_date = date_range[0]
    end_date = date_range[1]
    num_days = (end_date - start_date).days  # Calculate the number of days
else:
    st.warning("Please select a valid date range.")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

with st.spinner('Updating Report...'):
    if uploaded_file is not None:
            # Load the data
        df = pd.read_excel(uploaded_file)
            

            # Process the data
        cleaned_df = clean_and_process_data(df,num_days)
        
            # Calculate and display overstock items
        overstock = cleaned_df[cleaned_df['Days_of_Stock'] > days_stock_to_maintain]
        overstock['Excess_Stock_Value'] = 0  # Initialize a new column for Excess Stock Value

            # Calculate excess stock value based on conditions
        overstock.loc[overstock['Days_of_Stock'] > days_stock_to_maintain, 'Excess_Stock_Value'] = np.where(
            overstock['In_rate'] != 0,
            (overstock['Days_of_Stock'] - days_stock_to_maintain) * overstock['In_rate']*overstock['Average_sales'],
            (overstock['Days_of_Stock'] - days_stock_to_maintain) * overstock['Close_rate']*overstock['Average_sales']
        )
    

        understock = cleaned_df[(cleaned_df['Days_of_Stock'] < (lead_time*1.5))&(cleaned_df['Days_of_Stock'] >= 0)]
        negative_stock = cleaned_df[(cleaned_df['Days_of_Stock'] < 0)]
    
        excess_stock_value = overstock['Excess_Stock_Value'].sum()

        # Calculate overstocked and understocked items count
        overstocked_items_count = len(overstock)
        understocked_items_count = len(understock)
        negative_stock_count = len(negative_stock)

        # Display results
            # Calculate the total closing stock value correctly
        total_closing_stock_value = (cleaned_df['Close_quantity'] * cleaned_df['Close_rate']).sum()
        total_sales = cleaned_df['Out_value'].sum()
        total_purchases = cleaned_df['In_value'].sum()

        # Calculate total number of SKUs
        total_skus = len(cleaned_df)

        # Calculate percentages
        overstocked_items_percentage = (overstocked_items_count / total_skus) * 100 if total_skus > 0 else 0
        excess_stock_percentage = (excess_stock_value / total_closing_stock_value) * 100 if total_closing_stock_value > 0 else 0


        # Display results with actual percentages
        st.title('Results')
        total_columns = 4
        column_ratios = [1] * total_columns  # Equal width for each column

        m1, m2, m3, m4 = st.columns(column_ratios)
        m5,m6,m7,m8 =  st.columns(column_ratios)

        m1.metric(
            label='Overstocked Items Count', 
            value=int(overstocked_items_count), 
            delta=f'{overstocked_items_percentage:.2f}%' + ' of total SKUs', 
            delta_color='inverse'
        )

        m2.metric(
            label='Reorder Items Count', 
            value=int(understocked_items_count), 
            delta='Re-order now to avoid stockouts', 
            delta_color='normal'
        )

        m3.metric(
            label='Excess Stock Value', 
            value=int(excess_stock_value), 
            delta=f'{excess_stock_percentage:.2f}%' + ' of total stock value', 
            delta_color='inverse'
        )

        m4.metric(
            label='Negative Stock Count', 
            value=int(negative_stock_count)
        )

        m5.metric(
            label='Total Sales', 
            value=int(total_sales)
        )

        m6.metric(
            label='Total Purchases', 
            value=int(total_purchases)
        )
                

        st.title('Re-order')
        st.dataframe(understock, use_container_width=True)
        
        st.title('Overstocked')
        st.dataframe(overstock, use_container_width=True)

        
    else:
        st.warning("Please upload an Excel file to proceed.")
