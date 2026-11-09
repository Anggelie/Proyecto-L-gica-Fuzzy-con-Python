# Control inteligente de ventilación con lógica difusa

Proyecto de Lógica Matemática: opción 2, Python y `scikit-fuzzy`.

## Integrantes
- David Sebastián Lemus Nitsch — 241155
- Arodi Josué Chávez Ramírez — 241112
- Jorge Carlos Chupina Moscoso — 22213
- Yehosua Friedrich Hercules Pérez — 241452
- Anggelie Lizeth Velásques Asencio — 221181
- Tracey Dally Ramírez Balcarcel — 241035

## Descripción
Simulación de un ventilador que recomienda una velocidad según temperatura (0–40 °C) y humedad relativa (0–100 %). Se utiliza inferencia Mamdani con nueve reglas y desfusificación por centroide.

## Ejecutar
```bash
python -m venv .venv
# En Windows: .venv\Scripts\activate
# En macOS o Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Pruebas
```bash
python -m pytest -q
```

Por defecto, pytest ejecuta las pruebas de la carpeta `tests` del proyecto principal.

## Archivos
- `src/controller.py`: funciones de pertenencia y reglas.
- `app.py`: simulador con gráficas.
- `tests/test_controller.py`: pruebas.
- `docs/Informe_Logica_Difusa.tex`: informe editable para Overleaf.

El documento PDF se genera compilando el archivo `.tex` en Overleaf o con `pdflatex`.

**Nota:** los rangos y reglas son didácticos; la salida es una recomendación simulada.
