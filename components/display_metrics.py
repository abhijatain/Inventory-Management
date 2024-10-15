import streamlit as st
import altair as alt
import pandas as pd

def display_metrics(total_opening_stock_value,excess_stock_value, overstock, understock, negative_stock, total_sales, total_purchases, unsold_stock_value, total_closing_stock_value):
    # Create a DataFrame for metrics
    st.subheader("Results", divider="orange")
    s_t_r = (total_sales)/((total_closing_stock_value+total_opening_stock_value)/2)
    metrics_data = {
        "Results": [
            "Overstocked Items Count", 
            "Excess Stock Value", 
            "Unsold Stock Value", 
            "Negative Stock Count", 
            "Reorder Items Count", 
            "Total Sales", 
            "Total Purchases", 
            "Total Closing Stock Value",
            "Total Opening Stock Value",
            "Stock Turnover Ratio" 
        ],
        "Value": [
            len(overstock), 
            excess_stock_value, 
            unsold_stock_value, 
            len(negative_stock), 
            len(understock), 
            total_sales, 
            total_purchases, 
            total_closing_stock_value,
            total_opening_stock_value,
            s_t_r
        ],
        "Comments": [
            "High overstock might indicate over-purchasing",  # Overstock comment
            "Excess stock value affects working capital",      # Excess stock value comment
            "Unsold stock leads to inventory carrying costs",  # Unsold stock value comment
            "Negative stock may need urgent investigation",    # Negative stock comment
            "Re-order now to avoid stockouts",                 # Reorder items comment
            "Good sales performance",                          # Total sales comment
            "Purchases should align with forecast",            # Total purchases comment
            "Closing stock value reflects end-of-period inventory",
            "Opening stock value reflects start-of-period inventory",
               "A higher STR indicates efficient inventory management."   # Closing stock value comment
        ]
    }

    metrics_df = pd.DataFrame(metrics_data)

    # Format values with commas for thousands separator
    metrics_df["Value"] = metrics_df["Value"].apply(lambda x: f"{x:,.2f}")


    # Apply color formatting based on the metric type
    def color_metrics(val, metric):
        if isinstance(val, str):
            val = val.replace(',', '')
        val = int(val)
        
        # Custom color conditions per metric
        if metric == "Overstocked Items Count":
            color = 'red' if val > 500 else 'orange' if val > 200 else 'green'
        elif metric == "Excess Stock Value":
            color = 'red' if val > 10000 else 'orange' if val > 5000 else 'green'
        elif metric == "Unsold Stock Value":
            color = 'red' if val > 5000 else 'orange' if val > 2000 else 'green'
        elif metric == "Negative Stock Count":
            color = 'red' if val > 0 else 'green'
        elif metric == "Reorder Items Count":
            color = 'orange' if val > 50 else 'green'
        elif metric == "Total Sales":
            color = 'green' if val > 10000 else 'orange'
        elif metric == "Total Purchases":
            color = 'green' if val > 9000 else 'orange'
        else:  # "Total Closing Stock Value"
            color = 'green' if val > 3 else 'orange'

        return f'color: {color}'

    # Apply styles to the table for value column based on the metric name
    styled_df = metrics_df.style.apply(lambda x: [color_metrics(v, m) for v, m in zip(x, metrics_df['Results'])], subset=["Value"])

    # Display the table with Streamlit
    st.dataframe(metrics_df,use_container_width=True,)

def display_charts(overstock, understock,negative_stock,filtered_df,unsold_stock):
    # Display Re-order Items chart
    with st.expander("Re-order Items", expanded=True):
        st.data_editor(understock[['SKUs', 'Open_quantity', 'In_quantity', 
                                   'Out_quantity', 'Close_quantity', 
                                   'Average_sales', 'Days_of_Stock','Quantity_to_reorder','Reorder_point']], use_container_width=True)
        
        st.caption("NOTE: The :diamonds: location shows the reorder point.")
        st.altair_chart(
            # Layer 1: Bar chart.
            alt.Chart(understock.head(50))
            .mark_bar(
                orient="horizontal",
            )
            .encode(
                x="Close_quantity",
                y="SKUs",
            )
            # Layer 2: Chart showing the reorder point.
            + alt.Chart(understock.head(50))
            .mark_point(
                shape="diamond",
                filled=True,
                size=50,
                color="salmon",
                opacity=1,
            )
            .encode(
                x="Reorder_point",
                y="SKUs",
            ),
            use_container_width=True,
        )


    # Display Overstocked Items chart
    with st.expander("Overstocked Items", expanded=False):
        st.dataframe(overstock[['SKUs', 'Open_quantity', 'In_quantity', 
                                'Out_quantity', 'Close_quantity', 
                                'Average_sales', 'Days_of_Stock', 'Excess_Stock_Value','Ideal_Stock_Value']], 
                                use_container_width=True)
        
        st.caption("NOTE: The :diamonds: location shows the desirable quantity of stock to have")
        st.altair_chart(
            # Layer 1: Bar chart.
            alt.Chart(overstock.sort_values(by='Close_quantity',ascending=False).head(50))
            .mark_bar(
                orient="horizontal",
            )
            .encode(
                x="Close_quantity",
                y="SKUs",
            )
            # Layer 2: Chart showing the ideal stock value.
            + alt.Chart(overstock.sort_values(by='Close_quantity',ascending=False).head(50))
            .mark_point(
                shape="diamond",
                filled=True,
                size=50,
                color="salmon",
                opacity=1,
            )
            .encode(
                x="Ideal_Stock_Quanity",
                y="SKUs",
            ),
            use_container_width=True,
        )

    with st.expander("Unsold Stock Items", expanded=False):
        st.data_editor(unsold_stock[['SKUs', 'Open_quantity', 'Open_rate', 'Open_value', 
                          'In_quantity', 'In_rate', 'In_value', 
                          'Out_quantity', 'Out_rate', 'Out_value', 
                          'Close_quantity', 'Close_rate', 'Close_value']], use_container_width=True)

    with st.expander("Negative Stock Items", expanded=False):
        st.data_editor(negative_stock[['SKUs', 'Open_quantity', 'Open_rate', 'Open_value', 
                          'In_quantity', 'In_rate', 'In_value', 
                          'Out_quantity', 'Out_rate', 'Out_value', 
                          'Close_quantity', 'Close_rate', 'Close_value']], use_container_width=True)

    with st.expander("All Items", expanded=False):
        st.data_editor(filtered_df, use_container_width=True)