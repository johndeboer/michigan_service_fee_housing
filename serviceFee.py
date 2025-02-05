from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
from st_keyup import st_keyup

global df
global filteredDf

source_url = 'https://www.michigan.gov/taxes/professionals/tax-exempt-housing'

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = True

    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = df.columns
        for column in to_filter_columns:
            user_text_input = st_keyup(
                f"Filter {column}",
                key=column,
                debounce=200
            )
            if user_text_input:
                df = df[df[column].astype(str).str.contains(user_text_input, case=False)]

    return df

st.title('Michigan Service Fee Housing List')
st.write("This list represents the service fee housing addresses on file with the Michigan Department of Treasury, and may be useful for preparing certain Michigan Homestead Property Tax Credit claims.")
st.caption(f"Last downloaded from {source_url} on February 5, 2025.")
st.caption("__*** Data is not all-inclusive, see the source website for disclaimers.__ ***")

df = pd.read_excel('./Service Fee and Exempt Housing.xlsx')

df.drop(df.columns[0], axis=1, inplace=True)
df.rename(columns={df.columns[0]: 'Zip Code', df.columns[1]: 'Street Address'}, inplace=True)
df['Zip Code'] = df['Zip Code'].astype('str')

df_container = st.container()
with df_container:

    st.dataframe(filter_dataframe(df), hide_index=True, width=2000, height=600)

