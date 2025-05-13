import streamlit as st
import pandas as pd
import os
from datetime import datetime

EXCEL_FILE = "base_datos.xlsx"

if not os.path.exists(EXCEL_FILE):
    df_init = pd.DataFrame(columns=["FECHA", "CODIGO", "CELULAR 1", "CELULAR 2", "CORREO 1", "CORREO 2", "OBS"])
    df_init.to_excel(EXCEL_FILE, index=False)

df = pd.read_excel(EXCEL_FILE)

st.set_page_config(page_title="Buscador y Registrador", layout="centered")
st.title("📋 Buscador y Registrador de Datos")

with st.form("registro_form"):
    fecha = st.date_input("FECHA", value=datetime.today())
    codigo = st.text_input("CÓDIGO")
    celular1 = st.text_input("CELULAR 1")
    celular2 = st.text_input("CELULAR 2")
    correo1 = st.text_input("CORREO 1")
    correo2 = st.text_input("CORREO 2")
    obs = st.text_area("OBSERVACIONES")

    col1, col2 = st.columns(2)
    with col1:
        registrar = st.form_submit_button("✅ REGISTRAR")
    with col2:
        borrar = st.form_submit_button("🗑️ BORRAR")

    if borrar:
        st.experimental_rerun()

    if registrar:
        nuevo_registro = {
            "FECHA": fecha,
            "CODIGO": codigo.strip(),
            "CELULAR 1": celular1.strip(),
            "CELULAR 2": celular2.strip(),
            "CORREO 1": correo1.strip(),
            "CORREO 2": correo2.strip(),
            "OBS": obs.strip()
        }

        existe = ((df["CODIGO"] == nuevo_registro["CODIGO"]) |
                  (df["CELULAR 1"] == nuevo_registro["CELULAR 1"]) |
                  (df["CELULAR 2"] == nuevo_registro["CELULAR 2"]) |
                  (df["CORREO 1"] == nuevo_registro["CORREO 1"]) |
                  (df["CORREO 2"] == nuevo_registro["CORREO 2"])).any()

        if existe:
            st.warning("⚠️ DATOS EXISTENTES")
        else:
            df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            st.success("✅ DATOS REGISTRADOS")
