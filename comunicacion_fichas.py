import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from io import BytesIO
import requests
import psycopg2


st.write("hola 11 de junio ...")

conn = psycopg2.connect(
    dbname = st.secrets.connections.postgresql.database,
    user = st.secrets.connections.postgresql.username,
    password = st.secrets.connections.postgresql.password,
    host = st.secrets.connections.postgresql.host,
    port = st.secrets.connections.postgresql.port
)
cursor = conn.cursor()

cursor.execute("SELECT version();")
st.write(cursor.fetchone())

sql = """CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    department VARCHAR(50)
);
"""
cursor.execute(sql)

sql = """INSERT INTO employees (name, age, department) VALUES
    ('Alice Johnson', 30, 'Engineering'),
    ('Bob Smith', 25, 'Marketing'),
    ('Charlie Brown', 35, 'Sales');
"""
cursor.execute(sql)

sql = """SELECT * FROM employees;"""
cursor.execute(sql)
rows = cursor.fetchall()
df = pd.DataFrame(rows)

st.dataframe(df)



cur.close()
conn.close()



with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")
