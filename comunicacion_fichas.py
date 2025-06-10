import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from io import BytesIO
import requests


st.write("hola 10 de junio :)")

url = "https://docs.google.com/spreadsheets/d/1dyHiJaR3UySmG_7gQtamrDVfAqYFR_xW/edit?gid=1506068283#gid=1506068283"
r = requests.get(url)
data = r.content
df = pd.read_csv(BytesIO(data), index_col=0)

st.dataframe(df.head())



with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")
