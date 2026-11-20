# Test automatici per verificare il funzionamento della classe Tavolo.

import unittest

from models.tavolo import Tavolo
from exceptions import DatiNonValidiError, TavoloOccupatoError


class TestTavolo(unittest.TestCase):

    def test_creazione_tavolo(self):
        # Verifica che un tavolo venga creato correttamente.
        tavolo = Tavolo(1, 4)

        self.assertEqual(tavolo.numero, 1)
        self.assertEqual(tavolo.posti, 4)
        self.assertTrue(tavolo.libero)

    def test_occupazione_tavolo(self):
        # Verifica che un tavolo libero possa essere occupato.
        tavolo = Tavolo(1, 4)

        tavolo.occupa()

        self.assertFalse(tavolo.libero)

    def test_liberazione_tavolo(self):
        # Verifica che un tavolo occupato possa essere liberato.
        tavolo = Tavolo(1, 4)

        tavolo.occupa()
        tavolo.libera()

        self.assertTrue(tavolo.libero)

    def test_doppia_occupazione(self):
        # Verifica che non si possa occupare due volte lo stesso tavolo.
        tavolo = Tavolo(1, 4)

        tavolo.occupa()

        with self.assertRaises(TavoloOccupatoError):
            tavolo.occupa()

    def test_posti_non_validi(self):
        # Verifica che non sia possibile creare un tavolo con zero posti.
        with self.assertRaises(DatiNonValidiError):
            Tavolo(1, 0)


if __name__ == "__main__":
    unittest.main()
