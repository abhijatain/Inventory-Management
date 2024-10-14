import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.sidebar.success("Select a demo above.")


st.markdown(
    """
    # 📊 Inventory Management System

    Welcome to the Inventory Management System! This tool helps in analyzing key inventory metrics such as overstock, understock, and unsold stock to optimize your inventory levels and improve operations.

    ### Steps and Formulas Used in the App:

    #### 1. **Overstock Identification:**
    Overstocked items are those where the current stock exceeds the desired levels. This excess stock ties up capital and increases storage costs.
    - **Metric:** Overstocked items are identified by comparing the actual stock value (`Close_quantity`) against an ideal stock level (`Ideal_Stock_Value`). 
    - **Goal:** Minimize excess stock to free up resources and reduce holding costs.
    """
)

st.latex(r'''
\text{Excess Stock Value} = \text{Close Stock Value} - \text{Ideal Stock Value}
''')

st.latex(r'''
\text{Ideal Stock Value} = \text{Average Daily Sales} \times \text{Days of Stock to Maintain}
''')


st.markdown(
    """
    #### 2. **Reorder Point:**
    The reorder point is the stock level at which a new order should be placed to avoid running out of stock.
    - **Metric:** Items in the reorder category are identified if their `Close_quantity` is less than the `Reorder_point`.
    - **Goal:** Reorder at the right time to prevent stockouts and maintain operational continuity.
    """
)

st.latex(r'''
\text{Reorder Point} = \text{Lead Time Demand} + \text{Safety Stock}
''')

st.latex(r'''
\text{Lead Time Demand} = \text{Average Daily Sales} \times \text{Lead Time}
''')


st.latex(r'''
\text{Safety Stock} = (\text{Maximum Daily Sales} \times \text{Maximum Lead Time})\\ - (\text{Average Daily Sales} \times \text{Average Lead Time})
''')


st.markdown(
    """
    #### 3. **Negative Stock:**
    Negative stock occurs when sales or usage are recorded without the inventory being updated correctly. This results in an inaccurate representation of actual stock.
    - **Metric:** The count of items with negative stock (`Close_quantity < 0`) is displayed.
    - **Goal:** Address negative stock promptly to avoid inventory discrepancies.

    #### 4. **Unsold Stock Value:**
    Unsold stock represents the items that have not been sold in a given period, which ties up capital and space.
    - **Goal:** Minimize unsold stock by reducing order quantities or running promotions.
    """
)

st.latex(r'''
\text{Unsold Stock Value} = \sum \text{Stock Value of items with zero sales}
''')

st.markdown(
    """
    #### 5. **Total Sales and Purchases:**
    Total sales and purchases provide insights into inventory movement and trends.
    - **Metric:** Sum of sales (`Out_quantity`) and purchases (`In_quantity`) during a specific period.
    - **Goal:** Understand inventory flow to ensure efficient stock replenishment.

    #### 6. **Days of Stock:**
    Days of stock refers to how long the current stock will last based on the average daily sales.
    - **Goal:** Maintain optimal stock levels so that there’s enough inventory for a set number of days without overstocking.
    """
)

st.latex(r'''
\text{Days of Stock} = \frac{\text{Close\_quantity}}{\text{Average Daily Sales}}
''')

st.markdown(
    """   
    #### 7. **Stock Turnover Ratio (STR):**  
      The STR measures how many times inventory is sold and replaced over a period.   
      - A higher STR indicates efficient inventory management.
    """
)
st.latex(r'''
      \text{Stock Turnover Ratio} = \frac{\text{Cost of Goods Sold (COGS)}}{\text{Average Inventory}}
''')
st.latex(r'''
\text{Average Inventory} = \frac{\text{Beginning Inventory} + \text{Ending Inventory}}{2}
''')

st.markdown(
    """
    ### Key Metrics in the Dashboard:

    - **Overstocked Items Count:** 
      - Items where `Close_quantity` exceeds `Ideal_Stock_Value`.  
      - You should regularly review overstocked items to reduce holding costs.

    - **Excess Stock Value:** 
      - Value of stock that exceeds the ideal levels.  
      - This helps in identifying capital tied up in excess inventory.

    - **Unsold Stock Value:** 
      - The value of inventory with zero sales over a period.  
      - Unsold stock should be minimized to improve cash flow and inventory turnover.

    - **Negative Stock Count:** 
      - Count of SKUs where stock has gone negative.  
      - Address negative stock to maintain accurate inventory levels.

    - **Reorder Items Count:** 
      - Items where the `Close_quantity` is below the `Reorder_point`.  
      - Reorder these items to avoid potential stockouts.

    - **Total Sales and Purchases:** 
      - These metrics provide insight into the flow of goods and help in forecasting future inventory requirements.

    - **Total Closing Stock Value:** 
      - The total value of the current inventory on hand.  
      - This helps in assessing the financial impact of holding stock.

    ### Optimization Goals:
    - **Minimize overstock** to reduce holding costs.
    - **Ensure timely reordering** to avoid stockouts.
    - **Monitor unsold stock** to identify slow-moving items.
    - **Correct negative stock** to maintain accurate inventory levels.
 
    For more information, you can refer to [inventory management best practices](https://www.investopedia.com/terms/i/inventory-management.asp).
    """
)




