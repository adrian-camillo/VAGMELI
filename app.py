import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Carga de datos
def load_data():
    df = pd.read_csv('Ventas por Artículo (6).csv', encoding="ISO-8859-1", delimiter=';')
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)
    
    # Convertir columnas con comas en decimales a float
    df['Cantidad'] = df['Cantidad'].str.replace(',', '.').astype(float)
    
    return df

df = load_data()

# Título de la aplicación
st.title('Análisis de Ventas')

# Selección de Rango de Fechas
fecha_min = df['Fecha'].min().date()
fecha_max = df['Fecha'].max().date()
fecha_inicio, fecha_fin = st.date_input('Selecciona un rango de fechas:', [fecha_min, fecha_max])
fecha_inicio = pd.Timestamp(fecha_inicio)
fecha_fin = pd.Timestamp(fecha_fin)

# Selección de Eje X
opciones_eje_x = ['Fecha', 'Proveedor', 'Color', 'Temporada', 'Familia N1', 'Familia N2', 'Familia N3']
opciones_eje_x = [opc for opc in opciones_eje_x if opc in df.columns]
eje_x = st.selectbox('Elige la columna para el Eje X:', opciones_eje_x)

# Selección de Eje Y
columnas_numericas = df.columns[df.dtypes.isin(['int64', 'float64'])].tolist()
eje_y = st.selectbox('Elige la columna para el Eje Y:', columnas_numericas)

df_filtrado = df[(df['Fecha'] >= fecha_inicio) & (df['Fecha'] <= fecha_fin)]
df_filtrado = df_filtrado[df_filtrado[eje_y] >= 0]

# Selección de tipo de gráfico
tipos_grafico = ["Barra", "Línea", "Circular", "Dispersión"]
tipo_grafico = st.selectbox('Selecciona el tipo de gráfico:', tipos_grafico)

# Limitar el número de registros mostrados para ciertas columnas
if eje_x in ["Familia N2", "Familia N3", "Proveedor", "Color"]:
    num_registros = st.slider('Selecciona el número de registros principales a mostrar:', 5, 50, 10)
    datos_graficar = df_filtrado.groupby(eje_x).agg({eje_y: 'sum'}).reset_index()
    datos_graficar = datos_graficar.sort_values(by=eje_y, ascending=False).head(num_registros)
else:
    datos_graficar = df_filtrado

# Generar gráfico según el tipo seleccionado
if tipo_grafico == "Barra":
    fig = px.bar(datos_graficar, x=eje_x, y=eje_y, title=f"{eje_y} por {eje_x}")
elif tipo_grafico == "Línea":
    fig = px.line(datos_graficar, x=eje_x, y=eje_y, title=f"Tendencia de {eje_y} por {eje_x}")
elif tipo_grafico == "Circular":
    fig = px.pie(datos_graficar, names=eje_x, values=eje_y, title=f"Distribución de {eje_y} por {eje_x}")
elif tipo_grafico == "Dispersión":
    fig = px.scatter(datos_graficar, x=eje_x, y=eje_y, title=f"Relación entre {eje_x} y {eje_y}")

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # Fondo transparente
    xaxis_title=eje_x,
    yaxis_title=eje_y,
    xaxis_tickangle=-90  # Etiquetas del eje X rotadas a 90 grados
)

st.plotly_chart(fig)
