import streamlit as st
import pandas as pd
from supabase import create_client, Client
import gdown

id = "14LD9iisP2aqx9tmypqKq7lGMmC853Rwn"
output = "archivo.csv"
gdown.download(id=id, output=output)
#df_clubs = pd.read_csv(output)
df_clubs = pd.read_csv(output, index_col=0, sep=';', encoding='latin-1')
st.write(df_clubs)



url: str = "https://tvglznbmklajgnffgdok.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2Z2x6bmJta2xhamduZmZnZG9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3MTg1MDcsImV4cCI6MjA0MzI5NDUwN30.SM2Zmc6BdSvbTaLUl-ZSVDoQlPliMCblQTvmEIfWnOY"
supabase: Client = create_client(url, key)    

#consulta_fila = supabase.table('partidos').select("*").eq("id","1").execute()
#consulta=st.write(consulta_fila)

consulta_tabla_partidos = supabase.table('partidos').select("*").execute()
datos_consulta_tabla_partidos = consulta_tabla_partidos.data
nombres_campos = datos_consulta_tabla_partidos[0].keys() # Los nombres de los campos en un diccionario

df_datos_consulta_partidos = pd.DataFrame(datos_consulta_tabla_partidos)
df_datos_columnas = pd.DataFrame(nombres_campos)

df = pd.DataFrame(
    [
       {"id": 1, "FECHA": "Juan", "HORA": "Perez", "COMPETICION": "Liga", "EQUIPO_LOCAL": "Real Madrid", "EQUIPO_VISITANTE": "Barcelona", "RESULTADO": "2-1"},
   ]
)
edited_df = st.data_editor(df, num_rows="dynamic")
#*************************************************************
with st.form("formulario_grabacion_partidos"):
    
    st.write("GRABACION DE PARTIDOS")
    
    fecha = st.date_input('FECHA')
    hora = st.time_input('HORA')
    campo = st.text_input('CAMPO')
    competicion = st.selectbox('COMPETICION', ['LIGA','Torneo','Amistoso'], index=None, placeholder='Seleccione una competicion')
    
    col1, col2 = st.columns(2)
    with col1:
        equipo_atco = st.selectbox('EQUIPO ATCO',("Alevin A F7", "Benjamin A", "Benjamin B", "Prebenjamin A"),index=None,placeholder="Seleccione un Equipo",
    )
    with col2:
        goles_atco = st.number_input('GOLES ATLETICO', step=1)
    
    col3, col4 = st.columns(2)
    with col3:
        equipo_rival = st.text_input('EQUIPO RIVAL')
    with col4:
        goles_rival = st.number_input('GOLES RIVAL', step=1)

    col5, col6 = st.columns(2)
    with col5:
        portero_titular = st.selectbox('PORTERO TITULAR',("Luis Garcia", "Pedro Garcia", "Luis Fernandez", "Juan Vargas"),index=None,placeholder="Seleccione un Portero",
    )
    with col6:
        min_titular = st.number_input('MINUTOS PORTERO TITULAR', step=1)

    col7, col8 = st.columns(2)
    with col7:
        portero_suplente = st.selectbox('PORTERO SUPLENTE',("Luis Garcia", "Pedro Garcia", "Luis Fernandez", "Juan Vargas"),index=None,placeholder="Seleccione un Portero",
    )
    with col8:
        min_suplente = st.number_input('MINUTOS PORTERO SUPLENTE', step=1)

    
    st.form_submit_button('Grabar Partido')
#*************************************************************





#*************************************************************
# This is outside the form
st.write(fecha,hora,competicion,equipo_atco,goles_atco,equipo_rival,goles_rival)

#*************************************************************


st.write(df_datos_consulta_partidos, df_datos_columnas,df)
 
