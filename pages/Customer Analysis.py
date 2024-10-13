import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(page_title='Customer Analysis',  layout='wide', page_icon=':ambulance:')

st.title("Customer Analysis")

uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xls", "xlsx"])


with st.spinner('Updating Report...'):
    if uploaded_file is not None:
        # Load the data
        df = pd.read_excel(uploaded_file)
        # Step 1: Find the index where the row starts with "Date"
        start_row = df[df.iloc[:, 0] == 'Date'].index[0]

        # Step 2: Drop all rows above the row where "Date" starts
        df_cleaned = df.iloc[start_row:]

        # Step 3: Rename the columns using the first row (the 'Date' row)
        df_cleaned.columns = df_cleaned.iloc[0]  # Set the first row as column names

        # Step 4: Drop the first row since it's now the header
        df_cleaned = df_cleaned.drop(df_cleaned.index[0])

        # Step 5: Select columns only up to "Gross Total"
        columns_to_keep = ['Date', 'Particulars', 'Voucher Type', 'Voucher No.', 'Quantity', 'Value', 'Gross Total']
        df_cleaned = df_cleaned[columns_to_keep]

        # Reset the index (optional, to clean up the index)
        df_cleaned = df_cleaned.reset_index(drop=True)

        df_cleaned['Voucher Type'] = df_cleaned['Voucher Type'].ffill()
        df_cleaned['Voucher No.'] = df_cleaned['Voucher No.'].ffill()

        final = df_cleaned[df_cleaned['Date'].isna()]
        final = final.drop(columns=['Date','Gross Total'])

        valid_voucher_types = ['Pharma Sales R', 'Pharma Sales W']
        final = final[final['Voucher Type'].isin(valid_voucher_types)]

        grouped_df = final.groupby('Voucher No.')[['Quantity', 'Value']].sum()

        # Step 2: Store it in another DataFrame for analysis
        analysis_df = grouped_df.reset_index()

        quantity_bins = [-float('inf'), 1, 2, 3, 4, 5, 10, float('inf')]
        quantity_labels = ['below 1', '1-2', '2-3', '3-4', '4-5', '5-10', '>10']

        value_bins = [-float('inf'), 50, 100, 200, 300, 400, float('inf')]
        value_labels = ['below 50', '50-100', '100-200', '200-300', '300-400', 'above 400']

        analysis_df['Value Bin'] = pd.cut(analysis_df['Value'], bins=value_bins, labels=value_labels, right=False)
        analysis_df['Quantity Bin'] = pd.cut(analysis_df['Quantity'], bins=quantity_bins, labels=quantity_labels, right=False)


        st.dataframe(analysis_df, use_container_width=True)

        quantity_data = analysis_df['Quantity Bin'].value_counts().reset_index()

# Rename columns for Altair to recognize them
        quantity_data.columns = ['Quantity Bin', 'count']
        
        st.subheader("Quanity Wise Breakdown", divider="orange")
        st.altair_chart(
            alt.Chart(quantity_data)
            .mark_bar(orient="horizontal")
            .encode(
                x="count",
                y="Quantity Bin",
            ),
            use_container_width=True,
        )

        value_data = analysis_df['Value Bin'].value_counts().reset_index()
        value_data.columns = ['Value Bin', 'count']
        st.subheader("Value Wise Breakdown", divider="orange")
        st.altair_chart(
            alt.Chart(value_data)
            .mark_bar(orient="horizontal")
            .encode(
                x="count",
                y="Value Bin",
            ),
            use_container_width=True,
        )
    else:
        st.warning("Please upload an Excel file to proceed.")