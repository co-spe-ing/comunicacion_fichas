import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from io import BytesIO
import requests
import psycopg2

st.write("hola 11 de junio ...")

###################################################################
# ABRIR CONEXIÓN A BD
###################################################################
def nuevaConexion():
    conn = psycopg2.connect(
        dbname = st.secrets.connections.postgresql.database,
        user = st.secrets.connections.postgresql.username,
        password = st.secrets.connections.postgresql.password,
        host = st.secrets.connections.postgresql.host,
        port = st.secrets.connections.postgresql.port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor
    
conn, cursor = nuevaConexion()
###################################################################
# pruebas
###################################################################
cursor.execute("SELECT version();")
st.write(cursor.fetchone())

sql = """SELECT * FROM personas;"""
cursor.execute(sql)
rows = cursor.fetchall()
col_names = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=col_names)
st.dataframe(df)
personasdf = df

###################################################################
# CREAR Y POBLAR TABLAS
###################################################################
crearYPoblarTablas = False
if crearYPoblarTablas:
    ###################################################################
    # CREAR TABLAS
    ###################################################################
    sqlTabla1 = """CREATE TABLE personas (
        cedula VARCHAR(20) PRIMARY KEY,
        nombres VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        cargo VARCHAR(100) NOT NULL,
        tipoNombramiento VARCHAR(100) NOT NULL,
        nivel2 VARCHAR(200) NOT NULL,
        nivel3 VARCHAR(200) NOT NULL,
        nivel4 VARCHAR(200) NOT NULL,
        proceso VARCHAR(300) NOT NULL,
        subproceso VARCHAR(300) NOT NULL
        );"""
    sqlTabla2 = """CREATE TABLE fichas (
        id SERIAL PRIMARY KEY,
        cedula VARCHAR(20) NOT NULL,
        ficha VARCHAR(12) NOT NULL,
        fechaComunicacion DATE NOT NULL,
        motivoCambio VARCHAR(30) NOT NULL,
        observaciones VARCHAR(2000) NOT NULL,
        fechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    cursor.execute("DROP TABLE IF EXISTS personas;")
    cursor.execute("DROP TABLE IF EXISTS fichas;")
    cursor.execute(sqlTabla1)
    cursor.execute(sqlTabla2)
    
    ###################################################################
    # INSERTAR DATOS DE PERSONAS EN TABLA
    ###################################################################
    doc_id = '1dyHiJaR3UySmG_7gQtamrDVfAqYFR_xW'
    sheet_id = '1506068283'
    sheet_url = f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={sheet_id}'
    personas = pd.read_csv(sheet_url)

    st.write("¡ya leyó el gsheets!")
    
    for k, row in personas.iterrows():
        print(k)
        cursor.execute(
            """INSERT INTO personas (cedula, nombres, apellidos, cargo, tipoNombramiento, nivel2, nivel3, nivel4, proceso, subproceso) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (row["Identificación"], row["Nombres"], row["Apellidos"], row["Cargo"], row["Tipo Nombramiento"], row["Dependencia Nivel 2"], row["Dependencia Nivel 3"], row["Dependencia Nivel 4"], row["Proceso"], row["Subproceso"])
        )
        if k % 100:
            cursor.close()
            conn.close()
            conn, cursor = nuevaConexion()
            
    st.write("¡¡¡ya insertó en la bd!!!")
    
    sql = """SELECT * FROM personas;"""
    cursor.execute(sql)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=col_names)
    st.dataframe(df.head())

###################################################################
# CERRAR CONEXIÓN A BD
###################################################################
cursor.close()
conn.close()

with st.form("formulario_persona"):
    optCedula = st.selectbox('Cédula', personasdf["cedula"])
    botonSeleccionPersona = st.form_submit_button("Seleccionar persona")
    if botonSeleccionPersona:
        nombres = personasdf.loc[personasdf["cedula"]==optCedula, "nombres"]
        apellidos = personasdf.loc[personasdf["cedula"]==optCedula, "apellidos"]
        cargo = personasdf.loc[personasdf["cedula"]==optCedula, "cargo"]
        tiponombramiento = personasdf.loc[personasdf["cedula"]==optCedula, "tiponombramiento"]
        nivel2 = personasdf.loc[personasdf["cedula"]==optCedula, "nivel2"]
        nivel3 = personasdf.loc[personasdf["cedula"]==optCedula, "nivel3"]
        nivel4 = personasdf.loc[personasdf["cedula"]==optCedula, "nivel4"]
        proceso = personasdf.loc[personasdf["cedula"]==optCedula, "proceso"]
        subproceso = personasdf.loc[personasdf["cedula"]==optCedula, "subproceso"]
        st.write(nombres)
        st.write(apellidos)
        st.write(cargo)
        st.write(tiponombramiento)
        st.write(nivel2)
        st.write(nivel3)
        st.write(nivel4)
        st.write(proceso)
        st.write(subproceso)

    
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")


