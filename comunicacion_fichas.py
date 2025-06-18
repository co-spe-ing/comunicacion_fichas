import streamlit as st
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from io import BytesIO
import requests
import psycopg2
from io import StringIO
import Levenshtein

st.logo("https://github.com/co-spe-ing/comunicacion_fichas/blob/e692aa5b85ae682f32a68e637c38310dd414c9d3/Logo.png")
st.write("Bogotá, 18 de junio de 2025.")



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

def consultaSQL(query):
    conn, cursor = nuevaConexion()
    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    resdf = pd.DataFrame(rows, columns=col_names)
    cursor.close()
    conn.close()
    return(resdf)

@st.cache_resource
def inicializar():
    ###################################################################
    # CREAR Y POBLAR TABLAS
    ###################################################################
    crearYPoblarTablas = True
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
        sqlTabla2 = """CREATE TABLE fichaxpersona (
            id SERIAL PRIMARY KEY,
            cedula VARCHAR(20) NOT NULL,
            ficha VARCHAR(12) NOT NULL,
            fechaComunicacion DATE NOT NULL,
            motivoCambio VARCHAR(30) NULL,
            observaciones VARCHAR(2000) NULL,
            fechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
        sqlTabla3 = """CREATE TABLE fichas (
            cargo VARCHAR(100) NOT NULL,
            ficha VARCHAR(12) PRIMARY KEY,
            proceso VARCHAR(300) NOT NULL,
            subproceso VARCHAR(300) NOT NULL
            );"""
        conn, cursor = nuevaConexion()
        #cursor.execute("DROP TABLE IF EXISTS personas;")
        cursor.execute("DROP TABLE IF EXISTS fichaxpersona;")
        cursor.execute("DROP TABLE IF EXISTS fichas;")
        #cursor.execute(sqlTabla1)
        cursor.execute(sqlTabla2)
        cursor.execute(sqlTabla3)
        
        ###################################################################
        # INSERTAR DATOS EN TABLA FICHAS
        ###################################################################
        sheet_url = "https://raw.githubusercontent.com/co-spe-ing/comunicacion_fichas/refs/heads/main/Fichas.csv"
        fichas = pd.read_csv(sheet_url, sep=";")
        buffer = StringIO()
        fichas.to_csv(buffer, index=False, header=False, sep='|')
        buffer.seek(0)
        cursor.copy_from(buffer, 'fichas', sep='|')

        ###################################################################
        # INSERTAR DATOS EN TABLA PERSONAS
        ###################################################################
        #doc_id = '1dyHiJaR3UySmG_7gQtamrDVfAqYFR_xW'
        #sheet_id = '1506068283'
        #sheet_url = f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={sheet_id}'
        #personas = pd.read_csv(sheet_url)
    
        #st.write("¡ya leyó el gsheets!")
        
        #for k, row in personas.iterrows():
        #    print(k)
        #    cursor.execute(
        #        """INSERT INTO personas (cedula, nombres, apellidos, cargo, tipoNombramiento, nivel2, nivel3, nivel4, proceso, subproceso) 
        #        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        #        (row["Identificación"], row["Nombres"], row["Apellidos"], row["Cargo"], row["Tipo Nombramiento"], row["Dependencia Nivel 2"], row["Dependencia Nivel 3"], row["Dependencia Nivel 4"], row["Proceso"], row["Subproceso"])
        #    )
        #    if k % 100:
        #        cursor.close()
        #        conn.close()
        #        conn, cursor = nuevaConexion()

        cursor.close()
        conn.close()

    ###################################################################
    # LEER DATOS
    ###################################################################
    personasdf = consultaSQL("""SELECT * FROM personas;""")
    fichasdf = consultaSQL("""SELECT * FROM fichas;""")
    
    return personasdf, fichasdf
    
personasdf, fichasdf = inicializar()

cedulaSeleccionada = st.selectbox(label='Cédula', options=personasdf["cedula"], index=None, placeholder="Selecciona una cédula...", )
if (cedulaSeleccionada != None):
    nombres = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "nombres"].to_numpy()[0]
    apellidos = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "apellidos"].to_numpy()[0]
    cargo = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "cargo"].to_numpy()[0]
    tiponombramiento = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "tiponombramiento"].to_numpy()[0]
    nivel2 = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "nivel2"].to_numpy()[0]
    nivel3 = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "nivel3"].to_numpy()[0]
    nivel4 = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "nivel4"].to_numpy()[0]
    proceso = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "proceso"].to_numpy()[0]
    subproceso = personasdf.loc[personasdf["cedula"]==cedulaSeleccionada, "subproceso"].to_numpy()[0]
    
    # Consular si previamente ya le han asignado ficha al funcionario
    fichaPrevia = ""
    sql = """SELECT ficha FROM fichaxpersona WHERE cedula='"""+cedulaSeleccionada+"""' ORDER BY fecharegistro DESC;"""
    resdf = consultaSQL(sql)
    if not resdf.empty: 
        fichaPrevia = resdf.iloc[0,0]
    
    st.write("**Cédula:**",cedulaSeleccionada)
    st.write("**Nombres:**",nombres)
    st.write("**Apellidos:**", apellidos)
    st.write("**Cargo:**", cargo)
    st.write("**Tipo de nombramiento:**", tiponombramiento)
    if nivel4 != "NaN": st.write("**Dependencia:**", nivel2, "-", nivel3, "-", nivel4) 
    else: st.write("**Dependencia:**", nivel2, "-", nivel3)
    st.write("**Proceso:**", proceso)
    st.write("**Subproceso:**", subproceso)
    st.write("**Ficha:**", fichaPrevia)

    # Solo mostrar las fichas del proceso, subrpoceso y cargo.
    distancias = fichasdf["proceso"].apply(lambda x: Levenshtein.distance(x, proceso))
    procesodefichas = fichasdf.loc[distancias.idxmin(),"proceso"]
    distancias = fichasdf["subproceso"].apply(lambda x: Levenshtein.distance(x, subproceso))
    subprocesodefichas = fichasdf.loc[distancias.idxmin(),"subproceso"]
    fichasDelProcesoYCargo = fichasdf.loc[(fichasdf["cargo"].str.upper()==cargo) & ((fichasdf["proceso"]==procesodefichas) & (fichasdf["subproceso"]==subprocesodefichas)), "ficha"]
    
    ficha = st.selectbox(label="Ficha", options=fichasDelProcesoYCargo, index=None, placeholder="Selecciona una ficha...",)
    fechaFicha = st.date_input(label="Fecha de comunicación de la ficha", value="today", format="DD/MM/YYYY")
    motivo = st.selectbox(label="Motivo del cambio de ficha (Opcional). Solo diligenciar si a alguien con ficha diligenciada se le cambia de nuevo la ficha.", options=("Reubicación","Cambio de funciones"), index=None, placeholder="Selecciona el motivo...")
    observaciones = st.text_area(label="Observaciones (Opcional).", height=150)

    st.write("**¡Antes de guardar verifica que los datos han sido diligenciados correctamente!**")
    if st.button("Guardar"):
        if ficha and fechaFicha:
            if fichaPrevia != "":
                if motivo:
                    conn, cursor = nuevaConexion()
                    cursor.execute("""INSERT INTO fichaxpersona (cedula, ficha, fechaComunicacion, motivoCambio, observaciones) 
                                    VALUES (%s, %s, %s, %s, %s);""", (cedulaSeleccionada, ficha, fechaFicha, motivo, observaciones))
                    cursor.close()
                    conn.close()
                    st.success("Se ha guardado correctamente.")
                else:
                    st.warning("Por favor ingresa el motivo del cambio de ficha.")
            else:
                conn, cursor = nuevaConexion()
                cursor.execute("""INSERT INTO fichaxpersona (cedula, ficha, fechaComunicacion, motivoCambio, observaciones) 
                                    VALUES (%s, %s, %s, %s, %s);""", (cedulaSeleccionada, ficha, fechaFicha, motivo, observaciones))
                cursor.close()
                conn.close()
                st.success("Se ha guardado correctamente.")
        else:
            st.warning("Por favor ingresa la ficha y la fecha de comunicación de la ficha.")

resdf = consultaSQL("""SELECT * FROM fichaxpersona;""")
st.dataframe(resdf)
    
        



