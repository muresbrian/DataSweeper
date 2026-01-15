import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(page_title="Barredora", page_icon="🧹", layout="wide")

# Título
st.title("🧹 Limpiador de Datos Pro")
st.markdown("Sube tus archivos CSV o Excel para limpiarlos automáticamente.")

# Función para cargar datos
def load_data(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Widget de subida de archivos
uploaded_file = st.file_uploader("Sube un archivo (CSV o Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    if df is not None:
        # Información Original
        st.subheader("📊 Vista Previa de Datos Originales")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Filas originales: {df.shape[0]}")
        with col2:
            st.info(f"Columnas originales: {df.shape[1]}")
            
        st.dataframe(df.head())

        # Botón de Limpieza en la barra lateral
        with st.sidebar:
            st.header("Opciones")
            limpiar = st.button("Limpiar Datos", type="primary")

        if limpiar:
            # Lógica de Limpieza
            original_rows = df.shape[0]
            
            # 1. Eliminar duplicados
            df_cleaned = df.drop_duplicates()
            
            # 2. Eliminar filas vacías
            df_cleaned = df_cleaned.dropna(how='all')
            
            # 3. Capitalizar columnas de texto
            # Convertimos a string solo las columnas de tipo object para aplicar capitalize
            # Pero cuidado, si hay números mezclados puede ser tricky. 
            # El requerimiento dice: "Convertir todas las columnas de texto"
            
            text_cols = df_cleaned.select_dtypes(include=['object']).columns
            for col in text_cols:
                # Aplicamos capitalize a cada valor, convirtiendo primero a string para asegurar
                # Usamos map o apply. .str.capitalize() funciona bien en series.
                df_cleaned[col] = df_cleaned[col].astype(str).str.capitalize()

            # Resultados
            st.divider()
            st.success("✅ ¡Datos limpiados exitosamente!")
            
            cleaned_rows = df_cleaned.shape[0]
            rows_removed = original_rows - cleaned_rows
            
            st.subheader("📉 Estadísticas de Limpieza")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Filas Nuevas", cleaned_rows)
            with m2:
                st.metric("Filas Eliminadas", rows_removed)
            with m3:
                 st.metric("Columnas", df_cleaned.shape[1])

            st.dataframe(df_cleaned.head())
            
            # Exportación
            # Convertir DataFrame a CSV
            csv_buffer = io.StringIO()
            df_cleaned.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="📥 Descargar CSV Procesado",
                data=csv_data,
                file_name=f"cleaned_{uploaded_file.name.rsplit('.', 1)[0]}.csv",
                mime="text/csv"
            )
