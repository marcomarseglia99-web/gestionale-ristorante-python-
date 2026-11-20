# Test automatici per verificare il funzionamento della classe Piatto.

import unittest

from models.piatto import Piatto
from exceptions import DatiNonValidiError


class TestPiatto(unittest.TestCase):

    def test_creazione_piatto(self):
        # Verifica che un piatto venga creato correttamente.
        piatto = Piatto(1, "Carbonara", "primo", 10.50)

        self.assertEqual(piatto.nome, "Carbonara")
        self.assertEqual(piatto.categoria, "primo")
        self.assertEqual(piatto.prezzo, 10.50)
        self.assertTrue(piatto.disponibile)

    def test_modifica_prezzo(self):
        # Verifica che il prezzo possa essere modificato.
        piatto = Piatto(1, "Carbonara", "primo", 10.50)

        piatto.prezzo = 12.00

        self.assertEqual(piatto.prezzo, 12.00)

    def test_prezzo_negativo(self):
        # Verifica che un prezzo negativo venga rifiutato.
        with self.assertRaises(DatiNonValidiError):
            Piatto(1, "Carbonara", "primo", -5.00)

    def test_categoria_non_valida(self):
        # Verifica che una categoria inesistente venga rifiutata.
        with self.assertRaises(DatiNonValidiError):
            Piatto(1, "Carbonara", "pizza", 10.50)

    def test_nome_vuoto(self):
        # Verifica che un nome vuoto venga rifiutato.
        with self.assertRaises(DatiNonValidiError):
            Piatto(1, "", "primo", 10.50)


if __name__ == "__main__":
    unittest.main()
