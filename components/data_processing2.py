import pandas as pd
import numpy as np

def clean_and_process_data(df, num_days, lead_time):
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
    
   
    # Replace NaN values with 0 for simpler calculations
    cleaned_df = cleaned_df.fillna(0).infer_objects(copy=False)

    # Calculate average daily sales based on the date range (num_days)
    cleaned_df['Average_sales'] = cleaned_df['Out_quantity'] / num_days

    cleaned_df['Days_of_Stock'] = np.where(cleaned_df['Average_sales'] != 0,
                                        cleaned_df['Close_quantity'] / cleaned_df['Average_sales'], 
                                        -1)

    # Convert 'Days_of_Stock' to integer rounded down
    cleaned_df['Days_of_Stock'] = np.floor(cleaned_df['Days_of_Stock']).astype(int)

    # Reorder point calculation
    cleaned_df['Reorder_point'] = np.where(cleaned_df['Average_sales'] != 0,
                                           (cleaned_df['Average_sales'] * lead_time) * 1.5, 
                                           -1)
    
    cleaned_df['Quantity_to_reorder'] = num_days* cleaned_df['Average_sales']
    return cleaned_df
