import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from src.controller import build_system, evaluate

st.set_page_config(page_title="Ventilación difusa", page_icon="🌡️", layout="wide")
st.title("Control inteligente de ventilación")
st.write("Simulación de un controlador Mamdani con temperatura y humedad.")
a, b = st.columns(2)
with a:
    temperatura = st.slider("Temperatura (°C)", 0.0, 40.0, 25.0, .5)
with b:
    humedad = st.slider("Humedad relativa (%)", 0.0, 100.0, 60.0, 1.0)
salida = evaluate(temperatura, humedad)
st.metric("Velocidad recomendada", f"{salida:.1f} %")
st.progress(int(round(salida)))
st.caption("Modelo didáctico; no controla un dispositivo real.")
st.subheader("Reglas del controlador")
st.table({
    "Temperatura": ["Fría", "Fría", "Fría", "Templada", "Templada", "Templada", "Caliente", "Caliente", "Caliente"],
    "Humedad": ["Baja", "Media", "Alta", "Baja", "Media", "Alta", "Baja", "Media", "Alta"],
    "Velocidad": ["Baja", "Baja", "Media", "Baja", "Media", "Alta", "Alta", "Alta", "Alta"]
})
st.write("Inferencia Mamdani: mínimo para AND, máximo para agregación y centroide para desfusificación.")

_, variables = build_system()
st.subheader("Funciones de pertenencia")
fig, axes = plt.subplots(1, 3, figsize=(13, 3.5))
for ax, variable, titulo in zip(axes, variables, ["Temperatura", "Humedad", "Velocidad"]):
    for etiqueta, termino in variable.terms.items():
        ax.plot(variable.universe, termino.mf, label=etiqueta)
    ax.set_title(titulo)
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(alpha=.2)
st.pyplot(fig)
plt.close(fig)
if st.checkbox("Mostrar superficie de control"):
    temperaturas = np.linspace(0, 40, 21)
    humedades = np.linspace(0, 100, 21)
    valores = np.array([[evaluate(float(t), float(h)) for t in temperaturas] for h in humedades])
    fig2, ax = plt.subplots()
    imagen = ax.contourf(temperaturas, humedades, valores, levels=15)
    ax.set(xlabel="Temperatura (°C)", ylabel="Humedad (%)")
    fig2.colorbar(imagen, ax=ax, label="Velocidad (%)")
    st.pyplot(fig2)
    plt.close(fig2)
