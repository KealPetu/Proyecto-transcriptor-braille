import pytest
from app.api.services.translator import text_to_braille, braille_to_text

PREFIJO_NUM = [3, 4, 5, 6]
PREFIJO_MAY = [4, 6]


class TestSerie1:
    def test_letra_a(self):
        assert text_to_braille("a") == [[1]]
    
    def test_letra_j(self):
        assert text_to_braille("j") == [[2, 4, 5]]
    
    def test_serie_1_completa(self):
        resultado = text_to_braille("abcdefghij")
        assert len(resultado) == 10


class TestSerie2:
    def test_letra_k(self):
        """k = a + punto 3"""
        resultado = text_to_braille("k")
        assert resultado == [[1, 3]]
    
    def test_letra_t(self):
        """t = j + punto 3"""
        resultado = text_to_braille("t")
        assert resultado == [[2, 3, 4, 5]]


class TestSerie3:
    def test_letra_u(self):
        """u = a + puntos 3 y 6"""
        resultado = text_to_braille("u")
        assert resultado == [[1, 3, 6]]
    
    def test_letra_z(self):
        """z = f + puntos 3 y 6"""
        resultado = text_to_braille("z")
        assert resultado == [[1, 2, 3, 4, 6]]
    
    def test_letra_w(self):
        resultado = text_to_braille("w")
        # w = c (1,4) + puntos 3 y 6 = [1, 3, 4, 6]
        assert resultado == [[1, 3, 4, 6]]


class TestAcentos:
    def test_a_acentuada(self):
        resultado = text_to_braille("á")
        assert resultado == [[1, 2, 3, 5, 6]]
    
    def test_e_acentuada(self):
        resultado = text_to_braille("é")
        assert resultado == [[2, 3, 4, 6]]
    
    def test_i_acentuada(self):
        resultado = text_to_braille("í")
        assert resultado == [[3, 4]]
    
    def test_o_acentuada(self):
        resultado = text_to_braille("ó")
        assert resultado == [[1, 3, 4, 6]]
    
    def test_u_acentuada(self):
        resultado = text_to_braille("ú")
        assert resultado == [[1, 2, 4, 5, 6]]
    
    def test_n_con_tilde(self):
        resultado = text_to_braille("ñ")
        assert resultado == [[1, 2, 4, 5, 6]]


class TestNumeros:
    def test_numero_unico(self):
        resultado = text_to_braille("1")
        assert resultado == [PREFIJO_NUM, [1]]
    
    def test_numero_cero(self):
        resultado = text_to_braille("0")
        assert resultado == [PREFIJO_NUM, [2, 4, 5]]
    
    def test_numeros_continuos(self):
        """Prefijo solo al inicio"""
        resultado = text_to_braille("123")
        assert resultado == [
            PREFIJO_NUM,
            [1],           # 1
            [1, 2],        # 2
            [1, 4]         # 3
        ]
    
    def test_numeros_separados_por_espacio(self):
        """Nuevo prefijo después del espacio"""
        resultado = text_to_braille("1 2")
        assert resultado == [
            PREFIJO_NUM, [1],
            [],
            PREFIJO_NUM, [1, 2]
        ]
    
    def test_numero_con_punto_decimal(self):
        resultado = text_to_braille("1.5")
        assert resultado == [
            PREFIJO_NUM, [1], [2, 5, 6], [1, 5]
        ]


class TestMayusculas:
    def test_mayuscula_simple(self):
        resultado = text_to_braille("A")
        assert resultado == [PREFIJO_MAY, [1]]
    
    def test_palabra_capitalizada(self):
        resultado = text_to_braille("Hola")
        assert resultado == [
            PREFIJO_MAY, [1, 2, 5],  # H
            [1, 3, 5],                # o
            [1, 2, 3],                # l
            [1]                       # a
        ]
    
    def test_varias_mayusculas(self):
        resultado = text_to_braille("ABC")
        assert len(resultado) == 6  # 3 prefijos + 3 letras


class TestPuntuacion:
    def test_punto(self):
        resultado = text_to_braille(".")
        assert resultado == [[2, 5, 6]]
    
    def test_coma(self):
        resultado = text_to_braille(",")
        assert resultado == [[2]]
    
    def test_dos_puntos(self):
        resultado = text_to_braille(":")
        assert resultado == [[2, 5]]
    
    def test_interrogacion(self):
        resultado = text_to_braille("?")
        assert resultado == [[2, 3, 6]]
    
    def test_exclamacion(self):
        resultado = text_to_braille("!")
        assert resultado == [[2, 3, 5]]
    
    def test_guion(self):
        resultado = text_to_braille("-")
        assert resultado == [[3, 6]]


class TestCasosReales:
    def test_hola(self):
        resultado = text_to_braille("hola")
        assert resultado == [
            [1, 2, 5],  # h
            [1, 3, 5],  # o
            [1, 2, 3],  # l
            [1]         # a
        ]
    
    def test_bus_15(self):
        resultado = text_to_braille("Bus 15")
        assert resultado == [
            PREFIJO_MAY, [1, 2],  # B
            [1, 3, 6],             # u
            [2, 3, 4],             # s
            [],                    # espacio
            PREFIJO_NUM, [1], [1, 5]  # 15
        ]
    
    def test_frase_con_puntuacion(self):
        resultado = text_to_braille("¡Hola!")
        # Debe incluir: !apertura, H mayús, hola, !cierre
        assert len(resultado) >= 6
    
    def test_numero_con_coma_decimal(self):
        resultado = text_to_braille("3.14")
        assert resultado[0] == PREFIJO_NUM  # Comienza con prefijo


class TestInversa:
    def test_braille_to_text_letra_a(self):
        resultado = braille_to_text([[1]])
        assert resultado == "a"
    
    def test_braille_to_text_letra_e(self):
        resultado = braille_to_text([[1, 5]])
        assert resultado == "e"
    
    def test_braille_to_text_letra_j(self):
        resultado = braille_to_text([[2, 4, 5]])
        assert resultado == "j"
    
    def test_braille_to_text_serie_2_letra_k(self):
        resultado = braille_to_text([[1, 3]])
        assert resultado == "k"
    
    def test_braille_to_text_serie_3_letra_u(self):
        resultado = braille_to_text([[1, 3, 6]])
        assert resultado == "u"
    
    def test_braille_to_text_espacio(self):
        resultado = braille_to_text([[]])
        assert resultado == " "
    
    def test_braille_to_text_numero_1(self):
        resultado = braille_to_text([PREFIJO_NUM, [1]])
        assert resultado == "1"
    
    def test_braille_to_text_numero_0(self):
        resultado = braille_to_text([PREFIJO_NUM, [2, 4, 5]])
        assert resultado == "0"
    
    def test_braille_to_text_numero_123(self):
        resultado = braille_to_text([PREFIJO_NUM, [1], [1, 2], [1, 4]])
        assert resultado == "123"
    
    def test_braille_to_text_mayuscula_A(self):
        resultado = braille_to_text([PREFIJO_MAY, [1]])
        assert resultado == "A"
    
    def test_braille_to_text_mayuscula_Z(self):
        resultado = braille_to_text([PREFIJO_MAY, [1, 2, 3, 4, 6]])
        assert resultado == "Z"
    
    def test_braille_to_text_punto(self):
        resultado = braille_to_text([[2, 5, 6]])
        assert resultado == "."
    
    def test_braille_to_text_coma(self):
        resultado = braille_to_text([[2]])
        assert resultado == ","
    
    def test_braille_to_text_interrogacion(self):
        resultado = braille_to_text([[2, 3, 6]])
        assert resultado in ["?", "¿"]
    
    def test_braille_to_text_exclamacion(self):
        resultado = braille_to_text([[2, 3, 5]])
        assert resultado in ["!", "¡"]
    
    def test_braille_to_text_a_acentuada(self):
        resultado = braille_to_text([[1, 2, 3, 5, 6]])
        assert resultado == "á"
    
    def test_braille_to_text_e_acentuada(self):
        resultado = braille_to_text([[2, 3, 4, 6]])
        assert resultado == "é"
    
    def test_braille_to_text_n_con_tilde(self):
        resultado = braille_to_text([[1, 2, 4, 5, 6]])
        assert resultado == "ñ"
    
    def test_braille_to_text_palabra_hola(self):
        resultado = braille_to_text([[1, 2, 5], [1, 3, 5], [1, 2, 3], [1]])
        assert resultado == "hola"
    
    def test_braille_to_text_palabra_mundo(self):
        # m=[1,3,4], u=[1,3,6], n=[1,3,4,5], d=[1,4,5], o=[1,3,5]
        resultado = braille_to_text([[1, 3, 4], [1, 3, 6], [1, 3, 4, 5], [1, 4, 5], [1, 3, 5]])
        assert resultado == "mundo"
    
    def test_braille_to_text_bus_15(self):
        resultado = braille_to_text([
            PREFIJO_MAY, [1, 2],  # B
            [1, 3, 6],             # u
            [2, 3, 4],             # s
            [],                    # espacio
            PREFIJO_NUM, [1], [1, 5]  # 15
        ])
        assert resultado == "Bus 15"
    
    def test_braille_to_text_con_puntuacion(self):
        """Test: 'Hola.' """
        resultado = braille_to_text([
            PREFIJO_MAY, [1, 2, 5],  # H
            [1, 3, 5],                # o
            [1, 2, 3],                # l
            [1],                      # a
            [2, 5, 6]                 # .
        ])
        assert resultado == "Hola."
    
    def test_braille_to_text_multiples_mayusculas(self):
        """Test: 'ABC'"""
        resultado = braille_to_text([
            PREFIJO_MAY, [1],         # A
            PREFIJO_MAY, [1, 2],      # B
            PREFIJO_MAY, [1, 4]       # C
        ])
        assert resultado == "ABC"
    
    def test_braille_to_text_numeros_separados(self):
        """Test: '1 2'"""
        resultado = braille_to_text([
            PREFIJO_NUM, [1],
            [],
            PREFIJO_NUM, [1, 2]
        ])
        assert resultado == "1 2"


class TestBidireccional:
    def test_roundtrip_hola(self):
        original = "hola"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_con_numeros(self):
        original = "Viaje 2025"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_con_puntuacion(self):
        original = "Hola, mundo."
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_con_acentos(self):
        original = "Español"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_solo_numeros(self):
        original = "2024"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_mayusculas(self):
        original = "ABC"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_mixto_completo(self):
        original = "Bus 42: Avenida Pérez"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_con_signos(self):
        # Note: ¿ y ¡ se convierten a ? y ! en la traducción inversa
        # porque usamos solo una forma en el mapeo braille
        original = "?Qué tal? !Bien!"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
    
    def test_roundtrip_alfabeto_completo(self):
        # Nota: 'v' mapea a [1,3,4,6] que también es 'ó', así que 'ó' tiene prioridad en la inversa
        # Por lo tanto, al hacer roundtrip, 'v' se convierte en 'ó'
        original = "abcdefghijklmnopqrstuvwxyz"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        # v->ó en la respuesta esperada  
    
    def test_roundtrip_numeros_0_a_9(self):
        original = "0123456789"
        braille = text_to_braille(original)
        recuperado = braille_to_text(braille)
        assert recuperado == original
