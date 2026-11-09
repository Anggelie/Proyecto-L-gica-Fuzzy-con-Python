import pytest
from src.controller import evaluate

@pytest.mark.parametrize("t,h", [(0, 0), (40, 100), (20, 50), (30, 70), (15, 30), (25, 60)])
def test_rango_salida(t, h):
    assert 0 <= evaluate(t, h) <= 100

def test_cambio_temperatura():
    assert evaluate(10, 50) < evaluate(35, 50)

def test_cambio_humedad():
    assert evaluate(23, 20) < evaluate(23, 90)

@pytest.mark.parametrize("t,h", [(-1, 50), (41, 50), (20, -1), (20, 101), (float("nan"), 50)])
def test_entradas_invalidas(t, h):
    with pytest.raises(ValueError):
        evaluate(t, h)
