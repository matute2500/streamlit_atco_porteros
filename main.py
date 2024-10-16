import streamlit as st
import pandas as pd
import supabase
from supabase import create_client, Client
from json import loads, dumps

# Inyectar CSS personalizado
css = """
<style>
    .stDataFrame th {
        background-color: #4CAF50;
        color: white;
        font-family: Arial, sans-serif;
        font-size: 16px;
    }
    .stDataFrame td, .stDataFrame th {
        border: 2px solid #4CAF50;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

url: str = "https://tvglznbmklajgnffgdok.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2Z2x6bmJta2xhamduZmZnZG9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3MTg1MDcsImV4cCI6MjA0MzI5NDUwN30.SM2Zmc6BdSvbTaLUl-ZSVDoQlPliMCblQTvmEIfWnOY"
supabase: Client = create_client(url, key) 

sql = supabase.table('porteros').select("*").execute()
datos_consulta_tabla_partidos = sql.data

print (datos_consulta_tabla_partidos)





st.title("PORTEROS")
st.markdown("En esta seccion puede añadir porteros, modificar sus datos, mostrar un listado de los porteros y ver sus estadisticas")


tab1, tab2, tab3, tab4 = st.tabs(["LISTADO", "AÑADIR", "ESTADISTICAS", "MODIFICAR"])

with tab1:
    st.header("LISTADO DE PORTEROS")
    
with tab2:
    st.header("AÑADIR UN PORTERO")
    with st.form("formulario_grabacion_partidos"):
        st.write("GRABACION DE PARTIDOS")
        nombre = st.text_input('NOMBRE')
        apellidos = st.text_input('APELLIDOS')
        fecha_nacimiento = st.date_input('FECHA NACIMIENTO')
        edad = st.number_input('EDAD', step=1)
        equipo = st.selectbox('EQUIPO', ['Alevin A F7', 'Benjamin A', 'Benjamin B', 'Prebenjamin A'], index=None, placeholder='Seleccione un equipo')

        boton_grabar_portero = st.form_submit_button('Grabar PORTERO')
        if boton_grabar_portero:
            print(fecha_nacimiento)
            fecha_nacimiento_str = fecha_nacimiento.isoformat()
            print(fecha_nacimiento_str)
            supabase.table('porteros').insert({"nombre": nombre, "apellidos": apellidos, "fecha_nac": fecha_nacimiento_str, "edad": edad, "equipo": equipo,}).execute()

with tab3:
    st.header("ESTADISTICAS")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
with tab4:

    st.markdown("""
    <style>
    h2 {
        color: #96D4D4;
        font-family: Arial, sans-serif;
    }
    
        
    
    </style>
    """, unsafe_allow_html=True)

    st.header("MODIFICAR DATOS DE UN PORTERO")
    dataframe_datos_porteros = pd.DataFrame(datos_consulta_tabla_partidos)
    dataframe_datos_porteros['Modificar'] = ['Modificar'] * len(dataframe_datos_porteros)
    df_editar = st.data_editor(dataframe_datos_porteros, num_rows="dynamic", key='data_editor')

    
    button_modificar_portero = st.button("Modificar Portero")
    
    if button_modificar_portero:
        # Limpiar valores no finitos en la columna 'edad'
        #df_editar['edad'] = df_editar['edad'].fillna(0).replace([float('inf'), float('-inf')], 0).astype(int)
        
        porteros_list = df_editar.to_dict(orient='records')
        for portero in porteros_list:
            
            id_con_decimial = portero['id']
            print(id_con_decimial)
            id_sin_decimal = int(id_con_decimial)
            print(id_sin_decimal)
            edad_con_decimal = portero['edad']
            print(edad_con_decimal)
            edad_sin_decimal = int(edad_con_decimal)
            print(edad_sin_decimal)
            portero['id'] = id_sin_decimal
            portero['edad'] = edad_sin_decimal

        print(porteros_list)
        
        
        # Borrar todos los registros de la tabla 'porteros'
        #supabase.table('porteros').delete().neq('id', 0).execute()
        
        # Insertar los nuevos datos en la tabla 'porteros'
        #supabase.table('porteros').insert(porteros_list).execute()
        supabase.table('porteros').upsert(porteros_list).execute()
        
        st.write("Datos modificados correctamente")
