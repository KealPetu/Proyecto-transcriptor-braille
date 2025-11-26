import pytest
from app.api.services.translator import text_to_braille, braille_to_text

# Constantes de prefijos para facilitar la lectura de los tests
# Basado en documento [cite: 111, 142]
PREFIJO_NUM = [3, 4, 5, 6]
PREFIJO_MAY = [4, 6]

def test_alfabeto_basico():
    """
    Verifica la traducción simple de letras minúsculas (Serie 1).
    Caso de prueba: 'hola'
    """
    texto = "hola"
    resultado = text_to_braille(texto)
    
    expected = [
        [1, 2, 5],       # h
        [1, 3, 5],       # o
        [1, 2, 3],       # l
        [1]              # a
    ]
    assert resultado == expected

def test_numeros_continuos():
    """
    Verifica que el prefijo de número se coloque SOLO al principio 
    de una cantidad de varias cifras[cite: 128].
    Caso de prueba: '12'
    """
    texto = "12"
    resultado = text_to_braille(texto)
    
    # Esperamos: [PREFIJO] + [a] + [b]
    expected = [
        PREFIJO_NUM,
        [1],         # 1 (equivale a 'a')
        [1, 2]       # 2 (equivale a 'b')
    ]
    assert resultado == expected

def test_numeros_separados():
    """
    Verifica que el espacio rompa el modo numérico y se requiera
    nuevo prefijo[cite: 129].
    Caso de prueba: '1 2'
    """
    texto = "1 2"
    resultado = text_to_braille(texto)
    
    # Esperamos: [PREFIJO][1] + [ESPACIO] + [PREFIJO][2]
    expected = [
        PREFIJO_NUM, [1],
        [],           # Espacio
        PREFIJO_NUM, [1, 2]
    ]
    assert resultado == expected

def test_mayusculas():
    """
    Verifica el prefijo de mayúsculas[cite: 142].
    Caso de prueba: 'A'
    """
    texto = "A"
    resultado = text_to_braille(texto)
    
    # Esperamos: [PREFIJO_MAY] + [a]
    expected = [
        PREFIJO_MAY,
        [1]
    ]
    assert resultado == expected

def test_mezcla_letras_numeros():
    """
    Verifica la transición entre texto y números.
    Caso de prueba: 'Bus 15' (Típico en señalética)
    """
    texto = "Bus 15"
    resultado = text_to_braille(texto)
    
    expected = [
        PREFIJO_MAY, [1, 2],    # B
        [1, 3, 6],              # u
        [2, 3, 4],              # s
        [],                     # Espacio
        PREFIJO_NUM,            # Prefijo número
        [1],                    # 1
        [1, 5]                  # 5
    ]
    assert resultado == expected

def test_bidireccionalidad_roundtrip():
    """
    Verifica que lo que se traduce a Braille y se devuelve a Texto 
    sea igual al original (ignorando case sensitivity si se desea, 
    pero nuestro sistema soporta mayúsculas).
    """
    original = "Hola 123 Mundo"
    braille = text_to_braille(original)
    recuperado = braille_to_text(braille)
    
    assert recuperado == original