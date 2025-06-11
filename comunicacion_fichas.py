import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from io import BytesIO
import requests
import psycopg2



st.write("hola 11 de junio ...")


# Connect to the database
conn = psycopg2.connect(
    dbname = st.secrets.connections.postgresql.database,
    user = st.secrets.connections.postgresql.username,
    password = st.secrets.connections.postgresql.password,
    host = st.secrets.connections.postgresql.host,
    port = st.secrets.connections.postgresql.port
)

cur = conn.cursor()
cur.execute("SELECT version();")
st.write(cur.fetchone())
cur.close()
conn.close()


#conn = st.connection("postgresql", type="sql")
#df = conn.query("SELECT version();", ttl="10m")
#st.dataframe(df)

#sql = """CREATE TABLE employees (
#    id SERIAL PRIMARY KEY,
#    name VARCHAR(100) NOT NULL,
#    age INT,
#    department VARCHAR(50)
#);
#"""
#conn.query(sql, ttl="10m")
#ql = """INSERT INTO employees (name, age, department) VALUES
#('Alice Johnson', 30, 'Engineering'),
#('Bob Smith', 25, 'Marketing'),
#('Charlie Brown', 35, 'Sales');
#"""
#conn.query(sql, ttl="10m")
#sql = """SELECT * FROM employees;"""
#df = conn.query(sql, ttl="10m")
#st.dataframe(df)


with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")
