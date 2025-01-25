import unittest
import pytest
from app import util


@pytest.mark.unit
class TestUtil(unittest.TestCase):
    
    def test_convert_to_number_correct_param(self):
        # Casos con enteros positivos y negativos
        self.assertEqual(4, util.convert_to_number("4"))
        self.assertEqual(0, util.convert_to_number("0"))
        self.assertEqual(0, util.convert_to_number("-0"))
        self.assertEqual(-1, util.convert_to_number("-1"))
        
        # Casos con flotantes positivos y negativos
        self.assertAlmostEqual(4.0, util.convert_to_number("4.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("0.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("-0.0"), delta=0.0000001)
        self.assertAlmostEqual(-1.0, util.convert_to_number("-1.0"), delta=0.0000001)

        # Casos con notación científica
        self.assertAlmostEqual(1e2, util.convert_to_number("1e2"), delta=0.0000001)  # 100
        self.assertAlmostEqual(1e-2, util.convert_to_number("1e-2"), delta=0.0000001)  # 0.01

        # Casos con espacios alrededor del número
        self.assertEqual(10, util.convert_to_number("  10  "))
        self.assertEqual(-5, util.convert_to_number("  -5  "))

    def test_convert_to_number_invalid_type(self):
        # Casos con valores no numéricos
        self.assertRaises(TypeError, util.convert_to_number, "")
        self.assertRaises(TypeError, util.convert_to_number, "3.h")
        self.assertRaises(TypeError, util.convert_to_number, "s")
        self.assertRaises(TypeError, util.convert_to_number, None)
        self.assertRaises(TypeError, util.convert_to_number, object())
        
        # Casos con espacios vacíos, deberíamos verificar si se debería levantar un error
        self.assertRaises(TypeError, util.convert_to_number, "   ")

        # Casos con valores que podrían ser ambiguos
        self.assertRaises(TypeError, util.convert_to_number, "10.0.1")  # Caso con punto extra
        self.assertRaises(TypeError, util.convert_to_number, "4,000")  # Comas en números

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
