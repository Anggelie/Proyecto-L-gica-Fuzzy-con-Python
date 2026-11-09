"""Controlador difuso Mamdani para un ventilador."""
from functools import lru_cache
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

@lru_cache(maxsize=1)
def build_system():
    temperatura = ctrl.Antecedent(np.arange(0, 40.1, .1), "temperatura")
    humedad = ctrl.Antecedent(np.arange(0, 100.1, .1), "humedad")
    velocidad = ctrl.Consequent(np.arange(0, 100.1, .1), "velocidad")
    temperatura["fria"] = fuzz.trapmf(temperatura.universe, [0, 0, 12, 20])
    temperatura["templada"] = fuzz.trimf(temperatura.universe, [15, 23, 31])
    temperatura["caliente"] = fuzz.trapmf(temperatura.universe, [26, 33, 40, 40])
    humedad["baja"] = fuzz.trapmf(humedad.universe, [0, 0, 25, 45])
    humedad["media"] = fuzz.trimf(humedad.universe, [30, 50, 70])
    humedad["alta"] = fuzz.trapmf(humedad.universe, [55, 75, 100, 100])
    velocidad["baja"] = fuzz.trapmf(velocidad.universe, [0, 0, 15, 35])
    velocidad["media"] = fuzz.trimf(velocidad.universe, [25, 50, 75])
    velocidad["alta"] = fuzz.trapmf(velocidad.universe, [65, 85, 100, 100])
    reglas = [
        ctrl.Rule(temperatura["fria"] & humedad["baja"], velocidad["baja"]),
        ctrl.Rule(temperatura["fria"] & humedad["media"], velocidad["baja"]),
        ctrl.Rule(temperatura["fria"] & humedad["alta"], velocidad["media"]),
        ctrl.Rule(temperatura["templada"] & humedad["baja"], velocidad["baja"]),
        ctrl.Rule(temperatura["templada"] & humedad["media"], velocidad["media"]),
        ctrl.Rule(temperatura["templada"] & humedad["alta"], velocidad["alta"]),
        ctrl.Rule(temperatura["caliente"] & humedad["baja"], velocidad["alta"]),
        ctrl.Rule(temperatura["caliente"] & humedad["media"], velocidad["alta"]),
        ctrl.Rule(temperatura["caliente"] & humedad["alta"], velocidad["alta"]),
    ]
    return ctrl.ControlSystem(reglas), (temperatura, humedad, velocidad)

def evaluate(temperature_c, humidity_pct):
    if not np.isfinite(temperature_c) or not np.isfinite(humidity_pct):
        raise ValueError("Las entradas deben ser números finitos.")
    if not 0 <= temperature_c <= 40 or not 0 <= humidity_pct <= 100:
        raise ValueError("Temperatura: 0 a 40 °C; humedad: 0 a 100 %.")
    sistema, _ = build_system()
    simulacion = ctrl.ControlSystemSimulation(sistema)
    simulacion.input["temperatura"] = float(temperature_c)
    simulacion.input["humedad"] = float(humidity_pct)
    simulacion.compute()
    return float(simulacion.output["velocidad"])
