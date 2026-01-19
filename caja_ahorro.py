import streamlit as st
import pandas as pd

st.set_page_config(page_title="Caja de Ahorro - Rendimientos", layout="wide")

st.title("💰 Calculadora de Rendimientos Diarios")

# --- SECCIÓN 1: CONFIGURACIÓN DEL BANCO ---
st.sidebar.header("Configuración del Banco")
capital_referencia = st.sidebar.number_input("Capital de referencia ($)", value=5000.0)
ganancia_referencia = st.sidebar.number_input("Ganancia por ese capital ($)", value=0.14, format="%.2f")

# Cálculo de la tasa diaria
tasa_diaria = ganancia_referencia / capital_referencia

st.sidebar.write(f"**Tasa aplicada:** {tasa_diaria:.6%}")

# --- SECCIÓN 2: DATOS DE LOS SOCIOS ---
st.header("Gestión de Ahorros de los Socios")

# Creamos una lista inicial de ejemplo (puedes cargar esto desde un CSV/Excel)
if 'datos_socios' not in st.session_state:
    data = {
        "Nombre": ["Fabián Aníbal"] + [f"Socio {i}" for i in range(2, 21)],
        "Saldo Ahorrado ($)": [130.0] + [0.0] * 19
    }
    st.session_state.datos_socios = pd.DataFrame(data)

# Editor de tabla (Excel-like)
edited_df = st.data_editor(st.session_state.datos_socios, num_rows="dynamic", use_container_width=True)

# --- SECCIÓN 3: RESULTADOS ---
st.divider()
st.subheader("Rendimientos Generados Hoy")

# Calcular rendimiento por fila
edited_df["Rendimiento Diario ($)"] = edited_df["Saldo Ahorrado ($)"] * tasa_diaria

# Mostrar resumen
total_ahorrado = edited_df["Saldo Ahorrado ($)"].sum()
total_rendimiento = edited_df["Rendimiento Diario ($)"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Ahorrado en Caja", f"${total_ahorrado:,.2f}")
col2.metric("Rendimiento a Repartir Hoy", f"${total_rendimiento:,.4f}")

st.dataframe(edited_df.style.format({"Saldo Ahorrado ($)": "{:.2f}", "Rendimiento Diario ($)": "{:.6f}"}))

# Botón para descargar a Excel
st.download_button(
    label="Descargar Reporte a Excel",
    data=edited_df.to_csv(index=False).encode('utf-8'),
    file_name='rendimientos_caja.csv',
    mime='text/csv',
)