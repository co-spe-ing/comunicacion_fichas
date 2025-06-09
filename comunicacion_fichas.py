import streamlit as st
import os
import pandas as pd
import openpyxl

funcionarios = pd.read_excel("C:/Users/econtrerasb1/Documents/TAREA CARPETAS/COMUNICACIÓN_FICHAS.xlsx")


with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")
