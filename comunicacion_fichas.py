import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from io import BytesIO
import requests


st.write("hola 11 de junio ...")


conn = st.connection("postgresql", type="sql")
df = conn.query("SELECT version();", ttl="10m")
st.dataframe(df)

df = conn.query("CREATE TABLE employees (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, age INT, department VARCHAR(50));", ttl="10m")
st.dataframe(df)





with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")
