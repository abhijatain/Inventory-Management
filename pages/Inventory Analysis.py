import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import altair as alt


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

    cleaned_df = cleaned_df[cleaned_df['SKUs'] != 'Grand Total']
    
    unique_particulars_df = pd.read_csv('categories.csv')

    voucher_type_mapping = dict(zip(unique_particulars_df['Particulars'], unique_particulars_df['Voucher Type']))

    # Use the map function to create a new column 'Voucher Type' in cleaned_df
    cleaned_df['Voucher Type'] = cleaned_df['SKUs'].map(voucher_type_mapping).fillna('Unknown')

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

col1, col2, col3 = st.columns(3)

# Place input widgets in the first column
with col1:
    lead_time = st.sidebar.number_input("Enter Lead Time (in days)", min_value=1, value=5,help='Time Taken for Items to be delivered')

# Place input widgets in the second column
with col2:
    days_stock_to_maintain = st.sidebar.number_input("Enter Days of Stock to Maintain", min_value=1, value=30,help='Enter Days for which you wish to maintain stock')

# Place input widgets in the third column
with col3:
    date_range = st.sidebar.date_input("Select Date Range for Data", [datetime.today(), datetime.today()],help='Enter the time period for which you have the data')


if len(date_range) == 2:
    start_date = date_range[0]
    end_date = date_range[1]
    num_days = (end_date - start_date).days  # Calculate the number of days
else:
    st.warning("Please select a valid date range.")

uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xls", "xlsx"])



with st.spinner('Updating Report...'):
    if uploaded_file is not None:
        # Load the data
        df = pd.read_excel(uploaded_file)

        # Process the data
        cleaned_df = clean_and_process_data(df, num_days)

        # Apply filter based on selected Voucher Type
        voucher_types = cleaned_df['Voucher Type'].unique()  
        selected_voucher = st.multiselect(
        "Choose Vouchers", list(voucher_types), ["Pharma"]
        )
        
        # If 'All' is selected, show all data, otherwise filter based on the voucher type
        filtered_df = cleaned_df[cleaned_df['Voucher Type'].isin(selected_voucher)]

        # Now, use the filtered_df for further calculations
        # Calculate overstock items
        overstock = filtered_df[filtered_df['Days_of_Stock'] > days_stock_to_maintain]
        overstock['Excess_Stock_Value'] = 0  # Initialize a new column for Excess Stock Value

        # Calculate excess stock value based on conditions
        overstock.loc[overstock['Days_of_Stock'] > days_stock_to_maintain, 'Excess_Stock_Value'] = np.where(
            overstock['In_rate'] != 0,
            (overstock['Days_of_Stock'] - days_stock_to_maintain) * overstock['In_rate'] * overstock['Average_sales'],
            (overstock['Days_of_Stock'] - days_stock_to_maintain) * overstock['Close_rate'] * overstock['Average_sales']
        )

         # Calculate undertsocked items
        understock = filtered_df[(filtered_df['Days_of_Stock'] < (lead_time * 1.5)) & (filtered_df['Days_of_Stock'] >= 0)]
        negative_stock = filtered_df[filtered_df['Days_of_Stock'] < 0]

        # Calculate excess stock value and counts
        excess_stock_value = overstock['Excess_Stock_Value'].sum()
        overstocked_items_count = len(overstock)
        understocked_items_count = len(understock)
        negative_stock_count = len(negative_stock)

        # Calculate the total closing stock value correctly
        total_closing_stock_value = (filtered_df['Close_quantity'] * filtered_df['Close_rate']).sum()
        total_sales = (filtered_df['Out_quantity'] * filtered_df['Out_rate']).sum()
        total_purchases = (filtered_df['In_quantity'] * filtered_df['In_rate']).sum()

        # Calculate total number of SKUs
        total_skus = len(filtered_df)

        # Calculate percentages
        overstocked_items_percentage = (overstocked_items_count / total_skus) * 100 if total_skus > 0 else 0
        excess_stock_percentage = (excess_stock_value / total_closing_stock_value) * 100 if total_closing_stock_value > 0 else 0

        # Calculate unsold stock based on NaN in 'Average_sales'
        unsold_stock = filtered_df[filtered_df['Out_quantity'] == 0]

        # Sum the unsold stock value (you can calculate based on 'Close_quantity' and 'Close_rate')
        # Assuming you want to calculate the total value of unsold stock:
        unsold_stock_value = (unsold_stock['Close_quantity'] * unsold_stock['Close_rate']).sum()


        # Display the metrics
        st.title('Results')

        total_columns = 4
        column_ratios = [1] * total_columns  # Equal width for each column
        m1, m2, m3, m4 = st.columns(column_ratios)
        m5, m6, m7, m8 = st.columns(column_ratios)

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

        m7.metric(
            label='Unsold Stock for the period', 
            value=int(unsold_stock_value),
            delta='Items value with 0 sales', 
            delta_color='inverse'
        )

        m8.metric(
            label='Total Closing', 
            value=int(total_closing_stock_value)
        )

        
        # Expandable sections for details
        with st.expander("Re-order Items", expanded=False):
            st.data_editor(understock, use_container_width=True)

        with st.expander("Overstocked Items", expanded=False):
            st.dataframe(overstock, use_container_width=True)

        with st.expander("All Items", expanded=False):
            st.data_editor(filtered_df, use_container_width=True)

        # Use filtered_df for any other analysis or display

        st.scatter_chart(
            understock,
            x="Days_of_Stock",
            y="Close_quantity",
            size="Close_rate",
            height=500
        )

    else:
        st.warning("Please upload an Excel file to proceed.")