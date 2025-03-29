import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos desde el archivo Excel
@st.cache_data
def cargar_datos():
    archivo = "RANKING ENERO 2025 EMERGIA.xlsx"
    datos = pd.read_excel(archivo, sheet_name="Datos", skiprows=3)
    datos = datos.dropna(subset=["Unnamed: 5"])  # Eliminar filas vacías
    datos.columns = datos.iloc[0]  # Usar la fila 0 como encabezado
    datos = datos[1:]  # Eliminar fila de encabezado anterior
    datos = datos.rename(columns={
        'TEAMLEADER': 'Team Leader',
        'Horas efectivas': 'Horas Efectivas',
        'Ventas Movil FBB': 'Ventas Móvil',
        'Total Ventas Fijo FBB': 'Ventas Fijo',
        '% Conversión Móvil': '% Conversión Móvil',
        '% Conversión Fijo': '% Conversión Fijo',
        '$ Total a pagar': 'Total $',
    })
    return datos

datos = cargar_datos()

st.title("🌟 Ranking de Desempeño - Emergia Enero 2025")
st.markdown("Filtra y consulta los resultados del equipo comercial.")

# Sidebar para filtros
with st.sidebar:
    st.header("Filtros")
    teamleaders = datos['Team Leader'].dropna().unique()
    seleccion_tl = st.multiselect("Selecciona Team Leaders", teamleaders, default=teamleaders)
    min_ventas = st.slider("Ventas Mínimas Móvil", 0, 300, 0)

# Aplicar filtros
datos_filtrados = datos[datos['Team Leader'].isin(seleccion_tl)]
datos_filtrados = datos_filtrados[datos_filtrados['Ventas Móvil'] >= min_ventas]

# Mostrar tabla con los datos filtrados
st.subheader("Tabla de resultados")
st.dataframe(datos_filtrados, use_container_width=True)

# Gráficas comparativas
st.subheader("📊 Visualización de KPIs")
kpi_opcion = st.selectbox("Selecciona KPI para comparar", ['Ventas Móvil', 'Ventas Fijo', 'Horas Efectivas', '% Conversión Móvil', '% Conversión Fijo'])
fig = px.bar(datos_filtrados, x='Team Leader', y=kpi_opcion, color='Team Leader', title=f"{kpi_opcion} por Team Leader")
st.plotly_chart(fig, use_container_width=True)

# Descargar datos
st.download_button("Descargar Excel Filtrado", datos_filtrados.to_excel(index=False), file_name="ranking_filtrado.xlsx")
