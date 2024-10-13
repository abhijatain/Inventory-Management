import numpy as np

def calculate_overstock(filtered_df, days_stock_to_maintain):
    overstock = filtered_df[filtered_df['Days_of_Stock'] > days_stock_to_maintain]
    overstock['Excess_Stock_Value'] = np.where(
        overstock['In_rate'] != 0,
        (overstock['Days_of_Stock'] - days_stock_to_maintain) * overstock['In_rate'] * overstock['Average_sales'],
        (overstock['Days_of_Stock'] - days_stock_to_maintain) * overstock['Close_rate'] * overstock['Average_sales']
    )
    overstock['Ideal_Stock_Value'] = overstock['Close_value'] - overstock['Excess_Stock_Value']
    return overstock

def calculate_understock(filtered_df, lead_time):
    understock = filtered_df[(filtered_df['Days_of_Stock'] < (lead_time * 1.5)) & (filtered_df['Days_of_Stock'] >= 0)]
    return understock

def calculate_negative_stock(filtered_df):
    negative_stock = filtered_df[filtered_df['Days_of_Stock'] < 0]
    return negative_stock
