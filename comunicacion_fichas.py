import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection

st.write("hola 10 de junio")

url = "https://docs.google.com/spreadsheets/d/1dyHiJaR3UySmG_7gQtamrDVfAqYFR_xW/edit?gid=1506068283#gid=1506068283"
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(data.head())


with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")
