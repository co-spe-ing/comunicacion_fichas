import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from io import BytesIO
import requests


st.write("hola 10 de junio ...")

# Initialize connection.
conn = st.connection("postgresql", type="sql")
# Perform query.
conn.query('CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT CHECK (age > 18),
    department VARCHAR(50),
    hired_date DATE DEFAULT CURRENT_DATE
);
', ttl="10m")

"""
sheet_name = 'Hoja1'
sheet_id = '1dyHiJaR3UySmG_7gQtamrDVfAqYFR_xW' 
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
r = requests.get(url)
data = r.content
df = pd.read_csv(BytesIO(data), index_col=0)
st.dataframe(df.head())
"""


with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")
