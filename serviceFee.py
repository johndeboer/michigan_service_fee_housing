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

@st.cache_data
def load_data():
    df = pd.read_excel('./Service Fee and Exempt Housing.xlsx')

    # df.drop(df.columns[0], axis=1, inplace=True)  // 2025-05-14: New source file removed blank column on Service Fee sheet
    df.rename(columns={df.columns[0]: 'Zip Code', df.columns[1]: 'Street Address'}, inplace=True)

    # Extract street name from address to sort by zip code and street name
    df['Street'] = df['Street Address'].str.extract(r'\s1?\/?2?\s?(.*)')  #Exclude anything before the first space, and optionally "1/2"
    df.sort_values(['Zip Code','Street'], inplace=True)
    df.drop(['Street'], axis=1, inplace=True)  #Only needed street for sorting, not display
    df['Zip Code'] = df['Zip Code'].astype('str') 
    return df


st.title('Michigan Service Fee Housing List')
st.write("This list represents the service fee housing addresses on file with the Michigan Department of Treasury, and may be useful for preparing certain Michigan Homestead Property Tax Credit claims.")
st.caption(f"Last downloaded from {source_url} on May 14, 2025.")
st.caption("__*** Data is not all-inclusive, see the source website for disclaimers.__ ***")

df = load_data()

df_container = st.container()
with df_container:

    st.dataframe(filter_dataframe(df), hide_index=True, width=2000, height=600)

