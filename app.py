"""Interfaz académica del controlador de ventilación difusa."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from src.controller import build_system, evaluate, explain, REGLAS

st.set_page_config(page_title="Ventilación difusa", page_icon="🌡️", layout="wide")
st.set_option("client.toolbarMode", "minimal")
st.markdown("""
<style>
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stMainMenu"],
[data-testid="stMainMenuPopover"],
[data-testid="stAppDeployButton"],
#MainMenu {display: none !important;}
</style>
""", unsafe_allow_html=True)
st.title("Control inteligente de ventilación", anchor=False)
st.write("Aplicación de scikit-fuzzy: inferencia Mamdani con temperatura y humedad.")

a, b = st.columns(2)
with a:
    temperatura = st.slider("Temperatura (°C)", 0.0, 40.0, 25.0, 0.5)
with b:
    humedad = st.slider("Humedad relativa (%)", 0.0, 100.0, 60.0, 1.0)

detalle = explain(temperatura, humedad)
salida = detalle["velocidad"]
st.metric("Velocidad recomendada del ventilador", f"{salida:.1f} %")
st.progress(int(round(salida)))
st.caption("Simulación académica: no controla un ventilador real.")

st.subheader("1. Pertenencia de las entradas", anchor=False)
c1, c2 = st.columns(2)
with c1:
    st.write("Temperatura")
    st.dataframe(pd.DataFrame([
        {"Conjunto": k.capitalize(), "Pertenencia": round(v, 4)}
        for k, v in detalle["temperatura"].items()
    ]), hide_index=True, use_container_width=True)
with c2:
    st.write("Humedad")
    st.dataframe(pd.DataFrame([
        {"Conjunto": k.capitalize(), "Pertenencia": round(v, 4)}
        for k, v in detalle["humedad"].items()
    ]), hide_index=True, use_container_width=True)

st.subheader("2. Reglas activadas", anchor=False)
st.write("La fuerza de cada regla se obtiene con el mínimo de las dos pertenencias.")
if detalle["reglas"]:
    st.dataframe(pd.DataFrame([
        {
            "Si temperatura": r["temperatura"].capitalize(),
            "Y humedad": r["humedad"].capitalize(),
            "Entonces velocidad": r["velocidad"].capitalize(),
            "Activación": round(r["activacion"], 4),
        }
        for r in detalle["reglas"]
    ]), hide_index=True, use_container_width=True)
else:
    st.warning("No se activaron reglas.")

st.subheader("3. Agregación y desfusificación", anchor=False)
st.write("Las salidas recortadas se combinan con el máximo. El centroide determina la velocidad final.")
fig, ax = plt.subplots(figsize=(9, 3))
ax.fill_between(detalle["universo"], detalle["agregada"], alpha=0.35, label="Salida agregada")
ax.plot(detalle["universo"], detalle["agregada"])
ax.axvline(salida, color="tab:red", linestyle="--", label=f"Centroide: {salida:.1f} %")
ax.set(xlabel="Velocidad (%)", ylabel="Pertenencia", xlim=(0, 100), ylim=(0, 1.05))
ax.grid(alpha=0.2)
ax.legend()
st.pyplot(fig)
plt.close(fig)

with st.expander("Ver las nueve reglas del controlador"):
    st.dataframe(pd.DataFrame([
        {"Temperatura": t.capitalize(), "Humedad": h.capitalize(), "Velocidad": v.capitalize()}
        for t, h, v in REGLAS
    ]), hide_index=True, use_container_width=True)

st.subheader("4. Funciones de pertenencia", anchor=False)
_, variables = build_system()
fig, axes = plt.subplots(1, 3, figsize=(13, 3.5))
for ax, variable, titulo in zip(axes, variables, ["Temperatura", "Humedad", "Velocidad"]):
    for etiqueta, termino in variable.terms.items():
        ax.plot(variable.universe, termino.mf, label={"fria": "Fría"}.get(etiqueta, etiqueta.capitalize()))
    ax.set_title(titulo)
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(alpha=0.2)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.subheader("5. Experimentos", anchor=False)
escenarios = [
    ("Frío", 10.0, 30.0),
    ("Templado", 25.0, 60.0),
    ("Caluroso", 35.0, 85.0),
]
filas = []
for nombre, t, h in escenarios:
    v = evaluate(t, h)
    filas.append({
        "Escenario": nombre,
        "Temperatura (°C)": t,
        "Humedad (%)": h,
        "Velocidad calculada (%)": round(v, 2),
    })
st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True)
st.caption("Resultados calculados al ejecutar el modelo; no son mediciones de un equipo físico.")

with st.expander("Mostrar superficie de control (puede tardar unos segundos)"):
    if st.button("Calcular superficie"):
        temperaturas = np.linspace(0, 40, 21)
        humedades = np.linspace(0, 100, 21)
        valores = np.array([[evaluate(float(t), float(h)) for t in temperaturas] for h in humedades])
        fig, ax = plt.subplots()
        imagen = ax.contourf(temperaturas, humedades, valores, levels=15)
        ax.set(xlabel="Temperatura (°C)", ylabel="Humedad (%)")
        fig.colorbar(imagen, ax=ax, label="Velocidad (%)")
        st.pyplot(fig)
        plt.close(fig)
