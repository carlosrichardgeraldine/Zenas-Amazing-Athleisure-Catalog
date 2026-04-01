import streamlit as st
# import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# from snowflake.snowpark import Session
import pandas as pd

session = get_active_session()

st.title("Zena's Amazing Athleisure Catalog")

# Query dropdown values
df = session.sql("""
    SELECT DISTINCT COLOR_OR_STYLE
    FROM CATALOG_FOR_WEBSITE
    ORDER BY COLOR_OR_STYLE
""").to_pandas()

options = df['COLOR_OR_STYLE'].tolist()

selected_value = st.selectbox("Pick a sweatsuit color or style", options)

# Show full row for selected value
if selected_value:
    df_row = session.sql(f"""
        SELECT *
        FROM CATALOG_FOR_WEBSITE
        WHERE COLOR_OR_STYLE = '{selected_value}'
    """).to_pandas()

    row = df_row.iloc[0]

    # st.subheader("Product Details")
    
    st.image(
        row['FILE_URL'],
        caption="Our warm, confortable, " + row['COLOR_OR_STYLE'] + " sweatsuit!"
    )
    
    st.write("**Price:** " + f"`$ {row['PRICE']}`")

    sizes_raw = row['SIZE_LIST']
    sizes = [s.strip() for s in sizes_raw.split('|') if s.strip()]
    st.write("**Sizes:**" + " ".join([f"`{size}`" for size in sizes]))
    # st.write(" ")
    
    st.write(f"{row['UPSELL_PRODUCT_DESC']}")
    

